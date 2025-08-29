import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ----------------------
# Load Data
# ----------------------
df = pd.read_csv("output.csv")
df["date"] = pd.to_datetime(df["date"])
regions = df["region"].unique()
price_increase_date = pd.to_datetime("2021-01-15")

# ----------------------
# Initialize Dash App
# ----------------------
app = dash.Dash(__name__)

# ----------------------
# Function to create subplots
# ----------------------
def create_subplot(region_filter="all"):
    if region_filter == "all":
        filtered_df = df
        region_list = regions
    else:
        filtered_df = df[df["region"] == region_filter]
        region_list = [region_filter]

    fig = make_subplots(
        rows=len(region_list),
        cols=1,
        shared_xaxes=True,
        subplot_titles=[f"Sales in {r.capitalize()}" for r in region_list]
    )

    for i, region in enumerate(region_list, start=1):
        region_df = filtered_df[filtered_df["region"] == region]

        # Line chart
        fig.add_trace(
            go.Scatter(
                x=region_df["date"],
                y=region_df["sales"],
                mode="lines+markers",
                line=dict(color="#FF6600", width=3),
                marker=dict(size=6, color="#FF6600"),
                name=region.capitalize(),
                hovertemplate='%{y} sales on %{x|%b %d, %Y}<extra></extra>'
            ),
            row=i, col=1
        )

        # Vertical line for price increase
        fig.add_shape(
            type="line",
            x0=price_increase_date,
            x1=price_increase_date,
            y0=0,
            y1=1,
            xref="x",
            yref=f"y{i}",
            line=dict(color="red", dash="dash")
        )

        # Annotation for price increase
        fig.add_annotation(
            x=price_increase_date,
            y=1 - (i - 1) / len(region_list),  # top of subplot i
            xref="x",
            yref="paper",
            text="Price Increase",
            showarrow=False,
            font=dict(color="red", size=12)
        )

    fig.update_layout(
        height=300 * len(region_list),
        title="Pink Morsel Sales Over Time by Region",
        template="plotly_white",
        showlegend=True,
        title_font=dict(size=24, color="#FF6600", family="Arial"),
        margin=dict(t=80, l=50, r=50, b=50)
    )

    return fig

# ----------------------
# Radio Button Options
# ----------------------
region_options = [
    {"label": "North", "value": "north"},
    {"label": "East", "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West", "value": "west"},
    {"label": "All", "value": "all"}
]

# ----------------------
# App Layout with CSS Enhancements
# ----------------------
app.layout = html.Div(
    style={"backgroundColor": "#f0f2f5", "fontFamily": "Arial, sans-serif", "padding": "20px"},
    children=[
        html.H1(
            "Pink Morsel Sales Dashboard",
            style={
                "textAlign": "center",
                "color": "white",
                "marginBottom": "30px",
                "background": "linear-gradient(to right, #ff9966, #ff5e62)",
                "padding": "15px",
                "borderRadius": "10px"
            }
        ),

        html.Div(
            [
                html.Label(
                    "Select Region:",
                    style={"fontWeight": "bold", "marginRight": "10px", "fontSize": "16px"}
                ),
                dcc.RadioItems(
                    id="region-selector",
                    options=region_options,
                    value="all",
                    inline=True,
                    inputStyle={"marginRight": "5px", "marginLeft": "15px", "cursor": "pointer"},
                    labelStyle={
                        "marginRight": "15px",
                        "fontSize": "16px",
                        "color": "#333",
                        "padding": "5px",
                        "borderRadius": "5px",
                        "transition": "0.3s"
                    },
                    className="radio-buttons"
                )
            ],
            style={"textAlign": "center", "marginBottom": "20px"}
        ),

        dcc.Graph(
            id="sales-chart",
            figure=create_subplot("all"),
            style={
                "border": "2px solid #FF6600",
                "borderRadius": "15px",
                "padding": "15px",
                "backgroundColor": "white",
                "boxShadow": "2px 2px 10px rgba(0,0,0,0.15)"
            }
        )
    ]
)

# ----------------------
# Callback to update chart based on region selection
# ----------------------
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-selector", "value")
)
def update_chart(selected_region):
    return create_subplot(selected_region)

# ----------------------
# Add hover CSS for radio buttons
# ----------------------
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Pink Morsel Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            .radio-buttons label:hover {
                background-color: #ffe6cc;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ----------------------
# Run the App
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
