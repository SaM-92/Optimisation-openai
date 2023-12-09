from pyomo.environ import *
import streamlit as st  # web development

def opt_engine(generators,demand):

    # Create a concrete model in Pyomo 
    model = ConcreteModel()

    # penalty for non-served energy 
    NSECost = 9000


    # The set of generators from the generators DataFrame

    model.G  = Set(initialize=RangeSet(0,generators.shape[0] -3), doc='set of generators') 

    # The set of hours in the demand DataFrame
    model.H = Set(initialize=RangeSet(0,len(demand.Hour)-1), doc='set of time')  

    # Generating capacity built (MW)
    model.CAP=Var(model.G,domain=NonNegativeReals)
    # Generation in each hour (MWh)

    model.GEN=Var(model.G,model.H,domain=NonNegativeReals)
    # Non-served energy in each hour (MWh)
    model.NSE=Var(model.H,domain=NonNegativeReals)

    #cDemandBalance (eq. 11)
    def cDemandBalance_(model,h):
        return(sum(model.GEN[i,h] for i in model.G) + model.NSE[h] == demand.Demand[h])
    model.cDemandBalance=Constraint(model.H,rule=cDemandBalance_)


    #cCapacity (eq. 12)
    def cCapacity_(model,g,h):
        return(model.GEN[g,h] <= model.CAP[g] )
    model.cCapacity=Constraint(model.G,model.H,rule=cCapacity_)

    # ---------------Objective Function-------------------
    def obj_rule(model):
        fixed_cost_=sum(generators["FixedCost"][i] * model.CAP[i] for i in model.G)
        variable_cost_=sum(generators["VarCost"][i] * model.GEN[i,h] for i in model.G for h in model.H)
        not_supplied_cost=sum(NSECost * model.NSE[h] for h in model.H)
        return (fixed_cost_+variable_cost_+not_supplied_cost)
    model.of=Objective(rule=obj_rule,sense=minimize)

    return model 

def solver_opt(model_):
    solver = SolverFactory('glpk')     
    #solver.options['thread']=4

    # solver.options['mipgap']=1e-1
    results = solver.solve(model_, tee=True)   
    model_.solutions.load_from(results)  
    if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
        # print('feasible')
        st.text('feasible')
    elif (results.solver.termination_condition == TerminationCondition.infeasible):
        # print('infeasible')
        st.text('infeasible')
    else:
        # print ('Solver Status:',  results.solver.status)
        st.text(f'Solver Status: {results.solver.status}')