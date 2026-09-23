import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# 1. Page Configuration 
st.set_page_config(
    page_title="Shaft Design Pro",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Injection for UI Overhaul
st.markdown("""
    <style>
    /* Hide default Streamlit headers and footers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Style the main title */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00E5FF, #007BFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    
    /* Style the metric cards */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #00E5FF;
        font-weight: 700;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1.1rem;
        color: #A0AEC0;
    }
    
    /* Add a subtle glow to the sidebar */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 2px 0 10px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<h1 class="main-title">⚙️ Torsion & Power Transmission Analyzer</h1>', unsafe_allow_html=True)
st.markdown("Optimize shaft geometry for maximum weight savings without compromising shear strength.")
st.markdown("---")

# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🎛️ Design Parameters")
    power_kw = st.number_input("Power (kW)", min_value=0.0, max_value=1000.0, value=50.0, step=1.0)
    rpm = st.number_input("Speed (RPM)", min_value=0.0, max_value=5000.0, value=1500.0, step=50.0)
    tau_mpa = st.number_input("Allowable Shear Stress (MPa)", min_value=0.0, max_value=300.0, value=50.0, step=5.0)
    
    st.markdown("### 📐 Geometry")
    k_ratio = st.slider("Hollow Ratio (Inner/Outer)", min_value=0.1, max_value=0.9, value=0.5, step=0.05)
    
    st.markdown("---")
    st.markdown("### 🎓 Project Details")
    st.text_input("Institution", "LJ Polytechnic", disabled=True)
    st.text_input("Course", "Diploma Mechanical (Sem 3)", disabled=True)
    st.text_area("Team Members", "1. [Name] (Enrollment)\n2. [Name] (Enrollment)")

# Validation
if power_kw == 0 or rpm == 0 or tau_mpa == 0:
    st.warning("⚠️ Please enter values greater than zero for Power, RPM, and Shear Stress.")
else:
    # Calculations
    torque_nm = (power_kw * 60 * 1000) / (2 * np.pi * rpm)
    tau_pa = tau_mpa * 10**6

    d_solid_m = ((16 * torque_nm) / (np.pi * tau_pa)) ** (1 / 3)
    d_solid_mm = d_solid_m * 1000

    d_outer_m = ((16 * torque_nm) / (np.pi * tau_pa * (1 - k_ratio**4))) ** (1 / 3)
    d_outer_mm = d_outer_m * 1000
    d_inner_mm = d_outer_mm * k_ratio

    area_solid = (np.pi / 4) * (d_solid_mm**2)
    area_hollow = (np.pi / 4) * (d_outer_mm**2 - d_inner_mm**2)
    weight_savings_pct = (1 - (area_hollow / area_solid)) * 100

    # Dashboard Metrics UI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Required Torque", value=f"{torque_nm:.1f} N·m")
    with col2:
        st.metric(label="Solid Shaft Dia", value=f"{d_solid_mm:.1f} mm")
    with col3:
        st.metric(label="Hollow Outer Dia", value=f"{d_outer_mm:.1f} mm", delta=f"Inner: {d_inner_mm:.1f} mm", delta_color="off")
    with col4:
        st.metric(label="Weight Savings", value=f"{weight_savings_pct:.1f} %")

    st.markdown("---")
    
    # Mathematical Expander (Guaranteed Viva Marks)
    with st.expander("📝 View Step-by-Step Engineering Calculations"):
        st.markdown("**1. Torque Transmitted ($T$)**")
        st.latex(rf"T = \frac{{P \times 60 \times 1000}}{{2 \pi N}} = \frac{{{power_kw} \times 60000}}{{2 \pi \times {rpm}}} = {torque_nm:.2f} \text{{ N·m}}")
        
        st.markdown("**2. Solid Shaft Diameter ($D$)**")
        st.latex(rf"D = \left( \frac{{16 T}}{{\pi \tau}} \right)^{{1/3}} = {d_solid_mm:.2f} \text{{ mm}}")
        
        st.markdown("**3. Hollow Shaft Outer Diameter ($D_o$)**")
        st.latex(rf"D_o = \left( \frac{{16 T}}{{\pi \tau (1 - k^4)}} \right)^{{1/3}} = {d_outer_mm:.2f} \text{{ mm}}")
        
        st.markdown("**4. Weight Savings**")
        st.markdown("Since density and length are constant, weight is proportional to cross-sectional area:")
        st.latex(rf"\% \text{{ Savings}} = \left( 1 - \frac{{A_{{hollow}}}}{{A_{{solid}}}} \right) \times 100 = {weight_savings_pct:.2f}\%")

    st.markdown("---")
    
    # Matplotlib UI Fixes & Area Math Bug Fix
    k_vals = np.linspace(0.1, 0.85, 50)
    savings_vals = []
    
    for k in k_vals:
        do_temp_m = ((16 * torque_nm) / (np.pi * tau_pa * (1 - k**4))) ** (1 / 3)
        do_temp_mm = do_temp_m * 1000 
        di_temp_mm = do_temp_mm * k
        
        a_h = (np.pi / 4) * (do_temp_mm**2 - di_temp_mm**2)
        sav = (1 - (a_h / area_solid)) * 100
        savings_vals.append(sav)

    # Styling the plot to look like a modern dashboard component
    plt.style.use('dark_background') 
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Make background transparent
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    ax.plot(k_vals, savings_vals, color="#00E5FF", linewidth=3, label="Efficiency Curve")
    ax.axvline(x=k_ratio, color="#FF0055", linestyle="--", linewidth=2, label=f"Selected Ratio: {k_ratio:.2f}")
    
    ax.ticklabel_format(useOffset=False, style='plain')
    
    ax.set_xlabel("Hollow Ratio (k)", fontsize=12, color="#A0AEC0")
    ax.set_ylabel("Weight Savings (%)", fontsize=12, color="#A0AEC0")
    
    # Clean up grid and borders
    ax.grid(True, linestyle="--", alpha=0.2, color="#ffffff")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#555555')
    ax.spines['bottom'].set_color('#555555')
    ax.legend(frameon=False)
    
    st.pyplot(fig)