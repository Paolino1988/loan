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




def amount_4(q,m,list_months, r,dr,r_min,d):
    list_am2 = []

    Q = 0
    ii=0
    for n in list_months:
      if n % m==0 and r>dr:
        r=r-dr
      elif r<=dr:
        r=r_min
      
      Q = (Q+q)*(1+r)
      list_am2.append(Q)

    return list_am2, list_am2[-1]/(1+d/12)**list_months[-1]


# ------------------------



# App Dash
# ------------------------

app = dash.Dash(__name__)
app.title = "Andamento Rata/Debito"
server = app.server 

app.layout = html.Div(
    style={"width": "80%", "margin": "auto", "padding": "24px", "backgroundColor": "#0f172a"},
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




      dcc.Graph(id = "summary-box") 
    ]
)

# ------------------------
# Callback
# ------------------------
@app.callback(
    Output("summary-box", "figure"),
    Input("a-slider", "value"),
    Input("b-slider", "value"),
    Input("c-slider", "value"),
    Input("d-slider", "value"),
    Input("e-slider", "value")
)
def update_graph(a, b, c,d,e,f,g):

    list_amount = amount_1(c, b, a / 1200)[0]
    list_months = amount_1(c, b, a / 1200)[1]
    list_amount_1 = amount_2(c, list_months, a / 1200, d / 100)[0]
    point_infl = amount_2(c, list_months, a / 1200, d / 100)[1]
    
    list_amount_2, point_infl1 = amount_3(b, list_months, a/1200, e/1200 )
    list_amount_4, point_infl2 = amount_4(b, f, list_months, a/1200, g/1200, e / 100)
  

    
    
    final_accumulo_rate = list_amount[-1] if list_amount else None
    final_debito_cumulato = list_amount_1[-1] if list_amount_1 else None
    final_debito_cumulato_infl = point_infl
    final_capitale_cumulato = list_amount_2[-1] if list_amount_2 else None
    final_capitale_cumulato_var = list_amount_4[-1] if list_amount_4 else None
    
    
    
    def format_currency(x, symbol="€"):
        # formattazione compatta: separatore migliaia, zero decimali
        try:
            return f"{symbol} {x:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            return f"{symbol} {x}"
    
    
    def fmt(x): return format_currency(x)
    
    text = (
          f"<b>Riepilogo</b><br><br>"
          f"<span style='color:	#adff2f'>Numero di Mesi per estinzione rispetto alla Rata fissata di {fmt(200)}</span>: <b>{list_months[-1]}</b><br>"
          f"<span style='color:#60a5fa'>Accumulo rate mensili per estinzione</span>: <b>{fmt(final_accumulo_rate)}</b><br>"
          f"<span style='color:#ef4444'>Debito cumulato senza rate nello stesso periodo</span>: <b>{fmt(final_debito_cumulato)}</b><br>"
          f"<span style='color:#ef4444'>Debito cumulato normalizzato per potere di acquisto inflazionato del {c}% annuo</span>: <b>{fmt(final_debito_cumulato_infl)}</b><br>"
          f"<span style='color:#34d399'>Capitale cumulato valutando un PAC pari alla rata di {fmt(200)} con remunerazione fissa del 3% </span>: <b>{fmt(final_capitale_cumulato)}</b><br>"
          f"<span style='color:#34d399'>_____ per potere di acquisto inflazionato del {c}% annuo</span>: <b>{fmt(point_infl1)}</b><br>"
          f"<span style='color:#ffd700'>Capitale cumulato valutando un PAC pari alla rata di {fmt(200)} con remunerazione fissa del 3% variabile ogni 6 mesi diminuito del 1% </span>: <b>{fmt(final_capitale_cumulato_var)}</b><br>"
          f"<span style='color:#ffd700'>_____ per potere di acquisto inflazionato del {c}% annuo</span>: <b>{fmt(point_infl2)}</b>"
     
     )
    
    fig = go.Figure()
    # nasconde assi e griglia, sfondo scuro elegante
    fig.update_layout(
        template="plotly_white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        margin=dict(l=40, r=40, t=60, b=40),
        title=dict(text="Scheda", x=0.5, xanchor="center", font=dict(color="#f1f5f9", size=22)),
    )
    
    fig.add_annotation(
        x=0.5, y=0.5, xref="paper", yref="paper",
        text=text,
        showarrow=False,
        font=dict(size=18, color="#e5e7eb"),
        align="left",
        bordercolor="#1f2937",
        borderwidth=1,
        borderpad=12,
        bgcolor="#111827",
        opacity=0.98,
    )



    return fig






if __name__ == '__main__':
    app.run_server(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8050)),
        debug=True
    )
