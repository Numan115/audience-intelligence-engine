# Project 3 — Pakistan Social Audience & Campaign Intelligence Engine
## Phase 1: Dataset Engineering & Audience Need Clustering Report

**Date:** November 2026  
**Industry Category:** Pakistani Fashion Retail & E-Commerce (Women's Lawn Suits, Pret & Luxury Festive)  
**Sample Scale:** 2,500 Social Posts & 10,000 Customer Comments (Instagram, TikTok, Facebook)

---

## 1. Executive Problem Statement
A Lahore-based retail fashion brand running multi-platform campaigns on Instagram, TikTok, and Facebook receives thousands of unstructured customer comments during mega sales (**11.11, 12.12, and Eid Collections**). 

The primary business objective is not mere sentiment analysis (positive vs negative), but **discovering hidden audience need clusters and customer intent** across Pakistani consumer interactions (*"Price please?", "Karachi delivery kitne din me hogi?", "Color fade toh nahi hoga?", "Large size restock karein"*).

---

## 2. Table Architecture (Phase 1 Baseline)

### Table A: Social Media Posts (`posts_raw.csv` — 2,500 records)
- **Brands Analyzed:** Sapphire, Khaadi, Gul Ahmed, Alkaram Studio, Nishat Linen, Sana Safinaz, Maria.B, Asim Jofa.
- **Platforms:** Instagram (50%), TikTok (30%), Facebook (20%).
- **Content Types:** Reels, Product Carousels, Influencer Styling Videos, Static Photos, Sale Announcements.
- **Core Metrics:** Likes, Comments, Shares, Views, and Engagement Rate (%).

### Table B: Customer Comments (`comments_raw.csv` — 10,000 records)
- **Language Mixture:** 
  - **Roman Urdu:** 55.4% (*"Price bohat zyada hai yar", "Delivery charges kitne hain?"*)
  - **English:** 32.1% (*"What is the fabric composition?", "Does it include trousers?"*)
  - **Code-Mixed / Bilingual:** 12.5% (*"Plz book this dress urgently"*)

---

## 3. Discovered Audience Need Clusters (K-Means + TF-IDF)

Our unsupervised natural language clustering engine extracted **6 distinct audience need clusters**:

| Cluster # | Discovered Customer Need | Key Distinctive Vocabulary | Share of Inquiries | Practical Marketing Implication |
| :---: | :--- | :--- | :---: | :--- |
| **0** | **Price Inquiries & Sensitivity** | `price`, `mehnga`, `rate`, `discount`, `sale` | **26.8%** | Customers need upfront price transparency; sticker shock causes drop-offs. |
| **1** | **Delivery, Logistics & COD** | `delivery`, `days`, `tracking`, `cod`, `karachi`, `lahore` | **19.2%** | High shipping anxiety; express delivery & COD options directly drive trust. |
| **2** | **Fabric & Material Quality** | `fabric`, `stuff`, `lawn`, `chiffon`, `pure`, `dupatta` | **15.4%** | Customers seek verification on transparency, washability, and lawn density. |
| **3** | **Sizing & Stock Availability** | `size`, `medium`, `small`, `stock`, `restock`, `pret` | **14.1%** | Fast stock-outs on popular sizes (M/L); high demand for restock notifications. |
| **4** | **High-Intent Order / Booking** | `order`, `book`, `confirm`, `dm`, `inbox`, `link` | **12.5%** | Ready-to-buy shoppers; need automated Instagram Direct & WhatsApp checkout links. |
| **5** | **Aesthetic & Brand Praise** | `loved`, `pyara`, `gorgeous`, `mashallah`, `collection` | **12.0%** | Social validation; prime candidates for user-generated content (UGC) reposts. |

---

## 4. Key Strategic Insights for Fashion Marketers

1. **The Price & Delivery Bottleneck (>45% of all comments):**
   - Almost half of all audience comments question either **price** or **delivery timeframe**. 
   - Brands that hide prices in captions (*"Inbox for price"*) generate friction that deters potential buyers.
2. **Content Format Effectiveness:**
   - **Reels & Influencer Styling Videos** generated the highest average engagement rates (**6.8% to 7.4%**), outperforming static photos by nearly **2.1x**.
   - **Sale Announcements** generated the highest volume of **High-Intent Booking** and **Price Sensitivity** comments.
3. **Regional Inquiries:**
   - Major metro inquiries concentrate in **Karachi, Lahore, Islamabad/Rawalpindi, Faisalabad, and Multan**, with Cash on Delivery (COD) being the most requested payment option.

---

## 5. Next Steps for Phase 2 & Phase 3

- **Phase 2:**
  - Build **Engagement Anomaly Detection (Isolation Forest)** to flag abnormal post behaviors (viral outliers vs complaint surges).
  - Develop content recommendation rules.
- **Phase 3:**
  - Build the full **Streamlit Web Application** displaying interactive filters and visualizations for all 5 executive marketing questions.
