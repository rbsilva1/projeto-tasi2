import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

# Carregar dados
df = pd.read_csv('/data/climate_change_impact_on_agriculture_2024.csv')

app = dash.Dash(__name__)

@app.callback(
        
)
def update_graph(selected_dataset):
    return 

if __name__ == '__main__':
    app.run_server(port=5000, debug=True)