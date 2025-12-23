# Streamlit Production Patterns

Enterprise-grade dashboard patterns for executive reporting.

## Project Structure

```
dashboard/
├── app.py                  # Main entry point
├── pages/
│   ├── 01_Executive_Summary.py
│   ├── 02_Revenue_Analysis.py
│   ├── 03_Unit_Economics.py
│   └── 04_Cohort_Analysis.py
├── components/
│   ├── __init__.py
│   ├── charts.py           # Plotly chart functions
│   ├── kpis.py             # KPI card components
│   └── filters.py          # Sidebar filters
├── data/
│   ├── __init__.py
│   ├── loader.py           # Data loading
│   └── transforms.py       # Data transformations
├── styles/
│   └── theme.css           # Custom CSS
├── .streamlit/
│   └── config.toml         # Streamlit config
└── requirements.txt
```

## Configuration

### .streamlit/config.toml

```toml
[theme]
primaryColor = "#003366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#333333"
font = "sans serif"

[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

## Main App Template

```python
# app.py
import streamlit as st
from components.charts import exec_line_chart, exec_waterfall
from components.kpis import kpi_row
from data.loader import load_data

# Page config
st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Executive typography */
    h1 {
        font-family: Georgia, serif;
        color: #003366;
    }

    /* KPI cards */
    .kpi-card {
        background: linear-gradient(135deg, #003366, #0066CC);
        padding: 24px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .kpi-value {
        font-size: 32px;
        font-weight: bold;
        margin: 8px 0;
    }

    .kpi-label {
        font-size: 14px;
        opacity: 0.9;
    }

    .kpi-delta {
        font-size: 14px;
        margin-top: 4px;
    }

    .kpi-delta.positive { color: #90EE90; }
    .kpi-delta.negative { color: #FF6B6B; }

    /* Clean tables */
    .dataframe {
        font-family: Arial, sans-serif;
        font-size: 12px;
    }

    /* Chart containers */
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Executive Dashboard")
st.markdown("---")

# Load data (cached)
@st.cache_data(ttl=3600)
def get_data():
    return load_data()

df = get_data()
```

## KPI Components

### kpis.py

```python
import streamlit as st

def kpi_card(label: str, value: str, delta: str = None, delta_positive: bool = True):
    """Render a single KPI card."""
    delta_class = "positive" if delta_positive else "negative"
    delta_html = f'<div class="kpi-delta {delta_class}">{delta}</div>' if delta else ""

    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)


def kpi_row(metrics: list[dict]):
    """
    Render a row of KPI cards.

    metrics = [
        {'label': 'MRR', 'value': '$125K', 'delta': '+12%', 'positive': True},
        {'label': 'ARR', 'value': '$1.5M', 'delta': '+45%', 'positive': True},
        ...
    ]
    """
    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):
        with col:
            kpi_card(
                label=metric['label'],
                value=metric['value'],
                delta=metric.get('delta'),
                delta_positive=metric.get('positive', True),
            )


def metric_comparison(current: float, prior: float, format_str: str = "${:,.0f}"):
    """Calculate and format metric comparison."""
    delta = current - prior
    delta_pct = (current - prior) / prior * 100 if prior != 0 else 0

    return {
        'value': format_str.format(current),
        'delta': f"{delta_pct:+.1f}%",
        'positive': delta >= 0,
    }
```

## Sidebar Filters

### filters.py

```python
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def date_range_filter(df: pd.DataFrame, date_col: str = 'date'):
    """Add date range filter to sidebar."""
    st.sidebar.markdown("### 📅 Date Range")

    min_date = df[date_col].min().date()
    max_date = df[date_col].max().date()

    # Quick select buttons
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Last 30 days"):
            start = max_date - timedelta(days=30)
            end = max_date
    with col2:
        if st.button("Last 90 days"):
            start = max_date - timedelta(days=90)
            end = max_date

    # Date inputs
    start_date = st.sidebar.date_input("Start", min_date)
    end_date = st.sidebar.date_input("End", max_date)

    return start_date, end_date


def segment_filter(df: pd.DataFrame, segment_col: str = 'segment'):
    """Add segment multi-select filter."""
    st.sidebar.markdown("### 🎯 Segments")

    segments = df[segment_col].unique().tolist()
    selected = st.sidebar.multiselect(
        "Select segments",
        options=segments,
        default=segments,
    )

    return selected


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply all filters to dataframe."""
    filtered = df.copy()

    if 'date_range' in filters:
        start, end = filters['date_range']
        filtered = filtered[
            (filtered['date'] >= pd.Timestamp(start)) &
            (filtered['date'] <= pd.Timestamp(end))
        ]

    if 'segments' in filters:
        filtered = filtered[filtered['segment'].isin(filters['segments'])]

    return filtered
```

## Data Caching

### loader.py

```python
import streamlit as st
import pandas as pd
from pathlib import Path

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_csv(path: str) -> pd.DataFrame:
    """Load CSV with caching."""
    return pd.read_csv(path, parse_dates=['date'])


@st.cache_data(ttl=3600)
def load_from_database(query: str) -> pd.DataFrame:
    """Load from database with caching."""
    import duckdb
    conn = duckdb.connect(':memory:')
    return conn.execute(query).df()


@st.cache_resource
def get_database_connection():
    """Cache database connection (doesn't expire)."""
    import duckdb
    return duckdb.connect('data/analytics.duckdb')


def invalidate_cache():
    """Clear all cached data."""
    st.cache_data.clear()
    st.toast("Cache cleared!", icon="🗑️")
```

## Multi-Page Dashboard

### pages/01_Executive_Summary.py

```python
import streamlit as st
from components.kpis import kpi_row, metric_comparison
from components.charts import exec_line_chart

st.title("Executive Summary")

# Get data from session state or reload
df = st.session_state.get('data')

# Calculate metrics
current_mrr = df[df['period'] == df['period'].max()]['mrr'].sum()
prior_mrr = df[df['period'] == df['period'].max() - 1]['mrr'].sum()

metrics = [
    {**metric_comparison(current_mrr, prior_mrr), 'label': 'MRR'},
    {**metric_comparison(current_mrr * 12, prior_mrr * 12), 'label': 'ARR'},
    {'label': 'LTV:CAC', 'value': '4.2x', 'delta': '+0.3x', 'positive': True},
    {'label': 'NRR', 'value': '115%', 'delta': '+5%', 'positive': True},
]

kpi_row(metrics)

st.markdown("---")

# Revenue trend
st.subheader("Revenue Growth Exceeds Plan by 15%")
fig = exec_line_chart(df, 'month', 'mrr', '')
st.plotly_chart(fig, use_container_width=True)
```

## File Upload Handler

```python
def file_upload_section():
    """Handle file uploads with format detection."""
    st.sidebar.markdown("### 📁 Data Upload")

    uploaded_file = st.sidebar.file_uploader(
        "Upload data file",
        type=['csv', 'xlsx', 'json', 'parquet'],
        help="Supports CSV, Excel, JSON, and Parquet formats"
    )

    if uploaded_file:
        file_type = uploaded_file.name.split('.')[-1].lower()

        try:
            if file_type == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_type in ['xlsx', 'xls']:
                df = pd.read_excel(uploaded_file)
            elif file_type == 'json':
                df = pd.read_json(uploaded_file)
            elif file_type == 'parquet':
                df = pd.read_parquet(uploaded_file)

            st.session_state['uploaded_data'] = df
            st.sidebar.success(f"✅ Loaded {len(df):,} rows")
            return df

        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")
            return None

    return None
```

## Export Functions

```python
def add_export_buttons(df: pd.DataFrame, fig=None):
    """Add download buttons for data and charts."""
    col1, col2, col3 = st.columns(3)

    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv,
            "data.csv",
            "text/csv",
        )

    with col2:
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False)
        st.download_button(
            "📥 Download Excel",
            excel_buffer.getvalue(),
            "data.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with col3:
        if fig:
            img_bytes = fig.to_image(format="png", scale=2)
            st.download_button(
                "📥 Download Chart",
                img_bytes,
                "chart.png",
                "image/png",
            )
```

## Deployment

### requirements.txt

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.18.0
altair>=5.0.0
openpyxl>=3.1.0
pdfplumber>=0.10.0
python-pptx>=0.6.21
duckdb>=0.9.0
```

### Deploy to Streamlit Cloud

1. Push to GitHub
2. Connect at share.streamlit.io
3. Configure secrets in dashboard
4. Set Python version in `runtime.txt`

### Deploy to Vercel

```json
// vercel.json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

## Performance Tips

```python
# 1. Use caching aggressively
@st.cache_data
def expensive_computation(df):
    return df.groupby('segment').agg(...)

# 2. Lazy load pages
if st.session_state.get('page') == 'cohort':
    from pages import cohort_analysis
    cohort_analysis.render()

# 3. Use DuckDB for large datasets
import duckdb
result = duckdb.query("SELECT * FROM df WHERE revenue > 1000").df()

# 4. Limit displayed rows
st.dataframe(df.head(1000))

# 5. Use fragments for partial updates (Streamlit 1.33+)
@st.fragment
def chart_section():
    fig = create_chart(df)
    st.plotly_chart(fig)
```
