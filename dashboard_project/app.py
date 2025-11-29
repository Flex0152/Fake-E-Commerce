import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from db import (
    connect_database, 
    get_cities, 
    get_city_profit,
    get_city_profit_per_year)
from pathlib import Path

# DB Path
DB_PATH = Path(".").parent / "data" / "warehouse.duckdb"

# Grundgerüst des Dashboards
app = dash.Dash(__name__)

def total_overview_orders():
    # Welcher Service ist der beliebteste?
    query = """
    SELECT 
    count(s.service_id) as in_total,
    s.Servicename
    FROM 
    tblOrders o
    JOIN tblServices s ON o.service_id = s.service_id
    GROUP BY o.service_id, s.Servicename
    ORDER BY in_total desc
    """
    with connect_database(DB_PATH) as con:
        df = con.execute(query).df()
        fig = px.pie(df, values='in_total', names='Servicename')
    return fig

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

# Alle Städte laden
cities_df = get_cities(DB_PATH)
cities = sorted(cities_df["City"].dropna().unique())

# Statisches Pie Chart
overview_fig = total_overview_orders()

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
