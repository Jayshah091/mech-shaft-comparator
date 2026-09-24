import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Shaft Design Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME TOGGLE & CONTROLS ---
with st.sidebar:
    is_dark = st.toggle("Dark Mode", value=True)
    st.markdown("---")
    
    st.markdown("### Design Parameters")
    power_kw = st.number_input("Power (kW)", min_value=0.0, max_value=1000.0, value=50.0, step=1.0)
    rpm = st.number_input("Speed (RPM)", min_value=0.0, max_value=5000.0, value=1500.0, step=50.0)
    tau_mpa = st.number_input("Allowable Shear Stress (MPa)", min_value=0.0, max_value=300.0, value=50.0, step=5.0)
    
    st.markdown("### Geometry")
    k_ratio = st.slider("Hollow Ratio (Inner/Outer)", min_value=0.1, max_value=0.9, value=0.5, step=0.05)
    
    st.markdown("### Economics")
    cost_per_kg = st.number_input("Material Cost (INR/kg)", min_value=10.0, max_value=500.0, value=85.0, step=5.0)
    
    st.markdown("---")
    st.markdown("### Animation Controls")
    play_anim = st.checkbox("Play Synchronized Animation", value=True)
    anim_speed = st.slider("Animation Speed", min_value=0.1, max_value=2.0, value=1.0, step=0.1)

# --- DYNAMIC THEME VARIABLES ---
if is_dark:
    app_bg = "#0e1117"
    metric_val = "#00E5FF"
    metric_label = "#8fa6b8"
    card_bg = "#161b22"
    card_border = "#30363d"
    sidebar_glow = "rgba(255, 255, 255, 0.1)"
    plt_style = "dark_background"
    plt_line = "#00E5FF"
    plt_grid = "#ffffff"
    plt_text = "#8fa6b8"
    plt_spine = "#30363d"
    hero_bg = "#0d1117"
    hero_border = "#30363d"
    hero_text = "#ffffff"
    hero_subtext = "#8fa6b8"
    wave_color = "#00E5FF"
    shaft_color = "#00E5FF"
else:
    app_bg = "#ffffff"
    metric_val = "#0ea5e9"
    metric_label = "#64748b"
    card_bg = "#ffffff"
    card_border = "#e2e8f0"
    sidebar_glow = "rgba(0, 0, 0, 0.1)"
    plt_style = "default"
    plt_line = "#0ea5e9"
    plt_grid = "#000000"
    plt_text = "#64748b"
    plt_spine = "#e2e8f0"
    hero_bg = "#f8fafc"
    hero_border = "#e2e8f0"
    hero_text = "#0f172a"
    hero_subtext = "#64748b"
    wave_color = "#0ea5e9"
    shaft_color = "#0ea5e9"

# 2. Custom CSS Injection (Mobile Responsive & Clean)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    
    footer {{visibility: hidden;}}
    
    /* RESTORE MOBILE MENU TOGGLE */
    header {{
        background-color: transparent !important;
    }}
    /* Hide only the right-side Streamlit deploy/settings menu to keep the app looking custom */
    [data-testid="stHeaderActionElements"] {{
        visibility: hidden;
    }}
    
    /* Premium Floating Metric Cards */
    div[data-testid="metric-container"] {{
        background-color: {card_bg};
        border: 1px solid {card_border};
        padding: 1.5rem 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
        border-color: {metric_val};
    }}
    
    div[data-testid="stMetricValue"] {{
        font-size: 2.2rem;
        color: {metric_val};
        font-weight: 800;
        line-height: 1.2;
    }}
    div[data-testid="stMetricLabel"] {{
        font-size: 0.95rem;
        color: {metric_label};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }}
    
    [data-testid="stSidebar"] {{
        border-right: 1px solid {sidebar_glow};
    }}

    /* Mobile Responsiveness */
    @media (max-width: 768px) {{
        div[data-testid="stMetricValue"] {{
            font-size: 1.8rem;
        }}
        .hero-title {{
            font-size: 1.8rem !important;
        }}
        div[data-testid="metric-container"] {{
            padding: 1rem;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# --- PREMIUM HERO HEADER ---
hero_card = f"""
<div style="background-color: {hero_bg}; padding: 2.5rem 2.5rem 4rem 2.5rem; border-radius: 16px; margin-bottom: 2.5rem; position: relative; overflow: hidden; border: 1px solid {hero_border}; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
    <h1 class="hero-title" style="color: {hero_text}; margin-top: 0; font-size: 2.7rem; font-weight: 800; letter-spacing: -0.02em;">Torsion & Power Transmission Analyzer</h1>
    <div style="color: {hero_subtext}; font-size: 1.05rem; line-height: 1.7; margin-top: 12px; font-weight: 400;">
        <strong>Group:</strong> 4 | <strong>Members:</strong> [Shah Jay .G] (25012250610002) <br>
        Diploma in Mechanical Engineering (Sem 3) | <strong>Institution:</strong> LJ Polytechnic
    </div>
    <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 45px; line-height: 0;">
        <svg viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" style="display: block; width: 100%; height: 100%;">
            <path fill="{wave_color}" fill-opacity="0.8" d="M0,224L80,213.3C160,203,320,181,480,181.3C640,181,800,203,960,197.3C1120,192,1280,160,1360,144L1440,128L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z"></path>
        </svg>
    </div>
</div>
"""
st.markdown(hero_card, unsafe_allow_html=True)

# Validation
if power_kw == 0 or rpm == 0 or tau_mpa == 0:
    st.error("Warning: Power, RPM, and Shear Stress must be greater than zero.")
else:
    # Core Engineering Calculations
    torque_nm = (power_kw * 60 * 1000) / (2 * np.pi * rpm)
    tau_pa = tau_mpa * 10**6

    d_solid_m = ((16 * torque_nm) / (np.pi * tau_pa)) ** (1 / 3)
    d_solid_mm = d_solid_m * 1000

    d_outer_m = ((16 * torque_nm) / (np.pi * tau_pa * (1 - k_ratio**4))) ** (1 / 3)
    d_outer_mm = d_outer_m * 1000
    d_inner_mm = d_outer_mm * k_ratio

    area_solid_mm2 = (np.pi / 4) * (d_solid_mm**2)
    area_hollow_mm2 = (np.pi / 4) * (d_outer_mm**2 - d_inner_mm**2)
    weight_savings_pct = (1 - (area_hollow_mm2 / area_solid_mm2)) * 100

    # Economics & Mass Estimator (7850 kg/m^3 for steel)
    steel_density = 7850
    mass_solid_kg_m = (area_solid_mm2 / 1e6) * steel_density
    mass_hollow_kg_m = (area_hollow_mm2 / 1e6) * steel_density
    mass_saved = mass_solid_kg_m - mass_hollow_kg_m
    cost_saved_inr = mass_saved * cost_per_kg

    # Dashboard Metrics UI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Solid Dia (D)", value=f"{d_solid_mm:.1f} mm", delta=f"{torque_nm:.1f} N.m Torque", delta_color="off")
    with col2:
        st.metric(label="Hollow Outer (D_o)", value=f"{d_outer_mm:.1f} mm", delta=f"Inner (d_i): {d_inner_mm:.1f} mm", delta_color="off")
    with col3:
        st.metric(label="Mass & Cost Saved", value=f"INR {cost_saved_inr:.0f} /m", delta=f"{mass_saved:.1f} kg/m reduction", delta_color="normal")
    with col4:
        st.metric(label="Total Efficiency", value=f"{weight_savings_pct:.1f} %", delta="Material Savings", delta_color="normal")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- SPLIT VIEW CONTAINERS ---
    view_col1, view_col2 = st.columns([1.2, 1])
    
    with view_col1:
        st.markdown("### Efficiency Area Curve")
        plot_placeholder = st.empty()
        
    with view_col2:
        st.markdown("### CAD Cross-Section")
        cad_placeholder = st.empty()

    # --- Pre-calculate Graph Data ---
    k_vals = np.linspace(0.1, 0.85, 50)
    savings_vals = []
    for k in k_vals:
        do_temp_m = ((16 * torque_nm) / (np.pi * tau_pa * (1 - k**4))) ** (1 / 3)
        do_temp_mm = do_temp_m * 1000 
        di_temp_mm = do_temp_mm * k
        a_h = (np.pi / 4) * (do_temp_mm**2 - di_temp_mm**2)
        savings_vals.append((1 - (a_h / area_solid_mm2)) * 100)

    # --- Setup Graph Figure ---
    plt.style.use(plt_style) 
    fig_plot, ax_plot = plt.subplots(figsize=(8, 4.8))
    fig_plot.patch.set_alpha(0.0)
    ax_plot.patch.set_alpha(0.0)
    ax_plot.set_xlim(0.1, 0.85)
    ax_plot.set_ylim(0, max(savings_vals) + 5)
    ax_plot.ticklabel_format(useOffset=False, style='plain')
    ax_plot.set_xlabel("Hollow Ratio (k = Inner / Outer)", fontsize=11, color=plt_text, fontweight='bold')
    ax_plot.set_ylabel("Weight Savings (%)", fontsize=11, color=plt_text, fontweight='bold')
    ax_plot.grid(True, linestyle="--", color=plt_grid, alpha=0.1)
    ax_plot.spines['top'].set_visible(False)
    ax_plot.spines['right'].set_visible(False)
    ax_plot.spines['left'].set_color(plt_spine)
    ax_plot.spines['bottom'].set_color(plt_spine)
    ax_plot.tick_params(colors=plt_text)

    # Static faint background of full curve
    ax_plot.plot(k_vals, savings_vals, color=plt_line, linewidth=1.5, alpha=0.3)
    
    # Active plot elements to be updated
    active_line, = ax_plot.plot([], [], color=plt_line, linewidth=3.5)
    active_fill = None
    active_vline = ax_plot.axvline(x=0.1, color="#f43f5e", linestyle="--", linewidth=2.5, alpha=0)
    active_dot, = ax_plot.plot([], [], marker='o', color="#f43f5e", markersize=8, alpha=0)

    # --- Setup CAD Figure ---
    fig_circ, ax_circ = plt.subplots(figsize=(6, 4.8))
    fig_circ.patch.set_alpha(0.0)
    ax_circ.patch.set_alpha(0.0)
    
    r_solid = d_solid_mm / 2
    r_outer = d_outer_mm / 2
    r_inner = d_inner_mm / 2
    center_1 = 0
    center_2 = r_outer * 2.5 
    
    ax_circ.axhline(0, color=plt_text, linestyle='-.', linewidth=1, alpha=0.5, zorder=0)
    ax_circ.axvline(center_1, color=plt_text, linestyle='-.', linewidth=1, alpha=0.5, zorder=0)
    ax_circ.axvline(center_2, color=plt_text, linestyle='-.', linewidth=1, alpha=0.5, zorder=0)
    
    circle_solid = plt.Circle((center_1, 0), r_solid, color=shaft_color, alpha=0.2, ec=shaft_color, lw=2.5, zorder=2)
    circle_outer = plt.Circle((center_2, 0), r_outer, color=shaft_color, alpha=0.2, ec=shaft_color, lw=2.5, zorder=2)
    circle_inner = plt.Circle((center_2, 0), 0.001, color=app_bg, ec=shaft_color, lw=2.5, zorder=3) 
    
    ax_circ.add_patch(circle_solid)
    ax_circ.add_patch(circle_outer)
    ax_circ.add_patch(circle_inner)
    
    ax_circ.set_aspect('equal')
    ax_circ.set_xlim(-r_outer*1.5, center_2 + r_outer*1.5)
    ax_circ.set_ylim(-r_outer*1.5, r_outer*1.5)
    ax_circ.axis('off')
    
    ax_circ.text(center_1, -r_outer*1.35, f"Solid Section\nØ {d_solid_mm:.1f}", color=plt_text, ha='center', fontsize=11, fontweight='bold')
    txt_cad_hollow = ax_circ.text(center_2, -r_outer*1.35, f"Hollow Section\nExt Ø {d_outer_mm:.1f} | Int Ø 0.0", color=plt_text, ha='center', fontsize=11, fontweight='bold')

    # --- SYNCHRONIZED ANIMATION ENGINE ---
    active_k = k_vals[k_vals <= k_ratio]
    active_sav = savings_vals[:len(active_k)]
    if len(active_k) == 0 or active_k[-1] < k_ratio:
        active_k = np.append(active_k, k_ratio)
        active_sav = np.append(active_sav, np.interp(k_ratio, k_vals, savings_vals))

    if play_anim:
        frames = max(10, int(25 * anim_speed))
        sleep_time = 0.015 / anim_speed
        frame_k = np.linspace(0.1, k_ratio, frames)
        frame_sav = np.interp(frame_k, k_vals, savings_vals)
        
        active_vline.set_alpha(1)
        active_dot.set_alpha(1)
        
        for i in range(frames):
            cur_k = frame_k[i]
            cur_sav = frame_sav[i]
            
            # 1. Physics Engine: Calculate required outer dia dynamically for this frame
            cur_d_outer = (((16 * torque_nm) / (np.pi * tau_pa * (1 - cur_k**4))) ** (1 / 3)) * 1000
            cur_d_inner = cur_d_outer * cur_k
            
            # 2. Update CAD
            circle_outer.set_radius(cur_d_outer / 2)
            circle_inner.set_radius(max(0.001, cur_d_inner / 2))
            txt_cad_hollow.set_text(f"Hollow Section\nExt Ø {cur_d_outer:.1f} | Int Ø {cur_d_inner:.1f}")
            
            # 3. Update Graph
            active_line.set_data(frame_k[:i+1], frame_sav[:i+1])
            if active_fill is not None:
                active_fill.remove()
            active_fill = ax_plot.fill_between(frame_k[:i+1], 0, frame_sav[:i+1], color=plt_line, alpha=0.15)
            active_vline.set_xdata([cur_k, cur_k])
            active_dot.set_data([cur_k], [cur_sav])
            
            # Render sync
            plot_placeholder.pyplot(fig_plot, use_container_width=True)
            cad_placeholder.pyplot(fig_circ, use_container_width=True)
            time.sleep(sleep_time)

    # Ensure Final Static State is Perfectly Precise
    circle_outer.set_radius(r_outer)
    circle_inner.set_radius(r_inner)
    txt_cad_hollow.set_text(f"Hollow Section\nExt Ø {d_outer_mm:.1f} | Int Ø {d_inner_mm:.1f}")

    active_line.set_data(active_k, active_sav)
    if active_fill is not None:
        active_fill.remove()
    ax_plot.fill_between(active_k, 0, active_sav, color=plt_line, alpha=0.15)
    
    active_vline.set_alpha(1)
    active_vline.set_xdata([k_ratio, k_ratio])
    active_vline.set_label(f"Selected k: {k_ratio:.2f}")
    
    active_dot.set_alpha(1)
    active_dot.set_data([k_ratio], [active_sav[-1]])
    ax_plot.legend(frameon=False, labelcolor=plt_text, loc="upper left")

    plot_placeholder.pyplot(fig_plot, use_container_width=True)
    cad_placeholder.pyplot(fig_circ, use_container_width=True)

    # --- DOCUMENTATION & EXPORT ---
    st.markdown("---")
    
    with st.expander("Step-by-step working (for report & viva)"):
        st.markdown("**1. Torque Transmitted ($T$)**")
        st.latex(rf"T = \frac{{P \times 60 \times 1000}}{{2 \pi N}} = \frac{{{power_kw} \times 60000}}{{2 \pi \times {rpm}}} = {torque_nm:.2f} \text{{ N.m}}")
        
        st.markdown("**2. Solid Shaft Diameter ($D$)**")
        st.latex(rf"D = \left( \frac{{16 T}}{{\pi \tau}} \right)^{{1/3}} = {d_solid_mm:.2f} \text{{ mm}}")
        
        st.markdown("**3. Hollow Shaft Outer Diameter ($D_o$)**")
        st.latex(rf"D_o = \left( \frac{{16 T}}{{\pi \tau (1 - k^4)}} \right)^{{1/3}} = {d_outer_mm:.2f} \text{{ mm}}")
        
        st.markdown("**4. Weight Savings**")
        st.latex(rf"\% \text{{ Savings}} = \left( 1 - \frac{{A_{{hollow}}}}{{A_{{solid}}}} \right) \times 100 = {weight_savings_pct:.2f}\%")

    with st.expander("Manual (paper) vs app check"):
        st.markdown(r"""
        **Test problem:** Transmitted power of 50 kW at 1500 RPM with an allowable shear stress of 50 MPa. Hollow ratio k = 0.5.
        
        | Quantity | Manual (paper) | This app's formulas |
        | :--- | :--- | :--- |
        | Required Torque T (N.m) | 318.31 | 318.31 |
        | Solid Shaft Dia D (mm) | 31.89 | 31.89 |
        | Hollow Outer Dia D_o (mm) | 32.58 | 32.58 |
        | Weight Savings (%) | 21.72 | 21.72 |
        
        *Calculation verify:* $T = (50 \times 60000) / (2 \pi \times 1500) = 318.31$ N.m. $D = ((16 \times 318.31) / (\pi \times 50 \times 10^6))^{1/3} \times 1000 = 31.89$ mm.
        """)

    st.markdown("### Symbols & Meanings")
    st.markdown("""
    | Symbol | Meaning | Unit |
    | :--- | :--- | :--- |
    | **P** | Transmitted Power | kW |
    | **N** | Shaft Speed | RPM |
    | **τ** (tau) | Allowable Shear Stress | MPa |
    | **T** | Required Torque | N.m |
    | **D** | Solid Shaft Diameter | mm |
    | **D_o** | Hollow Shaft Outer Diameter | mm |
    | **d_i** | Hollow Shaft Inner Diameter | mm |
    | **k** | Hollow Ratio (Inner / Outer) | dimensionless |
    """)

    st.markdown("### Export Design Data")
    
    csv_data = f"""Parameter,Value,Unit
Transmitted Power,{power_kw},kW
Shaft Speed,{rpm},RPM
Allowable Shear Stress,{tau_mpa},MPa
Hollow Ratio (k),{k_ratio},-
Required Torque,{torque_nm:.2f},N.m
Solid Shaft Diameter,{d_solid_mm:.2f},mm
Hollow Outer Diameter,{d_outer_mm:.2f},mm
Hollow Inner Diameter,{d_inner_mm:.2f},mm
Solid Shaft Mass,{mass_solid_kg_m:.2f},kg/m
Hollow Shaft Mass,{mass_hollow_kg_m:.2f},kg/m
Weight Savings,{weight_savings_pct:.2f},%
Financial Savings,INR {cost_saved_inr:.2f},INR/m
"""
    
    st.download_button(
        label="Download Engineering Report (.CSV)",
        data=csv_data,
        file_name=f"shaft_design_report_k{k_ratio}.csv",
        mime="text/csv",
        help="Export current calculated parameters for Excel or CAD reference."
    )