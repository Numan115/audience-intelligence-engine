"""
app.py
Interactive Streamlit Web Dashboard:
Pakistan Social Audience & Campaign Intelligence Engine
Answers the 5 core marketing questions across 5 tabs.
"""

import os
import sys
import pandas as pd
import streamlit as st

# Add src to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
import engine as E

st.set_page_config(
    page_title="Pakistan Social Audience Intelligence Engine",
    page_icon="👗",
    layout="wide"
)

# Header
st.title("👗 Pakistan Social Audience & Campaign Intelligence Engine")
st.markdown("*Clustering-based audience intelligence for Pakistani fashion e-commerce (Lawn Suits & Pret Collections)*")

# Load datasets
p_raw, c_raw = E.load_data(os.path.join(os.path.dirname(__file__), 'data'))
p = E.add_metrics(p_raw)

# Sidebar Filters
st.sidebar.header("🔍 Campaign & Channel Filters")

brands = sorted(p['brand'].unique())
selected_brands = st.sidebar.multiselect("Select Brands", brands, default=brands)

platforms = sorted(p['platform'].unique())
selected_platforms = st.sidebar.multiselect("Select Platforms", platforms, default=platforms)

campaigns = sorted(p['campaign'].unique())
selected_campaigns = st.sidebar.multiselect("Select Campaigns", campaigns, default=campaigns)

# ML Hyperparameters
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Model Parameters")
k_clusters = st.sidebar.slider("Number of Comment Clusters (k)", min_value=3, max_value=10, value=6)
contamination = st.sidebar.slider("Anomaly Detection Sensitivity", min_value=0.02, max_value=0.08, value=0.04, step=0.01)

# Apply filters
p_filtered = p[
    p['brand'].isin(selected_brands) &
    p['platform'].isin(selected_platforms) &
    p['campaign'].isin(selected_campaigns)
]
c_filtered = c_raw[c_raw['post_id'].isin(p_filtered['post_id'])].copy()

if p_filtered.empty or c_filtered.empty:
    st.warning("No data found matching the selected filters. Please expand your selections.")
    st.stop()

if "simulated" in set(p_filtered.get('data_source', [])):
    st.info("ℹ️ **Data Note:** Demonstration uses simulated records (`data_source = 'simulated'`). See `DATA_SOURCES.md` for real-world benchmark citations.")

# Compute Intelligence Modules
with st.spinner("Running NLP Clustering & Anomaly Detection..."):
    perf = E.content_performance(p_filtered)
    clustered_c = E.cluster_comments(c_filtered, k=k_clusters)
    anom_posts = E.find_anomalies(p_filtered, contamination=contamination)
    recs = E.generate_recommendations(clustered_c, perf)

# Top Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Posts Analyzed", f"{len(p_filtered):,}")
col2.metric("Customer Comments", f"{len(c_filtered):,}")
col3.metric("Top Content Format", f"{perf.index[0]} ({perf['avg_engagement_rate'].iloc[0]}%)")
col4.metric("Unusual Posts Flagged", f"{anom_posts['anomaly'].sum():,}")

st.markdown("---")

# 5 Main Tabs corresponding to the 5 Business Questions
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Content Attention",
    "2. Audience Wants",
    "3. Unusual Posts",
    "4. Audience Segments",
    "5. Recommended Actions"
])

# ----------------- TAB 1: CONTENT ATTENTION -----------------
with tab1:
    st.subheader("Which content types attract the most attention?")
    st.markdown("Compares **Reels, Product Photos, Influencer Posts, Styling Videos, and Sale Announcements** using engagement rate:")
    st.latex(r"\text{Engagement Rate} = \frac{\text{likes} + \text{comments} + \text{shares}}{\text{views}} \times 100")
    
    col_t1a, col_t1b = st.columns([1, 1])
    with col_t1a:
        st.dataframe(perf, use_container_width=True)
    with col_t1b:
        st.bar_chart(perf['avg_engagement_rate'])

# ----------------- TAB 2: AUDIENCE WANTS -----------------
with tab2:
    st.subheader("What does the audience want?")
    st.markdown("Unsupervised K-Means clustering discovered the primary customer needs hidden in unstructured Roman Urdu & English comments:")
    
    cluster_counts = clustered_c['cluster_name'].value_counts()
    st.bar_chart(cluster_counts)
    
    st.markdown("### 💬 Real Comment Samples by Discovered Topic")
    for cluster_name in cluster_counts.index:
        sample_comments = clustered_c[clustered_c['cluster_name'] == cluster_name]['comment_text'].drop_duplicates().head(5).tolist()
        with st.expander(f"📌 {cluster_name} ({cluster_counts[cluster_name]:,} comments)"):
            for s in sample_comments:
                st.write(f"- *\"{s}\"*")

# ----------------- TAB 3: UNUSUAL POSTS -----------------
with tab3:
    st.subheader("Which marketing patterns are unusual?")
    st.markdown("Isolation Forest detects posts whose engagement ratios deviate significantly from **comparable posts within the same content format**:")
    
    unusual = anom_posts[anom_posts['anomaly']].sort_values(by='anomaly_score', ascending=False)
    st.dataframe(
        unusual[['post_id', 'brand', 'platform', 'campaign', 'content_type', 'views', 'likes', 'comments_count', 'engagement_rate', 'anomaly_score']],
        use_container_width=True
    )

# ----------------- TAB 4: AUDIENCE SEGMENTS -----------------
with tab4:
    st.subheader("How do audience segments differ by language and need?")
    st.markdown("Cross-tabulation showing how Roman Urdu vs English comments distribute across customer need categories:")
    
    crosstab_lang = pd.crosstab(clustered_c['cluster_name'], clustered_c['language_type'], margins=True)
    st.dataframe(crosstab_lang, use_container_width=True)
    
    st.markdown("### Brand-by-Brand Audience Inquiry Profiles (%)")
    merged_c = clustered_c.merge(p_filtered[['post_id', 'brand']], on='post_id', how='left')
    crosstab_brand = pd.crosstab(merged_c['brand'], merged_c['cluster_name'], normalize='index') * 100
    st.dataframe(crosstab_brand.round(1), use_container_width=True)

# ----------------- TAB 5: NEXT STEPS -----------------
with tab5:
    st.subheader("What should the marketing team do next?")
    st.markdown("Evidence-based tactical actions for marketing, pricing, customer service, and campaign testing:")
    
    for r in recs:
        st.markdown(f"- {r}")

st.markdown("---")
st.caption("Pakistan Social Audience & Campaign Intelligence Engine | Built for Digital Marketing & Big Data Analytics")
