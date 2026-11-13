# Pakistan Social Audience & Campaign Intelligence Engine
**Clustering-Based Marketing Intelligence for Pakistani Fashion E-Commerce**

---

## 📌 Executive Summary & Business Problem

Imagine a Lahore-based online retail brand (e.g. *Sapphire, Khaadi, Gul Ahmed*) running digital marketing campaigns across **Instagram, TikTok, and Facebook** during peak shopping festivals (**11.11 Mega Sale, 12.12, and Eid Collections**).

The marketing team receives thousands of customer comments:
> *“Price please?”*  
> *“Is this available in Karachi?”*  
> *“Very beautiful dress!”*  
> *“Price bohat zyada hai.”*  
> *“Delivery kitne din mein hogi?”*  
> *“Any discount on this suit?”*  
> *“Ordered last week, still waiting.”*  
> *“Inbox me details send kar dein.”*  

**The Goal:** Build an intelligence engine that groups similar audience behaviors, discovers hidden customer needs, identifies unusual engagement patterns, and converts them into practical marketing decisions.

---

## 🏗️ Project Architecture (Phase 1 Baseline)

```text
Pakistan-Social-Audience-Intelligence-Engine/
│
├── data/
│   ├── raw/
│   │   ├── posts_raw.csv                      # Table A: 2,500 Social Posts
│   │   └── comments_raw.csv                   # Table B: 10,000 Comments (Roman Urdu & English)
│   └── processed/
│       ├── posts_cleaned.csv                  # Posts enriched with engagement & need profiles
│       └── comments_clustered.csv             # Comments tagged with TF-IDF K-Means clusters
│
├── notebooks/
│   └── phase1_clustering_foundation.ipynb     # Interactive Jupyter Notebook for Phase 1
│
├── src/
│   ├── generate_data.py                       # Simulates realistic Pakistani fashion dataset
│   ├── preprocess_nlp.py                      # Roman Urdu + English NLP normalizer
│   ├── audience_clustering.py                 # TF-IDF & K-Means clustering pipeline
│   └── generate_visualizations.py             # Phase 1 plots generator
│
├── visualizations/                            # Exported High-Resolution Charts
│   ├── 01_comment_cluster_distribution.png
│   ├── 02_brand_audience_needs_heatmap.png
│   ├── 03_content_type_engagement.png
│   └── 04_language_distribution.png
│
├── reports/
│   └── phase1_findings.md                     # Comprehensive Phase 1 Analytical Report
│
├── README.md                                  # Project Documentation
├── requirements.txt                           # Python Dependencies
└── .gitignore
```

---

## 📊 Phase 1 Results: Discovered Audience Need Clusters

Using **TF-IDF (Unigrams + Bigrams)** and **K-Means Clustering**, our NLP engine automatically identified the primary drivers of audience comments:

| Discovered Audience Need | Distinctive Roman Urdu / English Keywords | % of Comments | Marketing Impact |
| :--- | :--- | :---: | :--- |
| **Delivery, Shipping & Logistics** | `delivery`, `kitne din`, `karachi`, `lahore`, `tracking`, `cod` | **53.6%** | High shipping anxiety; express delivery & COD options build trust. |
| **Price Inquiry & Resistance** | `price`, `suit`, `zyada`, `mehnga`, `discount`, `rate` | **28.1%** | Upfront pricing transparency avoids customer drop-offs. |
| **Sizing & Stock Availability** | `size`, `medium`, `small`, `stock`, `restock`, `chart` | **18.3%** | Immediate demand for size charts and restock alerts. |

---

## 📈 Visualizations Index

- `01_comment_cluster_distribution.png` — Distribution of discovered audience need clusters.
- `02_brand_audience_needs_heatmap.png` — Cross-tabulation of inquiries across fashion brands.
- `03_content_type_engagement.png` — Engagement rate (%) comparison across Reels, Carousels, and Videos.
- `04_language_distribution.png` — Roman Urdu vs. English vs. Mixed language share.

---

## 🚀 How to Run Phase 1

1. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Generate datasets:**
   ```bash
   python src/generate_data.py
   ```
3. **Run audience clustering model:**
   ```bash
   python src/audience_clustering.py
   ```
4. **Generate visualization charts:**
   ```bash
   python src/generate_visualizations.py
   ```
5. **Explore Jupyter Notebook:**
   Open `notebooks/phase1_clustering_foundation.ipynb`.

---

## 🗺️ Project Roadmap
- [x] **Phase 1: Dataset Engineering & Unsupervised Audience Need Clustering** (Completed)
- [ ] **Phase 2: Engagement Anomaly Detection & Content Intelligence** (Next)
- [ ] **Phase 3: Interactive Streamlit Web Application & Final Decision System** (Next)
