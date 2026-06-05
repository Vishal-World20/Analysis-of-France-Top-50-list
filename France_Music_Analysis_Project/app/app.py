import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="France Top 50 · Playlist Analysis",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:          #0d0f14;
    --surface:     #161921;
    --surface2:    #1e2230;
    --border:      #2a2f42;
    --accent:      #e8f24a;        /* electric yellow-green */
    --accent2:     #5c6fff;        /* electric blue */
    --accent3:     #ff5c8a;        /* hot pink */
    --text:        #f0f2f5;
    --muted:       #6b7280;
    --radius:      12px;
}

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1400px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1a1f35 0%, #0d0f14 60%, #1a1424 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.8rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(232,242,74,.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 20%;
    width: 320px; height: 200px;
    background: radial-gradient(ellipse, rgba(92,111,255,.10) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: var(--accent);
    background: rgba(232,242,74,.1);
    border: 1px solid rgba(232,242,74,.25);
    border-radius: 99px;
    padding: .25rem .85rem;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 .6rem;
    background: linear-gradient(135deg, #f0f2f5 30%, #b0b8d8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1rem;
    color: var(--muted);
    font-weight: 400;
}

/* ── KPI cards ── */
.kpi-grid { display: flex; gap: 1.2rem; margin-bottom: 2rem; flex-wrap: wrap; }
.kpi-card {
    flex: 1; min-width: 180px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color .2s, transform .2s;
}
.kpi-card:hover { border-color: var(--accent); transform: translateY(-2px); }
.kpi-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,.03) 0%, transparent 60%);
    pointer-events: none;
}
.kpi-icon { font-size: 1.4rem; margin-bottom: .5rem; }
.kpi-label {
    font-size: .72rem;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: var(--muted);
    font-weight: 500;
    margin-bottom: .3rem;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
}
.kpi-accent-yellow .kpi-value { color: var(--accent); }
.kpi-accent-blue   .kpi-value { color: var(--accent2); }
.kpi-accent-pink   .kpi-value { color: var(--accent3); }
.kpi-accent-green  .kpi-value { color: #4ade80; }

/* ── Section headers ── */
.section-head {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: .6rem;
}
.section-head::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
    margin-left: .5rem;
}

/* ── Chart wrappers ── */
.chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem 1rem;
    margin-bottom: 1.5rem;
}

/* ── Top-track table ── */
.track-table { width: 100%; border-collapse: collapse; }
.track-table th {
    text-align: left;
    font-size: .7rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--muted);
    padding: .5rem .8rem;
    border-bottom: 1px solid var(--border);
}
.track-table td { padding: .65rem .8rem; font-size: .85rem; border-bottom: 1px solid rgba(255,255,255,.04); }
.track-table tr:last-child td { border-bottom: none; }
.track-table tr:hover td { background: rgba(255,255,255,.03); }
.pop-bar-bg { background: var(--surface2); border-radius: 99px; height: 6px; width: 100px; }
.pop-bar { background: linear-gradient(90deg, var(--accent2), var(--accent)); border-radius: 99px; height: 6px; }
.badge {
    display: inline-block;
    font-size: .65rem;
    padding: .15rem .55rem;
    border-radius: 99px;
    font-weight: 600;
    letter-spacing: .05em;
}
.badge-explicit { background: rgba(255,92,138,.15); color: var(--accent3); border: 1px solid rgba(255,92,138,.3); }
.badge-clean    { background: rgba(74,222,128,.12); color: #4ade80;        border: 1px solid rgba(74,222,128,.25); }

/* ── Sidebar filters label ── */
.sidebar-label {
    font-family: 'Syne', sans-serif;
    font-size: .8rem;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .4rem;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Streamlit multiselect tokens ── */
span[data-baseweb="tag"] {
    background-color: rgba(92,111,255,.25) !important;
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Plotly dark theme helper ─────────────────────────────────────────────────
CHART_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#9ca3af", size=12),
    margin=dict(l=16, r=16, t=40, b=16),
)
COLORS = ["#5c6fff", "#e8f24a", "#ff5c8a", "#4ade80", "#f97316", "#a78bfa"]


# ── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('data/Atlantic_France.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['duration_min'] = df['duration_ms'] / 60000
    df['album_type'] = df['album_type'].str.lower().str.strip()
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-label">🎛 Filters</div>', unsafe_allow_html=True)
    st.markdown("---")

    album_types = sorted(df['album_type'].dropna().unique())
    album_filter = st.multiselect(
        "Album Type",
        options=album_types,
        default=album_types,
        help="Filter charts by album type"
    )

    st.markdown("---")
    st.markdown('<div class="sidebar-label">📅 Date Range</div>', unsafe_allow_html=True)
    min_date, max_date = df['date'].min().date(), df['date'].max().date()
    date_range = st.date_input(
        "Select range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    st.markdown("---")
    st.markdown('<div class="sidebar-label">🏆 Top Tracks N</div>', unsafe_allow_html=True)
    top_n = st.slider("Show top N tracks", min_value=5, max_value=30, value=10, step=5)

    st.markdown("---")
    st.caption("France Top 50 · Playlist Analytics Dashboard")

# ── Filter data ───────────────────────────────────────────────────────────────
filtered = df[df['album_type'].isin(album_filter)]
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered = filtered[(filtered['date'] >= start) & (filtered['date'] <= end)]

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">🇫🇷 Atlantic Records · France</div>
    <div class="hero-title">France Top 50<br>Playlist Analysis</div>
    <div class="hero-sub">{len(filtered):,} tracks · {filtered['date'].nunique()} snapshot dates · {len(album_filter)} album type(s) selected</div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
avg_pop  = round(filtered['popularity'].mean(), 1)
avg_dur  = round(filtered['duration_min'].mean(), 2)
expl_pct = round(filtered['is_explicit'].mean() * 100, 1)
n_artists = filtered['artist_name'].nunique() if 'artist_name' in filtered.columns else "—"

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card kpi-accent-yellow">
        <div class="kpi-icon">⭐</div>
        <div class="kpi-label">Avg Popularity</div>
        <div class="kpi-value">{avg_pop}</div>
    </div>
    <div class="kpi-card kpi-accent-blue">
        <div class="kpi-icon">⏱</div>
        <div class="kpi-label">Avg Duration (min)</div>
        <div class="kpi-value">{avg_dur}</div>
    </div>
    <div class="kpi-card kpi-accent-pink">
        <div class="kpi-icon">🔞</div>
        <div class="kpi-label">Explicit Share</div>
        <div class="kpi-value">{expl_pct}%</div>
    </div>
    <div class="kpi-card kpi-accent-green">
        <div class="kpi-icon">🎤</div>
        <div class="kpi-label">Unique Artists</div>
        <div class="kpi-value">{n_artists}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">📀</div>
        <div class="kpi-label">Total Tracks</div>
        <div class="kpi-value">{len(filtered):,}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Row 1: Duration histogram + Popularity by album type ─────────────────────
st.markdown('<div class="section-head">📊 Distribution Analysis</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(
        filtered, x='duration_min', nbins=35,
        title="Song Duration Distribution",
        color_discrete_sequence=["#5c6fff"],
    )
    fig1.update_traces(marker_line_width=0, opacity=0.85)
    fig1.update_layout(
        **CHART_THEME,
        title=dict(text="Song Duration Distribution", font=dict(size=14, color="#f0f2f5")),
        xaxis_title="Duration (min)", yaxis_title="Count",
        bargap=0.05,
    )
    fig1.add_vline(
        x=filtered['duration_min'].mean(),
        line_dash="dash", line_color="#e8f24a",
        annotation_text=f"avg {avg_dur}m",
        annotation_font_color="#e8f24a",
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    fig2 = px.violin(
        filtered, x='album_type', y='popularity',
        color='album_type',
        box=True, points="outliers",
        title="Popularity by Album Type",
        color_discrete_sequence=COLORS,
    )
    fig2.update_layout(
        **CHART_THEME,
        title=dict(text="Popularity by Album Type", font=dict(size=14, color="#f0f2f5")),
        xaxis_title="Album Type", yaxis_title="Popularity",
        showlegend=False,
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 2: Rank box + Scatter ─────────────────────────────────────────────────
st.markdown('<div class="section-head">🎯 Position & Reach</div>', unsafe_allow_html=True)
col3, col4 = st.columns([1, 1])

with col3:
    fig3 = px.box(
        filtered, x='album_type', y='position',
        color='album_type',
        title="Rank Distribution by Album Type",
        color_discrete_sequence=COLORS,
        points="outliers",
    )
    fig3.update_layout(
        **CHART_THEME,
        title=dict(text="Rank Distribution by Album Type", font=dict(size=14, color="#f0f2f5")),
        xaxis_title="Album Type", yaxis_title="Chart Position",
        yaxis_autorange="reversed",
        showlegend=False,
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    fig4 = px.scatter(
        filtered,
        x='total_tracks', y='popularity',
        color='album_type',
        size='duration_min',
        size_max=18,
        opacity=0.75,
        title="Album Size vs Popularity",
        color_discrete_sequence=COLORS,
        hover_data=['position'] if 'position' in filtered.columns else None,
    )
    fig4.update_layout(
        **CHART_THEME,
        title=dict(text="Album Size vs Popularity", font=dict(size=14, color="#f0f2f5")),
        xaxis_title="Total Tracks in Album", yaxis_title="Popularity",
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 3: Trend over time (if date has spread) ───────────────────────────────
if filtered['date'].nunique() > 1:
    st.markdown('<div class="section-head">📈 Popularity Over Time</div>', unsafe_allow_html=True)
    trend = (
        filtered.groupby(['date', 'album_type'])['popularity']
        .mean().reset_index()
    )
    fig5 = px.line(
        trend, x='date', y='popularity', color='album_type',
        markers=True, color_discrete_sequence=COLORS,
    )
    fig5.update_traces(line_width=2.5, marker_size=6)
    fig5.update_layout(
        **CHART_THEME,
        title=dict(text="Average Popularity Over Time by Album Type", font=dict(size=14, color="#f0f2f5")),
        xaxis_title="Date", yaxis_title="Avg Popularity",
        hovermode="x unified",
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 4: Explicit vs Clean stacked bar ─────────────────────────────────────
st.markdown('<div class="section-head">🔞 Explicit Content Breakdown</div>', unsafe_allow_html=True)
col5, col6 = st.columns([1, 1])

with col5:
    expl_by_type = (
        filtered.groupby(['album_type', 'is_explicit'])
        .size().reset_index(name='count')
    )
    expl_by_type['label'] = expl_by_type['is_explicit'].map({True: 'Explicit', False: 'Clean', 1: 'Explicit', 0: 'Clean'})
    fig6 = px.bar(
        expl_by_type, x='album_type', y='count', color='label',
        barmode='stack',
        color_discrete_map={'Explicit': '#ff5c8a', 'Clean': '#4ade80'},
    )
    fig6.update_layout(
        **CHART_THEME,
        title=dict(text="Explicit vs Clean by Album Type", font=dict(size=14, color="#f0f2f5")),
        xaxis_title="Album Type", yaxis_title="Track Count",
        legend_title="Content",
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    # Donut: album type share
    type_counts = filtered['album_type'].value_counts().reset_index()
    type_counts.columns = ['album_type', 'count']
    fig7 = px.pie(
        type_counts, names='album_type', values='count',
        hole=0.6, color_discrete_sequence=COLORS,
    )
    fig7.update_traces(textinfo='percent+label', pull=[0.04]*len(type_counts))
    fig7.update_layout(
        **CHART_THEME,
        title=dict(text="Album Type Share", font=dict(size=14, color="#f0f2f5")),
        showlegend=True,
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Top-N Tracks table ────────────────────────────────────────────────────────
st.markdown(f'<div class="section-head">🏆 Top {top_n} Tracks by Popularity</div>', unsafe_allow_html=True)

top_tracks = filtered.nlargest(top_n, 'popularity').reset_index(drop=True)
name_col    = 'track_name'   if 'track_name'   in top_tracks.columns else top_tracks.columns[0]
artist_col  = 'artist_name'  if 'artist_name'  in top_tracks.columns else None
album_col   = 'album_name'   if 'album_name'   in top_tracks.columns else None

rows_html = ""
for i, row in top_tracks.iterrows():
    rank   = i + 1
    name   = row.get(name_col, "—")
    artist = row.get(artist_col, "—") if artist_col else "—"
    album  = row.get(album_col, "—")  if album_col  else "—"
    pop    = int(row['popularity'])
    dur    = round(row['duration_min'], 2)
    atype  = row['album_type']
    expl   = row.get('is_explicit', False)
    badge  = '<span class="badge badge-explicit">Explicit</span>' if expl else '<span class="badge badge-clean">Clean</span>'
    bar_w  = max(2, pop)
    rows_html += f"""
    <tr>
        <td style="color:#6b7280;font-weight:600;">#{rank}</td>
        <td style="font-weight:500;">{name}</td>
        <td style="color:#9ca3af;">{artist}</td>
        <td style="color:#9ca3af;">{atype}</td>
        <td>
            <div class="pop-bar-bg">
                <div class="pop-bar" style="width:{bar_w}%;"></div>
            </div>
            <span style="font-size:.75rem;color:#9ca3af;margin-left:.4rem;">{pop}</span>
        </td>
        <td style="color:#9ca3af;">{dur}m</td>
        <td>{badge}</td>
    </tr>"""

st.markdown(f"""
<div class="chart-card">
<table class="track-table">
    <thead>
        <tr>
            <th>#</th><th>Track</th><th>Artist</th><th>Album Type</th>
            <th>Popularity</th><th>Duration</th><th>Content</th>
        </tr>
    </thead>
    <tbody>{rows_html}</tbody>
</table>
</div>
""", unsafe_allow_html=True)

# ── Raw data expander ─────────────────────────────────────────────────────────
with st.expander("🗂 Raw Data Explorer", expanded=False):
    st.dataframe(
        filtered.sort_values('popularity', ascending=False),
        use_container_width=True,
        height=340,
    )
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇ Download filtered CSV",
        data=csv,
        file_name="france_top50_filtered.csv",
        mime="text/csv",
    )