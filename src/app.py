import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_csv('src/data/climate_change_impact_on_agriculture_2024.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Obter a lista de países únicos
unique_countries = df["Country"].unique()
unique_countries.sort()

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Dashboard de Dados Agrícolas", className="text-center mb-4"), width=12)
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="country-filter",
                    options=[{"label": country, "value": country} for country in unique_countries],
                    multi=True,
                    placeholder="Selecione o(s) país(es)...",
                ),
                width=12
            ),
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="scatterplot"), width=6),
                dbc.Col(dcc.Graph(id="linechart"), width=6),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="worldmap"), width=12),
            ],
            className="mb-4",
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="average-graph"), width=12),
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="media-anual"), width=12)
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="irrigacao_fertilizante"), width=12)
        ),
    ],
    fluid=True,
)
@app.callback(
    Output("irrigacao_fertilizante","figure"),  
    Input("country-filter","value")
)

def update_irrigacao_fertilizante(selected_countries):
    # Filtrar os dados se países forem selecionados
    filtered_df = df if not selected_countries else df[df["Country"].isin(selected_countries)]

    # Agrupar dados por país e calcular a média de acesso à irrigação e uso de fertilizantes
    grouped_df = filtered_df.groupby('Country')[['Irrigation_Access_%', 'Fertilizer_Use_KG_per_HA']].mean().reset_index()

    # Criar um gráfico de dispersão para analisar o uso de irrigação e fertilizantes por país
    fig = px.scatter(
        grouped_df,
        x='Irrigation_Access_%',
        y='Fertilizer_Use_KG_per_HA',
        text='Country',
        title="Distribuição Global do Uso de Irrigação e Fertilizantes por País",
        labels={'Irrigation_Access_%': 'Acesso à Irrigação (%)', 'Fertilizer_Use_KG_per_HA': 'Uso de Fertilizantes (KG/HA)'}
    )

    # Ajustes no layout
    fig.update_traces(marker=dict(size=12, color='green'), textposition='top center')
    fig.update_layout(
        xaxis=dict(title='Acesso à Irrigação (%)'),
        yaxis=dict(title='Uso de Fertilizantes (KG/HA)')
    )
    return fig

@app.callback(
    Output("media-anual","figure"),  
    Input("country-filter","value")
)
def update_media_anual(selected_countries):
    # Filtrar os dados se países forem selecionados
    filtered_df = df if not selected_countries else df[df["Country"].isin(selected_countries)]
    
    # Agrupar os dados por ano e tipo de colheita, calculando a média do uso de pesticidas
    filtered_df = filtered_df.groupby(['Year', 'Crop_Type']).agg(
        Pesticide_Use_KG_per_HA=('Pesticide_Use_KG_per_HA', 'mean')
    ).reset_index()

    # Criar o gráfico de linha
    fig = px.line(
        filtered_df,
        x="Year",
        y="Pesticide_Use_KG_per_HA",
        color="Crop_Type",
        markers=True,
        title="Média Anual de Uso de Pesticidas por Tipo de Colheita",
        labels={
            "Pesticide_Use_KG_per_HA": "Uso Médio de Pesticidas (KG/HA)",
            "Year": "Ano"
        }
    )

    # Atualizar o layout do gráfico
    fig.update_layout(
        xaxis=dict(dtick=1),  # Mostra cada ano no eixo X
        yaxis_title="Uso Médio de Pesticidas (KG/HA)",
        legend_title_text="Tipo de Colheita"
    )

    return fig

@app.callback(
    Output("average-graph", "figure"),
    Input("country-filter", "value")
)
def update_average_graph(selected_countries):
    filtered_df = df if not selected_countries else df[df["Country"].isin(selected_countries)]
    
    # Agrupar dados
    df_grouped = filtered_df.groupby('Country').agg({
        'Pesticide_Use_KG_per_HA': 'mean',  # Média do uso de pesticidas
        'Crop_Yield_MT_per_HA': 'mean'     # Média do rendimento agrícola
    }).reset_index()
    
    # Gráfico de dispersão
    fig = px.scatter(
        df_grouped,
        x='Pesticide_Use_KG_per_HA',
        y='Crop_Yield_MT_per_HA',
        color='Country',
        title="Uso de Pesticidas vs Rendimento Médio da Colheita por País",
        labels={
            'Pesticide_Use_KG_per_HA': 'Uso Médio de Pesticidas (KG/HA)',
            'Crop_Yield_MT_per_HA': 'Rendimento Médio da Colheita (MT/HA)'
        },
        template='plotly'
    )
    return fig

@app.callback(
    Output("scatterplot", "figure"),
    Input("country-filter", "value")
)
def update_scatterplot(selected_countries):
    filtered_df = df if not selected_countries else df[df["Country"].isin(selected_countries)]
    fig = px.scatter(
        filtered_df,
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
    Input("country-filter", "value")
)
def update_linechart(selected_countries: list):
    # Filtrar o DataFrame com base nos países selecionados
    if selected_countries:
        filtered_df = df[df["Country"].isin(selected_countries)]
    else:
        filtered_df = df

    # Agrupar os dados por País e Ano para evitar duplicados
    aggregated_df = filtered_df.groupby(["Country", "Year"], as_index=False).sum()

    # Criar o gráfico de linhas
    fig = px.line(
        aggregated_df,
        x="Year",
        y="Economic_Impact_Million_USD",
        color="Country",
        markers=True,
        title="Impacto Econômico ao Longo dos Anos",
        labels={
            "Economic_Impact_Million_USD": "Impacto Econômico (Milhões de Dólares)",
            "Year": "Ano",
            "Country": "País"
        }
    )

    # Melhorar o layout do gráfico
    fig.update_layout(
        title={
            "text": "Impacto Econômico ao Longo dos Anos",
            "x": 0.5,  # Centralizar o título
            "xanchor": "center"
        },
        xaxis_title="Ano",
        yaxis_title="Impacto Econômico (Milhões de Dólares)",
        legend_title="País",
        template="plotly_white"  # Tema mais limpo e profissional
    )

    # Adicionar personalizações para as linhas e pontos
    fig.update_traces(line_shape="spline",  # Suavizar as linhas
                      mode="lines+markers")  # Exibir linhas e marcadores

    return fig

@app.callback(
    Output("worldmap", "figure"),
    Input("country-filter", "value")
)
def update_worldmap(selected_countries):
    filtered_df = df if not selected_countries else df[df["Country"].isin(selected_countries)]
    fig = px.choropleth(
        filtered_df,
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
