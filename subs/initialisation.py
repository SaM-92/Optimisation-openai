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

            generators_names = st.selectbox(
                "Please select the column showing name of generators:", generators.columns
            )
        else:
            st.warning('Please upload a CSV file.')
            st.stop()
    else:
        # If the user chose to use the editable table, display the data editor
        generators = st.data_editor(df, num_rows="dynamic")
        FixedCost = "FixedCost"
        VarCost = "VarCost" 
        generators_names = "G"

    return(generators,FixedCost,VarCost,generators_names)    

def demand_reading(input_method):

    if input_method == 'Upload My Own Data':
        # File uploader
        uploaded_file = st.file_uploader("Upload your CSV file",key='demand')
        
        # Check if a file was uploaded
        if uploaded_file is not None:
            # Load the uploaded file into a DataFrame
            demand = pd.read_csv(uploaded_file)
            demand_column = st.selectbox(
                "Please select the column with demand observations:", demand.columns
            )
        else:
            st.warning('Please upload a CSV file.')
            st.stop()
    else:
        # If the user chose to use the default values, load the default data
        demand = pd.read_csv("expansion_data/demand_for_expansion.csv")
        demand_column=demand.Demand

    st.dataframe(demand)
    return(demand,demand_column)


def RES_reading(input_method):

    if input_method == 'Upload My Own Data':
        # File uploader
        uploaded_file = st.file_uploader("Upload your CSV file",key='RES')
        
        # Check if a file was uploaded
        if uploaded_file is not None:
            # Load the uploaded file into a DataFrame
            RES = pd.read_csv(uploaded_file)
            RES_wind = st.selectbox(
                "Please select the column with wind observations 🍃:", RES.columns
            )
            RES_solar = st.selectbox(
                "Please select the column with solar observations ☀️:", RES.columns
            )
        else:
            st.warning('Please upload a CSV file.')
            st.stop()
    else:
        # If the user chose to use the default values, load the default data
        RES = pd.read_csv("expansion_data/wind_solar_for_expansion.csv")
        RES_wind = "Wind"
        RES_solar = "Solar"
    st.dataframe(RES)    

    return (RES,RES_wind,RES_solar)

def not_supplied_energy():
    NSECost = st.slider(' Penalty for non-served energy ($/MWh)', 5000, 20000, 9000, key = 'NSECost')
    st.markdown("We recommend at least $9000/MWh")
    st.write("Penalty for non-served energy ", NSECost, '$/MWh')
    return NSECost