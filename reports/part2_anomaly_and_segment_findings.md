# Project 3 — Pakistan Social Audience & Campaign Intelligence Engine
## Part 2: Advanced Anomaly Detection & Cross-Segment Intelligence Report

**Author:** Muhammad Numan (Numan115)  
**Dataset:** 2,000 Social Posts & 8,000 Comments (Pakistani Fashion Retail)  
**Machine Learning Models:** Context-Aware Isolation Forest (Within-Format Normalization) & Cross-Tabulated Semantic Clustering

---

## 1. Executive Summary

In Part 2, we evaluate two advanced analytical dimensions:
1. **Unusual Marketing Patterns (Question 3):** Identifying campaigns whose engagement or comment patterns deviate significantly from comparable posts.
2. **Audience Segments & Behavior (Question 4):** Discovering how customer needs distribute across language (*Roman Urdu vs. English*) and across Pakistani retail brands (*Sapphire, Khaadi, Gul Ahmed, Maria.B, Asim Jofa*).

---

## 2. Context-Aware Anomaly Detection (Isolation Forest)

A common mistake in social media analytics is comparing all posts equally (e.g. comparing a Reel with 50,000 views to a static Product Photo with 3,000 views). 

Our model implements **within-content-type feature normalization**:
$$\text{Standardized Metric} = \frac{x - \mu_{\text{content\_type}}}{\sigma_{\text{content\_type}} + 10^{-9}}$$

### A. Contamination Sensitivity Analysis

| Contamination Rate | Anomalies Flagged | Avg Engagement Rate (Anomalies) | Avg Engagement Rate (Normal) | Strategic Focus |
| :---: | :---: | :---: | :---: | :--- |
| **2%** | **40 posts** | **7.46%** | 5.45% | Conservative: Flags only extreme statistical outliers. |
| **4% (Baseline)** | **80 posts** | **6.49%** | 5.45% | **Optimal Balance:** Captures viral breakouts and customer complaint spikes. |
| **8%** | **160 posts** | **5.83%** | 5.46% | Aggressive: Useful for comprehensive customer service audits. |

### B. Root-Cause Diagnosis of Flagged Anomalies

The 80 flagged anomalies were categorized into **4 distinct marketing archetypes**:

1. **Complaint / Inquiry Surge (43.8% of anomalies):**
   - *Pattern:* Abnormally high comment-to-like ratio (comments > likes).
   - *Root Cause:* Viral delivery delays during sale seasons (e.g., *"Ordered last week, still waiting!"*) or customer backlashes over color fading.
   - *Action:* Immediate customer service escalation with proactive tracking updates.

2. **Viral Breakout (26.2% of anomalies):**
   - *Pattern:* Likes and views exceed the 98th percentile for their format (engagement rates up to **14.2%**).
   - *Root Cause:* High-impact influencer styling reels or unexpected organic algorithmic lift.
   - *Action:* Replicate creative hook; boost post with paid ad budget.

3. **Viral Share Outlier (17.5% of anomalies):**
   - *Pattern:* Share rate exceeding 2.5x the format baseline.
   - *Root Cause:* Major 11.11 / Eid flash discount announcements shared by users across WhatsApp and Instagram Direct.
   - *Action:* Extend promo duration and pin checkout link.

4. **Dead Reach Outliers (12.5% of anomalies):**
   - *Pattern:* High impressions but sub-1.5% engagement rate.
   - *Root Cause:* Mismatched target audience or uninspired static imagery.
   - *Action:* Pause or redesign creative.

---

## 3. Audience Segment Personas by Language & Need

Cross-tabulating our Roman Urdu / English clustering results revealed **4 primary audience personas**:

| Persona Archetype | Dominant Language | Primary Need Category | % of Total Audience | Behavior & Action Plan |
| :--- | :--- | :--- | :---: | :--- |
| **The Bargain Seeker** | **Roman Urdu** (82%) | Discounts & Price Inquiries | **32.5%** | Highly price-sensitive. Asks *"kitna off hoga"* and *"discount code hai koi"*. Responds best to limited-time bundle promotions. |
| **The Anxious Buyer** | **Mixed / Roman Urdu** (74%) | Delivery & COD Inquiries | **24.2%** | High shipping anxiety. Needs Cash on Delivery reassurance and explicit Lahore/Karachi delivery timelines. |
| **The Brand Admirer** | **English** (68%) | Aesthetics & Praise | **21.8%** | Praises embroidery and styling (*"Mashallah gorgeous collection"*). Prime candidates for UGC influencer marketing. |
| **The Instant Purchaser** | **Bilingual** (55% / 45%) | Direct Order & Inbox Requests | **14.5%** | High purchase intent. Comments *"Book Medium for me, check DM"*. Requires automated WhatsApp/DM instant checkout. |

---

## 4. Brand-by-Brand Audience Inquiry Profiles

- **Sapphire & Khaadi:** Showed the highest proportion of **Discounts & Sale Inquiries** (~35%), reflecting massive price-conscious following during 11.11 and 12.12 sales.
- **Maria.B & Asim Jofa:** Showed the highest volume of **Fabric Quality & Specification questions** (~28%), as consumers scrutinize luxury festive chiffon and embroidery density before committing to high price tags.
- **Gul Ahmed & Nishat Linen:** Showed elevated **Delivery & Logistics inquiries** (~27%), emphasizing the need for reliable nationwide supply chain tracking.
