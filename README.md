# SEM Analysis: Brand Ambassador Impact on Purchase Decisions
**Author:** Galih Febriani Santika  
**Project Type:** Undergraduate Thesis (Mathematics)

## 📌 Project Overview
This project utilizes **Structural Equation Modeling (SEM)** to analyze how a Brand Ambassador (Stray Kids) influences the consumer decision-making process for Ultramilk products. By applying mathematical modeling and statistical validation, this research identifies which dimensions of a Brand Ambassador most effectively drive actual sales.

## 📊 Key Findings
* **Model Strength ($R^2$):** **52.5%**, indicating that the Brand Ambassador significantly explains over half of the variance in Purchase Decisions.
* **Leading Dimension:** **Trustworthiness (BA3.1)** was identified as the most influential factor (Estimate: 1.804), proving that consumer "Trust" in the idol's genuine consumption of the product is more vital than physical "Attractiveness."
* **Conversion Success:** The model shows high significance in the transition from awareness to **Actual Purchase (PD4.2)**, confirming the collaboration's effectiveness.

## 🛠️ Tech Stack & Methodology
* **Language:** Python 3.x
* **Key Libraries:** * `semopy`: For Structural Equation Modeling and path analysis.
    * `pandas` & `numpy`: For data cleaning and matrix manipulation.
    * `pingouin`: For Cronbach's Alpha reliability testing.
    * `matplotlib` & `seaborn`: For data visualization and correlation mapping.
* **Mathematical Approach:** Pearson Correlation for validity, Cronbach's Alpha for reliability, and Maximum Likelihood Estimation for SEM path coefficients.

## 📁 Repository Structure
```text
Brand-Ambassador-Impact-Analysis/
├── data/
│   └── Pembelian_Susu.xlsx       # Dataset (Survey Responses)
├── models/
│   └── BA_Analysis.py            # Main Python script for SEM & EDA
├── results/
│   └── path_diagram.png          # Visual representation of the SEM model
└── README.md