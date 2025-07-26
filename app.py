import streamlit as st

st.set_page_config(
    page_title="UK GAAP (FRS 102) Inventory Valuation Tool",
    layout="wide"
)

st.title("UK GAAP (FRS 102) Inventory Valuation Tool")
st.markdown("""
A professional tool for preparing finished goods inventory valuation, with audit considerations in mind. This model adheres to the principles of **FRS 102** for cost determination and provides a clear audit trail as required by **ISA (UK) 500**.
""")

st.subheader("Accountant's Rationale and Method Selection")
st.markdown("""
As per **FRS 102, Section 13**, inventory must be valued at the lower of cost and net realisable value. The 'cost' of finished goods includes all costs of purchase, costs of conversion, and other costs incurred in bringing the inventories to their present location and condition. This model focuses on the cost of conversion by systematically absorbing production overheads.

The selected overhead absorption basis (e.g., machine hours, labor hours) must be **'systematic and rational'** to be compliant.
""")

# --- Step 1: Define Cost Components ---
st.header("1. Input Direct Costs (Cost Per Unit)")
st.write("Enter the prime cost components for a single unit of production.")
col1, col2 = st.columns(2)
with col1:
    direct_materials = st.number_input(
        "Direct Materials per Unit ($)", 
        min_value=0.0, 
        value=10.00,
        step=0.01
    )
with col2:
    direct_labour = st.number_input(
        "Direct Labour per Unit ($)", 
        min_value=0.0, 
        value=15.00,
        step=0.01
    )

st.subheader("Prime Cost")
prime_cost = direct_materials + direct_labour
st.metric("Prime Cost per Unit", f"${prime_cost:,.2f}")

# --- Step 2: Overhead Absorption Parameters ---
st.header("2. Overhead Absorption Parameters")
st.write("Determine the Overhead Absorption Rate (OAR) using budgeted figures.")
col3, col4, col5 = st.columns(3)
with col3:
    budgeted_oh = st.number_input(
        "Budgeted Production Overheads ($)", 
        min_value=0, 
        value=120000,
        step=1000
    )
with col4:
    budgeted_activity = st.number_input(
        "Budgeted Activity Level (e.g., Machine Hours)", 
        min_value=1, 
        value=30000,
        step=100
    )
with col5:
    activity_type = st.selectbox(
        "Activity Type",
        options=["Machine Hours", "Direct Labour Hours", "Units Produced"]
    )
st.markdown(f"**Justification:** The use of {activity_type} as the absorption basis is considered **'systematic and rational'** as it is a primary driver of the overhead costs in the production process.")

# --- Calculations ---
try:
    oar = budgeted_oh / budgeted_activity
    st.subheader("Calculated Overhead Absorption Rate (OAR)")
    st.metric("OAR", f"${oar:,.2f} per {activity_type.lower()}")
    
    st.latex(f"OAR = \\frac{{\\text{{Budgeted Overheads}}}}{{\\text{{Budgeted Activity}}}} = \\frac{{\\${budgeted_oh:,}}}{{\\text{{{budgeted_activity:,} {activity_type.lower()}}}}} = \\${oar:,.2f}")

    # --- Step 3: Inventory & Valuation ---
    st.header("3. Inventory Valuation")
    st.write("Input the final production figures and closing inventory count.")
    col6, col7, col8 = st.columns(3)
    with col6:
        activity_per_unit = st.number_input(
            f"{activity_type} per Unit", 
            min_value=0.0, 
            value=1.5,
            step=0.1
        )
    with col7:
        closing_inventory = st.number_input(
            "Closing Finished Goods Inventory (Units)", 
            min_value=0, 
            value=1000,
            step=10
        )
    with col8:
        st.write("---")
        absorbed_oh_per_unit = oar * activity_per_unit
        total_full_cost_per_unit = prime_cost + absorbed_oh_per_unit
        st.metric("Full Cost Per Unit", f"${total_full_cost_per_unit:,.2f}")

    st.divider()

    st.header("4. Final Inventory Valuation for Financial Statements")
    total_inventory_value = closing_inventory * total_full_cost_per_unit
    st.success(f"**Total Closing Inventory Value: ${total_inventory_value:,.2f}**")
    
    st.markdown("""
        **Audit Documentation:** This figure is to be reported in the Statement of Financial Position (Balance Sheet). As per **ISA (UK) 500**, this calculation provides the audit evidence for the valuation of finished goods inventory. The consistent application of a 'systematic and rational' absorption basis satisfies the auditor's requirement for a reliable cost figure.
    """)

    # --- Over/Under Absorption Check for Audit Trail ---
    st.header("5. Audit Check: Over/Under Absorption")
    st.write("A critical step to reconcile total overheads and identify potential material variances.")
    col9, col10 = st.columns(2)
    with col9:
        actual_oh = st.number_input(
            "Actual Total Production Overheads ($)", 
            min_value=0, 
            value=125000,
            step=1000
        )
    with col10:
        actual_activity = st.number_input(
            f"Actual Total {activity_type}", 
            min_value=0, 
            value=31000,
            step=100
        )
    
    absorbed_oh_total = actual_activity * oar
    over_under_absorption = absorbed_oh_total - actual_oh
    
    if over_under_absorption > 0:
        st.info(f"**Total Over-Absorbed Overheads:** ${over_under_absorption:,.2f}")
        st.write("This indicates the company absorbed more overheads than were actually incurred. This is generally a favourable variance.")
    elif over_under_absorption < 0:
        st.warning(f"**Total Under-Absorbed Overheads:** ${-over_under_absorption:,.2f}")
        st.write("This indicates the company absorbed fewer overheads than were actually incurred. This is an adverse variance.")
    else:
        st.info("No over or under absorption.")
        
    st.markdown("""
        **Required Audit Action:** Any material over/under absorption variance must be investigated. The figure is typically taken to the Statement of Profit or Loss as an adjustment to the cost of sales.
    """)
    st.latex(f"\\text{{Under/Over Absorption}} = (\\text{{Actual Activity}} \\times OAR) - \\text{{Actual Overheads}}")
    st.latex(f"= (\\text{{{actual_activity:,}}} \\times \\${oar:,.2f}) - \\${actual_oh:,} = \\${over_under_absorption:,.2f}")


except (ZeroDivisionError, ValueError):
    st.error("Please ensure all input values are greater than zero to perform calculations.")
