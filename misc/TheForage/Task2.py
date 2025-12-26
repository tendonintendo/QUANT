import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

df = pd.read_csv("Nat_Gas.csv")
df["Dates"] = pd.to_datetime(df["Dates"])
df.set_index("Dates", inplace=True)

prices = df["Prices"]

df["delta_1"] = prices.diff()
q1, q99 = df["delta_1"].quantile([0.01, 0.99])
df["delta_1"] = df["delta_1"].clip(q1, q99)

df["returns"] = prices.pct_change()
df["direction"] = np.sign(df["returns"])
df["run_id"] = (df["direction"] != df["direction"].shift(1)).cumsum()

df["vol_6"] = df["returns"].rolling(6).std()
df["delta_3"] = prices.diff(3)

df["month"] = df.index.month
df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
df["delta_season"] = df["delta_1"] * df["month_sin"]

rows = []

for _, run in df.groupby("run_id"):
    run = run.dropna()
    if len(run) < 2:
        continue

    run_vol = run["returns"].std()

    for i in range(len(run) - 1):
        rows.append({
            "date": run.index[i],
            "delta_1": run["delta_1"].iloc[i],
            "run_direction": run["direction"].iloc[i],
            "run_volatility": run_vol,
            "vol_6": run["vol_6"].iloc[i],
            "month_sin": run["month_sin"].iloc[i],
            "month_cos": run["month_cos"].iloc[i],
            "current_price": run["Prices"].iloc[i],
            "delta_season": run["delta_season"].iloc[i],
            "delta_3": run["delta_3"].iloc[i],
            "target_delta": run["Prices"].iloc[i + 1] - run["Prices"].iloc[i],
        })

data = pd.DataFrame(rows).set_index("date").dropna()

data["run_volatility"] /= data["run_volatility"].median()
data["vol_6"] /= data["vol_6"].median()

split = int(len(data) * 0.8)
train = data.iloc[:split]
test = data.iloc[split:]

X_train = train.drop(columns="target_delta")
y_train = train["target_delta"]

X_test = test.drop(columns="target_delta")
y_test = test["target_delta"]

model = GradientBoostingRegressor(
    loss="huber",
    alpha=0.9,
    n_estimators=1200,
    learning_rate=0.01,
    max_depth=2,
    random_state=42
)

model.fit(X_train, y_train)

delta_pred = model.predict(X_test)
price_pred = X_test["current_price"].values + delta_pred
price_true = X_test["current_price"].values + y_test.values

rmse = np.sqrt(mean_squared_error(price_true, price_pred))
naive_rmse = np.sqrt(mean_squared_error(price_true, X_test["current_price"].values))

print("\nTEST SET PERFORMANCE (PRICE)")
print(f"Model RMSE : {rmse:.4f}")
print(f"Naive RMSE : {naive_rmse:.4f}")
print(f"Improvement: {(1 - rmse / naive_rmse) * 100:.2f}%")

def generate_price_curve(df, model, start_date, months_forward=12):
    dates = pd.date_range(start=start_date, periods=months_forward + 1, freq="ME")
    prices = {}

    last = df.loc[df.index <= start_date].iloc[-1]
    current_price = last["Prices"]
    delta_1 = last["delta_1"]
    delta_3 = last["delta_3"]
    direction = last["direction"]
    vol_6 = last["vol_6"]
    run_vol = df["returns"].std()

    for d in dates:
        month_sin = np.sin(2 * np.pi * d.month / 12)
        month_cos = np.cos(2 * np.pi * d.month / 12)

        X = pd.DataFrame([{
            "delta_1": delta_1,
            "run_direction": direction,
            "run_volatility": run_vol,
            "vol_6": vol_6,
            "month_sin": month_sin,
            "month_cos": month_cos,
            "current_price": current_price,
            "delta_season": delta_1 * month_sin,
            "delta_3": delta_3
        }])

        delta = model.predict(X)[0]
        next_price = current_price + delta

        prices[d] = next_price

        delta_3 = delta
        delta_1 = delta
        direction = np.sign(delta)
        current_price = next_price

    return prices

def price_storage_contract(
    price_curve,
    injection_schedule,
    withdrawal_schedule,
    inj_rate,
    wdr_rate,
    max_storage,
    storage_cost_per_month
):
    inventory = 0.0
    value = 0.0

    for date in sorted(price_curve.keys()):
        price = price_curve[date]

        inject = injection_schedule.get(date, 0.0)
        withdraw = withdrawal_schedule.get(date, 0.0)

        inject = min(inject, inj_rate, max_storage - inventory)
        withdraw = min(withdraw, wdr_rate, inventory)

        inventory += inject
        inventory -= withdraw

        value -= inject * price
        value += withdraw * price
        value -= inventory * storage_cost_per_month

    return value

start_date = df.index[-1]
price_curve = generate_price_curve(df, model, start_date)

injection_schedule = {
    start_date + pd.DateOffset(months=1): 50,
    start_date + pd.DateOffset(months=2): 50
}

withdrawal_schedule = {
    start_date + pd.DateOffset(months=5): 40,
    start_date + pd.DateOffset(months=6): 60
}

contract_value = price_storage_contract(
    price_curve=price_curve,
    injection_schedule=injection_schedule,
    withdrawal_schedule=withdrawal_schedule,
    inj_rate=50,
    wdr_rate=60,
    max_storage=100,
    storage_cost_per_month=0.05
)

print(f"\nSTORAGE CONTRACT VALUE: {contract_value:.2f}")
