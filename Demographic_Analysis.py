import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = "healthcare_dataset.csv"  # Update with the correct path if necessary
data = pd.read_csv(file_path)

# Ensure correct data types for date columns
data['Date of Admission'] = pd.to_datetime(data['Date of Admission'])
data['Discharge Date'] = pd.to_datetime(data['Discharge Date'])

# Age distribution
plt.figure(figsize=(10, 6))
sns.histplot(data['Age'], bins=20, kde=True, color='skyblue')
plt.title('Age Distribution of Patients', fontsize=16)
plt.xlabel('Age', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gender distribution
plt.figure(figsize=(6, 6))
gender_counts = data['Gender'].value_counts()
sns.barplot(x=gender_counts.index, y=gender_counts.values, palette='pastel')
plt.title('Gender Distribution', fontsize=16)
plt.xlabel('Gender', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.show()

# Common medical conditions
plt.figure(figsize=(12, 6))
condition_counts = data['Medical Condition'].value_counts().head(10)
sns.barplot(y=condition_counts.index, x=condition_counts.values, palette='coolwarm')
plt.title('Top 10 Medical Conditions', fontsize=16)
plt.xlabel('Count', fontsize=12)
plt.ylabel('Medical Condition', fontsize=12)
plt.show()
