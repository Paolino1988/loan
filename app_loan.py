import numpy as np
import dash
from dash import Dash, dash_table, dcc, html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import os

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

      if n % m==0:
        if r>dr and r-dr>=0.5/1200:
          r=r-dr
        else:
          r=0.5/1200
   
      Q = (Q+q)*(1+r)
      list_am2.append(Q)

    return list_am2, list_am2[-1]/(1+d/12)**list_months[-1]


# ------------------------



## ------------------ rata mutuo ----------------------- ##

def amount_mutuo(X,r,mm):
    i = r/12
    M = mm*12
    q_f = (X*i*(1+i)**M)/((1+i)**M-1)
    I_f = q_f*M - X

    I_i = X*i*(M-1)/2
    q_i_c = X/M
    q_i_0 = q_i_c + X*i
    q_i_f = q_i_c + X/M*i
    q_i_m = q_i_c + I_i/M

    return q_f, I_f, I_i, q_i_0, q_i_f, q_i_m


##--------------------------------------------------


## ------------------ ratio capitale/Interesse ----------------------- ##

def ratio_mutuo(X,r,mm):
    i = r/12
    M = mm*12
    q_f = (X*i*(1+i)**M)/((1+i)**M-1)
    list_interessi_f=[X*i]
    list_capitale_f = [0]
    list_interessi_i = [X*i]
    list_capitale_i = [0]
    list_ratio = []
    X_f = X
    X_i = X
    for k in range(1,M):
        X_f=(X_f*(1+i)-q_f)
        list_interessi_f.append(X_f*i)
        list_capitale_f.append(q_f-X_f*i)

        X_i = X_i*(1-k/M)
        list_interessi_i.append(X_i*i)
        list_capitale_i.append(X_i)
        list_ratio.append((X_i*i)*100/(X_i/M+X_i*i))

    
    return [ (x/q_f)*100 for x in list_interessi_f],  list_ratio[0]


##--------------------------------------------------









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
        dcc.Store(id="viewport-store"),
        dcc.Interval(id="viewport-ping", interval=1000),
        
        html.H2("Dashboard Dash – Plot dinamici"),

        html.H1("Fido/Scoperti"),

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
            marks={i: str(i) for i in range(1000, 10002, 1000)}
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
            marks={i: str(i) for i in [3,6,9,12]}
        ),
        
        
        html.Br(),

        html.Label("Percentuale di sottrazione del tasso di renumerazione rispetto al periodo di rotazione"),
        dcc.Slider(
           id="g-slider",
            min=0.25,
            max=2,
            step=0.25,
            value=1,
            marks={i: f"{i}%" for i in [0.25,0.5,0.75 ,1,1.25, 1.5,1.75, 2]}
        ),


        
        #dcc.Graph(
        #    id="summary-box"
        #),

        html.Div(id="summary-box", className="summary-wrap"),

        html.Br(),
        
        html.H1("Mutuo"),

        html.Br(),

        html.Label("Capitale (keuro)"),
        dcc.Input(
            id="x-input",
            type="number",
            value=100,
            min=50,
            step=1,
            style={"marginBottom": "20px"}
        ),
        
        html.Br(),

        html.Label("Numero di anni di Mutuo"),
        dcc.Slider(
            id="y-input",
            min=5,
            max=40,
            step=1,
            value=10,
            marks={i: str(i) for i in [j for j in range(5,41,5)]}
        ),

        html.Br(),

        html.Label("Tasso annuo (%)"),
        dcc.Slider(
            id="z-input",
            min=0.0,
            max=5,
            step=0.25,
            value=2,
            marks={i: f"{i}%" for i in [j/100 for j in range(0,505,50)]}
        ),


        html.Div(id="summary-box-mutuo", className="summary-wrap"),

        html.Br(),
        
        html.Div(id="percent-table-container")
        
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
def update_fido(a, b, c, d, e, f, g):

    # ---------------------------
    # 1) CALCOLI (identici ai tuoi)
    # ---------------------------
    list_amount, list_months = amount_1(c, b, a / 1200)
    list_amount_1, point_infl = amount_2(c, list_months, a / 1200, d / 100)
    list_amount_2, point_infl1 = amount_3(b, list_months, e / 1200, d / 100)
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






@app.callback(
    Output("summary-box-mutuo", "children"),
    Input("x-input", "value"),
    Input("z-input", "value"),
    Input("y-input", "value")
)
def update_mutuo(x,z,y):

    # ---------------------------
    # 1) CALCOLI (identici ai tuoi)
    # ---------------------------
    list_result = amount_mutuo(1000*x,z/100,y)
    
    q_f = list_result[0]
    I_f = list_result[1]
    I_i = list_result[2]
    q_i_0 = list_result[3]    
    q_i_f = list_result[4]
    q_i_m = list_result[5]

    perc_inter = ratio_mutuo(1000*x,z/100,y)[1]

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
    color_rata_fr = "#adff2f"
    color_interessi_fr = "#60a5fa"
    color_interessi_ita = "#ef4444"
    color_rata_it_0 = "#34d399"
    color_rata_it_f = "#ffd700"
    color_rata_it_m = "#8a2be2"
    col_ratio_mutuo = "#daa520"

    # ---------------------------
    # 4) RETURN DELLA CARD HTML
    # ---------------------------
    


    return html.Div(
        [

            html.Div("Riepilogo Mutuo", className="summary-title"),

            html.Div(
                [
                    html.Span(
                        f"Rata con Ammortamento Francese per numero mesi {y*12}",
                        className="summary-label",
                        style={"color": color_rata_fr},
                    ),
                    html.Span(
                        fmt(q_f),
                        className="summary-value",
                        style={"color": color_rata_fr},
                    ),
                ],
                className="summary-row",
            ),

            html.Div(
                [
                    html.Span(
                        f"Interessi totali con Ammortamento Francese con APR {z}%",
                        className="summary-label",
                        style={"color": color_interessi_fr},
                    ),
                    html.Span(
                        fmt(I_f),
                        className="summary-value",
                        style={"color": color_interessi_fr},
                    ),
                ],
                className="summary-row",
            ),

            html.Div(
                [
                    html.Span(
                        f"Interessi totali con Ammortamento Italiano con APR {z}%",
                        className="summary-label",
                        style={"color": color_interessi_ita},
                    ),
                    html.Span(
                        fmt(I_i),
                        className="summary-value",
                        style={"color": color_interessi_ita},
                    ),
                ],
                className="summary-row",
            ),

            html.Div(
                [
                    html.Span(
                        f"Prima rata con Ammortamento Italiano (rata massima) per numero mesi {y*12}",
                        className="summary-label",
                        style={"color": color_rata_it_0},
                    ),
                    html.Span(
                        fmt(q_i_0),
                        className="summary-value",
                        style={"color": color_rata_it_0},
                    ),
                ],
                className="summary-row",
            ),

            html.Div(
                [
                    html.Span(
                        f"...ultima rata con Ammortamento Italiano (rata minima)",
                        className="summary-label",
                        style={"color": color_rata_it_f},
                    ),
                    html.Span(
                        fmt(q_i_f),
                        className="summary-value",
                        style={"color": color_rata_it_f},
                    ),
                ],
                className="summary-row",
            ),


            html.Div(
                [
                    html.Span(
                        f"...Rata Media con Ammortamento Italiano",
                        className="summary-label",
                        style={"color": color_rata_it_m},
                    ),
                    html.Span(
                        fmt(q_i_m),
                        className="summary-value",
                        style={"color": color_rata_it_m},
                    ),
                ],
                className="summary-row",
            ),
        
            html.Div(
                [
                    html.Span(
                        "Percentuale di interesse su ogni rata per ammortamento Italiano",
                        className="summary-label",
                        style={"color": col_ratio_mutuo},
                    ),
                    html.Span(
                        f"{round(perc_inter,2)}%",
                        className="summary-value",
                        style={"color": col_ratio_mutuo},
                    ),
                ],
                className="summary-row",
            ),
        ],
        className="summary-card"
    )








@app.callback(
    Output("percent-table-container", "children"),
    Input("x-input", "value"),
    Input("z-input", "value"),
    Input("y-input", "value")
)
def update_graph(x, z, y):

    # ---------------------------
    # 1) CALCOLI
    # ---------------------------
    list_perc = ratio_mutuo(1000 * x, z / 100, y)[0]
    months = list(range(1, len(list_perc) + 1))

    data = [
        {
            "Mese": m,
            "Percentuale di interesse su rata (%)": round(p, 2)
        }
        for m, p in zip(months, list_perc)
    ]

    table = dash_table.DataTable(
        data=data,
        columns=[
            {"name": "Mese", "id": "Mese"},
            {"name": "Percentuale di interesse su rata (%)", "id": "Percentuale di interesse su rata (%)"},
        ],
        fixed_rows={"headers": True},
        style_table={
            "height": "350px",          
            "overflowY": "auto",       
            "border": "1px solid #ddd",
        },
        style_cell={
            "textAlign": "center",
            "padding": "8px",
            "fontFamily": "Arial",
            "fontSize": "14px",
            },
        style_cell_conditional=[
            {
                "if": {"column_id": "mese"},
                "width": "80px",
                "maxWidth": "80px",
                "minWidth": "80px",
            },
            {
                "if": {"column_id": "percentuale"},
                "width": "140px",
            },
        ],
        
        style_header={
            "backgroundColor": "#f3f4f6",
            "fontWeight": "bold",
            "borderBottom": "2px solid #d1d5db",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#fafafa",
            }
        ],
    )

    return html.Div(
    [
        html.H4(
            "Andamento percentuale degli interessi nel tempo",
            style={
                "marginBottom": "10px",
                "textAlign": "center",
                "color": "#374151",
            },
        ),
        table,
    ],
    style={
        "backgroundColor": "white",
        "padding": "12px",
        "borderRadius": "10px",
        "boxShadow": "0 4px 12px rgba(0,0,0,0.05)",
    },
)



    







if __name__ == '__main__':
    app.run_server(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8050)),
        debug=True
    )
