# main.py
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime

from subplotter import create_figure
from CSV_Handler import CSV_cleanner_and_manger, CSV_merger_and_short

# ---------- Load data ----------
filter_df_1 = CSV_cleanner_and_manger("data/daily_sales_data_0.csv")
filter_df_2 = CSV_cleanner_and_manger("data/daily_sales_data_1.csv")
filter_df_3 = CSV_cleanner_and_manger("data/daily_sales_data_2.csv")
merge_df = CSV_merger_and_short(filter_df_1, filter_df_2, filter_df_3)

merge_df['date'] = pd.to_datetime(merge_df['date'])
min_date = merge_df['date'].min()
max_date = merge_df['date'].max()

# ---------- Statistics helper ----------
def get_stats(df, date_range=None):
    if date_range:
        start, end = date_range
        df = df[(df['date'] >= start) & (df['date'] <= end)]

    before = df[df['date'] < datetime(2021, 1, 15)]
    after = df[df['date'] >= datetime(2021, 1, 15)]

    avg_before = before['sales'].mean() if not before.empty else 0
    avg_after = after['sales'].mean() if not after.empty else 0
    change_pct = ((avg_after - avg_before) / avg_before * 100) if avg_before != 0 else 0
    return avg_before, avg_after, change_pct

# ---------- Dash app ----------
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap"
])
app.title = "Pink Morsel Sales Dashboard"

PINK_PRIMARY = "#e83e8c"
PINK_DARK = "#b42d6e"

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("🍭 Pink Morsel Sales Dashboard",
                        id="header",
                        className="display-4",
                        style={"color": PINK_PRIMARY, "fontWeight": 600}),
                html.P(
                    "Daily sales across regions – the vertical red line marks the price increase on 2021‑01‑15.",
                    className="lead",
                    style={"color": "#6c757d"}
                ),
            ], className="text-center my-4"),
            width=12
        )
    ]),

    # Summary Statistics Cards
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Avg. Sales Before", className="card-title", style={"fontSize": "1rem"}),
                    html.H4(id="avg-before", children="$0", className="card-text", style={"color": PINK_DARK}),
                ])
            ], className="shadow-sm", style={"border-left": f"4px solid {PINK_PRIMARY}"}),
            width=4
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Avg. Sales After", className="card-title", style={"fontSize": "1rem"}),
                    html.H4(id="avg-after", children="$0", className="card-text", style={"color": PINK_DARK}),
                ])
            ], className="shadow-sm", style={"border-left": f"4px solid {PINK_PRIMARY}"}),
            width=4
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Change", className="card-title", style={"fontSize": "1rem"}),
                    html.H4(id="change-pct", children="0%", className="card-text", style={"color": PINK_DARK}),
                ])
            ], className="shadow-sm", style={"border-left": f"4px solid {PINK_PRIMARY}"}),
            width=4
        ),
    ], className="mb-4"),

    # Date Range Slider
    dbc.Row([
        dbc.Col([
            html.Label("Date Range:", className="font-weight-bold"),
            dcc.RangeSlider(
                id="date-slider",
                min=min_date.timestamp(),
                max=max_date.timestamp(),
                value=[min_date.timestamp(), max_date.timestamp()],
                marks={
                    int(min_date.timestamp()): min_date.strftime("%Y-%m"),
                    int(max_date.timestamp()): max_date.strftime("%Y-%m")
                },
                step=86400,
                tooltip={"placement": "bottom", "always_visible": True},
                allowCross=False,
                className="mt-2"
            )
        ], width=12, className="mb-4"),
    ]),

    # Region Picker
    dbc.Row([
        dbc.Col([
            html.Label("Region:", className="font-weight-bold"),
            dcc.RadioItems(
                id="region-picker",
                options=[
                    {"label": "North", "value": "north"},
                    {"label": "East",  "value": "east"},
                    {"label": "South", "value": "south"},
                    {"label": "West",  "value": "west"},
                    {"label": "All",   "value": "all"},
                ],
                value="all",
                inline=True,
                labelStyle={"marginRight": "15px", "marginLeft": "5px"},
                inputStyle={"marginRight": "5px"},
            )
        ], width=12, className="mb-4"),
    ]),

    # Faceted Chart
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody(
                    dcc.Graph(
                        id="sales-graph",
                        config={"displayModeBar": True, "responsive": True}
                    )
                )
            ], className="shadow-lg border-0"),
            width=12
        )
    ]),

    # Footer
    dbc.Row([
        dbc.Col(
            html.P("Data sourced from daily sales files – updated daily.",
                   className="text-muted text-center mt-4"),
            width=12
        )
    ])

], fluid=True, className="py-3", style={"fontFamily": "Poppins, sans-serif"})


# ---------- Callback ----------
@callback(
    Output("sales-graph", "figure"),
    Output("avg-before", "children"),
    Output("avg-after", "children"),
    Output("change-pct", "children"),
    Input("date-slider", "value"),
    Input("region-picker", "value"),
)
def update_dashboard(date_range, region):
    start_date = datetime.fromtimestamp(date_range[0])
    end_date = datetime.fromtimestamp(date_range[1])

    # Filter by date
    filtered_df = merge_df[
        (merge_df['date'] >= start_date) & (merge_df['date'] <= end_date)
    ]

    # Filter by region (skip if "all")
    if region != "all":
        filtered_df = filtered_df[filtered_df['region'] == region]

    fig = create_figure(filtered_df)

    avg_before, avg_after, change = get_stats(merge_df, (start_date, end_date))

    return fig, f"${avg_before:,.2f}", f"${avg_after:,.2f}", f"{change:+.1f}%"


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True, port=8050)