# Executive Chart Gallery

20+ chart templates for investor presentations and C-suite reporting.

## Color Palettes

### McKinsey Blue

```python
MCKINSEY = {
    'primary': '#003366',
    'secondary': '#0066CC',
    'tertiary': '#66A3D2',
    'accent': '#FF6B35',
    'positive': '#2E7D32',
    'negative': '#C62828',
    'neutral': '#757575',
    'background': '#FFFFFF',
}
```

### BCG Green

```python
BCG = {
    'primary': '#00A651',
    'secondary': '#006633',
    'tertiary': '#99CC99',
    'accent': '#FFC107',
    'text': '#333333',
}
```

### Bain Red

```python
BAIN = {
    'primary': '#CC0000',
    'secondary': '#990000',
    'accent': '#003366',
    'text': '#333333',
}
```

## Financial Charts

### Revenue Waterfall

```python
import plotly.graph_objects as go

def revenue_waterfall(data: dict, title: str = "Revenue Bridge"):
    """
    data = {
        'Starting ARR': 1000000,
        'New Business': 250000,
        'Expansion': 150000,
        'Contraction': -50000,
        'Churn': -100000,
        'Ending ARR': 1250000,
    }
    """
    labels = list(data.keys())
    values = list(data.values())

    measures = ['absolute'] + ['relative'] * (len(values) - 2) + ['total']

    fig = go.Figure(go.Waterfall(
        name="Revenue",
        orientation="v",
        measure=measures,
        x=labels,
        y=values,
        textposition="outside",
        text=[f"${v/1000:.0f}K" for v in values],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#2E7D32"}},
        decreasing={"marker": {"color": "#C62828"}},
        totals={"marker": {"color": "#003366"}},
    ))

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=20, family="Georgia")),
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        showlegend=False,
        yaxis=dict(
            title="Revenue ($)",
            tickformat="$,.0f",
            gridcolor='#E5E5E5',
        ),
    )

    return fig
```

### MRR Growth Chart with Target

```python
def mrr_growth_vs_target(df, title="MRR vs Target"):
    """
    df columns: month, actual_mrr, target_mrr
    """
    fig = go.Figure()

    # Target line (dashed)
    fig.add_trace(go.Scatter(
        x=df['month'],
        y=df['target_mrr'],
        mode='lines',
        name='Target',
        line=dict(color='#757575', dash='dash', width=2),
    ))

    # Actual line (solid)
    fig.add_trace(go.Scatter(
        x=df['month'],
        y=df['actual_mrr'],
        mode='lines+markers',
        name='Actual',
        line=dict(color='#003366', width=3),
        marker=dict(size=8),
    ))

    # Shade area between
    fig.add_trace(go.Scatter(
        x=df['month'].tolist() + df['month'].tolist()[::-1],
        y=df['actual_mrr'].tolist() + df['target_mrr'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(0,51,102,0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
    ))

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=20, family="Georgia")),
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        yaxis=dict(tickformat="$,.0f", gridcolor='#E5E5E5'),
        xaxis=dict(showgrid=False),
    )

    return fig
```

### CAC vs LTV Comparison

```python
def cac_ltv_comparison(cac, ltv, title="Unit Economics"):
    """Bar chart comparing CAC to LTV with ratio annotation."""
    ratio = ltv / cac

    fig = go.Figure(data=[
        go.Bar(
            x=['CAC', 'LTV'],
            y=[cac, ltv],
            marker_color=['#C62828', '#2E7D32'],
            text=[f"${cac:,.0f}", f"${ltv:,.0f}"],
            textposition='outside',
        )
    ])

    # Add ratio annotation
    fig.add_annotation(
        x=0.5, y=max(cac, ltv) * 1.15,
        text=f"<b>LTV:CAC = {ratio:.1f}x</b>",
        showarrow=False,
        font=dict(size=16, color='#003366'),
    )

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=20, family="Georgia")),
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        showlegend=False,
        yaxis=dict(tickformat="$,.0f", gridcolor='#E5E5E5'),
    )

    return fig
```

## Comparison Charts

### Competitive Positioning Matrix (XY Plot)

```python
def competitive_matrix(companies: list[dict], title="Competitive Positioning"):
    """
    companies = [
        {'name': 'Us', 'x': 8, 'y': 9, 'size': 100, 'color': 'primary'},
        {'name': 'Competitor A', 'x': 6, 'y': 7, 'size': 80, 'color': 'neutral'},
    ]
    """
    fig = go.Figure()

    for c in companies:
        color = MCKINSEY.get(c.get('color', 'neutral'), '#757575')
        fig.add_trace(go.Scatter(
            x=[c['x']],
            y=[c['y']],
            mode='markers+text',
            name=c['name'],
            text=[c['name']],
            textposition='top center',
            marker=dict(size=c.get('size', 50), color=color, opacity=0.7),
        ))

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=20, family="Georgia")),
        xaxis=dict(title="Feature Completeness", range=[0, 10], gridcolor='#E5E5E5'),
        yaxis=dict(title="Ease of Use", range=[0, 10], gridcolor='#E5E5E5'),
        plot_bgcolor='white',
        showlegend=False,
    )

    return fig
```

### Stacked Bar (Revenue by Segment)

```python
def revenue_by_segment(df, title="Revenue by Customer Segment"):
    """df columns: period, enterprise, mid_market, smb"""
    fig = go.Figure()

    segments = ['enterprise', 'mid_market', 'smb']
    colors = ['#003366', '#0066CC', '#66A3D2']

    for seg, color in zip(segments, colors):
        fig.add_trace(go.Bar(
            x=df['period'],
            y=df[seg],
            name=seg.replace('_', ' ').title(),
            marker_color=color,
        ))

    fig.update_layout(
        barmode='stack',
        title=dict(text=f"<b>{title}</b>", font=dict(size=20, family="Georgia")),
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        yaxis=dict(tickformat="$,.0f", gridcolor='#E5E5E5'),
    )

    return fig
```

## Time Series Charts

### Area Chart with Forecast

```python
def revenue_with_forecast(df, forecast_start, title="Revenue Projection"):
    """
    df columns: date, revenue, forecast
    """
    fig = go.Figure()

    # Historical (solid)
    historical = df[df['date'] < forecast_start]
    fig.add_trace(go.Scatter(
        x=historical['date'],
        y=historical['revenue'],
        fill='tozeroy',
        mode='lines',
        name='Actual',
        line=dict(color='#003366'),
        fillcolor='rgba(0,51,102,0.3)',
    ))

    # Forecast (dashed + lighter fill)
    forecast = df[df['date'] >= forecast_start]
    fig.add_trace(go.Scatter(
        x=forecast['date'],
        y=forecast['forecast'],
        fill='tozeroy',
        mode='lines',
        name='Forecast',
        line=dict(color='#0066CC', dash='dash'),
        fillcolor='rgba(0,102,204,0.2)',
    ))

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=20, family="Georgia")),
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        yaxis=dict(tickformat="$,.0f", gridcolor='#E5E5E5'),
    )

    return fig
```

## Pie & Donut Charts

### Revenue Mix Donut

```python
def revenue_mix_donut(data: dict, title="Revenue Mix"):
    """data = {'Subscriptions': 70, 'Services': 20, 'Other': 10}"""
    labels = list(data.keys())
    values = list(data.values())

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(colors=['#003366', '#0066CC', '#66A3D2', '#99C2E5']),
        textinfo='label+percent',
        textposition='outside',
    ))

    # Center annotation
    total = sum(values)
    fig.add_annotation(
        text=f"<b>100%</b><br>Revenue",
        x=0.5, y=0.5,
        font=dict(size=16),
        showarrow=False,
    )

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=20, family="Georgia")),
        font=dict(family="Arial", size=12),
        showlegend=True,
    )

    return fig
```

## KPI Cards (Streamlit)

```python
def kpi_card(label: str, value: str, delta: str = None, delta_color: str = "normal"):
    """Generate HTML for executive KPI card."""
    delta_html = ""
    if delta:
        color = "#2E7D32" if delta_color == "normal" and delta.startswith("+") else "#C62828"
        delta_html = f'<div style="color: {color}; font-size: 14px;">{delta}</div>'

    return f"""
    <div style="
        background: linear-gradient(135deg, #003366, #0066CC);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    ">
        <div style="font-size: 14px; opacity: 0.9;">{label}</div>
        <div style="font-size: 28px; font-weight: bold; margin: 8px 0;">{value}</div>
        {delta_html}
    </div>
    """
```

## Export Functions

```python
def export_chart(fig, filename: str, format: str = 'png'):
    """Export chart to file."""
    if format == 'png':
        fig.write_image(f"{filename}.png", scale=2, width=1200, height=600)
    elif format == 'html':
        fig.write_html(f"{filename}.html", include_plotlyjs='cdn')
    elif format == 'pdf':
        fig.write_image(f"{filename}.pdf", width=1200, height=600)
    elif format == 'svg':
        fig.write_image(f"{filename}.svg", width=1200, height=600)

def export_all_for_presentation(charts: dict, output_dir: str):
    """Export all charts for PowerPoint insertion."""
    from pathlib import Path
    Path(output_dir).mkdir(exist_ok=True)

    for name, fig in charts.items():
        fig.write_image(f"{output_dir}/{name}.png", scale=2, width=1200, height=600)

    print(f"Exported {len(charts)} charts to {output_dir}/")
```
