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
    s = q
    Q = X * (1 + r)-q
    n = 1
    list_months.append(n)
    list_am1.append(s)

    while Q >= q:
        Q = (Q) * (1 + r) - q
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

    Q = X

    for n in list_months:

      list_am2.append(Q * (1 + r)**(n))

    return list_am2, list_am2[-1]/(1+d/12)**list_months[-1]


# ------------------------


def amount_3(q,list_months, r,d):
    list_am2 = []

    Q = 0

    for n in list_months:
      Q = (Q+q)*(1+r)
      list_am2.append(Q)

    return list_am2, list_am2[-1]/(1+d/12)**list_months[-1]


# ------------------------




def amount_4(q,m,list_months, r,dr,d):
    list_am2 = []

    Q = 0
    ii=0
    for n in list_months:
      if n % m==0 and r>dr:
        r=r-dr
      elif r<=dr:
        r=0.5/1200
      
      Q = (Q+q)*(1+r)
      list_am2.append(Q)

    return list_am2, list_am2[-1]/(1+d/12)**list_months[-1]


# ------------------------



# App Dash
# ------------------------

app = dash.Dash(__name__)

app.clientside_callback(
    """
    function(n) {
        if (typeof window === 'undefined') {
            return {'w': 1200, 'h': 800};
        }
        return {'w': window.innerWidth, 'h': window.innerHeight};
    }
    """,
    Output("viewport-store", "data"),
    Input("viewport-ping", "n_intervals"),
)

app.title = "Andamento Rata/Debito"
server = app.server 

app.layout = html.Div(
    style={"width": "80%", "margin": "auto", "padding": "24px", "backgroundColor": "#ffffff"},
    children=[

        html.H2("Dashboard Dash – Plot dinamici"),

        html.Label("Tasso annuo debito (%)"),
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
            min=50,
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

        html.Label("Tasso di inflazione per valutare debito rispetto potere di acquisto"),
        dcc.Slider(
           id="d-slider",
            min=0.5,
            max=3,
            step=0.5,
            value=1,
            marks={i: f"{i}%" for i in range(1, 6)}
        ),

        html.Br(),

        html.Label("Tasso Renumerazione"),
        dcc.Slider(
           id="e-slider",
            min=0.5,
            max=5,
            step=0.5,
            value=1,
            marks={i: f"{i}%" for i in range(1, 6)}
        ),


        html.Br(),

        html.Label("Numero di mesi di rotazione del tasso di renumerazione"),
        dcc.Slider(
            id="f-slider",
            min=3,
            max=12,
            step=3,
            value=3,
            marks={i: str(i) for i in range(2, 12, 3)}
        ),
        
        
        html.Br(),

        html.Label("Percentuale di sottrazione del tasso di renumerazione rispetto al periodo di rotazione"),
        dcc.Slider(
           id="g-slider",
            min=0.5,
            max=2,
            step=0.5,
            value=1,
            marks={i: f"{i}%" for i in [0.5, 1, 1.5, 2]}
        ),


        
        #dcc.Graph(
        #    id="summary-box"
        #),

        html.Div(id="summary-box", className="summary-wrap")
    ]
)

# ------------------------
# Callback
# ------------------------

@app.callback(
    Output("summary-box", "children"),
    Input("a-slider", "value"),
    Input("b-slider", "value"),
    Input("c-slider", "value"),
    Input("d-slider", "value"),
    Input("e-slider", "value"),
    Input("f-slider", "value"),
    Input("g-slider", "value"),
)
def update_graph(a, b, c, d, e, f, g):

    # ---------------------------
    # 1) CALCOLI (identici ai tuoi)
    # ---------------------------
    list_amount, list_months = amount_1(c, b, a / 1200)
    list_amount_1, point_infl = amount_2(c, list_months, a / 1200, d / 100)
    list_amount_2, point_infl1 = amount_3(b, list_months, a / 1200, d / 100)
    list_amount_4, point_infl2 = amount_4(b, f, list_months, a / 1200, g / 1200, d / 100)

    final_accumulo_rate        = list_amount[-1]
    final_debito_cumulato      = list_amount_1[-1]
    final_debito_cumulato_infl = point_infl
    final_capitale_cumulato    = list_amount_2[-1]
    final_capitale_cumulato_var= list_amount_4[-1]

    # ---------------------------
    # 2) FORMATTAZIONE NUMERI
    # ---------------------------
    def format_currency(x, symbol="€"):
        try:
            return f"{symbol} {x:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except:
            return f"{symbol} {x}"

    def fmt(x):
        return "—" if x is None else format_currency(x)

    # ---------------------------
    # 3) COLORI
    # ---------------------------
    color_months = "#adff2f"
    color_accumulo = "#60a5fa"
    color_debito = "#ef4444"
    color_pac = "#34d399"
    color_var = "#ffd700"

    # ---------------------------
    # 4) RETURN DELLA CARD HTML
    # ---------------------------
    return html.Div(
        [

            html.Div("Riepilogo", className="summary-title"),
            html.Div("Valori finali (ultimo punto di ciascuna serie)", className="summary-sub"),

            html.Div(
                [
                    html.Span(
                        f"Numero di mesi per estinzione (rata {fmt(b)})",
                        className="summary-label",
                        style={"color": color_months},
                    ),
                    html.Span(
                        f"{list_months[-1]}",
                        className="summary-value",
                        style={"color": color_months},
                    ),
                ],
                className="summary-row",
            ),

            html.Div(
                [
                    html.Span(
                        "Accumulo rate mensili per estinzione",
                        className="summary-label",
                        style={"color": color_accumulo},
                    ),
                    html.Span(
                        fmt(final_accumulo_rate),
                        className="summary-value",
                        style={"color": color_accumulo},
                    ),
                ],
                className="summary-row",
            ),

            html.Div(
                [
                    html.Span(
                        "Debito cumulato senza rate nello stesso periodo",
                        className="summary-label",
                        style={"color": color_debito},
                    ),
                    html.Span(
                        fmt(final_debito_cumulato),
                        className="summary-value",
                        style={"color": color_debito},
                    ),
                ],
                className="summary-row",
            ),

            html.Div(
                [
                    html.Span(
                        f"Debito cumulato normalizzato per inflazione {d}%",
                        className="summary-label",
                        style={"color": color_debito},
                    ),
                    html.Span(
                        fmt(final_debito_cumulato_infl),
                        className="summary-value",
                        style={"color": color_debito},
                    ),
                ],
                className="summary-row",
            ),

            html.Div(
                [
                    html.Span(
                        f"PAC (rata {fmt(b)}) remunerazione fissa {e}%",
                        className="summary-label",
                        style={"color": color_pac},
                    ),
                    html.Span(
                        fmt(final_capitale_cumulato),
                        className="summary-value",
                        style={"color": color_pac},
                    ),
                ],
                className="summary-row",
            ),

            html.Div(
                [
                    html.Span(
                        f"... normalizzato per inflazione {d}%",
                        className="summary-label",
                        style={"color": color_pac},
                    ),
                    html.Span(
                        fmt(point_infl1),
                        className="summary-value",
                        style={"color": color_pac},
                    ),
                ],
                className="summary-row",
            ),

            html.Div(
                [
                    html.Span(
                        f"PAC variabile {e}% annua − {g}% ogni {f} mesi con minimo di 0.5%",
                        className="summary-label",
                        style={"color": color_var},
                    ),
                    html.Span(
                        fmt(final_capitale_cumulato_var),
                        className="summary-value",
                        style={"color": color_var},
                    ),
                ],
                className="summary-row",
            ),

            html.Div(
                [
                    html.Span(
                        f"... normalizzato per inflazione {d}%",
                        className="summary-label",
                        style={"color": color_var},
                    ),
                    html.Span(
                        fmt(point_infl2),
                        className="summary-value",
                        style={"color": color_var},
                    ),
                ],
                className="summary-row",
            ),
        ],
        className="summary-card"
    )

  
   







if __name__ == '__main__':
    app.run_server(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8050)),
        debug=True
    )
