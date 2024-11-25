import pandas as pd

# Load the dataset
file_path = './healthcare_dataset.csv'
data = pd.read_csv(file_path)

# View dataset structure
print(data.info())
print(data.head())
