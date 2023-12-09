import streamlit as st  # web development
import pandas as pd

def GenCo_reading(input_method):
    # Create a DataFrame with your default data
    data = {
        'Generators': ['Geo', 'Coal', 'CCGT', 'CT', 'Wind', 'Solar'],
        'Description': ['Geothermal', 'Supercritical Coal', 'Natural gas CCGT', 'Natural gas CT', 'Onshore wind', 'Tracking solar PV'],
        'FixedCost': [563500, 270280, 82400, 62888, 91000, 50850],
        'VarCost': [0, 24.2, 27.6, 43.8, 0, 0]
    }
    df = pd.DataFrame(data)

    if input_method == 'Upload CSV File':
        # File uploader
        uploaded_file = st.file_uploader("Upload your CSV file",key='Genco')

        # Check if a file was uploaded
        if uploaded_file is not None:
            # Load the uploaded file into a DataFrame
            generators = pd.read_csv(uploaded_file)
            st.dataframe(generators)
            FixedCost = st.selectbox(
                "Please select the column showing Fixed Costs:", generators.columns
            )
            VarCost = st.selectbox(
                "Please select the column showing Variable Costs:", generators.columns
            )
        else:
            st.warning('Please upload a CSV file.')
            st.stop()
    else:
        # If the user chose to use the editable table, display the data editor
        generators = st.data_editor(df, num_rows="dynamic")
        FixedCost = generators.FixedCost
        VarCost = generators.VarCost    

    return(generators,FixedCost,VarCost)    
