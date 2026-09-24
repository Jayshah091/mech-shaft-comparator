import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="Shaft Design Pro",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME TOGGLE & ANIMATION CONTROLS ---
with st.sidebar:
    is_dark = st.toggle("🌙 Dark Mode", value=True)
    st.markdown("---")
    
    st.markdown("### 🎛️ Design Parameters")
    power_kw = st.number_input("Power (kW)", min_value=0.0, max_value=1000.0, value=50.0, step=1.0)
    rpm = st.number_input("Speed (RPM)", min_value=0.0, max_value=5000.0, value=1500.0, step=50.0)
    tau_mpa = st.number_input("Allowable Shear Stress (MPa)", min_value=0.0, max_value=300.0, value=50.0, step=5.0)
    
    st.markdown("### 📐 Geometry")
    k_ratio = st.slider("Hollow Ratio (Inner/Outer)", min_value=0.1, max_value=0.9, value=0.5, step=0.05)
    
    st.markdown("---")
    st.markdown("### 🎬 Animation")
    play_anim = st.checkbox("▶ Play animation", value=True)
    anim_speed = st.slider("Speed", min_value=0.1, max_value=2.0, value=1.0, step=0.1)

# --- DYNAMIC THEME VARIABLES ---
if is_dark:
    metric_val = "#00E5FF"
    metric_label = "#A0AEC0"
    sidebar_glow = "rgba(255, 255, 255, 0.1)"
    plt_style = "dark_background"
    plt_line = "#00E5FF"
    plt_grid = "#ffffff"
    plt_text = "#A0AEC0"
    plt_spine = "#555555"
    hero_bg = "#0b1c2c"
    hero_border = "#1e3a5f"
    hero_text = "#ffffff"
    hero_subtext = "#8fa6b8"
    wave_color = "%2300E5FF"
else:
    metric_val = "#0056b3"
    metric_label = "#475467"
    sidebar_glow = "rgba(0, 0, 0, 0.1)"
    plt_style = "default"
    plt_line = "#0056b3"
    plt_grid = "#000000"
    plt_text = "#475467"
    plt_spine = "#cccccc"
    hero_bg = "#f0f7ff"
    hero_border = "#cce3fb"
    hero_text = "#003366"
    hero_subtext = "#475467"
    wave_color = "%230056b3"

# 2. Custom CSS Injection
st.markdown(f"""
    <style>
    /* Hide default Streamlit headers and footers */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Style the metric cards */
    div[data-testid="stMetricValue"] {{
        font-size: 2.2rem;
        color: {metric_val};
        font-weight: 700;
    }}
    div[data-testid="stMetricLabel"] {{
        font-size: 1.1rem;
        color: {metric_label};
    }}
    
    /* Dynamic sidebar border */
    [data-testid="stSidebar"] {{
        border-right: 1px solid {sidebar_glow};
    }}
    </style>
""", unsafe_allow_html=True)

# --- PREMIUM HERO HEADER ---
hero_card = f"""
<div style="background-color: {hero_bg}; padding: 2rem 2rem 3rem 2rem; border-radius: 10px; margin-bottom: 2rem; position: relative; overflow: hidden; border: 1px solid {hero_border};">
    <h1 style="color: {hero_text}; margin-top: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.5px;">Torsion & Power Transmission Analyzer</h1>
    <div style="color: {hero_subtext}; font-size: 0.95rem; line-height: 1.8; margin-top: 10px;">
        <strong>Group:</strong> 4 | <strong>Members:</strong> [Name] (Enrollment), [Name] (Enrollment) <br>
        Diploma in Mechanical Engineering (Sem 3) | <strong>Institution:</strong> LJ Polytechnic
    </div>
    <div style="position: absolute; bottom: -5px; left: 0; right: 0; width: 100%; height: 25px; background-image: url('data:image/svg+xml;utf8,<svg viewBox=\"0 0 1440 320\" xmlns=\"http://www.w3.org/2000/svg\" preserveAspectRatio=\"none\"><path fill=\"{wave_color}\" fill-opacity=\"0.7\" d=\"M0,224L80,213.3C160,203,320,181,480,181.3C640,181,800,203,960,197.3C1120,192,1280,160,1360,144L1440,128L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z\"></path></svg>'); background-size: 100% 100%; background-repeat: no-repeat;"></div>
</div>
"""
st.markdown(hero_card, unsafe_allow_html=True)

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
        st.metric(label="Required Torque (T)", value=f"{torque_nm:.1f} N·m")
    with col2:
        st.metric(label="Solid Shaft Dia (D)", value=f"{d_solid_mm:.1f} mm")
    with col3:
        st.metric(label="Hollow Outer Dia (D_o)", value=f"{d_outer_mm:.1f} mm", delta=f"Inner (d_i): {d_inner_mm:.1f} mm", delta_color="off")
    with col4:
        st.metric(label="Weight Savings", value=f"{weight_savings_pct:.1f} %")

    st.markdown("---")
    
    # Mathematical Expander
    with st.expander("📝 Step-by-step working (for report & viva)"):
        st.markdown("**1. Torque Transmitted ($T$)**")
        st.latex(rf"T = \frac{{P \times 60 \times 1000}}{{2 \pi N}} = \frac{{{power_kw} \times 60000}}{{2 \pi \times {rpm}}} = {torque_nm:.2f} \text{{ N·m}}")
        
        st.markdown("**2. Solid Shaft Diameter ($D$)**")
        st.latex(rf"D = \left( \frac{{16 T}}{{\pi \tau}} \right)^{{1/3}} = {d_solid_mm:.2f} \text{{ mm}}")
        
        st.markdown("**3. Hollow Shaft Outer Diameter ($D_o$)**")
        st.latex(rf"D_o = \left( \frac{{16 T}}{{\pi \tau (1 - k^4)}} \right)^{{1/3}} = {d_outer_mm:.2f} \text{{ mm}}")
        
        st.markdown("**4. Weight Savings**")
        st.latex(rf"\% \text{{ Savings}} = \left( 1 - \frac{{A_{{hollow}}}}{{A_{{solid}}}} \right) \times 100 = {weight_savings_pct:.2f}\%")

    st.markdown("---")
    st.markdown("### Efficiency Curve: Weight Savings vs. Geometry")
    
    # Generate Graph Data
    k_vals = np.linspace(0.1, 0.85, 50)
    savings_vals = []
    
    for k in k_vals:
        do_temp_m = ((16 * torque_nm) / (np.pi * tau_pa * (1 - k**4))) ** (1 / 3)
        do_temp_mm = do_temp_m * 1000 
        di_temp_mm = do_temp_mm * k
        
        a_h = (np.pi / 4) * (do_temp_mm**2 - di_temp_mm**2)
        sav = (1 - (a_h / area_solid)) * 100
        savings_vals.append(sav)

    # Apply the dynamic plot style
    plt.style.use(plt_style) 
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Keep background transparent
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Base axes configuration
    ax.set_xlim(0.1, 0.85)
    ax.set_ylim(0, max(savings_vals) + 5)
    ax.ticklabel_format(useOffset=False, style='plain')
    ax.set_xlabel("Hollow Ratio (k = Inner / Outer)", fontsize=12, color=plt_text)
    ax.set_ylabel("Weight Savings (%)", fontsize=12, color=plt_text)
    ax.grid(True, linestyle="--", color=plt_grid, alpha=0.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(plt_spine)
    ax.spines['bottom'].set_color(plt_spine)
    ax.tick_params(colors=plt_text)
    
    # --- ANIMATED PLOT RENDERING ---
    plot_placeholder = st.empty()
    
    if play_anim:
        line, = ax.plot([], [], color=plt_line, linewidth=3, label="Efficiency Curve")
        
        # Determine frame step based on selected speed
        step = max(1, int(3 * anim_speed))
        sleep_time = 0.02 / anim_speed
        
        for i in range(1, len(k_vals) + 1, step):
            line.set_data(k_vals[:i], savings_vals[:i])
            
            # Draw vertical line when reaching the end of the animation
            if i >= len(k_vals) - step:
                ax.axvline(x=k_ratio, color="#FF0055", linestyle="--", linewidth=2, label=f"Selected k: {k_ratio:.2f}")
                ax.legend(frameon=False, labelcolor=plt_text)
                
            plot_placeholder.pyplot(fig)
            time.sleep(sleep_time)
            
        # Ensure final state is drawn cleanly
        line.set_data(k_vals, savings_vals)
        plot_placeholder.pyplot(fig)
    else:
        # Static rendering if animation is disabled
        ax.plot(k_vals, savings_vals, color=plt_line, linewidth=3, label="Efficiency Curve")
        ax.axvline(x=k_ratio, color="#FF0055", linestyle="--", linewidth=2, label=f"Selected k: {k_ratio:.2f}")
        ax.legend(frameon=False, labelcolor=plt_text)
        plot_placeholder.pyplot(fig)

    # --- MANUAL VERIFICATION & SYMBOLS ---
    st.markdown("---")
    
    with st.expander("✅ Manual (paper) vs app check"):
        st.markdown("""
        **Test problem:** Transmitted power of 50 kW at 1500 RPM with an allowable shear stress of 50 MPa. Hollow ratio k = 0.5.
        
        | Quantity | Manual (paper) | This app's formulas |
        | :--- | :--- | :--- |
        | Required Torque T (N·m) | 318.31 | 318.31 |
        | Solid Shaft Dia D (mm) | 31.89 | 31.89 |
        | Hollow Outer Dia D_o (mm) | 32.58 | 32.58 |
        | Weight Savings (%) | 21.72 | 21.72 |
        
        *Calculation verify:* $T = (50 \times 60000) / (2 \pi \times 1500) = 318.31$ N·m. $D = ((16 \times 318.31) / (\pi \times 50 \times 10^6))^{1/3} \times 1000 = 31.89$ mm.
        """)

    st.markdown("### Symbols & Meanings")
    st.markdown("""
    | Symbol | Meaning | Unit |
    | :--- | :--- | :--- |
    | **P** | Transmitted Power | kW |
    | **N** | Shaft Speed | RPM |
    | **τ** (tau) | Allowable Shear Stress | MPa |
    | **T** | Required Torque | N·m |
    | **D** | Solid Shaft Diameter | mm |
    | **D_o** | Hollow Shaft Outer Diameter | mm |
    | **d_i** | Hollow Shaft Inner Diameter | mm |
    | **k** | Hollow Ratio (Inner / Outer) | dimensionless |
    """)