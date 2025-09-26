# Planetary Magnetic Rhythm Simulation System (Advanced Version)
# Developed by Ediongsenyene Amos

import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import base64
import io

# EMRP Metric Calculation Functions
def calculate_mcr(magnetic_field_strength):
    return round(magnetic_field_strength / 100, 2)

def calculate_bvi(mcr, atmospheric_pressure):
    return round((mcr * atmospheric_pressure) / 50000, 2)

def calculate_gei(solar_flux):
    return round(100 - (solar_flux / 10), 2)

# PDF Report Generator Function
def generate_pdf(mcr, bvi, gei, planet, inputs):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    textobject = c.beginText(50, 800)
    textobject.setFont("Helvetica", 12)
    textobject.textLine("Planet Magnetic Rhythm Simulation Report")
    textobject.textLine("-----------------------------------------")
    textobject.textLine(f"Planet: {planet}")
    textobject.textLine(f"Magnetic Field Strength (µT): {inputs['magnetic_field']}")
    textobject.textLine(f"Atmospheric Pressure (Pa): {inputs['atmospheric_pressure']}")
    textobject.textLine(f"Solar Flux (W/m²): {inputs['solar_flux']}")
    textobject.textLine("")
    textobject.textLine(f"MCR: {mcr}")
    textobject.textLine(f"BVI: {bvi}")
    textobject.textLine(f"GEI: {gei}")
    c.drawText(textobject)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Streamlit App Start
st.set_page_config(page_title="Planet Magnetic Rhythm Simulator", layout="centered")
st.title('🌍 Planet Magnetic Rhythm Simulation System (EMRP)')

# Initialize session state to store all simulations
if "simulation_results" not in st.session_state:
    st.session_state.simulation_results = []

# Planet Selection
planet = st.selectbox("Select Planet:", ["Earth", "Mars", "Custom Planet"])

default_values = {
    "Earth": {"magnetic_field": 50.0, "atmospheric_pressure": 101325, "solar_flux": 1361},
    "Mars": {"magnetic_field": 5.0, "atmospheric_pressure": 610, "solar_flux": 590}
}

if planet != "Custom Planet":
    data = default_values[planet]
else:
    data = {"magnetic_field": 0.0, "atmospheric_pressure": 0.0, "solar_flux": 0.0}

# Input Fields
magnetic_field = st.number_input("Magnetic Field Strength (µT):", min_value=0.0, value=data["magnetic_field"])
atmospheric_pressure = st.number_input("Atmospheric Pressure (Pa):", min_value=0.0, value=data["atmospheric_pressure"])
solar_flux = st.number_input("Solar Flux (W/m²):", min_value=0.0, value=data["solar_flux"])

inputs = {
    "magnetic_field": magnetic_field,
    "atmospheric_pressure": atmospheric_pressure,
    "solar_flux": solar_flux
}

# Run Simulation Button
if st.button("Run Simulation"):

    mcr = calculate_mcr(magnetic_field)
    bvi = calculate_bvi(mcr, atmospheric_pressure)
    gei = calculate_gei(solar_flux)

    st.success(f"MCR: {mcr}")
    st.success(f"BVI: {bvi}")
    st.success(f"GEI: {gei}")

    # Store in session state
    st.session_state.simulation_results.append({
        "Planet": planet,
        "Magnetic Field Strength (µT)": magnetic_field,
        "Atmospheric Pressure (Pa)": atmospheric_pressure,
        "Solar Flux (W/m²)": solar_flux,
        "MCR": mcr,
        "BVI": bvi,
        "GEI": gei
    })

    # Display Radar Chart
    fig = px.line_polar(
        r=[mcr, bvi, gei, mcr],
        theta=['MCR', 'BVI', 'GEI', 'MCR'],
        line_close=True,
        title="Magnetic Rhythm Metrics Radar Chart"
    )
    st.plotly_chart(fig)

    # Generate PDF Report
    pdf_buffer = generate_pdf(mcr, bvi, gei, planet, inputs)
    b64_pdf = base64.b64encode(pdf_buffer.read()).decode()
    href_pdf = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="simulation_report.pdf">📄 Download PDF Report</a>'
    st.markdown(href_pdf, unsafe_allow_html=True)

    # Display success message
    st.info("PDF Report is ready. Click the link above to download.")

# Display Stored Results (Session State)
if st.session_state.simulation_results:
    st.subheader("🗃️ All Simulations This Session")
    df = pd.DataFrame(st.session_state.simulation_results)
    st.dataframe(df)

    # CSV Export
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    b64_csv = base64.b64encode(csv_buffer.getvalue().encode()).decode()
    href_csv = f'<a href="data:file/csv;base64,{b64_csv}" download="all_simulations.csv">📥 Download All Results as CSV</a>'
    st.markdown(href_csv, unsafe_allow_html=True)
