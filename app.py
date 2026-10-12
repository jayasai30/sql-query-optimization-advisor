import streamlit as st

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
# CUSTOM BACKGROUND + UI DESIGN
# =========================================================

st.markdown(
    """
    <style>

    /* -----------------------------------------------------
       MAIN BACKGROUND
    ----------------------------------------------------- */

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


    /* -----------------------------------------------------
       MOVING GRAPHICS
    ----------------------------------------------------- */

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


    /* -----------------------------------------------------
       CONTENT ABOVE BACKGROUND
    ----------------------------------------------------- */

    .main .block-container {

        position: relative;

        z-index: 2;

        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* -----------------------------------------------------
       TITLE
    ----------------------------------------------------- */

    h1 {

        text-align: center;

        font-size: 42px !important;

        font-weight: 800 !important;

        letter-spacing: 1px;

        text-shadow:
            0 0 10px rgba(0, 180, 255, 0.5),
            0 0 25px rgba(120, 80, 255, 0.25);
    }


    /* -----------------------------------------------------
       SUBHEADINGS
    ----------------------------------------------------- */

    h2, h3 {

        color: #e8f7ff !important;

        text-shadow:
            0 0 8px rgba(0, 180, 255, 0.25);
    }


    /* -----------------------------------------------------
       TEXT
    ----------------------------------------------------- */

    p, label {

        color: #dcecff !important;
    }


    /* -----------------------------------------------------
       INPUT BOXES
    ----------------------------------------------------- */

    textarea,
    input {

        background-color: rgba(10, 25, 45, 0.90) !important;

        color: white !important;

        border: 1px solid rgba(0, 180, 255, 0.35) !important;

        border-radius: 10px !important;
    }


    textarea:focus,
    input:focus {

        border: 1px solid #00bfff !important;

        box-shadow:
            0 0 10px rgba(0, 191, 255, 0.35) !important;
    }


    /* -----------------------------------------------------
       BUTTON
    ----------------------------------------------------- */

    .stButton > button {

        width: 100%;

        border-radius: 10px;

        border: 1px solid rgba(0, 191, 255, 0.5);

        background:
            linear-gradient(
                90deg,
                #087ea4,
                #5b4bb7
            );

        color: white;

        font-size: 17px;

        font-weight: 700;

        padding: 0.65rem;

        transition: 0.3s;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 0 18px rgba(0, 191, 255, 0.45);
    }


    /* -----------------------------------------------------
       METRIC CARDS
    ----------------------------------------------------- */

    [data-testid="stMetric"] {

        background: rgba(10, 28, 50, 0.75);

        border: 1px solid rgba(0, 191, 255, 0.20);

        border-radius: 12px;

        padding: 12px;

        box-shadow:
            0 4px 18px rgba(0, 0, 0, 0.20);

        margin-bottom: 12px;
    }


    [data-testid="stMetricValue"] {

        color: #ffffff !important;

        font-weight: 700;
    }


    /* -----------------------------------------------------
       INFO / SUCCESS BOXES
    ----------------------------------------------------- */

    [data-testid="stAlert"] {

        background-color: rgba(10, 30, 50, 0.82) !important;

        border-radius: 10px;
    }


    /* -----------------------------------------------------
       DATAFRAME
    ----------------------------------------------------- */

    [data-testid="stDataFrame"] {

        border-radius: 10px;

        overflow: hidden;

        border: 1px solid rgba(0, 191, 255, 0.20);
    }


    /* -----------------------------------------------------
       SQL CODE DISPLAY
    ----------------------------------------------------- */

    code {

        color: #8ee7ff !important;
    }


    /* -----------------------------------------------------
       FOOTER
    ----------------------------------------------------- */

    .project-footer {

        text-align: center;

        margin-top: 35px;

        padding: 15px;

        color: #8faec7;

        font-size: 13px;

        border-top: 1px solid rgba(0, 191, 255, 0.15);
    }
    /* -----------------------------------------------------
   STREAMLIT TOP HEADER
----------------------------------------------------- */

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
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🚀 Analyze Query",
    use_container_width=True
):

    if query.strip() == "":

        st.warning(
            "Please enter a SQL query."
        )

    elif table_name.strip() == "":

        st.warning(
            "Please enter the main table name."
        )

    else:

        try:

            # =================================================
            # ANALYZE QUERY
            # =================================================

            (
                features,
                ml_prediction,
                final_prediction,
                explain_result
            ) = analyze_sql_query(
                query,
                table_name
            )


            # =================================================
            # QUERY ANALYSIS
            # =================================================

            st.subheader(
                "📊 Query Analysis"
            )


            col1, col2, col3 = st.columns(3)


            # -------------------------------------------------
            # COLUMN 1
            # -------------------------------------------------

            with col1:

                st.metric(
                    "JOINs",
                    features["joins"]
                )

                st.metric(
                    "WHERE Conditions",
                    features["where_conditions"]
                )

                st.metric(
                    "Tables",
                    features["table_count"]
                )

                st.metric(
                    "Table Rows",
                    features["table_size"]
                )


            # -------------------------------------------------
            # COLUMN 2
            # -------------------------------------------------

            with col2:

                st.metric(
                    "ORDER BY",
                    features["order_by"]
                )

                st.metric(
                    "GROUP BY",
                    features["group_by"]
                )

                st.metric(
                    "Aggregate Functions",
                    features["aggregate_functions"]
                )

                st.metric(
                    "LIMIT",
                    features["limit"]
                )


            # -------------------------------------------------
            # COLUMN 3
            # -------------------------------------------------

            with col3:

                st.metric(
                    "SELECT *",
                    features["select_all"]
                )

                st.metric(
                    "Subquery",
                    features["subquery"]
                )

                st.metric(
                    "Index Available",
                    features["index_available"]
                )


            # =================================================
            # ML PREDICTION
            # =================================================

            st.subheader(
                "🤖 Machine Learning Prediction"
            )

            st.info(
                f"ML Model Prediction: **{ml_prediction}**"
            )


            # =================================================
            # FINAL RECOMMENDATION
            # =================================================

            st.subheader(
                "🎯 Final Optimization Recommendation"
            )

            st.success(
                f"Recommended Action: **{final_prediction}**"
            )


            # =================================================
            # EXPLANATION
            # =================================================

            explanations = {

                "NO_CHANGE":
                    "The query does not show a major optimization issue.",

                "AVOID_SELECT_ALL":
                    "Avoid SELECT *. Select only the columns that are required.",

                "CREATE_INDEX":
                    "Consider creating an index on columns used frequently in WHERE or JOIN conditions.",

                "REDUCE_JOINS":
                    "The query contains multiple JOINs. Check whether all JOINs are necessary.",

                "OPTIMIZE_ORDER_BY":
                    "ORDER BY may require additional sorting. Consider indexing the sorting columns.",

                "OPTIMIZE_GROUP_BY":
                    "GROUP BY with aggregation can require additional processing. Review the grouping columns and indexes.",

                "OPTIMIZE_SUBQUERY":
                    "The query contains a subquery. Check whether it can be rewritten using a JOIN or another efficient query structure.",

                "OPTIMIZE_AGGREGATION":
                    "Aggregation functions such as SUM, AVG or COUNT may require additional processing.",

                "USE_LIMIT":
                    "Consider using LIMIT when only a small number of rows are required."
            }


            explanation = explanations.get(
                final_prediction,
                "Review the query for possible optimization."
            )


            st.info(
                f"💡 **Explanation:** {explanation}"
            )


            # =================================================
            # DETAILED FEATURES
            # =================================================

            st.subheader(
                "🔎 Detailed Feature Values"
            )


            feature_data = {

                "JOINs":
                    features["joins"],

                "WHERE":
                    features["where"],

                "WHERE Conditions":
                    features["where_conditions"],

                "ORDER BY":
                    features["order_by"],

                "GROUP BY":
                    features["group_by"],

                "SELECT *":
                    features["select_all"],

                "Subquery":
                    features["subquery"],

                "Aggregate Functions":
                    features["aggregate_functions"],

                "Table Count":
                    features["table_count"],

                "LIMIT":
                    features["limit"],

                "Table Size":
                    features["table_size"],

                "Index Available":
                    features["index_available"]
            }


            st.dataframe(
                feature_data,
                use_container_width=True
            )


            # =================================================
            # MYSQL EXPLAIN
            # =================================================

            st.subheader(
                "🧠 MySQL EXPLAIN Analysis"
            )


            st.write(
                "MySQL EXPLAIN shows how MySQL plans "
                "to execute the SQL query."
            )


            if explain_result:

                st.dataframe(
                    explain_result,
                    use_container_width=True
                )

            else:

                st.warning(
                    "No EXPLAIN information was returned."
                )


        except Exception as e:

            st.error(
                f"Error while analyzing query: {e}"
            )


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