import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go

# Load data from .txt files
file1 = pd.read_csv("UVEX.txt", delim_whitespace=True, names=["wavelength_air", "wavelength_vacuum", "flux_photon", "flux_erg"])
file2 = pd.read_csv("GIANO.txt", delim_whitespace=True, names=["wavelength_air", "wavelength_vacuum", "flux_photon", "flux_erg"])

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # Required for deployment

app.layout = html.Div([
    html.H1("Interactive Spectrum Viewer"),
    
    # Checkbox for wavelength selection
    html.Label("Select Wavelength Type:"),
    dcc.Checklist(
        id="wavelength_check",
        options=[{"label": "Use Vacuum Wavelength", "value": "vacuum"}],
        value=[],  # Default: Air Wavelength
        inline=True
    ),
    
    # Checkbox for flux unit selection
    html.Label("Select Flux Unit:"),
    dcc.Checklist(
        id="flux_check",
        options=[{"label": "Use Erg Flux Units", "value": "erg"}],
        value=[],  # Default: Photon Flux
        inline=True
    ),

    # Checkbox for choosing datasets
    html.Label("Select Dataset(s) to Display:"),
    dcc.Checklist(
        id="file_check",
        options=[
            {"label": "Show Spectrum 1", "value": "file1"},
            {"label": "Show Spectrum 2", "value": "file2"}
        ],
        value=["file1", "file2"],  # Default: Both datasets
        inline=True
    ),

    # Graph output
    dcc.Graph(id="spectrum_plot"),
])

# Callback to update plot
@app.callback(
    Output("spectrum_plot", "figure"),
    Input("wavelength_check", "value"),
    Input("flux_check", "value"),
    Input("file_check", "value"),
)
def update_plot(wavelength_type, flux_type, selected_files):
    fig = go.Figure()

    # Determine x-axis label based on wavelength selection
    wavelength_col = "wavelength_vacuum" if "vacuum" in wavelength_type else "wavelength_air"
    x_label = "Wavelength in Vacuum (Å)" if "vacuum" in wavelength_type else "Wavelength in Air (Å)"

    # Determine y-axis label based on flux selection
    flux_col = "flux_erg" if "erg" in flux_type else "flux_photon"
    y_label = "Flux (erg/s/cm²/Å/arcsec²)" if "erg" in flux_type else "Flux (photons/s/cm²/Å/arcsec²)"

    if "file1" in selected_files:
        fig.add_trace(go.Scatter(
            x=file1[wavelength_col], 
            y=file1[flux_col], 
            mode="lines", 
            name="Spectrum 1"
        ))

    if "file2" in selected_files:
        fig.add_trace(go.Scatter(
            x=file2[wavelength_col], 
            y=file2[flux_col], 
            mode="lines", 
            name="Spectrum 2"
        ))

    # Update layout
    fig.update_layout(
        title="Spectrum Plot",
        xaxis_title=x_label,
        yaxis_title=y_label,
        template="plotly_white",
        hovermode="x",
    )

    return fig

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)