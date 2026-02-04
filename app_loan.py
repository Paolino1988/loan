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




def amount_4(q,m,list_months, r,dr,d):
    list_am2 = []

    Q = 0
    ii=0
    for n in list_months:
      if n % m==0 and r>dr:
        r=r-dr
      elif r<=dr:
        r=0.05/1200
      
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




      
    dcc.Graph(
        id="summary-box",
        config={"displayModeBar": False},
        style={"height": "70vh"} 
    )

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
    Input("e-slider", "value"),
    Input("f-slider", "value"),
    Input("g-slider", "value")
)
def update_graph(a, b, c,d,e,f,g):

    list_amount = amount_1(c, b, a / 1200)[0]
    list_months = amount_1(c, b, a / 1200)[1]
    list_amount_1 = amount_2(c, list_months, a / 1200, d / 100)[0]
    point_infl = amount_2(c, list_months, a / 1200, d / 100)[1]
    
    list_amount_2, point_infl1 = amount_3(b, list_months, a/1200, d/100 )
    list_amount_4, point_infl2 = amount_4(b, f, list_months, a/1200, g/1200, d / 100)


    
    
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
    
   
   

    # --- Card responsive stile "mobile" per Annotazione Plotly ---
    
    def estimate_text_stats(html_inline_text: str):
        """
        Heuristica semplice per adattare font-size e altezza figura:
        - conta le righe in base ai <br>
        - stima la larghezza massima per righe lunghe
        """
        # normalizza: togli tag che non impattano sul conteggio righe
        clean = html_inline_text.replace("</b>", "").replace("</span>", "")
        # spezza in righe sui <br>
        lines = [ln.strip() for ln in clean.split("<br>") if ln.strip() != ""]
        n_lines = max(1, len(lines))
    
        # stima lunghezza massima (numero caratteri) tra le righe
        import re
        # rimuovi i tag <span ...>
        span_re = re.compile(r"<span[^>]*>", re.IGNORECASE)
        no_tags_lines = [re.sub(span_re, "", ln) for ln in lines]
        max_line_len = max((len(ln) for ln in no_tags_lines), default=0)
    
        return n_lines, max_line_len
    
    def pick_font_and_layout(n_lines: int, max_line_len: int):
        """
        Regole:
        - più righe → font più piccolo e figura più alta
        - righe molto lunghe → riduci leggermente il font
        """
        # base
        font_size = 20
        height = 520
        v_center = 0.5  # centro verticale
    
        # aggiusta per numero di righe
        if n_lines <= 8:
            font_size = 20
            height = 560
        elif n_lines <= 12:
            font_size = 18
            height = 640
        elif n_lines <= 16:
            font_size = 17
            height = 720
        else:
            font_size = 16
            height = 800
    
        # aggiusta per righe molto lunghe
        if max_line_len >= 110:
            font_size -= 2
        elif max_line_len >= 90:
            font_size -= 1
    
        # clamp minimo/massimo
        font_size = max(14, min(font_size, 22))
        height = max(520, min(height, 960))
    
        return font_size, height, v_center
    
    # 1) Stima righe e lunghezza
    _n_lines, _max_line_len = estimate_text_stats(text)
    # 2) Scegli font-size e height in modo adattivo
    _font_size, _height, _y_center = pick_font_and_layout(_n_lines, _max_line_len)
    
    # 3) Crea figura con margini e titolo; margini un po' più ampi su mobile
    fig = go.Figure()
    fig.update_layout(
        template="plotly_white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        margin=dict(l=56, r=56, t=80, b=56),
        title=dict(
            text="Scheda",
            x=0.5,
            xanchor="center",
            font=dict(color="#f1f5f9", size=22)
        ),
        height=_height,
    )
    
    # 4) "Card" centrale: shape rettangolare responsivo (padding interno comodo)
    #    Allarga leggermente i bordi su schermi piccoli grazie ai margini sopra
    x0, x1 = 0.07, 0.93
    y0, y1 = 0.14, 0.86
    
    fig.add_shape(
        type="rect",
        xref="paper", yref="paper",
        x0=x0, y0=y0, x1=x1, y1=y1,
        line=dict(color="#1f2937", width=1),
        fillcolor="#111827",
        layer="below"
    )
    
    # 5) Annotazione centrata nel box; solo HTML inline in `text`
    fig.add_annotation(
        x=(x0 + x1) / 2,
        y=(y0 + y1) / 2,
        xref="paper", yref="paper",
        xanchor="center", yanchor="middle",
        text=text,                 # <-- usa il tuo testo con <b>, <span>, <br>
        showarrow=False,
        align="left",              # 'left' = leggibilità migliore per righe lunghe
        font=dict(size=_font_size, color="#e5e7eb"),
        bordercolor="#1f2937",
        borderwidth=1,
        borderpad=14,
        bgcolor="rgba(0,0,0,0)",   # sfondo fornito dallo shape
        opacity=1.0,
    )

    return fig







if __name__ == '__main__':
    app.run_server(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8050)),
        debug=True
    )
