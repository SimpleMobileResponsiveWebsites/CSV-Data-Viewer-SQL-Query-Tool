import streamlit as st
import pandas as pd
import pandasql as psql
import io

# Page configuration
st.set_page_config(page_title="CSV Data Viewer & SQL Query Tool", layout="wide")

# Sidebar: Upload CSV Files
st.sidebar.title("Upload CSV Files")
uploaded_files = st.sidebar.file_uploader("Upload one or multiple CSV files", accept_multiple_files=True, type=["csv"])

# Initialize uploaded data list and dictionary to store dataframes
dataframes = {}
if uploaded_files:
    st.sidebar.success(f"{len(uploaded_files)} files uploaded successfully!")
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        dataframes[uploaded_file.name] = df
else:
    st.sidebar.warning("Please upload at least one CSV file to proceed.")

# Sidebar: File Selection & Data Preview
st.sidebar.title("Dataset Preview & Options")
selected_file = st.sidebar.selectbox("Select a file to preview", options=list(dataframes.keys()) if dataframes else [])

if selected_file:
    df = dataframes[selected_file]
    st.write(f"**Preview of `{selected_file}` dataset:**")
    
    # Display the DataFrame with selectable rows and columns
    with st.expander("Choose Rows and Columns to Display"):
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select columns to display", options=all_columns, default=all_columns)
        
        # Let user choose number of rows to display
        max_rows = st.slider("Select number of rows to display", min_value=1, max_value=min(100, len(df)), value=10)
        
        # Display selected portion of DataFrame
        st.dataframe(df[selected_columns].head(max_rows))

# SQL Query Section
st.sidebar.title("SQL Query Options")
st.write("### SQL Query on Uploaded Data")
sql_query = st.text_area("Write an SQL query to filter, join, or sort your datasets", "SELECT * FROM df LIMIT 5")

if st.button("Run SQL Query"):
    if not sql_query.strip():
        st.warning("Please enter a SQL query.")
    else:
        try:
            query_result = psql.sqldf(sql_query, globals())
            st.write("**Query Result:**")
            st.dataframe(query_result)
        except Exception as e:
            st.error(f"Error in SQL query: {e}")

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

            if x_axis and y_axis:
                chart_type = st.selectbox("Chart type", ["Scatter Plot", "Line Chart", "Bar Chart"])
                
                # Display the chart based on user selection
                if chart_type == "Scatter Plot":
                    st.write(f"**Scatter Plot:** {x_axis} vs {y_axis}")
                    st.plotly_chart(px.scatter(df, x=x_axis, y=y_axis))
                elif chart_type == "Line Chart":
                    st.write(f"**Line Chart:** {x_axis} vs {y_axis}")
                    st.plotly_chart(px.line(df, x=x_axis, y=y_axis))
                elif chart_type == "Bar Chart":
                    st.write(f"**Bar Chart:** {x_axis} vs {y_axis}")
                    st.plotly_chart(px.bar(df, x=x_axis, y=y_axis))

# Conclusion
st.write("This tool allows you to filter, analyze, and visualize your CSV data using SQL queries and custom visualizations.")
