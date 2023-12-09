import plotly.graph_objects as go
import streamlit as st  # web development
import numpy as np

def time_series_plot(df,name):
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df.loc[:,name], name=name
        )
    )
    fig.update_layout(
        title={'text': f"Time Series of {name}", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
        xaxis_title='Time',
        yaxis_title=f'{name}'
)
    st.plotly_chart(fig,use_container_width=True)

def plot_cumulative_distribution(demand):
    cumulative_distribution = np.linspace(0.,1.,len(demand))
    demand_ = demand.sort_values(by='Demand')
    demand_ = demand_.reset_index(drop=True)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=demand_['Demand'], y=cumulative_distribution, mode='lines',line=dict(width=2,color='red')))
    fig2.update_layout(
        title={'text':'Load duration as cumulative distribution','y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
        xaxis_title='Demand',
        yaxis_title='Cumulative Distribution'
    )
    st.plotly_chart(fig2,use_container_width=True)
