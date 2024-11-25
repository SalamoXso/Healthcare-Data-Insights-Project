import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load the dataset
file_path = "cleaned_healthcare_data.csv"  # Update with the correct path if necessary
data = pd.read_csv(file_path)

# Ensure correct data types for date columns
data['Date of Admission'] = pd.to_datetime(data['Date of Admission'])
data['Discharge Date'] = pd.to_datetime(data['Discharge Date'])

# Add a new column for length of stay
data['Length of Stay (Days)'] = (data['Discharge Date'] - data['Date of Admission']).dt.days

# Streamlit UI
st.title("Healthcare Data Insights Dashboard")
st.sidebar.title("Analysis Options")
analysis_option = st.sidebar.selectbox(
    "Select Analysis",
    [
        "Age Distribution", 
        "Gender Distribution", 
        "Top Medical Conditions", 
        "Timeline Analysis", 
        "Treatment Analysis"
    ]
)

# Age Distribution
if analysis_option == "Age Distribution":
    st.header("Age Distribution of Patients")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['Age'], bins=20, kde=True, color='skyblue', ax=ax)
    ax.set_title('Age Distribution of Patients', fontsize=16)
    ax.set_xlabel('Age', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    st.pyplot(fig)

# Gender Distribution
elif analysis_option == "Gender Distribution":
    st.header("Gender Distribution")
    gender_counts = data['Gender'].value_counts()
    st.bar_chart(gender_counts)

# Common Medical Conditions
elif analysis_option == "Top Medical Conditions":
    st.header("Top 10 Medical Conditions")
    condition_counts = data['Medical Condition'].value_counts().head(10)
    st.bar_chart(condition_counts)

# Timeline Analysis
elif analysis_option == "Timeline Analysis":
    st.header("Timeline Analysis")
    # Monthly admissions
    monthly_admissions = data['Date of Admission'].dt.to_period('M').value_counts().sort_index()
    st.subheader("Admissions Over Time")
    st.line_chart(monthly_admissions)

    # Average length of stay over time
    avg_length_stay = data.groupby(data['Date of Admission'].dt.to_period('M'))['Length of Stay (Days)'].mean()
    st.subheader("Average Length of Stay Over Time")
    st.line_chart(avg_length_stay)

# Treatment Analysis
elif analysis_option == "Treatment Analysis":
    st.header("Treatment Analysis")
    # Most common medications
    st.subheader("Most Common Medications")
    medication_counts = data['Medication'].value_counts().head(10)
    st.bar_chart(medication_counts)

    # Medications vs. Medical Conditions
    st.subheader("Medications by Medical Condition")
    medication_condition = data.groupby('Medical Condition')['Medication'].value_counts().unstack().fillna(0)
    st.dataframe(medication_condition.style.background_gradient(cmap="viridis"))
