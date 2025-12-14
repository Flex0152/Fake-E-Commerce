import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from db import DuckDBManager
from pathlib import Path


# DB
DB_PATH = Path(".").parent / "data" / "warehouse.duckdb"
DATA_PATH = Path(".").parent / "data" / "example.csv"
db = DuckDBManager(DB_PATH, DATA_PATH)
db.create_table()

# Grundgerüst des Dashboards
app = dash.Dash(__name__)

def total_overview_orders_fig():
    # Welcher Service ist der beliebteste?
    df = db.total_overview_orders()
    fig = px.pie(df, values='in_total', names='Servicename')
    return fig

@app.callback(
    Output("count-by-year", "figure"),
    Input("city-dropdown", "value")
)
def update_year_chart(selected_city):
    if not selected_city:
        return px.bar(title="No city selected")

    df = db.get_city_profit_per_year(selected_city)

    fig = px.bar(
        df,
        x="Year",
        y="Sales",
        title=f"Total Service per Year for {selected_city}"
    )

    fig.update_layout(xaxis_tickangle=-45)
    return fig

@app.callback(
    Output("profit-chart", "figure"),
    Input("city-dropdown", "value")
)
def update_chart(selected_city):
    if not selected_city:
        return px.bar(title="No city selected")

    df = db.get_city_profit(selected_city)

    fig = px.bar(
        df,
        x="servicename",
        y="total_costs",
        title=f"Total Service Costs for {selected_city}",
        labels={"total_costs": "Total Revenue", "servicename": "Service"}
    )

    fig.update_layout(xaxis_tickangle=-45)
    return fig


# Alle Städte laden
cities_df = db.get_cities()
cities = sorted(cities_df["City"].dropna().unique())

# Statisches Pie Chart
overview_fig = total_overview_orders_fig()

app.layout = html.Div([
    html.H1("Profit Dashboard", style={"textAlign": "center"}),
    html.Div(
        [
            dcc.Graph(id="total_overview", figure=overview_fig)
        ]
    ),

    html.Div([
        html.Label("Choose a city:"),
        dcc.Dropdown(
            id="city-dropdown",
            options=[{"label": c, "value": c} for c in cities],
            value=cities[0] if cities else None,
            clearable=False
        )
    ], style={"width": "30%", "margin": "auto"}),
    
    dcc.Graph(id="profit-chart"),
    dcc.Graph(id="count-by-year"),
])


if __name__ == "__main__":
    app.run(debug=True)
