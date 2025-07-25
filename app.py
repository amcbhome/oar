import streamlit as st

st.title("ACCA Overhead Absorption Calculator & Explainer")
st.write("An interactive tool to understand and calculate overhead absorption, based on the ACCA F2/MA and PM syllabus.")

st.header("1. Input Budgeted Data")
st.write("Enter your company's planned financial and operational figures.")

# --- Input Section ---
col1, col2, col3 = st.columns(3)

with col1:
    budgeted_fixed_oh = st.number_input(
        "Budgeted Fixed Overheads ($)", 
        min_value=0, 
        value=120000,
        step=1000
    )
with col2:
    budgeted_activity_level = st.number_input(
        "Budgeted Activity Level (e.g., Machine Hours)", 
        min_value=1, 
        value=30000,
        step=100
    )
with col3:
    budgeted_units = st.number_input(
        "Budgeted Units of Production", 
        min_value=1, 
        value=20000,
        step=100
    )

st.header("2. Input Actual Data")
st.write("Enter the figures for the actual period.")

col4, col5, col6 = st.columns(3)
with col4:
    actual_fixed_oh = st.number_input(
        "Actual Fixed Overheads ($)", 
        min_value=0, 
        value=125000,
        step=1000
    )
with col5:
    actual_activity_level = st.number_input(
        "Actual Activity Level (e.g., Machine Hours)", 
        min_value=1, 
        value=31000,
        step=100
    )
with col6:
    actual_units = st.number_input(
        "Actual Units of Production", 
        min_value=1, 
        value=21000,
        step=100
    )

st.divider()

# --- Calculations Section ---
st.header("3. Calculations & Results")
st.write("Here are the step-by-step calculations, just like you would perform in an ACCA exam.")

try:
    # Calculation 1: Overhead Absorption Rate (OAR)
    oar_per_activity = budgeted_fixed_oh / budgeted_activity_level
    st.subheader("Step 3a: Overhead Absorption Rate (OAR)")
    st.metric(
        label="OAR per Activity Unit",
        value=f"${oar_per_activity:,.2f} per hour",
        help="This is the predetermined rate for absorbing overheads. It's calculated using budgeted figures."
    )
    st.latex(f"OAR = \\frac{{\\text{{Budgeted Fixed Overheads}}}}{{\\text{{Budgeted Activity Level}}}} = \\frac{{\\${budgeted_fixed_oh:,}}}{{\\text{{{budgeted_activity_level:,} hours}}}} = \\${oar_per_activity:,.2f}")
    
    # Calculation 2: Total Absorbed Overheads
    absorbed_oh = actual_activity_level * oar_per_activity
    st.subheader("Step 3b: Total Absorbed Overheads")
    st.metric(
        label="Total Overheads Absorbed",
        value=f"${absorbed_oh:,.2f}",
        help="The amount of overheads charged to production, based on actual activity and the OAR."
    )
    st.latex(f"\\text{{Absorbed Overheads}} = \\text{{Actual Activity}} \\times \\text{{OAR}} = \\text{{{actual_activity_level:,} hours}} \\times \\${oar_per_activity:,.2f} = \\${absorbed_oh:,.2f}")

    # Calculation 3: Over or Under Absorption
    over_under_absorption = absorbed_oh - actual_fixed_oh
    st.subheader("Step 3c: Over/Under Absorption")
    
    if over_under_absorption > 0:
        st.success(f"Over-absorbed Overheads: ${over_under_absorption:,.2f}")
        st.write("This is a favorable result, as more overheads were absorbed than were actually incurred.")
    elif over_under_absorption < 0:
        st.error(f"Under-absorbed Overheads: ${-over_under_absorption:,.2f}")
        st.write("This is an adverse result, as fewer overheads were absorbed than were actually incurred.")
    else:
        st.info("Exactly absorbed overheads. No variance.")
    
    st.latex(f"\\text{{Over/Under Absorption}} = \\text{{Absorbed Overheads}} - \\text{{Actual Overheads}} = \\${absorbed_oh:,.2f} - \\${actual_fixed_oh:,} = \\${over_under_absorption:,.2f}")

    # --- Variance Analysis (ACCA PM) ---
    st.header("4. ACCA PM Variance Analysis")
    st.write("The total over/under absorption can be split into two key variances.")

    # Variance 1: Fixed Overhead Expenditure Variance
    expenditure_variance = budgeted_fixed_oh - actual_fixed_oh
    if expenditure_variance >= 0:
        exp_emoji = "🎉"
        exp_text = "Favorable"
    else:
        exp_emoji = "😔"
        exp_text = "Adverse"

    st.subheader("Expenditure Variance")
    st.write(f"The variance due to a difference between budgeted and actual spending on overheads.")
    st.metric(
        label=f"Fixed Overhead Expenditure Variance",
        value=f"${abs(expenditure_variance):,.2f}",
        delta_color="normal",
        delta=exp_text
    )

    # Variance 2: Fixed Overhead Volume Variance
    oar_per_unit = budgeted_fixed_oh / budgeted_units
    volume_variance = (actual_units - budgeted_units) * oar_per_unit
    if volume_variance >= 0:
        vol_emoji = "🎉"
        vol_text = "Favorable"
    else:
        vol_emoji = "😔"
        vol_text = "Adverse"

    st.subheader("Volume Variance")
    st.write(f"The variance due to producing more or fewer units than budgeted.")
    st.metric(
        label=f"Fixed Overhead Volume Variance",
        value=f"${abs(volume_variance):,.2f}",
        delta_color="normal",
        delta=vol_text
    )

    # Reconciliation
    st.subheader("Reconciliation")
    st.write("The two variances should reconcile with the total over/under absorption.")
    st.info(f"Total Variance = Expenditure Variance + Volume Variance")
    st.info(f"${over_under_absorption:,.2f} = ${expenditure_variance:,.2f} + ${volume_variance:,.2f}")

except (ZeroDivisionError, ValueError):
    st.error("Please ensure all input values are greater than zero to perform calculations.")

