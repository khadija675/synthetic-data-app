import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string
import io

st.title("Synthetic Data Generator")

# Sidebar for user inputs
st.sidebar.header("Data Generation Parameters")
num_rows = st.sidebar.slider("Number of Rows", 10, 1000, 100)
num_columns = st.sidebar.slider("Number of Columns", 1, 20, 5)

# Initialize column configurations
if 'columns_config' not in st.session_state:
    st.session_state.columns_config = {}

# Function to generate random string
def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to generate synthetic data
def generate_synthetic_data(rows, columns, config):
    data = {}
    for col_idx in range(columns):
        col_name = f"Column_{col_idx + 1}"
        col_type = config.get(col_name, {}).get('type', 'Numeric')
        
        if col_type == 'Numeric':
            data[col_name] = np.random.normal(
                loc=config.get(col_name, {}).get('mean', 0),
                scale=config.get(col_name, {}).get('std', 1),
                size=rows
            )
        elif col_type == 'Categorical':
            categories = config.get(col_name, {}).get('categories', ['A', 'B', 'C'])
            data[col_name] = np.random.choice(categories, size=rows)
        elif col_type == 'Datetime':
            start_date = datetime.now() - timedelta(days=365)
            data[col_name] = [start_date + timedelta(days=random.randint(0, 365)) for _ in range(rows)]
        elif col_type == 'Text':
            data[col_name] = [random_string() for _ in range(rows)]
    
    return pd.DataFrame(data)

# Column configuration
st.header("Configure Columns")
for col_idx in range(num_columns):
    col_name = f"Column_{col_idx + 1}"
    with st.expander(f"Configure {col_name}"):
        col_type = st.selectbox(
            f"Data Type for {col_name}",
            ['Numeric', 'Categorical', 'Datetime', 'Text'],
            key=f"type_{col_idx}"
        )
        
        col_config = {'type': col_type}
        
        if col_type == 'Numeric':
            col_config['mean'] = st.number_input(
                f"Mean for {col_name}",
                value=0.0,
                key=f"mean_{col_idx}"
            )
            col_config['std'] = st.number_input(
                f"Standard Deviation for {col_name}",
                value=1.0,
                min_value=0.1,
                key=f"std_{col_idx}"
            )
        elif col_type == 'Categorical':
            categories = st.text_input(
                f"Categories for {col_name} (comma-separated)",
                value="A,B,C",
                key=f"cat_{col_idx}"
            )
            col_config['categories'] = [cat.strip() for cat in categories.split(',')]
        
        st.session_state.columns_config[col_name] = col_config

# Generate and display data
if st.button("Generate Data"):
    df = generate_synthetic_data(num_rows, num_columns, st.session_state.columns_config)
    st.session_state.generated_data = df
    st.write("Generated Data Preview:")
    st.dataframe(df.head())
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="synthetic_data.csv",
        mime="text/csv"
    )

# Display full data if generated
if 'generated_data' in st.session_state:
    st.header("Full Generated Data")
    st.dataframe(st.session_state.generated_data)