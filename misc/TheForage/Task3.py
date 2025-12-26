import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

df = pd.read_csv("Task 3 and 4_Loan_Data.csv")

feature_cols = [
    'credit_lines_outstanding', 'loan_amt_outstanding', 
    'total_debt_outstanding', 'income', 'years_employed', 'fico_score'
]

X = df[feature_cols]
y = df['default']

model_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', LogisticRegression(max_iter=1000, C=0.1))
])

model_pipeline.fit(X, y)

def estimate_expected_loss(credit_lines, loan_amt, total_debt, income, years, fico, recovery_rate=0.10):
    input_data = pd.DataFrame([[
        credit_lines, loan_amt, total_debt, income, years, fico
    ]], columns=feature_cols)

    pd_value = model_pipeline.predict_proba(input_data)[0][1]
    lgd = 1 - recovery_rate
    expected_loss = pd_value * loan_amt * lgd
    
    return {
        "Probability of Default": f"{pd_value:.2%}",
        "Expected Loss": f"${expected_loss:,.2f}"
    }

example_borrower = {
    "credit_lines": 3,
    "loan_amt": 5000,
    "total_debt": 15000,
    "income": 50000,
    "years": 2,
    "fico": 620
}

result = estimate_expected_loss(**example_borrower)
print(result)