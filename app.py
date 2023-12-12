import streamlit as st  # web development
from pyomo.environ import *
from subs.data_processing import time_series_plot, plot_cumulative_distribution
from subs.optimisation_engine import opt_engine, solver_opt, interpret_outputs
from subs.initialisation import (
    GenCo_reading,
    demand_reading,
    RES_reading,
    not_supplied_energy,
)
from subs.openai_api import opt_gpt_summarise

st.set_page_config(
    page_title="Capacity Expansion Model", page_icon="🏭", layout="centered"
)


st.image("./images/header.png")

st.title("A Basic Power System Capacity Expansion Model")


st.sidebar.markdown("Created by Saeed Misaghian")
st.sidebar.markdown("📧 [sam.misaqian@gmail.com](mailto:sam.misaqian@gmail.com)")
st.sidebar.markdown("🔗 [GitHub](https://github.com/SaM-92)")
st.sidebar.markdown("🔗 [LinkedIn](https://www.linkedin.com/in/saeed-misaghian/)")

st.sidebar.markdown(
    "📕 This model and associated data are taken from [here](https://github.com/Power-Systems-Optimization-Course/power-systems-optimization/blob/master/Notebooks/03-Basic-Capacity-Expansion.ipynb)"
)

st.markdown("### 🏭 Generators Input Data")


# Ask the user whether they want to upload a CSV file or use the editable table
input_genco = st.radio(
    "How do you want to input the data?", ("Use Editable Table", "Upload CSV File")
)

generators, FixedCost, VarCost, generators_names = GenCo_reading(input_genco)

number_of_generators = generators.shape[0]


st.markdown("### 📊 Demand Input Data")
# Ask the user whether they want to use the default values or upload their own data
input_demand = st.radio(
    "Do you want to use the default values for year long load data or upload your own data?",
    ("Use Default Values", "Upload My Own Data"),
)

demand, demand_column = demand_reading(input_demand)


st.markdown("### 🍃🌍☀️ Renewables Capacity Factors")

input_RES = st.radio(
    "Do you want to use the default values for year long renewables data or upload your own data?",
    ("Use Default Values", "Upload My Own Data"),
)

RES, RES_wind, RES_solar = RES_reading(input_RES)
st.write("Penalty for non-served energy ", RES_wind, "$/MWh")
st.markdown("### 💡 Penalty for non-served energy ($/MWh)")

NSECost = not_supplied_energy()


st.markdown("### ⚙️ Optimisation Engine")
consider_renewables = st.checkbox(
    "Tick the box if you want to consider renewables", value=True, key="renewables"
)

if consider_renewables:
    # Default value is set to 50
    max_capacity_wind = st.slider(
        "Maximum Capacity of Wind Compared to the Yearlong Peak Load",
        min_value=0,
        max_value=100,
        value=0,
        key="capacity_wind",
    )

    max_capacity_solar = st.slider(
        "Maximum Capacity of Solar Compared to the Yearlong Peak Load ",
        min_value=0,
        max_value=100,
        value=0,
        key="capacity_solar",
    )

st.write("Maximum Capacity of Wind Compared to the Yearlong Peak Load ", max_capacity_wind, "%")
st.write("Maximum Capacity of Solar Compared to the Yearlong Peak Load ", max_capacity_solar, "%")


if 'output_results' not in st.session_state:
    st.session_state.output_results = None 

if st.button("Run the Model"):
    opt_model = opt_engine(
        generators,
        FixedCost,
        VarCost,
        generators_names,
        demand,
        demand_column,
        RES,
        RES_wind,
        RES_solar,
        NSECost,
        max_capacity_wind,
        max_capacity_solar,
    )
    state_solution = solver_opt(opt_model)
    
    st.session_state.output_results = interpret_outputs(
        opt_model, generators, generators_names, demand, demand_column, state_solution
    )

    time_series_plot(demand, "Demand")
    plot_cumulative_distribution(demand)

if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0
if "text_error" not in st.session_state:
    st.session_state.text_error = ""

st.markdown("### 🤖 OpenAI ")
if st.session_state.output_results is not None:
    # Check the number of requests
    if st.session_state.n_requests >= 3:
        st.session_state.text_error = "Too many requests. Please try later."
        st.session_state.n_requests = 1
        st.write(st.session_state.text_error)
    else:
        st.write(opt_gpt_summarise(generators,st.session_state.output_results))
        # Increment the number of requests
        st.session_state.n_requests += 1
