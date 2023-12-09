import streamlit as st  # web development
import datetime
# from subs.data_loader import load_data, process_data_for_analysis , process_uploaded_file, convert_time , process_time_resolution_and_duplicates , display_column_statistics
# from subs.visualisation import visualize_missing_values , visualize_data_by_date_range , visualise_time_series_data
import black 

# You need to instal both Pyomo and glpk package before running the code 

from pyomo.environ import *
import numpy as np
import math
import pandas   as pd
from pandas import Series, DataFrame
from subs.data_processing import time_series_plot, plot_cumulative_distribution
from subs.optimisation_engine import opt_engine , solver_opt
from subs.initialisation import GenCo_reading
st.set_page_config(
    page_title="Capacity Expansion Model",
    page_icon="🏭",
)
st.image("./images/header.png")

st.title("A Basic Power System Capacity Expansion Model")
st.markdown("Created by Saeed Misaghian")
st.markdown("📧 Contact me: [sam.misaqian@gmail.com](mailto:sam.misaqian@gmail.com)")
st.markdown("🔗 [GitHub](https://github.com/SaM-92)")
st.markdown("🔗 [LinkedIn](https://www.linkedin.com/in/saeed-misaghian/)")

st.markdown("📕 This model and associated data are taken from [this repos](https://github.com/Power-Systems-Optimization-Course/power-systems-optimization/blob/master/Notebooks/03-Basic-Capacity-Expansion.ipynb)")

st.markdown("### 🏭 Generators Input Data")


# Ask the user whether they want to upload a CSV file or use the editable table
input_method = st.radio('How do you want to input the data?', ('Use Editable Table','Upload CSV File' ))

generators,FixedCost,VarCost = GenCo_reading(input_method)



st.markdown("### 📊 Demand Input Data")
# Ask the user whether they want to use the default values or upload their own data
input_method = st.radio('Do you want to use the default values for year long load data or upload your own data?', ('Use Default Values', 'Upload My Own Data'))

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


st.dataframe(demand)


st.markdown("### 🍃🌍☀️ Renewables Capacity Factors")

input_method = st.radio('Do you want to use the default values for year long renewables data or upload your own data?', ('Use Default Values', 'Upload My Own Data'))

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

st.dataframe(RES)

st.markdown("### 💡 Penalty for non-served energy ($/MWh)")
NSECost = st.slider(' Penalty for non-served energy ($/MWh)', 500, 20000, 5000)
st.markdown("We recommend at least $9000/MWh")
st.write("Penalty for non-served energy ", NSECost, '$/MWh')


# generators["FixedCost"]
# generators["VarCost"]
# number_of_generators
# name_of_generators



st.markdown("### ⚙️ Optimisation Engine")
if st.button('Run the Model'):
    time_series_plot(demand,'Demand')
    plot_cumulative_distribution(demand)
    # opt_model = opt_engine(generators,demand,NSECost) 
    # solver_opt(opt_model)
