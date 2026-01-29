# 🚀 SAP S-Predict: Sales Delivery Delay Analysis

### 📌 Project Overview
**S-Predict** is an end-to-end analytical solution designed to identify risks in the supply chain. It bridges the gap between **SAP S/4HANA (Backend)** and **Python/Power BI** to provide real-time visibility into order delays and revenue at risk.



---

### 🛠️ Technical Architecture
This project follows a **Side-by-Side Extension** pattern:

1. **Core ABAP Layer (RAP):**
   - Designed custom database table `ZSALES_HEADER_SP`.
   - Developed **CDS View Entities** for data modeling.
   - Exposed data via **OData V4 Service Bindings**.

2. **Analytics Layer (Python):**
   - Engineered an ETL pipeline using **Pandas**.
   - Performed **Date Arithmetic** to calculate delivery variance (Actual vs. Planned).
   - Applied a custom **Risk Scoring Algorithm**.

3. **Visualization Layer (Power BI):**
   - Developed an executive dashboard focusing on **Revenue at Risk**.
   - Created DAX measures to analyze product aging and shipping bottlenecks.

---

### 🌉 Data Integration Logic
Due to BTP Trial environment authentication constraints (HTTP 401), the data transfer was implemented via a structured **CSV Data Bridge**. 
- **Source:** SAP ADT Data Preview (Structured Export).
- **Transformation:** Python handles YYYYMMDD date conversions and risk categorization.
- **Output:** A refined dataset prepared for business intelligence consumption.

---

### 📂 Repository Structure
- **/ABAP**: Database Table, CDS View, and Service source code.
- **/Python**: `s_predict.py` script for data processing.
- **/Data**: Raw and processed datasets (`sap_export.csv`).
- **/Dashboard**: Power BI `.pbix` file for visualization.

---

### 💡 Key Skills Demonstrated
- **SAP Technologies:** ABAP on HANA, RAP, CDS, OData V4.
- **Data Science:** Python, Pandas, ETL Processes.
- **Business Intelligence:** Power BI, Data Visualization, DAX.
