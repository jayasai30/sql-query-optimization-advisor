
import streamlit as st
import pandas as pd

from advisor import analyze_sql_query


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SQL Query Optimization Advisor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM BACKGROUND AND UI DESIGN
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(
                circle at 10% 20%,
                rgba(0, 180, 255, 0.15),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 80%,
                rgba(120, 80, 255, 0.15),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #07111f 0%,
                #0b1728 45%,
                #10152b 100%
            );
        color: white;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        background-image:
            linear-gradient(
                rgba(0, 180, 255, 0.035) 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                rgba(0, 180, 255, 0.035) 1px,
                transparent 1px
            );
        background-size: 50px 50px;
        animation: gridMove 12s linear infinite;
        z-index: 0;
    }

    @keyframes gridMove {
        from {
            background-position: 0 0, 0 0;
        }
        to {
            background-position: 50px 50px, 50px 50px;
        }
    }

    .main .block-container {
        position: relative;
        z-index: 2;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        text-align: center;
        font-size: 42px !important;
        font-weight: 800 !important;
        letter-spacing: 1px;
        text-shadow:
            0 0 10px rgba(0, 180, 255, 0.5),
            0 0 25px rgba(120, 80, 255, 0.25);
    }

    h2, h3 {
        color: #e8f7ff !important;
        text-shadow: 0 0 8px rgba(0, 180, 255, 0.25);
    }

    p, label {
        color: #dcecff !important;
    }

    textarea, input {
        background-color: rgba(10, 25, 45, 0.90) !important;
        color: white !important;
        border: 1px solid rgba(0, 180, 255, 0.35) !important;
        border-radius: 10px !important;
    }

    textarea:focus, input:focus {
        border: 1px solid #00bfff !important;
        box-shadow: 0 0 10px rgba(0, 191, 255, 0.35) !important;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid rgba(0, 191, 255, 0.5);
        background: linear-gradient(90deg, #087ea4, #5b4bb7);
        color: white;
        font-size: 17px;
        font-weight: 700;
        padding: 0.65rem;
        transition: 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 18px rgba(0, 191, 255, 0.45);
    }

    [data-testid="stMetric"] {
        background: rgba(10, 28, 50, 0.75);
        border: 1px solid rgba(0, 191, 255, 0.20);
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.20);
        margin-bottom: 12px;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700;
    }

    [data-testid="stAlert"] {
        background-color: rgba(10, 30, 50, 0.82) !important;
        border-radius: 10px;
    }

    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(0, 191, 255, 0.20);
    }

    code {
        color: #8ee7ff !important;
    }

    .project-footer {
        text-align: center;
        margin-top: 35px;
        padding: 15px;
        color: #8faec7;
        font-size: 13px;
        border-top: 1px solid rgba(0, 191, 255, 0.15);
    }

    header[data-testid="stHeader"] {
        background-color: rgba(7, 17, 31, 0.95) !important;
        visibility: visible !important;
    }

    header[data-testid="stHeader"] * {
        visibility: visible !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TITLE
# =========================================================

st.title("🔍 SQL Query Optimization Advisor")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#a9c7df;
        font-size:17px;
        margin-bottom:25px;
    ">
        An ML-based system that analyzes SQL queries
        and provides optimization recommendations.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INPUT SECTION
# =========================================================

st.subheader("📝 Enter SQL Query")

query = st.text_area(
    "SQL Query",
    height=200,
    placeholder="""Example:

SELECT customer_name
FROM customers
WHERE city = 'Chennai';
"""
)

table_name = st.text_input(
    "Main Table Name",
    value="customers"
)


# =========================================================
# ANALYZE QUERY
# =========================================================

if st.button("🚀 Analyze Query", use_container_width=True):

    if not query.strip():
        st.warning("Please enter a SQL query.")

    elif not table_name.strip():
        st.warning("Please enter the main table name.")

    else:
        try:
            # ---------------------------------------------
            # CALL ADVISOR
            # ---------------------------------------------

            result = analyze_sql_query(query, table_name)

            # Temporary diagnostic
            st.write(
                "DEBUG: Number of returned values =",
                len(result)
            )

            if not isinstance(result, (tuple, list)):
                st.error(
                    "advisor.py did not return a tuple or list. "
                    f"Received: {type(result).__name__}"
                )
                st.stop()

            if len(result) != 7:
                st.error(
                    "Expected 7 values from advisor.py, "
                    f"but received {len(result)}."
                )
                st.stop()

            (
                features,
                ml_prediction,
                final_prediction,
                advice,
                suggested_sql,
                explain_result,
                database_status
            ) = result

            # ---------------------------------------------
            # QUERY ANALYSIS
            # ---------------------------------------------

            st.subheader("📊 Query Analysis")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("JOINs", features["joins"])
                st.metric(
                    "WHERE Conditions",
                    features["where_conditions"]
                )
                st.metric("Tables", features["table_count"])
                st.metric("Table Rows", features["table_size"])

            with col2:
                st.metric("ORDER BY", features["order_by"])
                st.metric("GROUP BY", features["group_by"])
                st.metric(
                    "Aggregate Functions",
                    features["aggregate_functions"]
                )
                st.metric("LIMIT", features["limit"])

            with col3:
                st.metric("SELECT *", features["select_all"])
                st.metric("Subquery", features["subquery"])
                st.metric(
                    "Index Available",
                    features["index_available"]
                )

            # ---------------------------------------------
            # ML PREDICTION
            # ---------------------------------------------

            st.subheader("🤖 Machine Learning Prediction")

            st.info(f"ML Model Prediction: {ml_prediction}")

            # ---------------------------------------------
            # FINAL RECOMMENDATION
            # ---------------------------------------------

            st.subheader("🎯 Final Optimization Recommendation")

            st.success(
                "Recommended Action: "
                f"**{str(final_prediction).replace('_', ' ')}**"
            )

            # ---------------------------------------------
            # ADVICE
            # ---------------------------------------------

            st.subheader("💡 Optimization Advice")
            st.write(advice)

            # ---------------------------------------------
            # SUGGESTED SQL
            # ---------------------------------------------

            st.subheader("🛠️ Suggested SQL or Action")

            st.code(
                suggested_sql,
                language="sql"
            )

            st.caption(
                "Review suggested SQL before using it. "
                "Examples may need adjustment for your database schema."
            )

            # ---------------------------------------------
            # DATABASE STATUS
            # ---------------------------------------------

            st.subheader("🗄️ Database Status")
            st.info(database_status)

            # ---------------------------------------------
            # FEATURE DETAILS
            # ---------------------------------------------

            st.subheader("🔎 Detailed Feature Values")

            feature_data = {
                "Feature": [
                    "JOINs",
                    "WHERE",
                    "WHERE Conditions",
                    "ORDER BY",
                    "GROUP BY",
                    "SELECT *",
                    "Subquery",
                    "Aggregate Functions",
                    "Table Count",
                    "LIMIT",
                    "Table Size",
                    "Index Available"
                ],
                "Value": [
                    features["joins"],
                    features["where"],
                    features["where_conditions"],
                    features["order_by"],
                    features["group_by"],
                    features["select_all"],
                    features["subquery"],
                    features["aggregate_functions"],
                    features["table_count"],
                    features["limit"],
                    features["table_size"],
                    features["index_available"]
                ]
            }

            st.dataframe(
                pd.DataFrame(feature_data),
                use_container_width=True,
                hide_index=True
            )

            # ---------------------------------------------
            # MYSQL EXPLAIN
            # ---------------------------------------------

            st.subheader("🧠 MySQL EXPLAIN Analysis")

            st.write(
                "MySQL EXPLAIN shows how MySQL plans "
                "to execute a SQL query."
            )

            if explain_result:
                st.dataframe(
                    pd.DataFrame(explain_result),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning(
                    "EXPLAIN results are unavailable. "
                    "The online demo has no live MySQL connection."
                )

        except Exception as e:
            st.error(f"Error while analyzing query: {e}")

            with st.expander("Technical error details"):
                st.exception(e)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="project-footer">
        SQL Query Optimization Advisor |
        Machine Learning + MySQL EXPLAIN
    </div>
    """,
    unsafe_allow_html=True
)
