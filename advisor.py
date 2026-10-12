from feature_extractor import extract_features
from optimizer import predict_optimization
from database import explain_query


# -------------------------------------------------
# RULE-BASED VALIDATION
# -------------------------------------------------

def validate_recommendation(features, prediction):

    # SELECT * should be avoided
    if features["select_all"] == 1:
        return "AVOID_SELECT_ALL"

    # Missing index with WHERE condition
    if (
        features["where"] == 1
        and features["index_available"] == 0
        and features["table_size"] >= 500
    ):
        return "CREATE_INDEX"

    # Multiple JOINs
    if features["joins"] >= 2:
        return "REDUCE_JOINS"

    # Subquery
    if features["subquery"] == 1:
        return "OPTIMIZE_SUBQUERY"

    # GROUP BY with aggregation
    if (
        features["group_by"] == 1
        and features["aggregate_functions"] >= 1
    ):
        return "OPTIMIZE_GROUP_BY"

    # Aggregation without GROUP BY
    if (
        features["aggregate_functions"] >= 1
        and features["group_by"] == 0
    ):
        return "OPTIMIZE_AGGREGATION"

    # ORDER BY
    if features["order_by"] == 1:
        return "OPTIMIZE_ORDER_BY"

    # Large query without LIMIT
    if (
        features["table_size"] >= 1000
        and features["limit"] == 0
    ):
        return "USE_LIMIT"

    # Otherwise use ML prediction
    return prediction


# -------------------------------------------------
# MAIN SQL QUERY ANALYSIS
# -------------------------------------------------

def analyze_sql_query(query, table_name):

    # Extract features
    features = extract_features(
        query,
        table_name
    )

    # ML prediction
    ml_prediction = predict_optimization(
        features
    )

    # Validate ML prediction
    final_prediction = validate_recommendation(
        features,
        ml_prediction
    )

    # MySQL EXPLAIN
    explain_result = explain_query(
        query
    )

    return (
        features,
        ml_prediction,
        final_prediction,
        explain_result
    )


# -------------------------------------------------
# TEST
# -------------------------------------------------

if __name__ == "__main__":

    test_query = """
    SELECT
        c.customer_name,
        c.city,
        SUM(o.amount) AS total_spent
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    WHERE o.amount > 100
    GROUP BY c.customer_name, c.city
    ORDER BY total_spent DESC
    LIMIT 5;
    """

    table_name = "customers"

    (
        features,
        ml_prediction,
        final_prediction,
        explain_result
    ) = analyze_sql_query(
        test_query,
        table_name
    )

    print("\nSQL QUERY OPTIMIZATION ADVISOR")
    print("--------------------------------")

    print("\nML Prediction:")
    print(ml_prediction)

    print("\nFinal Recommendation:")
    print(final_prediction)

    print("\nMYSQL EXPLAIN ANALYSIS")
    print("--------------------------------")

    for row in explain_result:
        print(row)