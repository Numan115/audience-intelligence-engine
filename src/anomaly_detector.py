"""
anomaly_detector.py
Part 2 Core Module: Context-Aware Anomaly Detection & Diagnostic Engine.
Evaluates Isolation Forest across sensitivity thresholds (2%, 4%, 8%)
and performs root-cause feature attribution on social marketing anomalies.
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.dirname(__file__))
import engine as E

def run_anomaly_diagnostics(data_dir=None, output_dir=None):
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        
    os.makedirs(output_dir, exist_ok=True)
    vis_dir = os.path.join(os.path.dirname(__file__), '..', 'visualizations')
    os.makedirs(vis_dir, exist_ok=True)
    
    posts, comments = E.load_data(data_dir)
    p = E.add_metrics(posts)
    v = p['views'].clip(lower=1)
    
    # 1. Sensitivity Analysis across Contamination Rates
    contaminations = [0.02, 0.04, 0.08]
    sensitivity_results = []
    
    features = pd.DataFrame({
        'like_r': p['likes'] / v,
        'com_r': p['comments_count'] / v,
        'share_r': p['shares'] / v,
        'log_v': np.log1p(p['views'])
    })
    
    # Within-format standardization
    norm_features = features.groupby(p['content_type']).transform(
        lambda s: (s - s.mean()) / (s.std() + 1e-9)
    )
    
    for c_rate in contaminations:
        iso = IsolationForest(contamination=c_rate, random_state=42)
        preds = iso.fit_predict(norm_features) == -1
        sensitivity_results.append({
            'Contamination_Rate': f"{int(c_rate*100)}%",
            'Anomalies_Count': int(preds.sum()),
            'Avg_Engagement_Rate_Anomalies': round(p.loc[preds, 'engagement_rate'].mean(), 2),
            'Avg_Engagement_Rate_Normal': round(p.loc[~preds, 'engagement_rate'].mean(), 2)
        })
        
    df_sens = pd.DataFrame(sensitivity_results)
    sens_path = os.path.join(output_dir, 'anomaly_sensitivity_analysis.csv')
    df_sens.to_csv(sens_path, index=False)
    print("\n--- ANOMALY SENSITIVITY ANALYSIS ---")
    print(df_sens.to_string(index=False))
    
    # 2. In-Depth Root-Cause Attribution on Primary Model (4% Contamination)
    p_anom = E.find_anomalies(p, contamination=0.04)
    
    # Diagnose root cause
    diagnoses = []
    for _, row in p_anom.iterrows():
        if not row['anomaly']:
            diagnoses.append('Normal Post')
            continue
            
        like_r = row['like_rate']
        com_r = row['comment_rate']
        share_r = row['share_rate']
        eng = row['engagement_rate']
        
        if eng > 12.0:
            diagnoses.append('Viral Breakout (Extreme Like & Reach Surge)')
        elif com_r > 3.0:
            diagnoses.append('Complaint / Inquiry Surge (High Comment-to-Like Ratio)')
        elif share_r > 1.5:
            diagnoses.append('Viral Share Outlier (High Promotional Distribution)')
        elif eng < 1.5:
            diagnoses.append('Dead Reach (High Impressions with Low Conversion)')
        else:
            diagnoses.append('Multivariate Ratio Discrepancy')
            
    p_anom['diagnosis'] = diagnoses
    
    # Save diagnosed anomalies
    anom_only = p_anom[p_anom['anomaly']].sort_values(by='anomaly_score', ascending=False)
    anom_csv = os.path.join(output_dir, 'diagnosed_anomalies.csv')
    anom_only.to_csv(anom_csv, index=False)
    print(f"\nSaved {len(anom_only)} diagnosed anomalies to: {anom_csv}")
    
    print("\nTop 5 Flagged Anomalies:")
    cols_show = ['post_id', 'brand', 'content_type', 'views', 'likes', 'comments_count', 'engagement_rate', 'diagnosis']
    print(anom_only[cols_show].head(5).to_string(index=False))
    
    # 3. Visualizations
    sns.set_theme(style='whitegrid')
    
    # A. Scatter: Likes vs Comments with Anomalies Highlighted
    plt.figure(figsize=(10, 6))
    palette = {False: '#457b9d', True: '#e63946'}
    sns.scatterplot(
        data=p_anom, x='likes', y='comments_count', hue='anomaly', 
        palette=palette, alpha=0.7, s=50, style='anomaly', markers={False: 'o', True: 'X'}
    )
    plt.title('Anomaly Detection in Social Engagement (Isolation Forest)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Likes Count', fontsize=12)
    plt.ylabel('Comments Count', fontsize=12)
    plt.legend(title='Is Anomaly', labels=['Normal Post', 'Anomalous Post'])
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, '05_anomaly_detection_scatter.png'), dpi=300)
    plt.close()
    
    # B. Diagnosis Distribution
    plt.figure(figsize=(10, 5))
    diag_counts = anom_only['diagnosis'].value_counts()
    sns.barplot(y=diag_counts.index, x=diag_counts.values, palette='mako')
    plt.title('Root-Cause Breakdown of Flagged Marketing Anomalies', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Flagged Posts', fontsize=12)
    plt.ylabel('Anomaly Archetype', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, '06_anomaly_root_causes.png'), dpi=300)
    plt.close()
    
    print("\nPart 2 Visualizations saved successfully in visualizations/:")
    print(" - 05_anomaly_detection_scatter.png")
    print(" - 06_anomaly_root_causes.png")
    
    return p_anom, df_sens

if __name__ == '__main__':
    run_anomaly_diagnostics()
