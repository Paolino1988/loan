import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go

# =====================================================
# FUNZIONI DI CALCOLO (le tue, NON le tocco)
# =====================================================
# amount_mutuo(capitale, tasso_annuo, anni)
# -> [q_f, I_f, I_i, q_i_0, q_i_f, q_i_m]

# ratio_mutuo(capitale, tasso_annuo, anni)
# -> [lista_percentuali, percentuale_totale]

# =====================================================
# APP
# =====================================================
app = dash.Dash(__name__)
server = app.server

# =====================================================
# LAYOUT
# =====================================================
app.layout = html.Div(
    [
        html.H2("Simulatore Mutuo", style={"marginBottom": "20px"}),

        # ---------- INPUT ----------
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Importo mutuo (€)"),
                        dcc.Input(
                            id="x-input",
                            type="number",
                            value=150,
                            step=10,
                            style={"width": "100%"},
                        ),
                    ],
                    style={"width": "30%"},
                ),

                html.Div(
                    [
                        html.Label("APR (%)"),
                        dcc.Slider(
                            id="z-slider",
                            min=0.5,
                            max=10,
                            step=0.1,
                            value=3,
                            marks={i: f"{i}%" for i in range(1, 11)},
                        ),
                    ],
                    style={"width": "30%"},
                ),

                html.Div(
                    [
                        html.Label("Durata (anni)"),
                        dcc.Slider(
                            id="y-slider",
                            min=5,
                            max=30,
                            step=1,
                            value=20,
                            marks={i: str(i) for i in range(5, 31, 5)},
                        ),
                    ],
                    style={"width": "30%"},
                ),
            ],
            style={
                "display": "flex",
                "gap": "30px",
                "marginBottom": "40px",
            },
        ),

        # ---------- CARD RIEPILOGO ----------
        html.Div(id="summary-box-mutuo", style={"marginBottom": "40px"}),

        # ---------- GRAFICO ----------
        dcc.Graph(id="percent-graph"),
    ],
    style={"maxWidth": "1100px", "margin": "auto"},
)

# =====================================================
# CALLBACK RIEPILOGO MUTUO
# =====================================================
@app.callback(
    Output("summary-box-mutuo", "children"),
    Input("x-input", "value"),
    Input("z-slider", "value"),
    Input("y-slider", "value"),
)
def update_mutuo(x, z, y):

    if x is None:
        return "Inserisci un importo valido"

    capitale = 1000 * x
    tasso = z / 100

    q_f, I_f, I_i, q_i_0, q_i_f, q_i_m = amount_mutuo(capitale, tasso, y)
    _, perc_inter = ratio_mutuo(capitale, tasso, y)

    def fmt(val):
        return f"€ {val:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return html.Div(
        [
            html.Div("Riepilogo Mutuo", className="summary-title"),

            summary_row("Rata ammortamento Francese", fmt(q_f), "#adff2f"),
            summary_row("Interessi totali Francese", fmt(I_f), "#60a5fa"),
            summary_row("Interessi totali Italiano", fmt(I_i), "#ef4444"),
            summary_row("Prima rata Italiano", fmt(q_i_0), "#34d399"),
            summary_row("Ultima rata Italiano", fmt(q_i_f), "#ffd700"),
            summary_row("Rata media Italiano", fmt(q_i_m), "#8a2be2"),
            summary_row("Interessi / Capitale (%)", f"{perc_inter:.2f}%", "#daa520"),
        ],
        className="summary-card",
        style={
            "border": "1px solid #ddd",
            "padding": "20px",
            "borderRadius": "12px",
            "boxShadow": "0 4px 10px rgba(0,0,0,0.05)",
        },
    )

def summary_row(label, value, color):
    return html.Div(
        [
            html.Span(label, style={"color": color, "fontWeight": "600"}),
            html.Span(value, style={"color": color, "fontWeight": "600"}),
        ],
        style={
            "display": "flex",
            "justifyContent": "space-between",
            "marginBottom": "8px",
        },
    )

# =====================================================
# CALLBACK GRAFICO PERCENTUALE
# =====================================================
@app.callback(
    Output("percent-graph", "figure"),
    Input("x-input", "value"),
    Input("z-slider", "value"),
    Input("y-slider", "value"),
)
def update_percent_graph(x, z, y):

    if x is None:
        return go.Figure()

    capitale = 1000 * x
    tasso = z / 100

    list_perc = ratio_mutuo(capitale, tasso, y)[0]
    mesi = list(range(1, len(list_perc) + 1))

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=mesi,
            y=list_perc,
            mode="lines+markers",
            line=dict(width=3),
            marker=dict(size=6),
            hovertemplate="Mese %{x}<br>%{y:.2f}%<extra></extra>",
        )
    )

    fig.update_layout(
        title="Evoluzione percentuale nel tempo",
        xaxis_title="Mesi",
        yaxis_title="Percentuale",
        yaxis_ticksuffix="%",
        template="plotly_white",
        height=420,
    )

    return fig

# =====================================================
# RUN
# =====================================================
if __name__ == "__main__":
    app.run_server(debug=True)
