import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = "healthcare_dataset.csv"  # Update with the correct path if necessary
data = pd.read_csv(file_path)

# Ensure correct data types for date columns
data['Date of Admission'] = pd.to_datetime(data['Date of Admission'])
data['Discharge Date'] = pd.to_datetime(data['Discharge Date'])

# Admission types
plt.figure(figsize=(8, 6))
admission_counts = data['Admission Type'].value_counts()
sns.barplot(x=admission_counts.index, y=admission_counts.values, palette='viridis')
plt.title('Admission Types', fontsize=16)
plt.xlabel('Admission Type', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.show()

# Average billing amount by medical condition
plt.figure(figsize=(12, 6))
avg_billing = data.groupby('Medical Condition')['Billing Amount'].mean().sort_values(ascending=False).head(10)
sns.barplot(y=avg_billing.index, x=avg_billing.values, palette='magma')
plt.title('Top 10 Medical Conditions by Average Billing Amount', fontsize=16)
plt.xlabel('Average Billing Amount (USD)', fontsize=12)
plt.ylabel('Medical Condition', fontsize=12)
plt.show()

# Medication frequency
plt.figure(figsize=(10, 6))
medication_counts = data['Medication'].value_counts().head(10)
sns.barplot(y=medication_counts.index, x=medication_counts.values, palette='cubehelix')
plt.title('Top 10 Medications', fontsize=16)
plt.xlabel('Count', fontsize=12)
plt.ylabel('Medication', fontsize=12)
plt.show()
