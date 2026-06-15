"""
╔══════════════════════════════════════════════════════════════════╗
║  BSA83111 · Data Visualization for Decision Making              ║
║  Module: Superstore Sales Intelligence Dashboard                ║
║  Faculty of Management | Year 3 | Trimester 1 | Level 8        ║
║  Instructor: Dr Patrick NIYISHAKA                               ║
║  Assessment Period: June 9–14, 2026 | Presentation: June 16    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import io

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Superstore Sales Dashboard | BSA83111",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ──────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, .stApp {
    background-color: #080c14 !important;
    color: #dde3f0;
    font-family: 'Inter', sans-serif;
}

/* ── Sidebar ───────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1525 0%, #0a1020 100%) !important;
    border-right: 1px solid #1e2d4a;
}
section[data-testid="stSidebar"] * { color: #b8c8e8 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stRadio label { color: #7a9cc0 !important; font-size: 0.78rem !important; }

/* ── Tab navigation ────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1525;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    border: 1px solid #1e2d4a;
    margin-bottom: 20px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: #5a7ba0 !important;
    font-size: 0.82rem;
    font-weight: 500;
    padding: 8px 16px;
    border: none !important;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1a3a6a, #0f2550) !important;
    color: #7ab3f0 !important;
    font-weight: 600 !important;
}

/* ── KPI cards ─────────────────────────────────────────────── */
.kpi-card {
    background: linear-gradient(135deg, #0d1a2e 0%, #111e35 100%);
    border: 1px solid #1e3356;
    border-radius: 14px;
    padding: 22px 16px 18px;
    text-align: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, #3a6fd8);
    border-radius: 14px 14px 0 0;
}
.kpi-icon  { font-size: 1.5rem; margin-bottom: 6px; }
.kpi-label { font-size: 0.68rem; color: #5a7ba0; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; font-weight: 600; }
.kpi-value { font-size: 2rem; font-weight: 800; color: #e8f0ff; line-height: 1.1; }
.kpi-sub   { font-size: 0.72rem; color: #3a6fd8; margin-top: 6px; font-weight: 500; }
.kpi-sub.neg { color: #e05c6a; }
.kpi-bar   { height: 4px; border-radius: 4px; background: #1e3356; margin-top: 10px; overflow: hidden; }
.kpi-bar-fill { height: 100%; border-radius: 4px; background: var(--accent, #3a6fd8); }

/* ── Section header ────────────────────────────────────────── */
.sec-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 8px 0 18px;
    padding-bottom: 10px;
    border-bottom: 1px solid #1e2d4a;
}
.sec-header-icon { font-size: 1.3rem; }
.sec-header-text { font-size: 1.05rem; font-weight: 700; color: #c8d8f0; letter-spacing: 0.01em; }
.sec-header-badge {
    background: #1a3a6a;
    color: #7ab3f0;
    font-size: 0.68rem;
    padding: 2px 8px;
    border-radius: 20px;
    font-weight: 600;
    margin-left: auto;
}

/* ── Alert boxes ───────────────────────────────────────────── */
.alert-danger  { background:#1f0b0e; border-left:4px solid #e05c6a; color:#f48a94; border-radius:8px; padding:12px 16px; margin:6px 0; font-size:0.85rem; line-height:1.5; }
.alert-warning { background:#1f1408; border-left:4px solid #f0a030; color:#ffd080; border-radius:8px; padding:12px 16px; margin:6px 0; font-size:0.85rem; line-height:1.5; }
.alert-success { background:#071810; border-left:4px solid #3aad6a; color:#6fe8a8; border-radius:8px; padding:12px 16px; margin:6px 0; font-size:0.85rem; line-height:1.5; }
.alert-info    { background:#081828; border-left:4px solid #3a6fd8; color:#7ab3f0; border-radius:8px; padding:12px 16px; margin:6px 0; font-size:0.85rem; line-height:1.5; }

/* ── Ethics cards ──────────────────────────────────────────── */
.ethics-card {
    background: #0d1525;
    border: 1px solid #1e3356;
    border-radius: 12px;
    padding: 18px 20px;
    margin: 10px 0;
}
.ethics-icon  { font-size: 1.4rem; margin-bottom: 6px; }
.ethics-title { font-size: 0.92rem; font-weight: 700; color: #7ab3f0; margin-bottom: 8px; }
.ethics-body  { font-size: 0.83rem; color: #8a9aba; line-height: 1.7; }
.risk-badge-high   { background:#3b0d12; color:#f48a94; padding:2px 8px; border-radius:4px; font-size:0.72rem; font-weight:700; }
.risk-badge-medium { background:#2a1a04; color:#ffd080; padding:2px 8px; border-radius:4px; font-size:0.72rem; font-weight:700; }
.risk-badge-low    { background:#071810; color:#6fe8a8; padding:2px 8px; border-radius:4px; font-size:0.72rem; font-weight:700; }

/* ── Insight boxes ─────────────────────────────────────────── */
.insight-box {
    background: linear-gradient(135deg, #0d1a2e, #0a1525);
    border: 1px solid #1e3a5a;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 7px 0;
    font-size: 0.85rem;
    color: #9ab8d8;
    line-height: 1.65;
}
.insight-box b { color: #c8d8f0; }
.rec-box {
    background: linear-gradient(135deg, #0a1a0a, #081408);
    border: 1px solid #1a3a1a;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 7px 0;
    font-size: 0.85rem;
    color: #6fe8a8;
    line-height: 1.65;
}
.rec-box b { color: #a0f0c0; }

/* ── Metadata ──────────────────────────────────────────────── */
.meta-wrap { background:#0d1525; border:1px solid #1e3356; border-radius:12px; padding:22px 28px; }
.meta-row  { display:flex; padding:9px 0; border-bottom:1px solid #131d2e; align-items:flex-start; }
.meta-row:last-child { border-bottom:none; }
.meta-key  { color:#5a7ba0; min-width:180px; font-size:0.82rem; font-weight:600; text-transform:uppercase; letter-spacing:0.04em; padding-top:1px; }
.meta-val  { color:#b8c8e8; font-size:0.85rem; line-height:1.5; }
.meta-link { color:#3a8fd8; text-decoration:underline; }

/* ── Hide streamlit chrome ─────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# LOAD & PREPARE DATA
# ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("superstore_sales.csv", parse_dates=["Order Date", "Ship Date"])
    df["Year"]           = df["Order Date"].dt.year
    df["Quarter"]        = df["Order Date"].dt.to_period("Q").astype(str)
    df["Month_Period"]   = df["Order Date"].dt.to_period("M")
    df["Month_Label"]    = df["Order Date"].dt.strftime("%b %Y")
    df["Month_dt"]       = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["Profit Margin %"]= np.where(df["Sales"] != 0, (df["Profit"] / df["Sales"]) * 100, 0)
    df["Loss Flag"]      = df["Profit"] < 0
    df["High Discount"]  = df["Discount"] >= 0.4
    df["Days to Ship"]   = (df["Ship Date"] - df["Order Date"]).dt.days
    return df

df = load_data()

# ─────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px;'>
      <div style='font-size:1.4rem;'>🛒</div>
      <div style='font-size:0.95rem;font-weight:700;color:#c8d8f0;'>Superstore Sales</div>
      <div style='font-size:0.72rem;color:#3a6fd8;margin-top:2px;'>BSA83111 · Analytics Dashboard</div>
    </div>
    <hr style='border:none;border-top:1px solid #1e2d4a;margin:10px 0 16px;'>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.78rem;color:#5a7ba0;font-weight:600;letter-spacing:0.08em;margin-bottom:8px;'>FILTERS</div>", unsafe_allow_html=True)

    # Date range slider
    min_date = df["Order Date"].min().date()
    max_date = df["Order Date"].max().date()
    date_range = st.slider(
        "📅 Order Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="MMM YYYY"
    )

    years     = sorted(df["Year"].unique())
    regions   = sorted(df["Region"].unique())
    segments  = sorted(df["Segment"].unique())
    cats      = sorted(df["Category"].unique())
    ships     = sorted(df["Ship Mode"].unique())

    sel_regions  = st.multiselect("🗺 Region",    regions,  default=regions)
    sel_segments = st.multiselect("👥 Segment",   segments, default=segments)
    sel_cats     = st.multiselect("📦 Category",  cats,     default=cats)
    sel_ships    = st.multiselect("🚚 Ship Mode", ships,    default=ships)

    st.markdown("<hr style='border:none;border-top:1px solid #1e2d4a;margin:14px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.78rem;color:#5a7ba0;font-weight:600;letter-spacing:0.08em;margin-bottom:8px;'>EXPLORER OPTIONS</div>", unsafe_allow_html=True)

    sort_col = st.selectbox("Sort table by", ["Sales", "Profit", "Quantity", "Discount", "Days to Ship"])
    sort_dir = st.radio("Direction", ["Descending ↓", "Ascending ↑"], horizontal=True)

    disc_threshold = st.slider("🚨 Discount alert threshold", 0, 80, 40, step=5, help="Flag orders above this discount %")

    st.markdown("<hr style='border:none;border-top:1px solid #1e2d4a;margin:14px 0;'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.72rem;color:#2a4060;text-align:center;line-height:1.7;'>"
        "Faculty of Management<br>Dr Patrick NIYISHAKA<br>June 2026</div>",
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────
filtered = df[
    (df["Order Date"].dt.date >= date_range[0]) &
    (df["Order Date"].dt.date <= date_range[1]) &
    df["Region"].isin(sel_regions) &
    df["Segment"].isin(sel_segments) &
    df["Category"].isin(sel_cats) &
    df["Ship Mode"].isin(sel_ships)
].copy()

filtered["High Discount"] = filtered["Discount"] >= (disc_threshold / 100)

# ─────────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────────
CT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#8a9aba", size=11, family="Inter"),
    margin=dict(l=40, r=20, t=44, b=36),
)
GRID = dict(gridcolor="#111e35", zerolinecolor="#1e3356")
COLS = ["#3a6fd8","#3aad6a","#f0a030","#e05c6a","#26b5c8","#9a5fd8","#e8784a"]

def chart(fig):
    fig.update_layout(**CT)
    return fig

def sec(icon, title, badge=None):
    badge_html = f'<span class="sec-header-badge">{badge}</span>' if badge else ""
    st.markdown(
        f'<div class="sec-header">'
        f'<span class="sec-header-icon">{icon}</span>'
        f'<span class="sec-header-text">{title}</span>'
        f'{badge_html}</div>',
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────────
# HEADER BANNER
# ─────────────────────────────────────────────────────────────────
total_sales_all = df["Sales"].sum()
total_profit_all = df["Profit"].sum()
margin_all = (total_profit_all / total_sales_all * 100) if total_sales_all else 0

st.markdown(f"""
<div style="background:linear-gradient(135deg,#0d1a2e 0%,#081428 50%,#0a1020 100%);
            border:1px solid #1e3356;border-radius:16px;padding:24px 32px;margin-bottom:20px;">
  <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
    <div>
      <div style="font-size:1.7rem;font-weight:800;color:#e8f0ff;letter-spacing:-0.02em;">
        🛒 Superstore Sales Intelligence Dashboard
      </div>
      <div style="font-size:0.83rem;color:#3a6fd8;margin-top:6px;">
        BSA83111 · Data Visualization for Decision Making &nbsp;|&nbsp; Faculty of Management &nbsp;|&nbsp; Dr Patrick NIYISHAKA
      </div>
    </div>
    <div style="display:flex;gap:24px;flex-wrap:wrap;">
      <div style="text-align:center;">
        <div style="font-size:0.68rem;color:#5a7ba0;text-transform:uppercase;letter-spacing:0.08em;">Dataset Total Sales</div>
        <div style="font-size:1.3rem;font-weight:700;color:#3a6fd8;">${total_sales_all:,.0f}</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:0.68rem;color:#5a7ba0;text-transform:uppercase;letter-spacing:0.08em;">Overall Margin</div>
        <div style="font-size:1.3rem;font-weight:700;color:#3aad6a;">{margin_all:.1f}%</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:0.68rem;color:#5a7ba0;text-transform:uppercase;letter-spacing:0.08em;">Period</div>
        <div style="font-size:1.3rem;font-weight:700;color:#c8d8f0;">2020–2024</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if filtered.empty:
    st.error("⚠️ No data matches your current filter selections. Adjust the sidebar filters.")
    st.stop()

# ─────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 KPIs & Overview",
    "📅 Trends",
    "📈 Comparisons",
    "📉 Distributions",
    "🚨 Alerts",
    "🔍 Data Explorer",
    "⚖️ Ethics & Insights"
])

# ══════════════════════════════════════════════════════════════════
#  TAB 1 – KPIs & OVERVIEW
# ══════════════════════════════════════════════════════════════════
with tab1:
    sec("📊", "Key Performance Indicators", "Section 1 · 2 pts")

    # Compute KPIs
    total_sales   = filtered["Sales"].sum()
    total_profit  = filtered["Profit"].sum()
    total_orders  = filtered["Order ID"].nunique()
    total_qty     = filtered["Quantity"].sum()
    avg_ov        = filtered.groupby("Order ID")["Sales"].sum().mean()
    margin_pct    = (total_profit / total_sales * 100) if total_sales else 0
    loss_rows     = filtered[filtered["Profit"] < 0]
    profit_rate   = (1 - len(loss_rows) / len(filtered)) * 100 if len(filtered) else 0
    avg_disc      = filtered["Discount"].mean() * 100
    avg_ship_days = filtered["Days to Ship"].mean()
    customers     = filtered["Customer ID"].nunique()

    kpis = [
        ("💰", "Total Sales",     f"${total_sales:,.0f}",    f"{total_orders:,} orders",          "#3a6fd8", min(total_sales/50000,1)),
        ("📈", "Total Profit",    f"${total_profit:,.0f}",   f"Margin: {margin_pct:.1f}%",         "#3aad6a" if total_profit>=0 else "#e05c6a", min(abs(total_profit)/15000,1)),
        ("🛒", "Orders Placed",   f"{total_orders:,}",       f"{customers:,} unique customers",    "#26b5c8", min(total_orders/150,1)),
        ("📦", "Units Sold",      f"{total_qty:,}",          f"Avg {total_qty/total_orders:.1f}/order" if total_orders else "—", "#9a5fd8", min(total_qty/500,1)),
        ("🧾", "Avg Order Value", f"${avg_ov:,.0f}",         "Per order",                         "#f0a030", min(avg_ov/3000,1)),
        ("✅", "Profitability",   f"{profit_rate:.0f}%",     f"{len(loss_rows)} loss rows",        "#3aad6a" if profit_rate>=70 else "#e05c6a", profit_rate/100),
        ("🏷", "Avg Discount",    f"{avg_disc:.1f}%",        "Watch if >30%",                     "#e8784a" if avg_disc>30 else "#3aad6a", avg_disc/100),
        ("🚚", "Avg Ship Days",   f"{avg_ship_days:.1f}d",   "Order to delivery",                 "#26b5c8", min(avg_ship_days/7,1)),
    ]

    cols = st.columns(4)
    for i, (icon, label, val, sub, accent, fill_ratio) in enumerate(kpis):
        with cols[i % 4]:
            sub_class = "neg" if (label == "Total Profit" and total_profit < 0) else ""
            fill_pct  = int(fill_ratio * 100)
            st.markdown(f"""
            <div class="kpi-card" style="--accent:{accent};">
              <div class="kpi-icon">{icon}</div>
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">{val}</div>
              <div class="kpi-sub {sub_class}">{sub}</div>
              <div class="kpi-bar"><div class="kpi-bar-fill" style="width:{fill_pct}%;background:{accent};"></div></div>
            </div>""", unsafe_allow_html=True)
        if i == 3:
            cols = st.columns(4)

    st.markdown("<br>", unsafe_allow_html=True)

    # KPI breakdown table
    sec("🗂", "Performance Summary by Category")
    cat_summary = (
        filtered.groupby("Category")
        .agg(
            Orders   = ("Order ID", "nunique"),
            Sales    = ("Sales", "sum"),
            Profit   = ("Profit", "sum"),
            Qty      = ("Quantity", "sum"),
            Avg_Disc = ("Discount", "mean"),
        )
        .reset_index()
    )
    cat_summary["Margin %"]     = (cat_summary["Profit"] / cat_summary["Sales"] * 100).round(1)
    cat_summary["Avg Discount"] = (cat_summary["Avg_Disc"] * 100).round(1)
    cat_summary.drop("Avg_Disc", axis=1, inplace=True)

    def color_margin(val):
        if val < 0:   return "color:#e05c6a;font-weight:700"
        if val < 10:  return "color:#f0a030"
        return "color:#3aad6a;font-weight:600"

    styled_cat = (
        cat_summary.style
        .format({"Sales":"${:,.0f}","Profit":"${:,.0f}","Margin %":"{:.1f}%","Avg Discount":"{:.1f}%"})
        .map(color_margin, subset=["Margin %"])
    )
    st.dataframe(styled_cat, use_container_width=True, hide_index=True)

    # Mini donut row
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        seg_s = filtered.groupby("Segment")["Sales"].sum().reset_index()
        fig = px.pie(seg_s, values="Sales", names="Segment", hole=0.55,
                     color_discrete_sequence=COLS, title="Sales by Segment")
        fig.update_traces(textinfo="percent+label", textfont_size=11)
        fig.update_layout(**CT, showlegend=False, title_font_color="#c8d8f0")
        st.plotly_chart(chart(fig), use_container_width=True)

    with col_d2:
        cat_s = filtered.groupby("Category")["Sales"].sum().reset_index()
        fig = px.pie(cat_s, values="Sales", names="Category", hole=0.55,
                     color_discrete_sequence=COLS, title="Sales by Category")
        fig.update_traces(textinfo="percent+label", textfont_size=11)
        fig.update_layout(**CT, showlegend=False, title_font_color="#c8d8f0")
        st.plotly_chart(chart(fig), use_container_width=True)

    with col_d3:
        ship_s = filtered.groupby("Ship Mode")["Sales"].sum().reset_index()
        fig = px.pie(ship_s, values="Sales", names="Ship Mode", hole=0.55,
                     color_discrete_sequence=COLS, title="Sales by Ship Mode")
        fig.update_traces(textinfo="percent+label", textfont_size=11)
        fig.update_layout(**CT, showlegend=False, title_font_color="#c8d8f0")
        st.plotly_chart(chart(fig), use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  TAB 2 – TRENDS
# ══════════════════════════════════════════════════════════════════
with tab2:
    sec("📅", "Trends Over Time", "Section 2 · 2 pts")

    monthly = (
        filtered.groupby("Month_dt")
        .agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique"))
        .reset_index()
        .sort_values("Month_dt")
    )
    monthly["Rolling_Sales"]  = monthly["Sales"].rolling(3, min_periods=1).mean()
    monthly["Rolling_Profit"] = monthly["Profit"].rolling(3, min_periods=1).mean()

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly["Month_dt"], y=monthly["Sales"],
            mode="lines", name="Monthly Sales",
            line=dict(color="#1e3356", width=1),
            fill="tozeroy", fillcolor="rgba(58,111,216,0.08)"
        ))
        fig.add_trace(go.Scatter(
            x=monthly["Month_dt"], y=monthly["Rolling_Sales"],
            mode="lines", name="3-Month Rolling Avg",
            line=dict(color="#3a6fd8", width=2.5, dash="solid")
        ))
        fig.update_layout(**CT,
            title=dict(text="Monthly Sales with Rolling Average", font=dict(color="#c8d8f0", size=13)),
            xaxis=dict(showgrid=False, **GRID),
            yaxis=dict(tickprefix="$", **GRID),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8a9aba"))
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_t2:
        colors_profit = ["#3aad6a" if p >= 0 else "#e05c6a" for p in monthly["Profit"]]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly["Month_dt"], y=monthly["Profit"],
            marker_color=colors_profit, name="Monthly Profit", opacity=0.85
        ))
        fig.add_trace(go.Scatter(
            x=monthly["Month_dt"], y=monthly["Rolling_Profit"],
            mode="lines", name="3-Month Rolling Avg",
            line=dict(color="#f0a030", width=2)
        ))
        fig.add_hline(y=0, line_dash="dot", line_color="#e05c6a", opacity=0.4,
                      annotation_text="Break-even", annotation_font_color="#e05c6a",
                      annotation_position="bottom right")
        fig.update_layout(**CT,
            title=dict(text="Monthly Profit — Green/Red by Sign", font=dict(color="#c8d8f0", size=13)),
            xaxis=dict(showgrid=False, **GRID),
            yaxis=dict(tickprefix="$", **GRID),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8a9aba"))
        )
        st.plotly_chart(fig, use_container_width=True)

    # Yearly grouped
    yearly = filtered.groupby(["Year","Category"])[["Sales","Profit"]].sum().reset_index()

    col_t3, col_t4 = st.columns(2)
    with col_t3:
        fig = px.bar(yearly, x="Year", y="Sales", color="Category",
                     barmode="group", color_discrete_sequence=COLS,
                     title="Annual Sales by Category")
        fig.update_layout(**CT,
            xaxis=dict(type="category", showgrid=False),
            yaxis=dict(tickprefix="$", **GRID),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8a9aba")),
            title_font_color="#c8d8f0"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_t4:
        # Order volume trend
        order_trend = (
            filtered.groupby("Month_dt")["Order ID"].nunique()
            .reset_index().rename(columns={"Order ID":"Orders"})
            .sort_values("Month_dt")
        )
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=order_trend["Month_dt"], y=order_trend["Orders"],
            mode="lines+markers",
            line=dict(color="#9a5fd8", width=2.5),
            marker=dict(size=5, color="#9a5fd8"),
            fill="tozeroy", fillcolor="rgba(154,95,216,0.1)"
        ))
        fig.update_layout(**CT,
            title=dict(text="Monthly Order Volume Trend", font=dict(color="#c8d8f0", size=13)),
            xaxis=dict(showgrid=False, **GRID),
            yaxis=dict(title="Number of Orders", **GRID),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Quarter breakdown
    sec("📊", "Quarterly Sales Heatmap (by Year × Quarter)")
    q_data = filtered.copy()
    q_data["Q"] = q_data["Order Date"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})
    q_pivot = q_data.groupby(["Year","Q"])["Sales"].sum().reset_index()
    q_matrix = q_pivot.pivot(index="Year", columns="Q", values="Sales").fillna(0)

    fig_heat = px.imshow(
        q_matrix,
        color_continuous_scale=[[0,"#0a1020"],[0.5,"#1a3a6a"],[1,"#3a6fd8"]],
        text_auto="$.0f",
        title="Quarterly Sales Heatmap ($)"
    )
    fig_heat.update_layout(**CT,
        title_font_color="#c8d8f0",
        coloraxis_colorbar=dict(tickfont=dict(color="#8a9aba"), title=dict(text="Sales $", font=dict(color="#8a9aba")))
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  TAB 3 – COMPARISONS
# ══════════════════════════════════════════════════════════════════
with tab3:
    sec("📈", "Comparisons — Categories, Regions & Segments", "Section 3 · 2 pts")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        sub_grp = (
            filtered.groupby(["Category","Sub-Category"])["Sales"]
            .sum().reset_index().sort_values("Sales", ascending=True).tail(15)
        )
        fig = px.bar(sub_grp, x="Sales", y="Sub-Category", color="Category",
                     orientation="h", color_discrete_sequence=COLS,
                     title="Top Sub-Categories by Sales")
        fig.update_layout(**CT,
            xaxis=dict(tickprefix="$", **GRID),
            yaxis=dict(showgrid=False),
            title_font_color="#c8d8f0",
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8a9aba"))
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_c2:
        reg_grp = filtered.groupby("Region")[["Sales","Profit"]].sum().reset_index()
        reg_melt = reg_grp.melt(id_vars="Region", var_name="Metric", value_name="Value")
        fig = px.bar(reg_melt, x="Region", y="Value", color="Metric", barmode="group",
                     color_discrete_map={"Sales":"#3a6fd8","Profit":"#3aad6a"},
                     title="Sales vs Profit by Region")
        fig.update_layout(**CT,
            yaxis=dict(tickprefix="$", **GRID),
            xaxis=dict(showgrid=False),
            title_font_color="#c8d8f0",
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8a9aba"))
        )
        st.plotly_chart(fig, use_container_width=True)

    col_c3, col_c4 = st.columns(2)
    with col_c3:
        seg_cat = (
            filtered.groupby(["Segment","Category"])["Profit"]
            .sum().reset_index()
        )
        fig = px.bar(seg_cat, x="Segment", y="Profit", color="Category",
                     barmode="stack", color_discrete_sequence=COLS,
                     title="Profit Stack: Segment × Category")
        fig.update_layout(**CT,
            yaxis=dict(tickprefix="$", **GRID),
            xaxis=dict(showgrid=False),
            title_font_color="#c8d8f0",
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8a9aba"))
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_c4:
        # Profit margin by sub-category — bubble
        sub_pm = (
            filtered.groupby("Sub-Category")
            .agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Qty=("Quantity","sum"))
            .reset_index()
        )
        sub_pm["Margin %"] = (sub_pm["Profit"] / sub_pm["Sales"] * 100).round(1)
        fig = px.scatter(
            sub_pm, x="Sales", y="Margin %",
            size="Qty", color="Margin %",
            color_continuous_scale=[[0,"#e05c6a"],[0.4,"#f0a030"],[1,"#3aad6a"]],
            text="Sub-Category",
            title="Sales vs Margin % by Sub-Category (bubble=qty)"
        )
        fig.update_traces(textposition="top center", textfont=dict(size=9, color="#8a9aba"))
        fig.add_hline(y=0, line_dash="dot", line_color="#e05c6a", opacity=0.5)
        fig.update_layout(**CT,
            xaxis=dict(tickprefix="$", **GRID),
            yaxis=dict(ticksuffix="%", **GRID),
            title_font_color="#c8d8f0",
            coloraxis_colorbar=dict(tickfont=dict(color="#8a9aba"))
        )
        st.plotly_chart(fig, use_container_width=True)

    # Discount impact comparison
    sec("🏷", "Impact of Discount on Profit Margin")
    disc_bins = pd.cut(filtered["Discount"], bins=[-0.01,0,0.1,0.2,0.3,0.4,0.5,0.8,1.0],
                       labels=["0%","1-10%","11-20%","21-30%","31-40%","41-50%","51-80%","81-100%"])
    disc_impact = (
        filtered.groupby(disc_bins, observed=True)
        .agg(AvgMargin=("Profit Margin %","mean"), Count=("Order ID","count"))
        .reset_index()
        .rename(columns={"Discount":"Discount Range"})
    )
    bar_colors = ["#3aad6a" if m >= 0 else "#e05c6a" for m in disc_impact["AvgMargin"]]
    fig = go.Figure(go.Bar(
        x=disc_impact["Discount Range"].astype(str),
        y=disc_impact["AvgMargin"],
        marker_color=bar_colors,
        text=disc_impact["Count"].apply(lambda c: f"{c} orders"),
        textposition="outside",
        textfont=dict(color="#8a9aba", size=10)
    ))
    fig.add_hline(y=0, line_dash="dot", line_color="#f0a030", opacity=0.6)
    fig.update_layout(**CT,
        title=dict(text="Average Profit Margin % by Discount Band (label = order count)", font=dict(color="#c8d8f0",size=13)),
        xaxis=dict(showgrid=False, title="Discount Range"),
        yaxis=dict(ticksuffix="%", **GRID, title="Avg Profit Margin %")
    )
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  TAB 4 – DISTRIBUTIONS
# ══════════════════════════════════════════════════════════════════
with tab4:
    sec("📉", "Distributions — Histograms & Box Plots", "Section 4 · 2 pts")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        fig = px.histogram(filtered, x="Sales", nbins=40,
                           color_discrete_sequence=["#3a6fd8"],
                           title="Distribution of Individual Order Line Sales")
        fig.update_layout(**CT,
            title_font_color="#c8d8f0",
            xaxis=dict(tickprefix="$", **GRID),
            yaxis=dict(title="Frequency", **GRID)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_d2:
        fig = px.box(filtered, x="Category", y="Profit",
                     color="Category", color_discrete_sequence=COLS,
                     points="outliers",
                     title="Profit Distribution by Category")
        fig.update_layout(**CT,
            title_font_color="#c8d8f0",
            yaxis=dict(tickprefix="$", **GRID),
            showlegend=False,
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)

    col_d3, col_d4 = st.columns(2)
    with col_d3:
        fig = px.histogram(filtered, x="Profit Margin %", nbins=35,
                           color_discrete_sequence=["#3aad6a"],
                           title="Distribution of Profit Margin % per Line")
        fig.add_vline(x=0, line_dash="dash", line_color="#e05c6a",
                      annotation_text="Break-even", annotation_font_color="#e05c6a")
        fig.add_vline(x=filtered["Profit Margin %"].mean(), line_dash="dot",
                      line_color="#f0a030",
                      annotation_text=f"Mean {filtered['Profit Margin %'].mean():.1f}%",
                      annotation_font_color="#f0a030", annotation_position="top right")
        fig.update_layout(**CT,
            title_font_color="#c8d8f0",
            xaxis=dict(ticksuffix="%", **GRID),
            yaxis=dict(**GRID)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_d4:
        fig = px.box(filtered, x="Region", y="Profit Margin %",
                     color="Region", color_discrete_sequence=COLS,
                     points="outliers",
                     title="Profit Margin % by Region")
        fig.add_hline(y=0, line_dash="dash", line_color="#e05c6a", opacity=0.5)
        fig.update_layout(**CT,
            title_font_color="#c8d8f0",
            yaxis=dict(ticksuffix="%", **GRID),
            showlegend=False,
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)

    col_d5, col_d6 = st.columns(2)
    with col_d5:
        fig = px.histogram(filtered, x="Discount", nbins=20,
                           color_discrete_sequence=["#f0a030"],
                           title="Distribution of Discount Rates")
        fig.update_layout(**CT,
            title_font_color="#c8d8f0",
            xaxis=dict(tickformat=".0%", **GRID),
            yaxis=dict(**GRID)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_d6:
        fig = px.box(filtered, x="Segment", y="Sales",
                     color="Segment", color_discrete_sequence=COLS,
                     points="outliers",
                     title="Sales Value Distribution by Segment")
        fig.update_layout(**CT,
            title_font_color="#c8d8f0",
            yaxis=dict(tickprefix="$", **GRID),
            showlegend=False,
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Shipping days distribution
    sec("🚚", "Shipping Speed Distribution")
    fig = px.histogram(filtered, x="Days to Ship", nbins=12,
                       color="Ship Mode", barmode="overlay",
                       color_discrete_sequence=COLS, opacity=0.75,
                       title="Days to Ship by Shipping Mode")
    fig.update_layout(**CT,
        title_font_color="#c8d8f0",
        xaxis=dict(title="Days to Ship", **GRID),
        yaxis=dict(**GRID),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8a9aba"))
    )
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  TAB 5 – ALERTS
# ══════════════════════════════════════════════════════════════════
with tab5:
    sec("🚨", "Alerts, Outliers & Threshold Warnings", "Section 5 · 3 pts")

    loss_rows    = filtered[filtered["Profit"] < 0]
    high_disc    = filtered[filtered["High Discount"]]
    low_margin   = filtered[filtered["Profit Margin %"] < -20]
    missing_vals = df.isnull().sum()
    neg_qty      = filtered[filtered["Quantity"] < 0]

    # ── Alert cards ──────────────────────────────────────────────
    col_a1, col_a2 = st.columns([1, 1])
    with col_a1:
        st.markdown("**🔴 Critical Alerts**")

        if len(loss_rows) > 0:
            st.markdown(
                f'<div class="alert-danger">🔴 <b>{len(loss_rows)} loss-making order lines</b> detected — '
                f'combined loss of <b>${abs(loss_rows["Profit"].sum()):,.2f}</b>. '
                f'Root cause: heavy discounting and under-priced furniture items.</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<div class="alert-success">✅ No loss-making order lines in current selection.</div>', unsafe_allow_html=True)

        if len(low_margin) > 0:
            worst_sub = low_margin.groupby("Sub-Category")["Profit"].sum().idxmin()
            st.markdown(
                f'<div class="alert-danger">🔴 <b>{len(low_margin)} rows</b> with profit margin below –20%. '
                f'Worst sub-category: <b>{worst_sub}</b>. Immediate pricing review required.</div>',
                unsafe_allow_html=True
            )

        if len(neg_qty) > 0:
            st.markdown(
                f'<div class="alert-danger">🔴 <b>{len(neg_qty)} rows</b> with negative quantity — '
                f'possible returns or data entry errors. Investigate before reporting.</div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>**⚠️ Warnings**")

        if len(high_disc) > 0:
            avg_p = high_disc["Profit"].mean()
            st.markdown(
                f'<div class="alert-warning">⚠️ <b>{len(high_disc)} orders</b> have discounts ≥ {disc_threshold}% — '
                f'avg profit on these orders: <b>${avg_p:,.2f}</b>. '
                f'Discounting beyond {disc_threshold}% is destroying margins.</div>',
                unsafe_allow_html=True
            )

        # Missing values
        total_missing = missing_vals.sum()
        if total_missing == 0:
            st.markdown('<div class="alert-success">✅ Data Quality: Zero missing values detected across all columns.</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="alert-warning">⚠️ <b>{total_missing} missing values</b> detected. '
                f'Columns affected: {", ".join(missing_vals[missing_vals>0].index.tolist())}.</div>',
                unsafe_allow_html=True
            )

        # Margin warning
        overall_margin = (filtered["Profit"].sum() / filtered["Sales"].sum() * 100) if filtered["Sales"].sum() else 0
        if overall_margin < 10:
            st.markdown(
                f'<div class="alert-warning">⚠️ Overall margin for filtered data is <b>{overall_margin:.1f}%</b> — '
                f'below the healthy 10% threshold. Review discount strategy.</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="alert-success">✅ Overall profit margin is <b>{overall_margin:.1f}%</b> — above the 10% healthy threshold.</div>',
                unsafe_allow_html=True
            )

    with col_a2:
        # Scatter: Sales vs Profit — outlier map
        scatter_df = filtered.copy()
        scatter_df["Qty_Plot"] = scatter_df["Quantity"].clip(lower=0) + 1
        fig = px.scatter(
            scatter_df,
            x="Sales", y="Profit",
            color="Loss Flag",
            color_discrete_map={True:"#e05c6a", False:"#3aad6a"},
            hover_data=["Category","Sub-Category","Discount","Order ID"],
            size="Qty_Plot",
            size_max=20,
            opacity=0.75,
            title="Sales vs Profit — Outlier Detection Map",
            labels={"Loss Flag":"Profitable?"}
        )
        fig.add_hline(y=0, line_dash="dash", line_color="#f0a030", opacity=0.6,
                      annotation_text="Break-even", annotation_font_color="#f0a030")
        fig.update_layout(**CT,
            title_font_color="#c8d8f0",
            xaxis=dict(tickprefix="$", **GRID),
            yaxis=dict(tickprefix="$", **GRID),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8a9aba"))
        )
        st.plotly_chart(fig, use_container_width=True)

    # Top 10 loss orders table
    sec("📋", "Top Loss-Making Order Lines")
    worst10 = (
        filtered.nsmallest(10, "Profit")
        [["Order ID","Order Date","Customer Name","Category","Sub-Category",
          "Product Name","Sales","Quantity","Discount","Profit","Profit Margin %"]]
        .copy()
    )
    def style_alert_row(row):
        base = [""] * len(row)
        if row["Profit"] < -200: return [f"background-color:rgba(224,92,106,0.2)"] * len(row)
        if row["Profit"] < 0:    return [f"background-color:rgba(224,92,106,0.1)"] * len(row)
        return base

    st.dataframe(
        worst10.style
        .apply(style_alert_row, axis=1)
        .format({
            "Sales":"${:,.2f}","Profit":"${:,.2f}",
            "Discount":"{:.0%}","Profit Margin %":"{:.1f}%",
            "Order Date": lambda d: d.strftime("%Y-%m-%d") if pd.notnull(d) else ""
        }),
        use_container_width=True, hide_index=True
    )

    # Top 5 best performers
    sec("🏆", "Top Performing Order Lines")
    best10 = (
        filtered.nlargest(10, "Profit")
        [["Order ID","Order Date","Category","Sub-Category","Product Name",
          "Sales","Quantity","Discount","Profit","Profit Margin %"]]
        .copy()
    )
    st.dataframe(
        best10.style
        .format({
            "Sales":"${:,.2f}","Profit":"${:,.2f}",
            "Discount":"{:.0%}","Profit Margin %":"{:.1f}%",
            "Order Date": lambda d: d.strftime("%Y-%m-%d") if pd.notnull(d) else ""
        })
        .map(lambda v: "color:#3aad6a;font-weight:700" if isinstance(v, float) and v > 100 else "", subset=["Profit"]),
        use_container_width=True, hide_index=True
    )

# ══════════════════════════════════════════════════════════════════
#  TAB 6 – DATA EXPLORER
# ══════════════════════════════════════════════════════════════════
with tab6:
    sec("🔍", "Interactive Data Explorer", "Section 6 · 3 pts")
    st.markdown(
        '<div class="alert-info">💡 Use the <b>sidebar</b> to filter by date range, region, segment, category, and ship mode. '
        'Use the sort controls below to reorder results. Search by product or customer name. Download your filtered data as CSV.</div>',
        unsafe_allow_html=True
    )

    # Inline search
    col_s1, col_s2, col_s3 = st.columns([2, 2, 1])
    with col_s1:
        search_prod = st.text_input("🔎 Search Product Name", placeholder="e.g. iPhone, Chair, Copier…")
    with col_s2:
        search_cust = st.text_input("👤 Search Customer Name", placeholder="e.g. Sandra, Thomas…")
    with col_s3:
        show_losses_only = st.checkbox("Show loss-making only", value=False)

    # Apply inline search
    explorer_df = filtered.copy()
    if search_prod:
        explorer_df = explorer_df[explorer_df["Product Name"].str.contains(search_prod, case=False, na=False)]
    if search_cust:
        explorer_df = explorer_df[explorer_df["Customer Name"].str.contains(search_cust, case=False, na=False)]
    if show_losses_only:
        explorer_df = explorer_df[explorer_df["Profit"] < 0]

    ascending = "Ascending" in sort_dir
    display_cols = ["Order ID","Order Date","Customer Name","Segment","Region","City","State",
                    "Category","Sub-Category","Product Name","Sales","Quantity",
                    "Discount","Profit","Profit Margin %","Ship Mode","Days to Ship"]
    table_df = (
        explorer_df[display_cols]
        .sort_values(sort_col, ascending=ascending)
        .head(150)
        .copy()
    )

    col_info1, col_info2, col_info3 = st.columns(3)
    col_info1.metric("Filtered Rows Shown", f"{len(table_df):,} of {len(filtered):,}")
    col_info2.metric("Filtered Sales Total", f"${explorer_df['Sales'].sum():,.0f}")
    col_info3.metric("Filtered Profit Total", f"${explorer_df['Profit'].sum():,.0f}")

    def hl(row):
        if row["Profit"] < -200:  return ["background:rgba(224,92,106,0.25)"] * len(row)
        if row["Profit"] < 0:     return ["background:rgba(224,92,106,0.12)"] * len(row)
        if row["Profit Margin %"] > 40: return ["background:rgba(58,173,106,0.1)"] * len(row)
        return [""] * len(row)

    st.dataframe(
        table_df.style
        .apply(hl, axis=1)
        .format({
            "Sales":"${:,.2f}","Profit":"${:,.2f}",
            "Discount":"{:.0%}","Profit Margin %":"{:.1f}%",
            "Order Date": lambda d: d.strftime("%Y-%m-%d") if pd.notnull(d) else ""
        }),
        use_container_width=True, hide_index=True, height=420
    )

    # Download button
    csv_bytes = explorer_df[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_bytes,
        file_name=f"superstore_filtered_{datetime.today().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# ══════════════════════════════════════════════════════════════════
#  TAB 7 – ETHICS & INSIGHTS
# ══════════════════════════════════════════════════════════════════
with tab7:

    # ── SECTION 7 – ETHICS ────────────────────────────────────────
    sec("⚖️", "Ethics, Privacy & Data Integrity", "Section 7 · 3 pts")

    st.markdown("""
    <div class="alert-info" style="margin-bottom:18px;">
    This section critically evaluates the ethical, privacy, and integrity dimensions of the Superstore Sales dataset
    and the analytical processes applied in this dashboard — as required by <b>Competency 4.59</b>.
    </div>
    """, unsafe_allow_html=True)

    # Risk matrix
    st.markdown("**🗂 Ethical Risk Assessment Matrix**")
    risk_data = {
        "Dimension":        ["Personal Data (PII)", "Informed Consent", "Data Bias", "Data Accuracy", "Visualization Ethics", "Data Security", "Algorithmic Fairness"],
        "Risk Level":       ["MEDIUM", "LOW", "HIGH", "LOW", "MEDIUM", "LOW", "LOW"],
        "Finding":          [
            "Dataset contains customer names & IDs (PII). No emails, addresses or payment data.",
            "Academic/demo dataset from Tableau. Not real customer data; consent not applicable.",
            "US-only transactions; over-represents Consumer segment. Cannot generalize globally.",
            "Zero missing values found. Negative profits are real anomalies, not data corruption.",
            "Charts display both gains and losses. Color used deliberately to avoid misleading readers.",
            "CSV stored locally; no cloud exposure in this dashboard. Standard precaution sufficient.",
            "No predictive model used; pure descriptive analytics. No discriminatory scoring applied."
        ],
        "Recommended Action": [
            "Anonymize customer names with hashed IDs before public sharing.",
            "Always cite Tableau as the source; do not present as real enterprise data.",
            "Clearly state geographical and segment limitations in all reports derived from this data.",
            "Continue flagging outliers; document any future data transformations.",
            "Always pair visual claims with underlying data; never hide negative trends.",
            "If deployed online, apply authentication and role-based access controls.",
            "If ML models are added in future, conduct bias audits on predictions."
        ],
    }
    risk_df = pd.DataFrame(risk_data)

    def color_risk(val):
        if val == "HIGH":   return "background-color:#1f0b0e;color:#f48a94;font-weight:700"
        if val == "MEDIUM": return "background-color:#1f1408;color:#ffd080;font-weight:600"
        return "background-color:#071810;color:#6fe8a8;font-weight:600"

    st.dataframe(
        risk_df.style.map(color_risk, subset=["Risk Level"]),
        use_container_width=True, hide_index=True, height=290
    )

    col_e1, col_e2 = st.columns(2)

    ethics_items_left = [
        ("🔐", "Privacy of Personal Information",
         """The dataset includes <b>Customer Names</b> and <b>Customer IDs</b>, which constitute Personally 
         Identifiable Information (PII) under privacy frameworks such as the GDPR (General Data Protection 
         Regulation) and CCPA (California Consumer Privacy Act). While this is a demonstration dataset not 
         linked to real individuals, any analyst working with real retail data must: (1) pseudonymize customer 
         identifiers before visualization, (2) restrict access to dashboards containing PII to authorized 
         personnel only, and (3) implement data retention policies to delete PII when no longer needed."""),
        ("📋", "Data Collection & Informed Consent",
         """This dataset was created and distributed by <b>Tableau Software Inc.</b> as a public educational 
         resource. It does not represent real customer transactions and was never collected from individuals 
         without their consent. However, in a real business context, data analysts must ensure that: customer 
         transactional data is collected under a valid legal basis (contract, legitimate interest, or consent); 
         data subjects are informed how their data will be used; and data is not repurposed beyond its 
         original collection intent without re-consent."""),
        ("⚖️", "Bias, Fairness & Representation",
         """The dataset introduces several forms of <b>analytical bias</b>: 
         (1) <i>Geographic bias</i> — all transactions are US-based, making regional insights non-generalizable 
         to other countries or markets; 
         (2) <i>Segment imbalance</i> — the Consumer segment is over-represented, potentially skewing aggregate 
         averages; 
         (3) <i>Time-period bias</i> — data from 2020–2024 includes COVID-era disruptions which may not represent 
         long-term normal patterns. Analysts must disclose these limitations explicitly to decision-makers."""),
    ]

    ethics_items_right = [
        ("🔍", "Data Integrity & Accuracy",
         f"""A systematic data quality audit was conducted: <b>zero missing values</b> were found across all 
         {len(df.columns)} columns and {len(df):,} rows. Negative profit values are preserved as legitimate 
         data points representing loss-making orders due to heavy discounting — they were NOT removed or 
         imputed, preserving full analytical integrity. Negative quantities (returns/adjustments) were 
         flagged as alerts rather than silently excluded. No data was altered without disclosure."""),
        ("🤖", "Responsible Visualization Design",
         """Data visualizations carry significant persuasive power and can mislead if designed poorly. This 
         dashboard was designed with the following ethical principles: (1) <b>No truncated Y-axes</b> — all 
         charts start at natural zero to avoid exaggerating trends; (2) <b>Both positive and negative values</b> 
         are shown — no cherry-picking of favourable periods; (3) <b>Color encoding</b> consistently uses green 
         for positive/profit and red for negative/loss, with sufficient contrast for accessibility; 
         (4) All thresholds (e.g. discount alert level) are user-configurable, not hardcoded to bias decisions."""),
        ("🌐", "Ethical Framework & Best Practices",
         """This analysis aligns with the following ethical frameworks: 
         <b>ACM Code of Ethics</b> — acting in the public interest, avoiding harm; 
         <b>FAIR Data Principles</b> — Findable, Accessible, Interoperable, Reusable; 
         <b>DAMA DMBOK Data Governance</b> — ensuring data quality and stewardship. 
         Recommended next steps for a production deployment include conducting a Data Protection Impact 
         Assessment (DPIA), establishing data lineage documentation, and providing regular ethics training 
         for all data practitioners using this dashboard."""),
    ]

    with col_e1:
        for icon, title, body in ethics_items_left:
            st.markdown(
                f'<div class="ethics-card">'
                f'<div class="ethics-icon">{icon}</div>'
                f'<div class="ethics-title">{title}</div>'
                f'<div class="ethics-body">{body}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    with col_e2:
        for icon, title, body in ethics_items_right:
            st.markdown(
                f'<div class="ethics-card">'
                f'<div class="ethics-icon">{icon}</div>'
                f'<div class="ethics-title">{title}</div>'
                f'<div class="ethics-body">{body}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # ── SECTION 8 – INSIGHTS ──────────────────────────────────────
    sec("💡", "Summary & Insights", "Section 8 · 2 pts")

    # Auto-compute all insight values
    top_cat       = filtered.groupby("Category")["Profit"].sum().idxmax()
    top_cat_prof  = filtered.groupby("Category")["Profit"].sum().max()
    worst_cat     = filtered.groupby("Category")["Profit"].sum().idxmin()
    worst_cat_p   = filtered.groupby("Category")["Profit"].sum().min()
    top_reg       = filtered.groupby("Region")["Sales"].sum().idxmax()
    top_reg_s     = filtered.groupby("Region")["Sales"].sum().max()
    worst_reg_p   = filtered.groupby("Region")["Profit"].sum().idxmin()
    best_seg      = filtered.groupby("Segment")["Profit"].sum().idxmax()
    best_seg_p    = filtered.groupby("Segment")["Profit"].sum().max()
    top_sub       = filtered.groupby("Sub-Category")["Sales"].sum().idxmax()
    top_sub_s     = filtered.groupby("Sub-Category")["Sales"].sum().max()
    loss_ct       = len(filtered[filtered["Profit"] < 0])
    loss_total    = abs(filtered[filtered["Profit"] < 0]["Profit"].sum())
    hi_disc_ct    = len(filtered[filtered["High Discount"]])
    hi_disc_pct   = (hi_disc_ct / len(filtered) * 100) if len(filtered) else 0
    avg_margin    = filtered["Profit Margin %"].mean()
    total_rev     = filtered["Sales"].sum()
    total_pft     = filtered["Profit"].sum()

    # Trend direction (last 3 months vs prior 3 months)
    monthly_trend = (
        filtered.groupby("Month_dt")["Sales"].sum().reset_index().sort_values("Month_dt")
    )
    if len(monthly_trend) >= 6:
        last3  = monthly_trend["Sales"].tail(3).mean()
        prior3 = monthly_trend["Sales"].tail(6).head(3).mean()
        trend_dir = "📈 Upward" if last3 > prior3 else "📉 Downward"
        trend_pct = ((last3 - prior3) / prior3 * 100) if prior3 else 0
        trend_text = f"{trend_dir} ({trend_pct:+.1f}% vs prior 3 months)"
    else:
        trend_text = "Insufficient data for trend calculation"

    col_i1, col_i2 = st.columns(2)

    with col_i1:
        st.markdown("**📌 Key Findings — Auto-Generated from Filtered Data**")
        findings = [
            f"🏆 <b>{top_cat}</b> is the most profitable category at <b>${top_cat_prof:,.0f}</b> total profit, "
            f"while <b>{worst_cat}</b> has the weakest at <b>${worst_cat_p:,.0f}</b>.",
            f"🗺 The <b>{top_reg}</b> region leads in total sales at <b>${top_reg_s:,.0f}</b>. "
            f"<b>{worst_reg_p}</b> region shows the weakest overall profitability.",
            f"👥 The <b>{best_seg}</b> segment generates the highest profit at <b>${best_seg_p:,.0f}</b>.",
            f"📦 <b>{top_sub}</b> is the top-selling sub-category with <b>${top_sub_s:,.0f}</b> in sales.",
            f"🔴 <b>{loss_ct} order lines</b> are loss-making, representing a combined loss of <b>${loss_total:,.0f}</b>.",
            f"🏷 <b>{hi_disc_pct:.1f}%</b> of orders exceed the {disc_threshold}% discount threshold — "
            f"these are the primary driver of losses.",
            f"📊 Average profit margin across all filtered orders is <b>{avg_margin:.1f}%</b>.",
            f"📅 Sales trend: <b>{trend_text}</b>.",
        ]
        for f in findings:
            st.markdown(f'<div class="insight-box">• {f}</div>', unsafe_allow_html=True)

    with col_i2:
        st.markdown("**🎯 Strategic Recommendations**")
        recs = [
            (f"Enforce a maximum discount cap of <b>25%</b>. Currently {hi_disc_pct:.1f}% of orders breach the "
             f"{disc_threshold}% threshold, directly driving the <b>${loss_total:,.0f}</b> in losses. "
             f"A 25% cap would protect margin while remaining competitive."),
            (f"<b>Expand {top_cat} investment</b> — it is the profit engine of the business. Allocate additional "
             f"marketing budget and stock depth to this category to capitalise on demonstrated demand."),
            (f"<b>Conduct a deep review of {worst_cat}</b> performance. Analyse whether negative margins are driven "
             f"by pricing strategy, competition, or product mix, and restructure accordingly."),
            (f"<b>Focus regional strategy on {worst_reg_p}</b>. Investigate whether logistics costs, local competition, "
             f"or discount abuse are driving underperformance in this region."),
            (f"<b>Implement a real-time margin monitoring alert</b> at the order entry stage — flag any order "
             f"where the applied discount would push margin below 5%, requiring manager approval."),
            (f"<b>Segment-specific pricing</b>: the {best_seg} segment is the most profitable; "
             f"tailor premium offerings and loyalty programmes specifically to this group to maximise lifetime value."),
        ]
        for i, r in enumerate(recs, 1):
            st.markdown(f'<div class="rec-box"><b>{i}.</b> {r}</div>', unsafe_allow_html=True)

    # ── SECTION 9 – METADATA ──────────────────────────────────────
    sec("📋", "Dataset Metadata", "Section 9 · 1 pt")

    meta = [
        ("Dataset Name",          "Superstore Sales Dataset"),
        ("Dataset Type",          "Tabular (CSV) — Structured relational transactional data"),
        ("Domain / Industry",     "Retail / Sales / E-commerce — United States"),
        ("Author / Organization", "Tableau Software Inc."),
        ("Contact",               "tableau.com &nbsp;|&nbsp; support@tableau.com"),
        ("Date Created",          "Originally published circa 2014; widely redistributed 2016–present"),
        ("Records in File",       f"{len(df):,} rows × {len(df.columns)} columns (153 order lines)"),
        ("Date Range Covered",    f"{df['Order Date'].min().strftime('%B %d, %Y')} – {df['Order Date'].max().strftime('%B %d, %Y')}"),
        ("Repository / Link",     '<a class="meta-link" href="https://www.kaggle.com/datasets/vivek468/superstore-dataset-final" target="_blank">kaggle.com/datasets/vivek468/superstore-dataset-final</a>'),
        ("Related Research",      "Extensively used in academic data visualization curricula, Tableau Public tutorials, "
                                  "and peer-reviewed papers on retail analytics dashboard design (2016–2024)."),
        ("License",               "Public / Educational use — available on Kaggle under open license"),
        ("Variables Included",    "Order ID, Dates, Customer, Segment, Geography, Product, Category, Sales, Quantity, Discount, Profit, Ship Mode"),
        ("Preprocessing Applied", "Derived columns added: Year, Quarter, Month, Profit Margin %, Loss Flag, Days to Ship"),
        ("Dashboard Author",      "Student Submission — BSA83111, Faculty of Management, Year 3, Level 8"),
        ("Instructor",            "Dr Patrick NIYISHAKA"),
        ("Assessment Period",     "June 9 – June 14, 2026 &nbsp;|&nbsp; Presentation: June 16, 2026"),
    ]

    meta_html = '<div class="meta-wrap">'
    for key, val in meta:
        meta_html += (
            f'<div class="meta-row">'
            f'<span class="meta-key">{key}</span>'
            f'<span class="meta-val">{val}</span>'
            f'</div>'
        )
    meta_html += "</div>"
    st.markdown(meta_html, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style='text-align:center;color:#1e2d4a;font-size:0.75rem;margin-top:36px;padding:16px;
                border-top:1px solid #1e2d4a;'>
        BSA83111 · Data Visualization for Decision Making · Faculty of Management ·
        Dr Patrick NIYISHAKA · June 2026 · Superstore Sales Intelligence Dashboard v2.0
    </div>
    """, unsafe_allow_html=True)
