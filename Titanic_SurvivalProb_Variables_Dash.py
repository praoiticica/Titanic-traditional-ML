import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output

# Create the Dash application
app = dash.Dash(__name__)
server = app.server

# Load the dataset
df = pd.read_csv('titanic_datasets/titanic_cleaned.csv')  # Replace 'your_dataset.csv' with your actual dataset file

# Define the layout of the web application
app.layout = html.Div([
    html.H1('Interactive Plot'),
    html.Label('Select Variable:'),
    dcc.Dropdown(
        id='variable-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='Pclass'
    ),
    dcc.Graph(id='plot')
])

# Define the callback function to update the plot
@app.callback(
    Output('plot', 'figure'),
    [Input('variable-dropdown', 'value')]
)
def update_plot(variable):
    # Calculate the counts
    counts = df[variable].value_counts()
    
    # Calculate the probability of survival
    survived = df[df['Survived'] == 1][variable].value_counts().sort_index()
    not_survived = df[df['Survived'] == 0][variable].value_counts().sort_index()
    survival_prob = survived / (survived + not_survived)

    # Create subplots with shared x-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])   
    
    # Add a scatter trace for survival probability
    fig.add_trace(go.Scatter(x=survival_prob.index, y=survival_prob.values, mode='markers+lines', name='Survival Probability', marker_color='red'), secondary_y=False)
    # Add a bar trace for counts
    fig.add_trace(go.Bar(x=counts.index, y=counts.values, name='Counts', width=0.4, opacity=0.4, marker_color='royalblue'), secondary_y=True)
    
    # Set layout 
    fig.update_layout(
        title='Count and Survival Probability',
        height=600,
        width=900,
        font=dict(family="Sans serif", size=20),
        xaxis=dict(
            showline=True, linewidth=2, linecolor='black', mirror=True,
            showgrid=False, ticks='outside',
        ),
        yaxis=dict(
            title_text="Survival Probability",
            showline=True, linewidth=2, linecolor='black', mirror=True,
            showgrid=False,
            ticks='outside',
            tickfont=dict(color='red')
        ),
        yaxis2=dict(
            title_text="Counts",
            ticks='outside',
            tickfont=dict(color='blue')
        )
    )

    return fig

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
