
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Superstore Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F4F7FC;
    color: #1B3153;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F0F5FF 100%);
    border-right: 1px solid #E1E9F5;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

.block-container {
    max-width: 1500px;
    padding: 2rem 3rem 3rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 4px 20px;
}

.brand-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, #173B70, #3478F6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: white;
    box-shadow: 0 6px 15px rgba(37,99,235,.2);
}

.brand-name {
    font-size: 19px;
    font-weight: 800;
    color: #173B70;
}

.brand-sub {
    color: #8A9AB2;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

.status {
    background: #EAF8F1;
    border: 1px solid #D3EFDF;
    border-radius: 10px;
    color: #16845B;
    font-size: 12px;
    font-weight: 600;
    padding: 10px 12px;
    margin: 8px 0 20px;
}

.sidebar-heading {
    font-size: 11px;
    font-weight: 800;
    color: #8494AA;
    letter-spacing: 1.3px;
    margin: 20px 0 10px;
}

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 7px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: #FFFFFF;
    border: 1px solid #E5ECF5;
    border-radius: 10px;
    padding: 10px 12px;
    transition: all .2s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    border-color: #3478F6;
    background: #EFF5FF;
}

.hero {
    background: linear-gradient(115deg, #102F5C 0%, #1C4C8A 55%, #3478F6 100%);
    border-radius: 20px;
    padding: 30px 34px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 12px 28px rgba(23,59,112,.15);
}

.hero-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}

.hero-tag, .hero-live {
    background: rgba(255,255,255,.14);
    color: #FFFFFF;
    padding: 8px 12px;
    border-radius: 30px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}

.hero h1 {
    color: white;
    font-size: 32px;
    font-weight: 800;
    margin: 20px 0 8px;
}

.hero p {
    color: #DCE9FF;
    font-size: 14px;
    line-height: 1.7;
    max-width: 750px;
    margin-bottom: 0;
}

.hero-bottom {
    display: flex;
    flex-wrap: wrap;
    gap: 22px;
    margin-top: 22px;
    color: #E5EEFF;
    font-size: 12px;
    font-weight: 600;
}

.section-heading {
    color: #173B70;
    font-size: 19px;
    font-weight: 800;
    margin: 25px 0 14px;
}

.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E5EBF4;
    border-radius: 15px;
    padding: 19px;
    min-height: 125px;
    box-shadow: 0 4px 14px rgba(20,40,80,.035);
}

.kpi-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.kpi-label {
    color: #718096;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .4px;
}

.kpi-icon {
    width: 35px;
    height: 35px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    background: #EDF4FF;
}

.kpi-value {
    color: #173B70;
    font-size: 25px;
    font-weight: 800;
    margin-top: 12px;
}

.kpi-note {
    color: #15966B;
    font-size: 11px;
    font-weight: 600;
    margin-top: 4px;
}

div[data-testid="stPlotlyChart"] {
    background: white;
    border: 1px solid #E6ECF4;
    border-radius: 15px;
    padding: 9px;
    box-shadow: 0 4px 14px rgba(20,40,80,.025);
}

div[data-testid="stDataFrame"] {
    border: 1px solid #E5EBF4;
    border-radius: 12px;
}

.stSelectbox label, .stDateInput label {
    color: #42526E;
    font-weight: 600;
}

.footer {
    text-align: center;
    color: #8998AD;
    font-size: 11px;
    padding: 30px 10px 10px;
}

@media (max-width: 900px) {
    .block-container {
        padding: 1rem;
    }
    .hero {
        padding: 22px;
    }
    .hero h1 {
        font-size: 25px;
    }
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    data = pd.read_csv("superstore_sales.csv")
    data = data.dropna(subset=["Order Date"]).copy()

    data["Order Date"] = pd.to_datetime(
        data["Order Date"], format="mixed", errors="coerce"
    )
    data["Sales"] = pd.to_numeric(data["Sales"], errors="coerce")
    data["Profit"] = pd.to_numeric(data["Profit"], errors="coerce")
    data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")
    data["Discount"] = pd.to_numeric(data["Discount"], errors="coerce")

    data = data.dropna(subset=["Order Date", "Sales", "Profit"])
    data["Year-Month"] = data["Order Date"].dt.to_period("M").astype(str)

    return data


try:
    df = load_data()
except Exception as error:
    st.error(f"Dataset loading error: {error}")
    st.stop()


st.sidebar.markdown("""
<div class="brand">
    <div class="brand-icon">📊</div>
    <div>
        <div class="brand-name">SUPERSTORE</div>
        <div class="brand-sub">ANALYTICS PLATFORM</div>
    </div>
</div>
<div class="status">● &nbsp; Dashboard Active</div>
<div class="sidebar-heading">MAIN MENU</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Sales Analysis",
        "Product Analysis",
        "Regional Analysis",
        "Customer Analysis",
        "Discount Analysis"
    ],
    format_func=lambda x: {
        "Overview": "🏠  Overview",
        "Sales Analysis": "📈  Sales Analysis",
        "Product Analysis": "📦  Product Analysis",
        "Regional Analysis": "🌍  Regional Analysis",
        "Customer Analysis": "👥  Customer Analysis",
        "Discount Analysis": "🏷️  Discount Analysis"
    }[x],
    label_visibility="collapsed"
)

st.sidebar.markdown('<div class="sidebar-heading">DATA FILTERS</div>',
                    unsafe_allow_html=True)

regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
segments = ["All"] + sorted(df["Segment"].dropna().unique().tolist())

region_choice = st.sidebar.selectbox("Region", regions)
category_choice = st.sidebar.selectbox("Category", categories)
segment_choice = st.sidebar.selectbox("Customer Segment", segments)

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered = df.copy()

if region_choice != "All":
    filtered = filtered[filtered["Region"] == region_choice]

if category_choice != "All":
    filtered = filtered[filtered["Category"] == category_choice]

if segment_choice != "All":
    filtered = filtered[filtered["Segment"] == segment_choice]

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[
        (filtered["Order Date"].dt.date >= date_range[0]) &
        (filtered["Order Date"].dt.date <= date_range[1])
    ]

if filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

sales = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
orders = filtered["Order ID"].nunique()
customers = filtered["Customer ID"].nunique()
quantity = filtered["Quantity"].sum()
margin = profit / sales * 100 if sales else 0


st.markdown("""
<div class="hero">
    <div class="hero-top">
        <span class="hero-tag">✦ BUSINESS INTELLIGENCE</span>
        <span class="hero-live">● LIVE DASHBOARD</span>
    </div>
    <h1>Superstore Analytics</h1>
    <p>Your business performance, simplified. Explore revenue trends,
    customer insights and profitability with interactive analytics.</p>
    <div class="hero-bottom">
        <span>📈 Sales Intelligence</span>
        <span>◈ Customer Insights</span>
        <span>✦ Performance Tracking</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.caption(
    f"Showing {len(filtered):,} transaction records based on selected filters."
)


def make_card(label, value, icon, note):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-label">{label}</div>
            <div class="kpi-icon">{icon}</div>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def show_kpis():
    cols = st.columns(4)
    values = [
        ("TOTAL SALES", f"${sales:,.2f}", "💰", "Revenue generated"),
        ("TOTAL PROFIT", f"${profit:,.2f}", "📈", "Business profit"),
        ("TOTAL ORDERS", f"{orders:,}", "🛒", "Unique orders"),
        ("CUSTOMERS", f"{customers:,}", "👥", "Unique customers")
    ]

    for col, item in zip(cols, values):
        with col:
            make_card(*item)

    st.markdown("<br>", unsafe_allow_html=True)


def chart_style(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter", color="#42526E", size=12),
        title_font=dict(size=16, color="#173B70"),
        margin=dict(l=25, r=25, t=55, b=30),
        legend_title_text="",
        hoverlabel=dict(bgcolor="white", font_size=12)
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#EDF1F6")
    return fig


def show_monthly_sales():
    monthly = filtered.groupby("Year-Month", as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )

    fig = px.line(
        monthly,
        x="Year-Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Performance"
    )
    fig.update_traces(line_color="#2563EB", line_width=3)
    st.plotly_chart(chart_style(fig), use_container_width=True)


if page == "Overview":
    st.markdown('<div class="section-heading">Business Performance Overview</div>',
                unsafe_allow_html=True)

    show_kpis()

    col1, col2 = st.columns(2)

    with col1:
        show_monthly_sales()

    with col2:
        category = filtered.groupby("Category", as_index=False)["Sales"].sum()
        fig = px.bar(
            category,
            x="Category",
            y="Sales",
            color="Category",
            title="Revenue by Product Category",
            color_discrete_sequence=["#2563EB", "#14B8A6", "#8B9CF6"]
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        region = filtered.groupby("Region", as_index=False)["Sales"].sum()
        fig = px.pie(
            region,
            names="Region",
            values="Sales",
            hole=0.58,
            title="Regional Revenue Distribution"
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

    with col4:
        segment = filtered.groupby("Segment", as_index=False)["Sales"].sum()
        fig = px.bar(
            segment,
            x="Segment",
            y="Sales",
            color="Segment",
            title="Sales by Customer Segment"
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

    st.markdown('<div class="section-heading">Profitability Snapshot</div>',
                unsafe_allow_html=True)

    a, b, c = st.columns(3)
    a.metric("Profit Margin", f"{margin:.2f}%")
    b.metric("Units Sold", f"{quantity:,.0f}")
    c.metric("Average Order Value", f"${sales / orders:,.2f}" if orders else "$0")


elif page == "Sales Analysis":
    st.markdown('<div class="section-heading">Sales Performance Analysis</div>',
                unsafe_allow_html=True)
    show_kpis()
    show_monthly_sales()

    monthly = filtered.groupby("Year-Month", as_index=False)["Profit"].sum()
    fig = px.bar(monthly, x="Year-Month", y="Profit",
                 title="Monthly Profit Performance")
    fig.update_traces(marker_color="#14B8A6")
    st.plotly_chart(chart_style(fig), use_container_width=True)

    st.subheader("Monthly Sales Data")
    st.dataframe(
        filtered.groupby("Year-Month", as_index=False).agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique")
        ),
        use_container_width=True,
        hide_index=True
    )


elif page == "Product Analysis":
    st.markdown('<div class="section-heading">Product & Category Analysis</div>',
                unsafe_allow_html=True)
    show_kpis()

    product = filtered.groupby(["Category", "Sub-Category"], as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )

    fig = px.bar(
        product,
        x="Sub-Category",
        y="Sales",
        color="Category",
        title="Revenue by Sub-Category",
        barmode="group"
    )
    st.plotly_chart(chart_style(fig), use_container_width=True)

    fig = px.bar(
        product,
        x="Sub-Category",
        y="Profit",
        color="Category",
        title="Profit by Sub-Category"
    )
    st.plotly_chart(chart_style(fig), use_container_width=True)

    st.subheader("Product Performance Details")
    st.dataframe(
        product.sort_values("Sales", ascending=False),
        use_container_width=True,
        hide_index=True
    )


elif page == "Regional Analysis":
    st.markdown('<div class="section-heading">Regional Business Performance</div>',
                unsafe_allow_html=True)
    show_kpis()

    region = filtered.groupby("Region", as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(region, x="Region", y="Sales",
                     color="Region", title="Sales by Region")
        st.plotly_chart(chart_style(fig), use_container_width=True)

    with col2:
        fig = px.bar(region, x="Region", y="Profit",
                     color="Region", title="Profit by Region")
        st.plotly_chart(chart_style(fig), use_container_width=True)

    st.subheader("Regional Performance Details")
    st.dataframe(region, use_container_width=True, hide_index=True)


elif page == "Customer Analysis":
    st.markdown('<div class="section-heading">Customer Insights</div>',
                unsafe_allow_html=True)
    show_kpis()

    customer = filtered.groupby("Customer Name", as_index=False).agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order ID", "nunique"),
        Total_Quantity=("Quantity", "sum")
    )

    top = customer.sort_values("Total_Sales", ascending=False).head(10)

    fig = px.bar(
        top,
        x="Total_Sales",
        y="Customer Name",
        orientation="h",
        title="Top 10 Customers by Revenue"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    fig.update_traces(marker_color="#3478F6")
    st.plotly_chart(chart_style(fig), use_container_width=True)

    st.subheader("Top Customer Details")
    st.dataframe(top, use_container_width=True, hide_index=True)


elif page == "Discount Analysis":
    st.markdown('<div class="section-heading">Discount & Profitability Analysis</div>',
                unsafe_allow_html=True)
    show_kpis()

    discount = filtered.groupby("Discount", as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Average_Profit=("Profit", "mean"),
        Quantity=("Quantity", "sum")
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            discount,
            x="Discount",
            y="Average_Profit",
            title="Discount Level vs Average Profit"
        )
        fig.update_traces(marker_color="#3478F6")
        st.plotly_chart(chart_style(fig), use_container_width=True)

    with col2:
        fig = px.scatter(
            filtered,
            x="Discount",
            y="Profit",
            color="Category",
            render_mode="svg",
            opacity=0.55,
            title="Discount vs Profit Relationship"
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

    st.subheader("Discount Performance Details")
    st.dataframe(discount, use_container_width=True, hide_index=True)


st.markdown("""
<div class="footer">
    SUPERSTORE ANALYTICS &nbsp; | &nbsp; BUSINESS INTELLIGENCE DASHBOARD
    <br>Developed using Python • Streamlit • Pandas • Plotly
</div>
""", unsafe_allow_html=True)
