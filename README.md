# Electricity Generation Capacity Expansion Model with Decision Insights via OpenAI

This Streamlit application showcases a basic electricity generation capacity expansion model. The primary objective of this model is to minimise fixed and variable costs among a range of generators to match projected future electricity demands. Beyond presenting numerical results, our optimisation engine employs OpenAI's API to interpret outcomes in concise, user-friendly paragraphs. The diagram below illustrates the foundational structure of this model.


![overview](https://file+.vscode-resource.vscode-cdn.net/c%3A/Users/saeed.misaghian/Documents/Repos_Personal/Energy_market/images/overview.png)



## Model Description

The model first presents a basic optimization formulation of this optimal thermal generator capacity expansion problem, and the impact of variable renewable energy sources (wind, solar). It then presents a slightly modified formulation that co-optimizes thermal and renewable capacities.

The data for this model was originally developed by Jesse D. Jenkins and Michael R. Davidson (last updated: October 3, 2022), where they coded the model optimization in Julia. This app transfers it to Python and adds some features to the model.

Users can import data as a CSV file, or they can use the default values provided in the model. The model uses Pyomo, with the GLPK solver to solve the optimization problem. In the end, the outputs are sent to the OpenAI API, which interprets them and provides the user with a short paragraph about the decision made by the model.

## Libraries Used

The app uses the following libraries:

- Streamlit for web development
- Pyomo for optimization
- Plotly for data visualization
- Pandas for data manipulation
- Numpy for numerical computation

## Contact

Created by Saeed Misaghian

- 📧 Email
- 🔗 GitHub
- 🔗 LinkedIn

## References

- Original Model Repository
