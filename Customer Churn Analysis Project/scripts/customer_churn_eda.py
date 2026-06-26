import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

df = pd.read_csv("../data/Customer-Churn.csv")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].replace(" ", np.nan))
df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())

print(df.head())
print(df.info())
print(df.describe(include="all"))

sns.countplot(data=df, x="Churn")
plt.tight_layout()
plt.show()

conn = sqlite3.connect(":memory:")
df.to_sql("customers", conn, index=False, if_exists="replace")
print(pd.read_sql("""
SELECT Contract,
COUNT(*) AS Customers,
SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS Churned
FROM customers
GROUP BY Contract
""", conn))
conn.close()
