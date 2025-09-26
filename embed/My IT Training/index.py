import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# ------------------- Constants -------------------
SCHUMANN_RESONANCE = 7.83
MAX_FREQ_TOLERANCE = 2.5

# ------------------- Core Functions -------------------
def clamp(value, min_value=0.0, max_value=1.0):
    return max(min(value, max_value), min_value)

def calculate_MCI(freq, emf):
    diff = abs(freq - SCHUMANN_RESONANCE)
    score = 1 - (diff / MAX_FREQ_TOLERANCE) if diff <= MAX_FREQ_TOLERANCE else 0
    return clamp(score * (1 - emf))

def calculate_BVI(MCI):
    return clamp(MCI ** 2)

def calculate_HS(MCI, BVI, env_factor):
    return clamp(0.5 * MCI + 0.4 * BVI + 0.1 * env_factor)

def generate_results(custom_input):
    presets = [
        {"Environment": "Earth", "Frequency": 7.83, "EMF": 0.2, "Env Factor": 0.9},
        {"Environment": "Mars", "Frequency": 2.1, "EMF": 0.05, "Env Factor": 0.3},
        {"Environment": "EMRP Bubble", "Frequency": 7.8, "EMF": 0.01, "Env Factor": 1.0},
        {"Environment": "Urban Earth", "Frequency": 6.9, "EMF": 0.6, "Env Factor": 0.7},
        {"Environment": "Custom Input", **custom_input}
    ]
    for env in presets:
        env["MCI"] = calculate_MCI(env["Frequency"], env["EMF"])
        env["BVI"] = calculate_BVI(env["MCI"])
        env["HS"] = calculate_HS(env["MCI"], env["BVI"], env["Env Factor"])
    return pd.DataFrame(presets)

# ------------------- Streamlit App Setup -------------------
st.set_page_config("EMRP Simulator", layout="wide")
tabs = st.tabs(["🏠 Home", "📉 Charts", "📥 Download", "📘 About"])

# ------------------- Tab 1: Home -------------------
with tabs[0]:
    st.title("🌍 EMRP Magneto-Habitability Simulator")
    st.markdown("""
    **Student:** Ediongsenyene Amos  
    **Matric No.:** NOU181040419  
    **School:** National Open University of Nigeria  
    **Study Center:** Yenagoa Study Center  
    """)

    st.sidebar.header("🧪 Custom Environment Input")
    freq = st.sidebar.slider("Resonance Frequency (Hz)", 0.0, 15.0, 7.83, 0.01)
    emf = st.sidebar.slider("EMF Noise Level", 0.0, 1.0, 0.2, 0.01)
    env_factor = st.sidebar.slider("Environmental Factor", 0.0, 1.0, 0.9, 0.01)

    custom_input = {"Frequency": freq, "EMF": emf, "Env Factor": env_factor}
    df = generate_results(custom_input)
    custom = df[df["Environment"] == "Custom Input"].iloc[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🧲 MCI")
        st.markdown(f"**{custom.MCI:.2f}**")
        st.info("Magnetic Coherence Index:\nHow closely this frequency aligns with Earth's natural 7.83 Hz resonance.")

    with col2:
        st.markdown("### 🧬 BVI")
        st.markdown(f"**{custom.BVI:.2f}**")
        st.info("Biological Viability Index:\nLife-support potential derived from MCI².")

    with col3:
        st.markdown("### 🌱 HS")
        st.markdown(f"**{custom.HS:.2f}**")
        st.info("Habitability Score:\nCombined metric from MCI, BVI, and environment.")

    st.markdown("---")
    st.subheader("📁 Preset + Custom Simulation Results")
    st.dataframe(df.style.format({"MCI": "{:.2f}", "BVI": "{:.2f}", "HS": "{:.2f}"}), use_container_width=True)

# ------------------- Tab 2: Charts -------------------
with tabs[1]:
    st.subheader("📉 Visual Comparison")

    env_names = df["Environment"]
    mci_vals = df["MCI"]
    bvi_vals = df["BVI"]
    hs_vals = df["HS"]

    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(env_names))
    bar_width = 0.25

    ax.bar([p - bar_width for p in x], mci_vals, width=bar_width, label='MCI', color='royalblue')
    ax.bar(x, bvi_vals, width=bar_width, label='BVI', color='seagreen')
    ax.bar([p + bar_width for p in x], hs_vals, width=bar_width, label='HS', color='darkorange')

    ax.set_xticks(x)
    ax.set_xticklabels(env_names, rotation=15)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score (0–1)")
    ax.set_title("EMRP Comparison: MCI, BVI, HS")
    ax.legend()

    st.pyplot(fig)

    st.markdown("### 📈 Line Chart of Habitability Scores")
    st.line_chart(df.set_index("Environment")[["MCI", "BVI", "HS"]])

# ------------------- Tab 3: Download -------------------
with tabs[2]:
    st.subheader("📥 Export Results")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Download as CSV",
        data=csv,
        file_name="emrp_simulation_results.csv",
        mime="text/csv"
    )

# ------------------- Tab 4: About -------------------
with tabs[3]:
    st.title("📘 About This Project")
    st.markdown("""
### 🔬 Ediong’s Magnetic Rhythm Principle (EMRP)
The EMRP model explores the hypothesis that a planet's magnetic alignment determines its habitability.
The ideal frequency is Earth's **Schumann Resonance (7.83 Hz)**.

### 🧠 Model Formula Summary

**Magnetic Coherence Index (MCI):**
MCI = (1 - |f - 7.83| / 2.5) × (1 - EMF)

java
Copy
Edit

**Biological Viability Index (BVI):**
BVI = MCI²

java
Copy
Edit

**Habitability Score (HS):**
HS = 0.5 × MCI + 0.4 × BVI + 0.1 × Environmental Factor

markdown
Copy
Edit

### 🛠️ Technologies Used
- Python 3.11
- Streamlit
- Matplotlib
- Pandas

### 📚 Final Year Research Project
**By:** *Ediongsenyene Amos*  
**Matric No.:** *NOU181040419*  
**School:** *National Open University of Nigeria*  
**Center:** *Yenagoa Study Center*
    """)