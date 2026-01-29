import pandas as pd
import matplotlib.pyplot as plt
import os

def run_real_sap_analytics():
    # 1. SETUP PATHS
    input_file = r"D:\S-Predict\sap_export.csv"
    output_file = r"D:\S-Predict\sap_analytics_final.csv"
    
    print(f"🚀 S-Predict: Analyzing Real SAP Data...")

    try:
        # 2. LOAD DATA
        df = pd.read_csv(input_file)

        # 3. DATE CONVERSION (SAP Format YYYYMMDD to Python Date)
        df['PLANNED_DATE'] = pd.to_datetime(df['PLANNED_DATE'], format='%Y%m%d')
        df['ACTUAL_DATE'] = pd.to_datetime(df['ACTUAL_DATE'], format='%Y%m%d')

        # 4. CALCULATE DELAY VARIANCE
        # Delay = Actual Date - Planned Date
        df['Delay_Days'] = (df['ACTUAL_DATE'] - df['PLANNED_DATE']).dt.days

        # 5. RISK CATEGORIZATION (Job-Ready Logic)
        # High Risk: Delay > 3 days OR Price > 2000 with any delay
        def categorize_risk(row):
            if row['Delay_Days'] > 5:
                return 'High Risk'
            elif row['Delay_Days'] > 0:
                return 'At Risk'
            else:
                return 'On Track'

        df['Risk_Status'] = df.apply(categorize_risk, axis=1)

        # 6. SAVE THE TRANSFORMED DATA
        df.to_csv(output_file, index=False)
        print(f"✅ Success! Transformed data saved to: {output_file}")

        # 7. VISUALIZATION
        plt.figure(figsize=(10, 6))
        risk_counts = df['Risk_Status'].value_counts()
        risk_counts.plot(kind='pie', autopct='%1.1f%%', colors=['green', 'red', 'orange'])
        plt.title('SAP Supply Chain Risk Distribution')
        plt.ylabel('') # Hide the y-label for a cleaner look
        plt.show()

    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    run_real_sap_analytics()