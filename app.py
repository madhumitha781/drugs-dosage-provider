from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import DBSCAN
import os

app = Flask(__name__)

DATA_PATH = "realistic_drug_labels_side_effects.csv" 
def load_and_prepare(path):
    df = pd.read_csv(path)

    # Identify numeric columns correctly
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(exclude=['int64', 'float64']).columns

    # Fill missing values only in numeric columns with median
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # Fill missing values in categorical columns with mode
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # One-hot encode categorical features
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Scaling only numeric data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_encoded)

    return df, df_encoded, X_scaled, scaler, df_encoded.columns
 
if not os.path.exists(DATA_PATH):
    raise SystemExit(f"dataset.csv not found in folder. Please place your file named 'dataset.csv' in the app folder.")
display_df, enc_df, X_scaled, scaler, feature_cols = load_and_prepare(DATA_PATH)

# Run DBSCAN (you can tune eps and min_samples for your dataset)
dbscan = DBSCAN(eps=0.9, min_samples=5)   # default values — tune if needed
labels = dbscan.fit_predict(X_scaled)
enc_df['cluster'] = labels
display_df['cluster'] = labels  # keep for display

# helper: find matches for drug name (case-insensitive substring match)
def find_drug_rows_by_name(name):
    name = name.strip().lower()
    mask = display_df['drug_name'].astype(str).str.lower().str.contains(name)
    return display_df[mask]

# helper: get cluster statistics for dosage in a cluster (if dosage available)
def cluster_dosage_stats(cluster_id):
    if 'dosage_mg' not in enc_df.columns:
        return None
    cluster_vals = enc_df[enc_df['cluster'] == cluster_id]['dosage_mg'].dropna().astype(float)
    if len(cluster_vals) == 0:
        return None
    mean = cluster_vals.mean()
    std = cluster_vals.std(ddof=0)
    # Suggested safe limit rule: mean + 1 * std (you can change multiplier)
    suggested_limit = float(mean + std)
    return {'mean': float(mean), 'std': float(std), 'suggested_limit': suggested_limit}

# --- Routes -------------------------------------------------------------------
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/result", methods=['POST'])
def result():
    drug_input = request.form.get("drug_name", "").strip()
    if not drug_input:
        return render_template("result.html", error="Please enter a drug name.")

    matches = find_drug_rows_by_name(drug_input)

    if matches.empty:
        # Try exact match ignoring case
        exact_mask = display_df['drug_name'].astype(str).str.lower() == drug_input.lower()
        exact_matches = display_df[exact_mask]
        if exact_matches.empty:
            return render_template("result.html", error=f"No drug found matching '{drug_input}'.")
        matches = exact_matches

    # Use first matched row as primary result
    primary = matches.iloc[0].to_dict()

    # Extract displayed fields
    show_fields = {}
    for fld in ['drug_name', 'indications', 'side_effects', 'dosage_mg', 'administration_route',
                'contraindications', 'warnings', 'drug_class', 'manufacturer', 'price_usd']:
        if fld in primary:
            show_fields[fld] = primary.get(fld)

    cluster_id = primary.get('cluster', -1)

    # Similar drugs: other rows in same cluster (exclude the primary itself), limit 10
    similar_rows = display_df[(display_df['cluster'] == cluster_id) & (display_df['drug_name'] != primary.get('drug_name'))]
    similar = similar_rows[['drug_name', 'drug_class', 'dosage_mg', 'side_effects']].head(10).to_dict(orient='records') if not similar_rows.empty else []

    # dosage suggestion based on cluster stats
    dosage_stats = cluster_dosage_stats(cluster_id)

    return render_template("result.html",
                           error=None,
                           query=drug_input,
                           fields=show_fields,
                           cluster_id=int(cluster_id) if pd.notna(cluster_id) else -1,
                           similar=similar,
                           dosage_stats=dosage_stats)

if __name__ == "__main__":
    app.run(debug=True)
