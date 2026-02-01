import numpy as np
import dash
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# ------------------------
# Funzione di calcolo
# ------------------------
def amount_1(X, q, r):
    list_am1 = []
    list_months = []
    s = 0
    Q = X * (1 + r)
    n = 1

    while Q >= q:
        Q = (Q - q) * (1 + r)
        n += 1
        list_months.append(n)
        s += q
        list_am1.append(s)

    list_am1.append(s + Q * (1 + r))
    list_months.append(n + 1)

    return list_am1, list_months


# ------------------------

# ------------------------
# Funzione di calcolo
# ------------------------
def amount_2(X, list_months, r,d):
    list_am2 = []

    Q = X*(1+r)
    
    for n in list_months:
  
      list_am2.append(-Q * (1 + r)**(n-1))
    
    list_am2.append(-Q * (1 + r)**(n))
    return list_am2, list_am2[-1]/(1+d/12)**list_months[-1]


# ------------------------




# App Dash
# ------------------------

app = dash.Dash(__name__)
app.title = "Andamento Rata/Debito"
server = app.server 

app.layout = html.Div(
    style={"width": "80%", "margin": "auto"},
    children=[

        html.H2("Dashboard Dash – Plot dinamici"),

        html.Label("Tasso annuo (%)"),
        dcc.Slider(
            id="a-slider",
            min=0.5,
            max=5,
            step=0.5,
            value=2,
            marks={i: f"{i}%" for i in range(1, 6)}
        ),

        html.Br(),

        html.Label("Rata"),
        dcc.Slider(
            id="b-slider",
            min=0,
            max=1000,
            step=50,
            value=150,
            marks={i: str(i) for i in range(0, 1001, 200)}
        ),

        html.Br(),

        html.Label("Capitale iniziale"),
        dcc.Slider(
            id="c-slider",
            min=1000,
            max=10000,
            step=500,
            value=8000,
            marks={i: str(i) for i in range(1000, 10001, 2000)}
        ),

        html.Br(),

        html.Label("Tasso di inflazione"),
        dcc.Slider(
           id="d-slider",
            min=0.5,
            max=3,
            step=0.5,
            value=1,
            marks={i: f"{i}%" for i in range(1, 6)}
        ),


        dcc.Graph(id="main-graph")
    ]
)

# ------------------------
# Callback
# ------------------------
@app.callback(
    Output("main-graph", "figure"),
    Input("a-slider", "value"),
    Input("b-slider", "value"),
    Input("c-slider", "value"),
    Input("d-slider", "value")
)
def update_graph(a, b, c,d):

    list_amount, list_months = amount_1(c, b, a / 1200)
    list_amount_1 = amount_2(c, list_months, a / 1200,d)[0]
    point_infl = amount_2(c, list_months, a / 1200,d / 100)[1]
  
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list_months,
            y=list_amount,
            mode="lines+markers",
            marker=dict(size=8),
            name="Capitale + interessi cumulato"
        )
    )


    fig.add_trace(
        go.Scatter(
            x=list_months,
            y=list_amount_1,
            mode="lines+markers",
            marker=dict(size=8),
            name="Debito cumulato"
        )
    )


    fig.add_trace(
        go.Scatter(
            x=list_months[-1],
            y=point_infl,
            mode="markers",           
            marker=dict(
                size=12,              
                color="red",           
                symbol="x"             
        ),
            name="Debito cumulato finale con potere di acquisto (inflazione)"
        )
    )

    fig.update_layout(
        title="Rata vs Scoperto cumulato a parità di periodo",
        xaxis_title="Mesi",
        yaxis_title="Importo cumulato",
        template="plotly_white",
        height=500
    )

    return fig


if __name__ == '__main__':
    app.run_server(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8050)),
        debug=True
    )
