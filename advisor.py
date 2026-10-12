
from feature_extractor import extract_features
from optimizer import predict_optimization
from database import explain_query


def validate_recommendation(features, prediction):

    if features["select_all"] == 1:
        return "AVOID_SELECT_ALL"

    if (
        features["where"] == 1
        and features["index_available"] == 0
        and features["table_size"] >= 500
    ):
        return "CREATE_INDEX"

    if features["joins"] >= 2:
        return "REDUCE_JOINS"

    if features["subquery"] == 1:
        return "OPTIMIZE_SUBQUERY"

    if (
        features["group_by"] == 1
        and features["aggregate_functions"] >= 1
    ):
        return "OPTIMIZE_GROUP_BY"

    if (
        features["aggregate_functions"] >= 1
        and features["group_by"] == 0
    ):
        return "OPTIMIZE_AGGREGATION"

    if features["order_by"] == 1:
        return "OPTIMIZE_ORDER_BY"

    if (
        features["table_size"] >= 1000
        and features["limit"] == 0
    ):
        return "USE_LIMIT"

    return prediction


def generate_advice(recommendation):

    advice = {
        "AVOID_SELECT_ALL": (
            "Avoid SELECT *. Choose only the columns you need. "
            "This can reduce unnecessary data retrieval.",
            "SELECT customer_name, city FROM customers;"
        ),

        "CREATE_INDEX": (
            "Consider an index on the column used in WHERE "
            "or JOIN conditions. Verify the relevant column "
            "and query plan before creating it.",
            "-- Example only; replace with a real column:\n"
            "CREATE INDEX idx_city ON customers(city);"
        ),

        "REDUCE_JOINS": (
            "Review your JOIN operations and remove only those "
            "that are unnecessary for the required result.",
            "-- Keep only the JOINs needed by your query."
        ),

        "OPTIMIZE_GROUP_BY": (
            "Review your grouping columns and aggregation. "
            "Check EXPLAIN on a connected database for "
            "temporary tables or extra sorting.",
            "-- Review GROUP BY columns and suitable indexes."
        ),

        "OPTIMIZE_ORDER_BY": (
            "Review the sorting columns. An appropriate index "
            "may help, depending on the query and execution plan.",
            "-- Check the ORDER BY columns and query plan."
        ),

        "OPTIMIZE_SUBQUERY": (
            "Review the subquery and check whether a JOIN "
            "would be clearer or more efficient.",
            "-- Compare the subquery with a suitable JOIN."
        ),

        "OPTIMIZE_AGGREGATION": (
            "Check whether you can filter unnecessary rows "
            "before applying SUM, COUNT, AVG or other aggregates.",
            "-- Apply appropriate WHERE conditions before aggregation."
        ),

        "USE_LIMIT": (
            "If you need only a few results, consider LIMIT "
            "to restrict the returned rows.",
            "SELECT customer_name FROM customers LIMIT 10;"
        ),

        "NO_CHANGE": (
            "No major issue was detected by the current rules. "
            "This does not guarantee the query is optimal.",
            "-- Test execution time and EXPLAIN on a real database."
        )
    }

    return advice.get(
        recommendation,
        (
            "Review the query and validate possible changes "
            "before applying them.",
            "-- Check the query plan and actual execution time."
        )
    )


def analyze_sql_query(query, table_name):

    features = extract_features(query, table_name)

    ml_prediction = predict_optimization(features)

    final_prediction = validate_recommendation(
        features,
        ml_prediction
    )

    advice, suggested_sql = generate_advice(
        final_prediction
    )

    # MySQL EXPLAIN is optional in demo mode.
    # Without a hosted database, continue with the advisor.
    try:
        explain_result = explain_query(query)
        database_status = "Connected to database"
    except Exception:
        explain_result = []
        database_status = (
            "Demo mode: no online MySQL connection. "
            "Database execution details are unavailable."
        )

    return (
        features,
        ml_prediction,
        final_prediction,
        advice,
        suggested_sql,
        explain_result,
        database_status
    )
