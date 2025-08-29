import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load data
df = pd.read_csv("output.csv")

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Get unique regions
regions = df["region"].unique()

# Initialize Dash app
app = dash.Dash(__name__)

# Function to create subplot figure
def create_subplot():
    fig = make_subplots(
        rows=len(regions), cols=1,
        shared_xaxes=True,
        subplot_titles=[f"Sales in {r}" for r in regions]
    )

    # Add a line for each region in its own subplot
    for i, region in enumerate(regions, start=1):
        region_df = df[df["region"] == region]
        fig.add_trace(
            go.Scatter(
                x=region_df["date"],
                y=region_df["sales"],
                mode="lines+markers",
                name=region
            ),
            row=i, col=1
        )

    # Layout styling
    fig.update_layout(
        height=300 * len(regions),  # adjust height based on regions
        title="Sales Over Time by Region",
        template="plotly_white",
        showlegend=False
    )

    return fig

# App layout
app.layout = html.Div([
    html.H1("Sales Dashboard", style={"textAlign": "center"}),

    # Graph with subplots
    dcc.Graph(id="sales-chart", figure=create_subplot())
])

if __name__ == "__main__":
    app.run(debug=True)
