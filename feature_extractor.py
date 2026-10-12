from query_parser import analyze_query
from database import get_table_size, get_indexed_columns


# -------------------------------------------------
# ADVANCED FEATURE EXTRACTION
# -------------------------------------------------

def extract_features(query, table_name):

    # Analyze SQL query
    sql_features = analyze_query(query)

    # Get database information
    table_size = get_table_size(table_name)

    indexed_columns = get_indexed_columns(table_name)

    # Check whether any index exists
    index_available = 1 if len(indexed_columns) > 0 else 0

    # Combine all features
    features = {

        "joins": sql_features["joins"],

        "where": sql_features["where"],

        "where_conditions": sql_features["where_conditions"],

        "order_by": sql_features["order_by"],

        "group_by": sql_features["group_by"],

        "select_all": sql_features["select_all"],

        "subquery": sql_features["subquery"],

        "aggregate_functions": sql_features["aggregate_functions"],

        "table_count": sql_features["table_count"],

        "limit": sql_features["limit"],

        "table_size": table_size,

        "index_available": index_available
    }

    return features