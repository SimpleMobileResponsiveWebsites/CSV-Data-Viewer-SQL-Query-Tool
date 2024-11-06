# CSVDataViewerTool.py

import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Streamlit page configuration
st.set_page_config(page_title="CSV Data Viewer Tool", layout="wide")

# Helper function to load data with caching
@st.cache_data
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)

# Sidebar: Upload CSV Files
st.sidebar.title("Upload CSV Files")
uploaded_files = st.sidebar.file_uploader("Upload one or multiple CSV files", accept_multiple_files=True, type=["csv"])

# Initialize a dictionary to store DataFrames
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

if selected_file:
    df = dataframes[selected_file]
    st.write(f"### Preview of `{selected_file}` Dataset")
    
    # Display selectable rows and columns
    with st.expander("Choose Rows and Columns to Display"):
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select columns to display", options=all_columns, default=all_columns)
        
        max_rows = st.slider("Select number of rows to display", min_value=1, max_value=100, value=10)
        st.dataframe(df[selected_columns].head(max_rows))

    # **New Feature: Basic Filtering and Sorting Options**
    with st.expander("Filter and Sort Data"):
        # Filtering Example
        st.subheader("Filter Rows")
        filter_column = st.selectbox("Column to filter by", options=all_columns)
        if df[filter_column].dtype in ['int64', 'float64']:
            filter_value = st.number_input(f"Filter `{filter_column}` values greater than:", value=float(df[filter_column].mean()))
            filtered_df = df[df[filter_column] > filter_value]
            st.write(f"Filtered rows where `{filter_column}` > {filter_value}:")
            st.dataframe(filtered_df[selected_columns].head(max_rows))
        else:
            filter_value = st.text_input(f"Filter `{filter_column}` by value:", "")
            filtered_df = df[df[filter_column] == filter_value]
            st.write(f"Filtered rows where `{filter_column}` = '{filter_value}':")
            st.dataframe(filtered_df[selected_columns].head(max_rows))

        # Sorting Example
        st.subheader("Sort Data")
        sort_column = st.selectbox("Select column to sort by", options=all_columns)
        sort_order = st.radio("Sort order", options=["Ascending", "Descending"])
        sorted_df = df.sort_values(by=sort_column, ascending=(sort_order == "Ascending"))
        st.write(f"Data sorted by `{sort_column}` in {sort_order.lower()} order:")
        st.dataframe(sorted_df[selected_columns].head(max_rows))

# Data Merging (for multiple uploaded files)
if len(dataframes) > 1:
    st.write("### Merge Datasets")
    with st.expander("Join Two Datasets"):
        left_df_name = st.selectbox("Select left DataFrame", options=dataframes.keys())
        right_df_name = st.selectbox("Select right DataFrame", options=[k for k in dataframes.keys() if k != left_df_name])
        
        join_type = st.selectbox("Join Type", ["inner", "outer", "left", "right"])
        common_columns = list(set(dataframes[left_df_name].columns) & set(dataframes[right_df_name].columns))
        
        if common_columns:
            join_column = st.selectbox("Select column to join on", options=common_columns)
            merged_df = pd.merge(dataframes[left_df_name], dataframes[right_df_name], on=join_column, how=join_type)
            st.write(f"Preview of `{join_type}` join on `{join_column}`:")
            st.dataframe(merged_df.head(10))
        else:
            st.warning("No common columns found for joining.")

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
st.write("This tool allows you to filter, analyze, and visualize your CSV data using custom filtering and sorting options, data merging, and visualizations.")
