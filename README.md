# 🛒 Superstore Sales Intelligence Dashboard
### BSA83111 · Data Visualization for Decision Making
**Faculty of Management | Year 3 | Trimester 1 | Level 8**  
**Instructor:** Dr Patrick NIYISHAKA  
**Assessment Period:** June 9–14, 2026 | **Presentation:** June 16, 2026

---

## 📦 Files in This Submission

| File | Description |
|------|-------------|
| `dashboard.py` | Main Streamlit dashboard (submit this) |
| `superstore_sales.csv` | Dataset — must be in the **same folder** as dashboard.py |
| `requirements.txt` | Python dependencies for Streamlit Cloud |
| `.streamlit/config.toml` | Theme and server configuration |

---

## 🖥 Option A — Run Locally

### Step 1: Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the dashboard
```bash
streamlit run dashboard.py
```

The dashboard opens automatically at **http://localhost:8501**

> ⚠️ Both `dashboard.py` and `superstore_sales.csv` must be in the **same folder**.

---

## ☁️ Option B — Deploy on Streamlit Cloud (share.streamlit.io)

### Step 1: Create a GitHub repository
1. Go to [github.com](https://github.com) → **New repository**
2. Name it e.g. `bsa83111-dashboard`
3. Set it to **Public**

### Step 2: Upload all files to GitHub
Upload these 4 items to the root of your repository:
```
dashboard.py
superstore_sales.csv
requirements.txt
.streamlit/
    config.toml
```

### Step 3: Deploy on Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select:
   - **Repository:** your repo name
   - **Branch:** `main`
   - **Main file path:** `dashboard.py`
5. Click **"Deploy!"**

Your dashboard will be live at:  
`https://<your-username>-bsa83111-dashboard-dashboard-<hash>.streamlit.app`

---

## 📊 Dashboard Sections & Assessment Coverage

| # | Section | Content | Points |
|---|---------|---------|--------|
| 1 | **KPIs & Overview** | 8 KPI cards, category summary table, 3 donut charts | 2 pts |
| 2 | **Trends Over Time** | Monthly sales/profit with rolling avg, YoY bar, order volume, quarterly heatmap | 2 pts |
| 3 | **Comparisons** | Sub-category bars, region comparison, segment×category stack, discount impact | 2 pts |
| 4 | **Distributions** | 6 histograms & box plots (sales, profit, margin, discount, segment, ship days) | 2 pts |
| 5 | **Alerts & Highlights** | Colour-coded alerts, outlier scatter, top-10 loss & profit tables | 3 pts |
| 6 | **Data Explorer** | Product/customer search, loss filter, sort, colour-coded table, CSV download | 3 pts |
| 7 | **Ethics Section** | Risk matrix table + 6 ethics cards (privacy, consent, bias, integrity, viz, frameworks) | 3 pts |
| 8 | **Summary & Insights** | 8 auto-generated findings + 6 strategic recommendations | 2 pts |
| 9 | **Metadata** | Full dataset metadata table | 1 pt |
| **TOTAL** | | | **20 pts** |

---

## 🔧 Compatibility Notes

- Tested with **Python 3.10, 3.11, 3.12**
- Tested with **pandas 2.x** (uses `.map()` not deprecated `.applymap()`)
- Tested with **Streamlit 1.32+** (uses `@st.cache_data`, tabs, download_button)
- No external API calls, no authentication required
- Negative quantity values are safely handled in scatter plots (clipped to 0)

---

## 📚 Dataset Reference

- **Name:** Superstore Sales Dataset
- **Author:** Tableau Software Inc.
- **Source:** https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
- **License:** Public / Educational use
