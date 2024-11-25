import pandas as pd

# Load dataset
file_path = './healthcare_dataset.csv'
data = pd.read_csv(file_path)

# 1. Normalize 'Name' column
data['Name'] = data['Name'].str.title()

# 2. Convert date columns to datetime
data['Date of Admission'] = pd.to_datetime(data['Date of Admission'])
data['Discharge Date'] = pd.to_datetime(data['Discharge Date'])

# 3. Check for duplicates
duplicates = data.duplicated().sum()
print(f"Number of duplicate rows: {duplicates}")
data = data.drop_duplicates()

# 4. Handle missing values (if any)
missing_values = data.isnull().sum()
print(f"Missing values in each column:\n{missing_values}")

# Save cleaned data
cleaned_file_path = 'cleaned_healthcare_data.csv'
data.to_csv(cleaned_file_path, index=False)
print(f"Cleaned dataset saved to {cleaned_file_path}.")
