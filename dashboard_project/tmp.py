from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Beispieldaten
df = pd.DataFrame({
    'Jahr': [2020, 2021, 2022, 2023, 2024],
    'Umsatz': [100, 150, 180, 220, 250],
    'Kosten': [80, 100, 120, 140, 160]
})

# App initialisieren
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1('Dashboard mit mehreren Callbacks'),
    
    # Dropdown als gemeinsamer Input
    html.Label('Wähle eine Metrik:'),
    dcc.Dropdown(
        id='metrik-dropdown',
        options=[
            {'label': 'Umsatz', 'value': 'Umsatz'},
            {'label': 'Kosten', 'value': 'Kosten'}
        ],
        value='Umsatz'
    ),
    
    html.Br(),
    
    # Erste Komponente - Graph
    html.Div([
        html.H3('Zeitreihen-Graph'),
        dcc.Graph(id='zeitreihen-graph')
    ]),
    
    # Zweite Komponente - Statistik-Karten
    html.Div([
        html.H3('Statistiken'),
        html.Div(id='statistik-karten', style={'display': 'flex', 'gap': '20px'})
    ]),
    
    # Dritte Komponente - Textausgabe
    html.Div([
        html.H3('Analyse'),
        html.Div(id='text-ausgabe')
    ])
])

# Callback 1: Update Graph
@callback(
    Output('zeitreihen-graph', 'figure'),
    Input('metrik-dropdown', 'value')
)
def update_graph(ausgewaehlte_metrik):
    fig = px.line(
        df, 
        x='Jahr', 
        y=ausgewaehlte_metrik,
        title=f'{ausgewaehlte_metrik} über die Jahre',
        markers=True
    )
    fig.update_layout(
        xaxis_title='Jahr',
        yaxis_title=ausgewaehlte_metrik
    )
    return fig

# Callback 2: Update Statistik-Karten
@callback(
    Output('statistik-karten', 'children'),
    Input('metrik-dropdown', 'value')
)
def update_statistiken(ausgewaehlte_metrik):
    daten = df[ausgewaehlte_metrik]
    
    karten = [
        html.Div([
            html.H4('Durchschnitt'),
            html.P(f'{daten.mean():.2f}')
        ], style={'padding': '20px', 'backgroundColor': '#f0f0f0', 'borderRadius': '5px'}),
        
        html.Div([
            html.H4('Maximum'),
            html.P(f'{daten.max():.2f}')
        ], style={'padding': '20px', 'backgroundColor': '#f0f0f0', 'borderRadius': '5px'}),
        
        html.Div([
            html.H4('Minimum'),
            html.P(f'{daten.min():.2f}')
        ], style={'padding': '20px', 'backgroundColor': '#f0f0f0', 'borderRadius': '5px'})
    ]
    
    return karten

# Callback 3: Update Textausgabe
@callback(
    Output('text-ausgabe', 'children'),
    Input('metrik-dropdown', 'value')
)
def update_text(ausgewaehlte_metrik):
    daten = df[ausgewaehlte_metrik]
    wachstum = ((daten.iloc[-1] - daten.iloc[0]) / daten.iloc[0]) * 100
    
    return html.Div([
        html.P(f'Die ausgewählte Metrik ist: {ausgewaehlte_metrik}'),
        html.P(f'Gesamtwachstum: {wachstum:.2f}%'),
        html.P(f'Anzahl Datenpunkte: {len(daten)}')
    ])

# App starten
if __name__ == '__main__':
    app.run(debug=True)