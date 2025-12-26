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

df["month"] = df.index.month
df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
df["delta_season"] = df["delta_1"] * df["month_sin"]
df["delta_3"] = prices.diff(3)


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
            "target_delta": run["Prices"].iloc[i + 1] - run["Prices"].iloc[i],
            "delta_season": run["delta_season"].iloc[i],
            "delta_3": run["delta_3"].iloc[i],
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

print("\nFeature Importances:")
for f, imp in zip(X_train.columns, model.feature_importances_):
    print(f"{f:15}: {imp:.3f}")

plt.figure(figsize=(10,5))
plt.plot(test.index, price_true, label="Actual")
plt.plot(test.index, price_pred, label="Predicted")
plt.legend()
plt.show()
