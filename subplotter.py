import plotly.express as px
from datetime import datetime  # <-- NEW import


def create_figure(df):
    fig = px.line(
        df,
        x="date",
        y="sales",
        facet_col="region",
        facet_col_wrap=2,
        title="Pink Morsel Sales by Region",
        labels={"date": "Date", "sales": "Sales ($)"},
        color_discrete_sequence=['#e83e8c']  # optional pink line
    )
    # Add the price-increase line (annotation position changed)
    fig.add_vline(
        x=datetime(2021, 1, 15),  # <-- changed from string to datetime
        line_dash="dash",
        line_color="red",
        annotation_text="Price increase",
        annotation_position="top left",  # <-- changed from "top right"
        annotation_font_size=11,
        annotation_font_color="red"
    )

    # ---- NEW: Force Y-axis title on EVERY subplot ----
    for axis in fig.layout:
        if axis.startswith('yaxis'):
            fig.layout[axis].title.text = "Sales ($)"
            fig.layout[axis].title.standoff = 10

    # Optional: overall styling
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Poppins, sans-serif")
    )

    return fig