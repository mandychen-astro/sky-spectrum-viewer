import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Load data from files
wave_opt_air, wave_opt, flux_opt_photon, flux_opt_cgs = np.loadtxt("UVEX.txt", unpack=True)
wave_ir_air, wave_ir, flux_ir_photon, flux_ir_cgs = np.loadtxt("GIANO.txt", unpack=True)
flux_opt_cgs *= 1e16  # make numbers more readable
flux_ir_cgs *= 1e16  # make numbers more readable

# Initial plot uses air wavelength and photon flux
x1 = wave_opt_air
x2 = wave_ir_air
y1 = flux_opt_photon
y2 = flux_ir_photon

# Create figure and add traces with fixed colors
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x1,
    y=y1,
    mode="lines",
    name="UVEX",
    line=dict(color="blue"),
    visible=True
))

fig.add_trace(go.Scatter(
    x=x2,
    y=y2,
    mode="lines",
    name="GIANO",
    line=dict(color="red"),
    visible=True
))

# Function to create each of the 4 unit-combo buttons
def make_update_button(wave_key, flux_key):
    x1 = wave_opt if wave_key == "Vacuum" else wave_opt_air
    x2 = wave_ir if wave_key == "Vacuum" else wave_ir_air
    y1 = flux_opt_cgs if flux_key == "CGS" else flux_opt_photon
    y2 = flux_ir_cgs if flux_key == "CGS" else flux_ir_photon

    return dict(
        args=[
            {"x": [x1, x2], "y": [y1, y2]},
            {
                "xaxis": {
                    "title": {
                        "text": f"Wavelength in {wave_key} (Å)",
                        "font": dict(size=20)
                    },
                    "tickformat": "~g",
                    "tickfont": dict(size=18)
                },
                "yaxis": {
                    "title": {
                        "text": (
                            "Flux (1E-16 erg/s/cm²/Å/arcsec²)"
                            if flux_key == "CGS"
                            else "Flux (photons/s/cm²/Å/arcsec²)"
                        ),
                        "font": dict(size=20)
                    },
                    "tickfont": dict(size=18)
                }
            }
        ],
        label=f"{wave_key} / {flux_key}",
        method="update"
    )

# Buttons for all combinations
flux_wave_buttons = [
    make_update_button(w, f) for w in ["Air", "Vacuum"] for f in ["Photon", "CGS"]
]

# Spectrum visibility toggle buttons
trace_toggle_buttons = [
    dict(label="Both Spectra", method="update", args=[{"visible": [True, True]}]),
    dict(label="Only UVEX", method="update", args=[{"visible": [True, False]}]),
    dict(label="Only GIANO", method="update", args=[{"visible": [False, True]}]),
]

# Layout configuration
fig.update_layout(
    # title="Interactive Sky Spectrum Viewer (UVEX: Hanuschik 2003; GIANO: Oliva et al. 2015)",
    # xaxis_title="Wavelength in Air (Å)",
    # yaxis_title="Flux (photons/s/cm²/Å/arcsec²)",
    title=dict(
        text=(
            "Interactive Sky Spectrum Viewer<br>"
            "(UVEX: Hanuschik 2003; GIANO: Oliva et al. 2015)"
        ),
        x=0.5,
        xanchor="center",
        yanchor="top",
        font=dict(size=20)
    ),
    template="plotly_white",
    hovermode="closest",
    margin=dict(t=100, r=200),  # Extra space on right for buttons
    xaxis=dict(
        title=dict(text="Wavelength in Air (Å)", font=dict(size=20)),
        tickfont=dict(size=18),
        tickformat="~g",
        range=[3100, 18500]
    ),
    yaxis=dict(
        title=dict(text="Flux (photons/s/cm²/Å/arcsec²)", font=dict(size=20)),
        tickfont=dict(size=18)
    ),
    legend=dict(
        x=1.02,
        y=1,
        xanchor="left",
        yanchor="top",
        bgcolor="rgba(255,255,255,0.95)",
        bordercolor="lightgray",
        borderwidth=1,
        font=dict(size=18)
    ),
    updatemenus=[
        # Combo unit switcher
        dict(
            type="buttons",
            direction="down",
            buttons=flux_wave_buttons,
            showactive=True,
            x=1.02,
            xanchor="left",
            y=0.8,
            yanchor="top",
            font=dict(size=16)
        ),
        # Spectrum toggle
        dict(
            type="buttons",
            direction="down",
            buttons=trace_toggle_buttons,
            showactive=True,
            x=1.02,
            xanchor="left",
            y=0.4,
            yanchor="top",
            font=dict(size=16)
        )
    ],
    annotations=[
        dict(
            text='<a href="https://github.com/mandychen-astro/sky-spectrum-viewer" target="_blank">See details in the GitHub page</a>',
            xref="paper",
            yref="paper",
            x=0.55,
            y=0.98,
            showarrow=False,
            font=dict(size=18),
            xanchor="center",
            yanchor="bottom"
        ),
        dict(
            text="Choose the units:",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.02,
            y=0.80,
            xanchor="left",
            yanchor="bottom",
            font=dict(size=18)
        ),
        dict(
            text="Show Spectra:",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.02,
            y=0.40,
            xanchor="left",
            yanchor="bottom",
            font=dict(size=18)
        )
    ]
)

# Export to static HTML
pio.write_html(fig, file="spectrum_plot.html", full_html=True, include_plotlyjs="cdn")
