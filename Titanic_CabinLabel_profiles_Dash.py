import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the dataset
myTitanic_dataset = 'https://raw.githubusercontent.com/praoiticica/Titanic-traditional-ML/main/titanic_datasets/titanic_cleaned.csv'
df = pd.read_csv(myTitanic_dataset)
# Define the cabin labels available in the dataset
cabin_labels = df['Cabin_label'].unique()

# Create the Dash application
app = dash.Dash(__name__)
server = app.server

# Define the layout of the Dash application
app.layout = html.Div([
    dcc.Dropdown(
        id='cabin-dropdown',
        options=[{'label': label, 'value': label} for label in cabin_labels],
        value=cabin_labels[0]
    ),
    dcc.Graph(id='bar-graph')
])

# Define the callback function to update the graph based on the selected cabin label
@app.callback(
    dash.dependencies.Output('bar-graph', 'figure'),
    [dash.dependencies.Input('cabin-dropdown', 'value')]
)
def update_graph(cabin_label):
    # Filter the DataFrame for passengers with the selected cabin label
    cabin_passengers = df[df['Cabin_label'] == cabin_label]

    # Create subplots
    fig = make_subplots(rows=2, cols=4,
                        vertical_spacing=0.15,
                        horizontal_spacing=0.05,
                        subplot_titles=[
                            'Passenger Class',
                            'Sex',
                            'Fare_level',
                            'Age_group',
                            'Embarked',
                            'FamilySize',
                            'Companions',
                            'Titles'
                        ]
                       )

    # Define the column names and subplot indices
    column_names = ['Pclass', 'Sex', 'Fare_level', 'Age_group', 'Embarked', 'FamilySize', 'Companions', 'Title']
    subplot_indices = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4)]

    # Add traces for each column
    for i, column in enumerate(column_names):
        row, col = subplot_indices[i]
        counts = cabin_passengers[column].value_counts()
        max_count = counts.max()

        fig.add_trace(
            go.Bar(x=counts.index, y=counts.values, text=counts.values, textposition='outside', width=0.9),
            row=row, col=col
        )

        # Update x-axis and y-axis titles
        fig.update_xaxes(title=column, row=row, col=col)
        fig.update_yaxes(title='Counts', row=row, col=col, title_standoff=0.1)
        fig.update_traces(textfont={'size': 15}, row=row, col=col)

        # Calculate the y-axis range with a small margin
        y_range = [0, max_count * 1.12]  # Adjust the margin as desired
        fig.update_yaxes(range=y_range, row=row, col=col)

    # Update subplot size and spacing
    fig.update_layout(
        title='Variables distributions for passengers of the Cabin {}'.format(cabin_label),
        height=700, width=1500, showlegend=False,
        plot_bgcolor='white', paper_bgcolor='white',
    )

    # Set x-axis tickmode to 'linear' and dtick to 1 to show all tick values
    fig.update_xaxes(tickmode='linear', dtick=1)

    # Update subplot axis options
    for row in range(1, 3):
        for col in range(1, 5):
            fig.update_xaxes(showline=True, mirror=True, linecolor='black', row=row, col=col)
            fig.update_yaxes(showline=True, mirror=True, linecolor='black', row=row, col=col)

    return fig

# Run the Dash application
if __name__ == '__main__':
    app.run_server(port = 8053, debug = False)