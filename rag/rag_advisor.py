def get_financial_advice(question, df):

    total = df["Amount"].sum()

    average = df["Amount"].mean()

    transactions = len(df)

    category_summary = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    highest = category_summary.index[0]

    highest_amount = category_summary.iloc[0]

    advice = f"""
### 📊 Financial Summary

- **Total Spending:** ₹{total:,.0f}
- **Average Expense:** ₹{average:,.0f}
- **Transactions:** {transactions}
- **Highest Spending Category:** {highest} (₹{highest_amount:,.0f})

### 💡 Suggestions

✅ Reduce spending in **{highest}** if possible.

✅ Follow the **50-30-20 Rule**

✅ Save at least 20% of your income.

Question Asked:
{question}
"""

    return advice