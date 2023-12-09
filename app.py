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
from subs.data_processing import time_series_plot
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

generators = pd.read_csv("expansion_data/generators_for_expansion.csv")
demand = pd.read_csv("expansion_data/demand_for_expansion.csv")

st.dataframe(generators)
st.dataframe(demand)

time_series_plot(demand,Demand)