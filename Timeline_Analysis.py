import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = "healthcare_dataset.csv"  # Update with the correct path if necessary
data = pd.read_csv(file_path)

# Ensure correct data types for date columns
data['Date of Admission'] = pd.to_datetime(data['Date of Admission'])
data['Discharge Date'] = pd.to_datetime(data['Discharge Date'])


# Admission trends over time
plt.figure(figsize=(14, 6))
data['Year'] = data['Date of Admission'].dt.year
admission_trends = data['Year'].value_counts().sort_index()
sns.lineplot(x=admission_trends.index, y=admission_trends.values, marker='o', color='teal')
plt.title('Admission Trends Over the Years', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Admissions', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Length of hospital stays
data['Length of Stay'] = (data['Discharge Date'] - data['Date of Admission']).dt.days
plt.figure(figsize=(10, 6))
sns.histplot(data['Length of Stay'], bins=30, kde=True, color='coral')
plt.title('Length of Hospital Stays', fontsize=16)
plt.xlabel('Days', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
