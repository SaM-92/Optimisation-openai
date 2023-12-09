import plotly.graph_objects as go

def time_series_plot(df,name):
        # Create a line plot for each column in the DataFrame
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_day_of_interest.index, y=df.name, name=name
        )
    )

