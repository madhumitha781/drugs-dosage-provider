💊 Drug Clustering & Recommendation Tool – DBSCAN Web App
📌 Overview
This project is a Flask-based web application that uses the DBSCAN clustering algorithm to group drugs with similar attributes (e.g., indications, side effects, dosage, etc.).
Users can search for a drug and instantly get:

Detailed drug information.

A list of similar drugs in the same cluster.

Suggested dosage limits based on cluster statistics.

This tool is useful for drug research, healthcare analytics, and pharmaceutical recommendation systems.

✨ Features
📂 Preloaded Drug Dataset – Uses a realistic dataset of drug labels and side effects.

🤖 DBSCAN Clustering – Groups similar drugs based on encoded attributes.

🔄 Automatic Data Preprocessing – Handles missing values, encodes categorical data, and scales numeric values.

💊 Drug Search – Find a drug by name and see:

Drug details (indications, side effects, dosage, administration route, contraindications, warnings, manufacturer, price, etc.).

Similar drugs in the same cluster.

Suggested dosage limit from cluster statistics.

🌐 Web Interface – Easy-to-use search form and results page.

🛠️ Tech Stack
Backend: Python, Flask

ML & Data Processing: pandas, numpy, scikit-learn

Clustering Algorithm: DBSCAN

Frontend: HTML templates (Flask render_template)

📦 Installation
1️⃣ Clone the repository
bash
Copy
Edit
git clone https://github.com/yourusername/drug-clustering-app.git
cd drug-clustering-app
2️⃣ Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Add dataset
Place the dataset file realistic_drug_labels_side_effects.csv in the project folder.
This file should contain columns such as:

Copy
Edit
drug_name, indications, side_effects, dosage_mg, administration_route,
contraindications, warnings, drug_class, manufacturer, price_usd, ...
🚀 Usage
1️⃣ Run the Flask app
bash
Copy
Edit
python app.py
The app will run on http://127.0.0.1:5000.

2️⃣ Search for a drug
Enter a drug name in the search box.

View detailed information and similar drugs from the same cluster.

Get suggested dosage limits from statistical analysis.
<img width="1366" height="443" alt="Screenshot (54)" src="https://github.com/user-attachments/assets/2e66a7c4-2428-4747-9095-752dafae533a" />
<img width="1362" height="695" alt="Screenshot (55)" src="https://github.com/user-attachments/assets/7abfa06c-47b9-4aee-9569-968a0d6f8715" />



⚠️ Notes
The dataset must contain both numeric and categorical columns; categorical data will be one-hot encoded.

DBSCAN parameters (eps, min_samples) can be tuned inside app.py for better clustering results.

Missing values are automatically handled:

Numeric → replaced with median.

Categorical → replaced with mode.

📜 License
This project is licensed under the MIT License – you are free to use, modify, and distribute.
