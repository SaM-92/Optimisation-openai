from pyomo.environ import *
import streamlit as st  # web development
import pandas as pd  
import numpy as np 

def opt_engine(
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
):
    # Create a concrete model in Pyomo
    model = ConcreteModel()

    # penalty for non-served energy
    NSECost = NSECost

    # The set of generators from the generators DataFrame

    model.G = Set(
        initialize=[i for i in generators[generators_names]],
        doc="set of generators",
    )

    # The set of hours in the demand DataFrame
    model.H = Set(
        initialize=RangeSet(0, len(demand.reset_index().index) - 1), doc="set of time"
    )

    # Generating capacity built (MW)
    model.CAP = Var(model.G, domain=NonNegativeReals)

    # Generation in each hour (MWh)
    model.GEN = Var(model.G, model.H, domain=NonNegativeReals)

    # Non-served energy in each hour (MWh)
    model.NSE = Var(model.H, domain=NonNegativeReals)

    # cDemandBalance (eq. 11)
    def cDemandBalance_(model, h):
        return (
            sum(model.GEN[i, h] for i in model.G) + model.NSE[h]
            == demand[demand_column][h]
        )

    model.cDemandBalance = Constraint(model.H, rule=cDemandBalance_)

    #cCapacity (eq. 12)
    def cCapacity_(model,g,h):
        if g != RES_wind or RES_solar:
            return(model.GEN[g,h] <= model.CAP[g] )
        elif g==RES_wind:
            return(model.GEN[g,h] <= model.CAP[g] *RES[RES_wind])
        elif g==RES_solar:
            return(model.GEN[g,h] <= model.CAP[g] *RES[RES_solar])
    model.cCapacity=Constraint(model.G,model.H,rule=cCapacity_)

    def RES_max_cap_(model,g):
        if g == RES_wind:
            return(model.CAP[g] <= np.max(demand[demand_column])*max_capacity_wind)
        elif g == RES_solar:
            # return(model.GEN[g,h] <= model.CAP[g]*max_capacity_solar)
            return(model.CAP[g] <= np.max(demand[demand_column])**max_capacity_solar)
        else:
            return Constraint.Skip
    model.RES_max_cap=Constraint(model.G,rule=RES_max_cap_)


    # ---------------Objective Function-------------------
    # Create dictionaries for fixed and variable costs
    fixed_costs = generators.set_index(generators_names)[FixedCost].to_dict()
    var_costs = generators.set_index(generators_names)[VarCost].to_dict()

    def obj_rule(model):
        fixed_cost_ = sum(fixed_costs[i] * model.CAP[i] for i in model.G)
        variable_cost_ = sum(
            var_costs[i] * model.GEN[i, h] for i in model.G for h in model.H
        )
        not_supplied_cost = sum(NSECost * model.NSE[h] for h in model.H)
        return fixed_cost_ + variable_cost_ + not_supplied_cost

    model.of = Objective(rule=obj_rule, sense=minimize)

    return model


def solver_opt(model_):
    with st.spinner("Solving the model..."):
        solver = SolverFactory("glpk")
        # solver.options['thread']=4

        # solver.options['mipgap']=1e-1
        results = solver.solve(model_, tee=True)
        model_.solutions.load_from(results)
        if (results.solver.status == SolverStatus.ok) and (
            results.solver.termination_condition == TerminationCondition.optimal
        ):
            # print('feasible')
            st.text("✔️ Feasible")
            state_solution = True
            
        elif results.solver.termination_condition == TerminationCondition.infeasible:
            # print('infeasible')
            st.text("❌ infeasible")
            state_solution = False
        else:
            # print ('Solver Status:',  results.solver.status)
            st.text(f"Solver Status: {results.solver.status}")
    return state_solution 

def interpret_outputs(model_,generators,generators_names,demand,demand_column,state_solution):
    # if state_solution == True:
    #             # Create a dictionary for generator indices
    #             generator_indices = {name: i for i, name in enumerate(generators[generators_names])}

    #             # Initialize an empty DataFrame
    #             results_df  = pd.DataFrame(columns=['Resource', 'MW', 'Percent_MW', 'GWh', 'Percent_GWh'])

    #             # Record generation capacity and energy results
    #             for i in model_.G:
    #                 generation = value(sum(model_.GEN[i,h] for h in model_.H))
    #                 MWh_share = generation/sum(demand[demand_column])*100
    #                 cap_share = value(model_.CAP[i])/np.max(demand[demand_column])*100
    #                 new_row  = pd.DataFrame({
    #                     'Resource': generators[generators_names][generator_indices[i]], 
    #                     'MW': value(model_.CAP[i]),
    #                     'Percent_MW': cap_share,
    #                     'GWh': generation/1000,
    #                     'Percent_GWh': MWh_share
    #                 },index=[0])

    #                 results_df = pd.concat([results_df, new_row], ignore_index=True)

                    
    #             # Calculate how much non-served energy there was and add to results
    #             NSE_MW = 0 
    #             for h in model_.H:
    #                 initial= value(model_.NSE[h]) 
    #                 if initial > NSE_MW:
    #                     NSE_MW=initial   
    #             NSE_MWh = value(sum(model_.NSE[h] for h in model_.H))

    #             new_row  = pd.DataFrame({
    #                     'Resource': "NSE", 
    #                     'MW': NSE_MW,
    #                     'Percent_MW': NSE_MW/(np.max(demand[demand_column]))*100,
    #                     'GWh': NSE_MWh/1000,
    #                     'Percent_GWh':100* NSE_MWh/sum(demand[demand_column])
    #                 },index=[0]) 
                
    #             results_df = pd.concat([results_df, new_row], ignore_index=True) 

    #             st.write(results_df)

    if state_solution == True:
        generator_indices = {name: i for i, name in enumerate(generators[generators_names])}
        results = []  # Create an empty list to hold DataFrames

        for i in model_.G:
            generation = value(sum(model_.GEN[i, h] for h in model_.H))
            MWh_share = generation / sum(demand[demand_column]) * 100
            cap_share = value(model_.CAP[i]) / np.max(demand[demand_column]) * 100
            new_row = pd.DataFrame({
                'Resource': generators[generators_names][generator_indices[i]],
                'MW': value(model_.CAP[i]),
                'Percent_MW': cap_share,
                'GWh': generation / 1000,
                'Percent_GWh': MWh_share
            }, index=[0])
            
            results.append(new_row)  # Append each DataFrame to the list

        # Calculate how much non-served energy there was and add to results
        NSE_MW = 0 
        for h in model_.H:
            initial= value(model_.NSE[h]) 
            if initial > NSE_MW:
                NSE_MW=initial   
        NSE_MWh = value(sum(model_.NSE[h] for h in model_.H))

        # Create the DataFrame for NSE
        new_nse_row = pd.DataFrame({
            'Resource': "NSE",
            'MW': NSE_MW,
            'Percent_MW': NSE_MW / (np.max(demand[demand_column])) * 100,
            'GWh': NSE_MWh / 1000,
            'Percent_GWh': 100 * NSE_MWh / sum(demand[demand_column])
        }, index=[0])

        results.append(new_nse_row)

        # Concatenate all DataFrames in the results list
        results_df = pd.concat(results, ignore_index=True)

        st.write(results_df)
