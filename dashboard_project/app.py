import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from db import (
    connect_database, 
    get_cities, 
    get_city_profit,
    get_city_profit_per_year, 
    DB_PATH)

# DuckDB-Verbindung herstellen
con = connect_database(DB_PATH)

# Grundgerüst des Dashboards
app = dash.Dash(__name__)

# Alle Städte laden
cities_df = get_cities(con)
cities = sorted(cities_df["City"].dropna().unique())
con.close()

app.layout = html.Div([
    html.H1("City Profit Dashboard", style={"textAlign": "center"}),

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


@app.callback(
    Output("count-by-year", "figure"),
    Input("city-dropdown", "value")
)
def update_year_chart(selected_city):
    if not selected_city:
        return px.bar(title="No city selected")

    try:
        con = connect_database(DB_PATH)
        df = get_city_profit_per_year(selected_city, con)

        fig = px.bar(
            df,
            x="Year",
            y="Sales",
            title=f"Total Service per Year for {selected_city}"
        )

        fig.update_layout(xaxis_tickangle=-45)
    finally:
        con.close()

    return fig

@app.callback(
    Output("profit-chart", "figure"),
    Input("city-dropdown", "value")
)
def update_chart(selected_city):
    if not selected_city:
        return px.bar(title="No city selected")

    try:
        con = connect_database(DB_PATH)
        df = get_city_profit(selected_city, con)

        fig = px.bar(
            df,
            x="servicename",
            y="total_costs",
            title=f"Total Service Costs for {selected_city}",
            labels={"total_costs": "Total Revenue", "servicename": "Service"}
        )

        fig.update_layout(xaxis_tickangle=-45)
    finally:
        con.close()

    return fig


if __name__ == "__main__":
    app.run(debug=True)
