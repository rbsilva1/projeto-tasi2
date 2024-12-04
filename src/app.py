import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px


# Carregar dados
df = pd.read_csv('data/climate_change_impact_on_agriculture_2024.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Dashboard de Dados Agrícolas", className="text-center mb-4"), width=12)
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="scatterplot"), width=6),
                dbc.Col(dcc.Graph(id="linechart"), width=6),
            ],
            className="mb-4",
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="worldmap"), width=12),
        ),
    ],
    fluid=True,
)

@app.callback(
    Output("scatterplot", "figure"),
    Input("scatterplot", "id")
)
def update_scatterplot(_):
    fig = px.scatter(
        df,
        x="Average_Temperature_C",
        y="Crop_Yield_MT_per_HA",
        color="Crop_Type",
        size="CO2_Emissions_MT",
        hover_data=["Country", "Region"],
        title="Temperatura Média vs. Rendimento Agrícola",
    )
    return fig

@app.callback(
    Output("linechart", "figure"),
    Input("linechart", "id")
)
def update_linechart(_):
    fig = px.line(
        df,
        x="Year",
        y="Economic_Impact_Million_USD",
        color="Country",
        markers=True,
        title="Impacto Econômico ao Longo dos Anos",
    )
    return fig

@app.callback(
    Output("worldmap", "figure"),
    Input("worldmap", "id")
)
def update_worldmap(_):
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Soil_Health_Index",
        hover_name="Country",
        title="Índice de Saúde do Solo por País",
        color_continuous_scale="Viridis",
    )
    return fig

# Executa o aplicativo
if __name__ == "__main__":
    app.run_server(debug=True)

