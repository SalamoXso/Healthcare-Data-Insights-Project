import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud

# Set page config as the first Streamlit command
st.set_page_config(page_title="Healthcare Data Insights Dashboard", layout="wide")

# Load the dataset
@st.cache_data
def load_data():
    file_path = "cleaned_healthcare_data.csv"  # Update with the correct path if necessary
    data = pd.read_csv(file_path)
    data['Date of Admission'] = pd.to_datetime(data['Date of Admission'])
    data['Discharge Date'] = pd.to_datetime(data['Discharge Date'])
    data['Length of Stay (Days)'] = (data['Discharge Date'] - data['Date of Admission']).dt.days
    return data

data = load_data()

# Streamlit UI
st.title("Healthcare Data Insights Dashboard")

# Sidebar
st.sidebar.title("Analysis Options")
analysis_option = st.sidebar.selectbox(
    "Select Analysis",
    [
        "Overview",
        "Patient Demographics", 
        "Medical Conditions", 
        "Timeline Analysis", 
        "Treatment Analysis",
        "Length of Stay Analysis"
    ]
)

# Overview
if analysis_option == "Overview":
    st.header("Overview of Healthcare Data")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Patients", len(data))
    col2.metric("Avg Age", f"{data['Age'].mean():.1f}")
    col3.metric("Avg Length of Stay", f"{data['Length of Stay (Days)'].mean():.1f} days")
    col4.metric("Unique Conditions", data['Medical Condition'].nunique())
    
    st.subheader("Quick Insights")
    fig = go.Figure()
    fig.add_trace(go.Box(y=data['Age'], name="Age Distribution"))
    fig.add_trace(go.Box(y=data['Length of Stay (Days)'], name="Length of Stay Distribution"))
    fig.update_layout(title="Age and Length of Stay Distributions", height=500)
    st.plotly_chart(fig, use_container_width=True)

# Patient Demographics
elif analysis_option == "Patient Demographics":
    st.header("Patient Demographics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Age Distribution")
        fig = px.histogram(data, x='Age', nbins=20, marginal='box')
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Gender Distribution")
        fig = px.pie(data, names='Gender', hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Age Distribution by Gender")
    fig = px.box(data, x='Gender', y='Age', color='Gender')
    st.plotly_chart(fig, use_container_width=True)

# Medical Conditions
elif analysis_option == "Medical Conditions":
    st.header("Medical Conditions Analysis")
    
    top_n = st.slider("Select number of top conditions to display", 5, 20, 10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top {top_n} Medical Conditions")
        condition_counts = data['Medical Condition'].value_counts().head(top_n)
        fig = px.bar(x=condition_counts.index, y=condition_counts.values)
        fig.update_layout(xaxis_title="Medical Condition", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Word Cloud of Medical Conditions")
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(data['Medical Condition']))
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

# Timeline Analysis
elif analysis_option == "Timeline Analysis":
    st.header("Timeline Analysis")
    
    # Monthly admissions
    monthly_admissions = data['Date of Admission'].dt.to_period('M').value_counts().sort_index()
    monthly_admissions.index = monthly_admissions.index.astype(str)
    
    st.subheader("Admissions Over Time")
    fig = px.line(x=monthly_admissions.index, y=monthly_admissions.values)
    fig.update_layout(xaxis_title="Month", yaxis_title="Number of Admissions")
    st.plotly_chart(fig, use_container_width=True)
    
    # Average length of stay over time
    avg_length_stay = data.groupby(data['Date of Admission'].dt.to_period('M'))['Length of Stay (Days)'].mean()
    avg_length_stay.index = avg_length_stay.index.astype(str)
    
    st.subheader("Average Length of Stay Over Time")
    fig = px.line(x=avg_length_stay.index, y=avg_length_stay.values)
    fig.update_layout(xaxis_title="Month", yaxis_title="Average Length of Stay (Days)")
    st.plotly_chart(fig, use_container_width=True)

# Treatment Analysis
# Treatment Analysis
elif analysis_option == "Treatment Analysis":
    st.header("Treatment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Most Common Medications")
        medication_counts = data['Medication'].value_counts().head(10)
        fig = px.bar(x=medication_counts.index, y=medication_counts.values)
        fig.update_layout(xaxis_title="Medication", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Treatment Effectiveness")
        if 'Treatment Outcome' in data.columns:
            treatment_effectiveness = data.groupby('Medication')['Treatment Outcome'].value_counts(normalize=True).unstack()
            fig = px.bar(treatment_effectiveness, barmode='stack')
            fig.update_layout(xaxis_title="Medication", yaxis_title="Proportion of Outcomes")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Column 'Treatment Outcome' not found in the data.")
    
    st.subheader("Medications by Medical Condition")
    selected_condition = st.selectbox("Select a Medical Condition", data['Medical Condition'].unique())
    condition_data = data[data['Medical Condition'] == selected_condition]
    medication_counts = condition_data['Medication'].value_counts().head(10)
    fig = px.bar(x=medication_counts.index, y=medication_counts.values)
    fig.update_layout(xaxis_title="Medication", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

    #Length of Stay Analysis
elif analysis_option == "Length of Stay Analysis":
    st.header("Length of Stay Analysis")

    # Distribution of Length of Stay
    st.subheader("Distribution of Length of Stay")
    fig = px.histogram(data, x='Length of Stay (Days)', nbins=50, marginal='box')
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig, use_container_width=True)

    # Average Length of Stay by Medical Condition
    st.subheader("Average Length of Stay by Medical Condition")
    avg_length_stay_by_condition = data.groupby('Medical Condition')['Length of Stay (Days)'].mean().reset_index()
    fig = px.bar(x=avg_length_stay_by_condition['Medical Condition'], y=avg_length_stay_by_condition['Length of Stay (Days)'], 
                 title="Average Length of Stay by Medical Condition")
    fig.update_layout(xaxis_title="Medical Condition", yaxis_title="Average Length of Stay (Days)")
    st.plotly_chart(fig, use_container_width=True)

    # Length of Stay Over Time
    st.subheader("Length of Stay Over Time")
    avg_length_stay_over_time = data.groupby(data['Date of Admission'].dt.to_period('M'))['Length of Stay (Days)'].mean()
    avg_length_stay_over_time.index = avg_length_stay_over_time.index.astype(str)
    fig = px.line(x=avg_length_stay_over_time.index, y=avg_length_stay_over_time.values, 
                  title="Average Length of Stay Over Time")
    fig.update_layout(xaxis_title="Month", yaxis_title="Average Length of Stay (Days)")
    st.plotly_chart(fig, use_container_width=True)

    # Top 10 Conditions with Longest Average Length of Stay
    st.subheader("Top 10 Conditions with Longest Average Length of Stay")
    top_conditions = avg_length_stay_by_condition.nlargest(10, 'Length of Stay (Days)')
    fig = px.bar(x=top_conditions['Medical Condition'], y=top_conditions['Length of Stay (Days)'], 
                 title="Top 10 Conditions with Longest Average Length of Stay")
    fig.update_layout(xaxis_title="Medical Condition", yaxis_title="Average Length of Stay (Days)")
    st.plotly_chart(fig, use_container_width=True)