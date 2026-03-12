import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Nigerian Construction AI",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Nigerian Construction AI Predictor")
st.markdown("**Machine learning models for predicting construction delays, material requirements, costs, and project risks**")

# ---------------------------
# Load Options from API
# ---------------------------
@st.cache_data
def get_options():
    try:
        response = requests.get(f"{API_URL}/options")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

options = get_options()

if options is None:
    st.error("Cannot connect to API. Please ensure the backend is running.")
    st.stop()

# ---------------------------
# Tabs
# ---------------------------
tab1, tab2 = st.tabs(["⏱️ Delay Prediction", "🧱 Material Requirements"])

# ---------------------------
# TAB 1: Delay Prediction
# ---------------------------
with tab1:
    st.header("Project Delay Prediction")
    st.markdown("Predict potential delays based on project characteristics and Nigerian market conditions.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Project Details")
        built_up_area = st.number_input("Built-up Area (m²)", min_value=50, max_value=2000, value=200, key="built_up_area")
        plot_size = st.number_input("Plot Size (m²)", min_value=100, max_value=5000, value=400, key="plot_size")
        number_of_floors = st.selectbox("Number of Floors", [1,2,3,4], index=1, key="floors")
        building_type = st.selectbox("Building Type", options["building_types"], key="building_type")
    
    with col2:
        st.subheader("Location & Timeline")
        state = st.selectbox("State", options["states"], key="state")
        area_type = st.selectbox("Area Type", options["area_types"], key="area_type")
        start_season = st.selectbox("Start Season", options["seasons"], key="start_season")
        planned_days = st.number_input("Planned Completion (days)", min_value=30, max_value=1000, value=240, key="planned_days")
    
    with col3:
        st.subheader("Specifications & Budget")
        foundation_type = st.selectbox("Foundation Type", options["foundation_types"], key="foundation_type")
        roof_type = st.selectbox("Roof Type", options["roof_types"], key="roof_type")
        finishing_quality = st.selectbox("Finishing Quality", options["finishing_qualities"], key="finishing_quality")
        initial_budget = st.number_input("Initial Budget (₦)", min_value=1000000, max_value=500000000, value=20000000, step=1000000, key="initial_budget")
    
    col4, col5 = st.columns(2)
    with col4:
        contractor_exp = st.selectbox("Contractor Experience", options["contractor_experiences"], key="contractor_exp")
    with col5:
        pm_experience = st.number_input("Project Manager Experience (years)", min_value=0, max_value=40, value=5, key="pm_experience")

    if st.button("🔮 Predict Delay", type="primary", use_container_width=True, key="predict_delay_btn"):
        payload = {
            "built_up_area_m2": built_up_area,
            "plot_size_m2": plot_size,
            "number_of_floors": number_of_floors,
            "planned_completion_days": planned_days,
            "initial_budget_naira": initial_budget,
            "project_manager_experience_years": pm_experience,
            "state": state,
            "area_type": area_type,
            "building_type": building_type,
            "foundation_type": foundation_type,
            "roof_type": roof_type,
            "finishing_quality": finishing_quality,
            "start_season": start_season,
            "contractor_experience": contractor_exp
        }

        with st.spinner("Analyzing project parameters..."):
            try:
                response = requests.post(f"{API_URL}/predict-delay", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Prediction Complete!")

                    # KPI Metrics
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Planned Duration", f"{planned_days} days")
                    with col_b:
                        st.metric("Expected Delay", f"{result['predicted_delay_days']} days", delta=f"{result['predicted_delay_days']}")
                    with col_c:
                        st.metric("Total Expected Duration", f"{result['expected_completion_days']} days")

                    # Delay Risk
                    delay_percentage = (result['predicted_delay_days'] / planned_days) * 100
                    if delay_percentage < 10:
                        st.info("✨ Low delay risk - Good project conditions!")
                    elif delay_percentage < 25:
                        st.warning("⚠️ Moderate delay risk - Plan for contingencies")
                    else:
                        st.error("🚨 High delay risk - Consider project optimization")

                    # Smart Construction Advisor
                    st.subheader("🧠 Smart Construction Advisor")
                    for tip in result.get("advisor_recommendations", []):
                        st.info(tip)

                    # Simple Cost Estimation
                    material_prices = {
                        "cement_bags": 7500,
                        "blocks_quantity": 350,
                        "sand_tons": 7000,
                        "granite_tons": 9000,
                        "steel_kg": 1200
                    }
                    st.subheader("💰 Estimated Material Cost (Approx.)")
                    if 'material_predictions' in result:
                        total_cost = 0
                        for m, qty in result['material_predictions'].items():
                            cost = qty * material_prices.get(m, 0)
                            total_cost += cost
                            st.write(f"{m.replace('_', ' ').title()}: ₦{cost:,.0f}")
                        st.success(f"Estimated Total Material Cost: ₦{total_cost:,.0f}")

                    # ---------------------------
                    # Delay Reduction Simulator
                    # ---------------------------
                    st.subheader("🕹️ Delay Reduction Simulator")
                    st.markdown("Adjust parameters below to see how predicted delay changes:")

                    sim_contractors = st.selectbox(
                        "Contractor Experience (Simulator)", 
                        options["contractor_experiences"], 
                        index=options["contractor_experiences"].index(contractor_exp),
                        key="sim_contractor"
                    )

                    sim_start_season = st.selectbox(
                        "Start Season (Simulator)", 
                        options["seasons"], 
                        index=options["seasons"].index(start_season),
                        key="sim_season"
                    )

                    sim_pm_experience = st.slider(
                        "Project Manager Experience (years) (Simulator)", 
                        0, 40, pm_experience,
                        key="sim_pm"
                    )

                    # Simulator payload
                    sim_payload = payload.copy()
                    sim_payload["contractor_experience"] = sim_contractors
                    sim_payload["start_season"] = sim_start_season
                    sim_payload["project_manager_experience_years"] = sim_pm_experience

                    if st.button("⚡ Simulate Delay Reduction", key="simulate_button"):
                        try:
                            sim_response = requests.post(f"{API_URL}/predict-delay", json=sim_payload)
                            if sim_response.status_code == 200:
                                sim_result = sim_response.json()
                                st.metric("Simulated Expected Delay", f"{sim_result['predicted_delay_days']} days")
                                st.metric("Simulated Total Duration", f"{sim_result['expected_completion_days']} days")
                                st.success("Simulation complete! Adjust parameters and try again.")
                            else:
                                st.error(f"Simulation Error: {sim_response.json().get('detail', 'Unknown error')}")
                        except Exception as e:
                            st.error(f"Connection error during simulation: {str(e)}")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

# ---------------------------
# TAB 2: Material Requirements
# ---------------------------
with tab2:
    st.header("Material Requirements Prediction")
    st.markdown("Estimate the quantity of materials needed for your construction project.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Project Specifications")
        m_built_up_area = st.number_input("Built-up Area (m²)", min_value=50, max_value=2000, value=200, key="mat_area")
        m_plot_size = st.number_input("Plot Size (m²)", min_value=100, max_value=5000, value=400, key="mat_plot")
        m_floors = st.selectbox("Number of Floors", [1,2,3,4], index=1, key="mat_floors")
        m_building_type = st.selectbox("Building Type", options["building_types"], key="mat_building")
    
    with col2:
        st.subheader("Construction Details")
        m_foundation = st.selectbox("Foundation Type", options["foundation_types"], key="mat_foundation")
        m_roof = st.selectbox("Roof Type", options["roof_types"], key="mat_roof")
        m_finishing = st.selectbox("Finishing Quality", options["finishing_qualities"], key="mat_finishing")

    if st.button("📊 Predict Materials", type="primary", use_container_width=True, key="predict_materials_btn"):
        payload = {
            "built_up_area_m2": m_built_up_area,
            "plot_size_m2": m_plot_size,
            "number_of_floors": m_floors,
            "building_type": m_building_type,
            "foundation_type": m_foundation,
            "roof_type": m_roof,
            "finishing_quality": m_finishing
        }

        with st.spinner("Calculating material requirements..."):
            try:
                response = requests.post(f"{API_URL}/predict-materials", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    materials = result["material_predictions"]

                    st.success("✅ Material Estimates Ready!")
                    st.subheader("📦 Required Materials")
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.metric("🏗️ Cement", f"{materials['cement_bags']:.0f} bags")
                        st.metric("🧱 Blocks", f"{materials['blocks_quantity']:.0f} units")
                    with col_m2:
                        st.metric("⛰️ Sand", f"{materials['sand_tons']:.1f} tons")
                        st.metric("🪨 Granite", f"{materials['granite_tons']:.1f} tons")
                    with col_m3:
                        st.metric("🔩 Steel", f"{materials['steel_kg']:.0f} kg")
                    st.divider()
                    st.info("💡 **Note:** These are estimates based on typical Nigerian construction standards. Actual requirements may vary based on specific design and site conditions.")

                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

# ---------------------------
# Footer
# ---------------------------
st.divider()
st.markdown("""
### About This Application
This AI-powered tool uses machine learning models trained on Nigerian construction data to:
- Predict potential project delays considering local factors (rainy seasons, location, contractor experience)
- Estimate material requirements for construction projects
- Estimate approximate material costs
- Calculate construction risk scores
- Provide smart advisor recommendations to reduce delays
- **Simulate changes to reduce project delays using the Delay Reduction Simulator**

**Factors Considered:**
- Nigerian weather patterns and rainy season impacts
- State-specific challenges (Lagos traffic, remote area logistics)
- Contractor and project manager experience
- Building specifications and quality levels
""")