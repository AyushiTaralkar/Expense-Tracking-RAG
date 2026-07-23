import streamlit as st
import pandas as pd
import plotly.express as px


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="ArthaSage AI",
    page_icon="💰",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
background:linear-gradient(135deg,#050816,#0B1228);
}

.hero{
background:linear-gradient(120deg,#001F3F,#001B4D);
padding:35px;
border-radius:20px;
border:1px solid #00D9FF;
box-shadow:0 0 25px rgba(0,217,255,.25);
margin-bottom:20px;
}

.card{
background:linear-gradient(145deg,#0B1228,#101B3D);
border-radius:18px;
padding:20px;
border:1px solid #007BFF;
box-shadow:0 0 15px rgba(0,217,255,.15);
text-align:center;
}

.metric-title{
font-size:15px;
color:#B0B8C5;
}

.metric-value{
font-size:30px;
font-weight:bold;
color:white;
}

.stButton>button{
background:linear-gradient(90deg,#0066ff,#00d9ff);
color:white;
font-weight:bold;
border:none;
border-radius:10px;
width:100%;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_default():
    return pd.read_csv("data/Personal_Finance_Dataset.csv")

# ---------------- HERO ----------------

st.markdown("""
<div class="hero">

<h1 style="color:#00D9FF;">
💰 ArthaSage AI
</h1>

<h3 style="color:white;">
Your AI Powered Personal Finance Copilot
</h3>

<p style="color:#CBD5E1;font-size:18px;">
Track • Analyze • Predict • Get AI Financial Advice
</p>

</div>
""", unsafe_allow_html=True)

# ---------------- CSV UPLOAD ----------------

st.subheader("📂 Upload Your Expense CSV")

uploaded_file = st.file_uploader(
    "Choose your transaction CSV",
    type=["csv"]
)

# Stop here if no file is uploaded
if uploaded_file is None:

    st.info("👆 Please upload a CSV file to begin.")

    st.markdown("""
    ### Supported CSV Format

    | Date | Category | Amount | Description |
    |------|----------|--------|-------------|
    | 2026-01-01 | Food | 350 | Breakfast |
    | 2026-01-02 | Travel | 800 | Cab Ride |

    **Required columns**
    - Date
    - Category
    - Amount
    - Description (optional)
    """)

    st.stop()

# Read uploaded CSV
df = pd.read_csv(uploaded_file)

st.success("✅ Dataset Loaded Successfully")

# ---------------- KPI ----------------

total = df["Amount"].sum()
average = df["Amount"].mean()
transactions = len(df)
top_category = (
    df.groupby("Category")["Amount"]
    .sum()
    .idxmax()
)

st.subheader("💎 Financial Overview")

c1,c2,c3,c4 = st.columns(4)

cards = [
("💰 Total Spending",f"₹{total:,.0f}"),
("📊 Avg Expense",f"₹{average:,.0f}"),
("🧾 Transactions",transactions),
("🏆 Top Category",top_category)
]

for col,(title,value) in zip([c1,c2,c3,c4],cards):
    col.markdown(f"""
    <div class="card">
    <div class="metric-title">{title}</div>
    <div class="metric-value">{value}</div>
    </div>
    """,unsafe_allow_html=True)

st.divider()
# ---------------- SPENDING ANALYTICS ----------------

st.subheader("📈 Spending Intelligence")

# Category Summary
category_data = (
    df.groupby("Category", as_index=False)["Amount"]
    .sum()
)

left, right = st.columns(2)

# ---------------- PIE CHART ----------------

with left:

    fig1 = px.pie(
        category_data,
        names="Category",
        values="Amount",
        hole=0.55,
        title="Category Wise Spending"
    )

    fig1.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_x=0.25
    )

    st.plotly_chart(
        fig1,
        width="stretch"
    )

# ---------------- BAR CHART ----------------

with right:

    fig2 = px.bar(
        category_data,
        x="Category",
        y="Amount",
        title="Total Spending by Category",
        text_auto=True
    )

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_x=0.2,
        xaxis_title="Category",
        yaxis_title="Amount (₹)"
    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )

# ---------------- MONTHLY TREND ----------------

if "Date" in df.columns:

    st.divider()

    st.subheader("📅 Monthly Spending Trend")

    try:

        df["Date"] = pd.to_datetime(df["Date"])

        monthly = (
            df.groupby(
                df["Date"].dt.to_period("M")
            )["Amount"]
            .sum()
        )

        monthly.index = monthly.index.astype(str)

        fig3 = px.line(
            x=monthly.index,
            y=monthly.values,
            markers=True,
            title="Monthly Expenses"
        )

        fig3.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            title_x=0.25,
            xaxis_title="Month",
            yaxis_title="Amount (₹)"
        )

        st.plotly_chart(
            fig3,
            width="stretch"
        )

    except Exception as e:

        st.warning(
            "Couldn't generate monthly trend. "
            "Please make sure the Date column is valid."
        )

st.divider()
# ---------------- AI ADVISOR ----------------

st.divider()

st.subheader("🤖 ArthaSage AI Advisor")

st.markdown("""
<div class="card">

<h3 style="color:white;">
AI Financial Assistant
</h3>

<p style="color:#CBD5E1;">
The public demo showcases the interface and financial dashboard.

The full version uses:
• LangChain
• FAISS Vector Database
• Google Gemini
• Retrieval-Augmented Generation (RAG)

to provide personalized financial recommendations.
</p>

</div>
""", unsafe_allow_html=True)

question = st.text_area(
    "Ask a financial question",
    placeholder="Example: How can I reduce my monthly expenses?"
)

if st.button("✨ Generate Advice"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:

        total_spending = df["Amount"].sum()
        avg_spending = df["Amount"].mean()
        top_category = (
            df.groupby("Category")["Amount"]
            .sum()
            .idxmax()
        )

        advice = f"""
### 💡 Demo Financial Insights

**Your Question**

> {question}

### Quick Analysis

- Total Spending: ₹{total_spending:,.2f}
- Average Expense: ₹{avg_spending:,.2f}
- Highest Spending Category: **{top_category}**

### Recommendations

• Review your spending in **{top_category}**, as it represents your largest expense category.

• Set a monthly budget and track your expenses regularly.

• Aim to save at least **20%** of your monthly income.

• Consider reducing unnecessary subscriptions and impulse purchases.

---

⚡ **Note:** This is a lightweight public demo.

The complete version integrates **LangChain + FAISS + Google Gemini** to generate personalized AI-powered financial advice based on your uploaded transaction history.
"""

        st.success("Analysis Complete!")

        st.markdown(advice)
# ---------------- DATASET ----------------

st.divider()

st.subheader("📂 Transaction History")

st.dataframe(
    df,
    width="stretch"
)

# ---------------- DOWNLOAD CSV ----------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Current Dataset",
    data=csv,
    file_name="transactions.csv",
    mime="text/csv"
)

# ---------------- DATASET STATS ----------------

st.divider()

st.subheader("📈 Dataset Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Categories",
    df["Category"].nunique()
)

if "Date" in df.columns:
    try:
        first_date = pd.to_datetime(df["Date"]).min().date()
        last_date = pd.to_datetime(df["Date"]).max().date()

        col2.metric(
            "From",
            str(first_date)
        )

        col3.metric(
            "To",
            str(last_date)
        )

    except:
        pass

# ---------------- FOOTER ----------------

st.divider()

st.markdown(
"""
<center>

<h4 style="color:#00D9FF;">
💰 ArthaSage AI
</h4>

<p style="color:gray;">
AI Powered Personal Finance Copilot
</p>

</center>
""",
unsafe_allow_html=True
)
