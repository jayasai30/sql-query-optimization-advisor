
from feature_extractor import extract_features
from optimizer import predict_optimization
from database import explain_query


def validate_recommendation(features, prediction):
    # Use actual query features to avoid unrelated recommendations
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

    if features["table_size"] >= 1000 and features["limit"] == 0:
        return "USE_LIMIT"

    # Do not accept a subquery prediction if no subquery exists.
    if prediction == "OPTIMIZE_SUBQUERY" and features["subquery"] == 0:
        return "NO_CHANGE"

    return prediction


def generate_advice(recommendation):
    advice = {
        "AVOID_SELECT_ALL": (
            "Avoid SELECT *. Choose only the columns you need.",
            "-- Select only the required columns."
        ),
        "CREATE_INDEX": (
            "Consider an index on the relevant WHERE or JOIN column. "
            "Check the schema and query plan before creating one.",
            "-- Check whether an index on the filtered column would help."
        ),
        "REDUCE_JOINS": (
            "Review your JOIN operations and remove only unnecessary joins.",
            "-- Keep only JOINs needed for the required result."
        ),
        "OPTIMIZE_GROUP_BY": (
            "Review grouping columns and aggregation. Check EXPLAIN "
            "on a connected database for extra sorting or temporary tables.",
            "-- Review GROUP BY columns and suitable indexes."
        ),
        "OPTIMIZE_ORDER_BY": (
            "Review the sorting columns. An appropriate index may help, "
            "depending on the execution plan.",
            "-- Check ORDER BY columns and the query plan."
        ),
        "OPTIMIZE_SUBQUERY": (
            "Review the subquery and compare it with a suitable JOIN "
            "when the result remains equivalent.",
            "-- Compare the subquery with a suitable JOIN."
        ),
        "OPTIMIZE_AGGREGATION": (
            "Check whether unnecessary rows can be filtered before aggregation.",
            "-- Apply appropriate filters before aggregation when valid."
        ),
        "USE_LIMIT": (
            "If you need only a few results, consider using LIMIT.",
            "-- Add LIMIT only when a restricted result set is appropriate."
        ),
        "NO_CHANGE": (
            "No specific optimization issue was detected by the current rules. "
            "This does not guarantee that the query is optimal.",
            "-- Test execution time and EXPLAIN on a connected database."
        )
    }

    return advice.get(
        recommendation,
        (
            "Review the query and validate changes before applying them.",
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

    advice, suggested_sql = generate_advice(final_prediction)

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
