import streamlit as st
import pandas as pd
import pandasql as psql
import plotly.express as px
from io import StringIO

# Streamlit page configuration
st.set_page_config(page_title="CSV Data Viewer & SQL Query Tool", layout="wide")

# Helper function to load and cache data
@st.cache_data
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)

# Sidebar: Upload CSV Files
st.sidebar.title("Upload CSV Files")
uploaded_files = st.sidebar.file_uploader("Upload one or multiple CSV files", accept_multiple_files=True, type=["csv"])

# Initialize a dictionary to store dataframes
dataframes = {}
if uploaded_files:
    st.sidebar.success(f"{len(uploaded_files)} files uploaded successfully!")
    for uploaded_file in uploaded_files:
        try:
            df = load_data(uploaded_file)
            dataframes[uploaded_file.name] = df
        except Exception as e:
            st.sidebar.error(f"Failed to load {uploaded_file.name}: {e}")
else:
    st.sidebar.warning("Please upload at least one CSV file to proceed.")

# Sidebar: File Selection & Data Preview
st.sidebar.title("Dataset Preview & Options")
selected_file = st.sidebar.selectbox("Select a file to preview", options=list(dataframes.keys()))

# Display the selected DataFrame
if selected_file:
    df = dataframes[selected_file]
    st.write(f"### Preview of `{selected_file}` Dataset")
    
    # Display selectable rows and columns
    with st.expander("Choose Rows and Columns to Display"):
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select columns to display", options=all_columns, default=all_columns)
        
        max_rows = st.slider("Select number of rows to display", min_value=1, max_value=100, value=10)
        st.dataframe(df[selected_columns].head(max_rows))

# SQL Query Section
st.write("### Run SQL Query on Uploaded Data")
sql_query = st.text_area("Write an SQL query to filter, join, or sort your data", "SELECT * FROM df LIMIT 5")

if st.button("Run SQL Query"):
    if not sql_query.strip():
        st.warning("Please enter a SQL query.")
    else:
        if selected_file:  # Ensure a file is selected and loaded
            try:
                # Execute the query using pandasql, ensuring 'df' is passed explicitly
                query_result = psql.sqldf(sql_query, {"df": df})
                st.write("**Query Result:**")
                st.dataframe(query_result)
            except Exception as e:
                st.error(f"Error in SQL query: {e}")
        else:
            st.error("No data file selected. Please upload and select a CSV file to continue.")

# Visualization Section
st.write("### Data Visualization")
if selected_file:
    with st.expander("Choose Columns for Visualization"):
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if len(numeric_columns) < 2:
            st.warning("Please select a file with at least two numeric columns for visualization.")
        else:
            x_axis = st.selectbox("X-axis", options=numeric_columns)
            y_axis = st.selectbox("Y-axis", options=numeric_columns)
            chart_type = st.selectbox("Chart Type", ["Scatter Plot", "Line Chart", "Bar Chart"])
            
            # Generate the chart
            if x_axis and y_axis:
                if chart_type == "Scatter Plot":
                    fig = px.scatter(df, x=x_axis, y=y_axis)
                elif chart_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis)
                elif chart_type == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis)
                
                st.plotly_chart(fig)

# Conclusion
st.write("This tool allows you to filter, analyze, and visualize your CSV data using SQL queries and custom visualizations.")
