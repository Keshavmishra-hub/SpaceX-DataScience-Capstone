# 🚀 SpaceX Falcon 9 Launch Analysis — Data Science Capstone

This capstone project explores the SpaceX Falcon 9 rocket's first-stage landing outcomes to determine if we can **predict a successful landing**, using historical launch data. The motivation stems from the cost savings SpaceX achieves through reusable rockets, significantly reducing the $165 million traditional launch cost to ~$62 million.

---

## 📌 Table of Contents

- [Project Summary](#project-summary)
- [Data Sources](#data-sources)
- [Methodology](#methodology)
- [EDA Highlights](#eda-highlights)
- [Interactive Visualizations](#interactive-visualizations)
- [Predictive Modeling](#predictive-modeling)
- [Key Insights](#key-insights)
- [Conclusions](#conclusions)
- [Project Structure](#project-structure)

---

## 📄 Project Summary

- **Goal:** Predict if the Falcon 9 rocket's first stage will successfully land.
- **Tools Used:** Python, Pandas, Plotly Dash, Folium, SQL, Scikit-learn.
- **Techniques:** API & Web Scraping, Data Wrangling, EDA, Interactive Dashboards, Machine Learning.

---

## 📊 Data Sources

- **SpaceX REST API** ([script](spacex-data-collection-api.ipynb))  
- **Wikipedia Web Scraping** ([script](spacex-webscraping.ipynb))  
  Used `requests` and `BeautifulSoup` to extract launch history.

---

## 🛠️ Methodology

1. **Data Wrangling**  
   - Cleaned and encoded columns (e.g., converted `Outcome` to binary).
   - Merged datasets from API and Wikipedia.

2. **EDA (Exploratory Data Analysis)**  
   - SQL queries ([script](spacex-eda-sql.ipynb))
   - Visual plots ([script](spacex-eda-viz.ipynb))

3. **Interactive Visualization**  
   - Folium maps for launch site proximity ([script](spacex_launch_site_location.ipynb))
   - Plotly Dash app ([script](spacex_dash_app.py))

4. **Machine Learning**  
   - Binary classification models: Logistic Regression, KNN, SVM, Decision Tree.
   - Pipeline: preprocessing → model selection → hyperparameter tuning.

---

## 📈 EDA Highlights

- **Success by Launch Site:**  
  `KSC LC-39A` had the highest number of successful launches (76.9%).

- **Success by Payload:**  
  Lightweight payloads (2,000–4,000 kg) had the highest success rate.

- **Success by Orbit Type:**  
  Orbits like GEO, HEO, SSO, and ES-L1 had better landing outcomes.

- **Yearly Trends:**  
  Consistent improvement since 2013, peaking in 2019.

---

## 🌍 Interactive Visualizations

- **Folium Map:**  
  - Visualizes all launch sites.
  - Highlights distances and proximities.
  - [Notebook](spacex_launch_site_location.ipynb)

- **Plotly Dash App:**  
  - Dropdowns, sliders, pie charts, scatter plots.
  - Compare success rates across sites, payloads, and boosters.
  - [Code](spacex_dash_app.py)

---

## 🤖 Predictive Modeling

- **Models Tested:**  
  - K-Nearest Neighbors → Accuracy: 84%  
  - Logistic Regression → Accuracy: 84%  
  - SVM → Accuracy: 84%  
  - **Decision Tree → Accuracy: 87%**

- **Best Model:**  
  Decision Tree Classifier  
  - Recall for successful landings: **1.0**  
  - Precision: Moderate (some false positives)  
  - [Notebook](spacex_machine_learning_prediction.ipynb)

---

## 📌 Key Insights

- **High Flight Number = Higher Reliability**  
  Shows maturity and learning curve in rocket engineering.

- **Orbit & Payload Mass Play a Crucial Role**  
  Certain orbits/payloads strongly affect success chances.

- **Interactive Dashboards Enable Business Insights**  
  Useful for planning, simulations, and competitor benchmarking.

---

## ✅ Conclusions

- Falcon 9’s landing success is **predictable using historical data**.
- Reusability is **strongly correlated with orbit, payload mass, and site**.
- KSC LC-39A is the most efficient site.
- **Decision Tree** is the best classification model with 87% test accuracy.

---


