
from query_parser import analyze_query
from database import (
    get_table_size,
    get_indexed_columns
)


# Sample database information for free online demo mode
DEMO_TABLES = {
    "customers": {
        "rows": 10,
        "indexed_columns": ["customer_id"]
    },
    "products": {
        "rows": 10,
        "indexed_columns": ["product_id"]
    },
    "orders": {
        "rows": 15,
        "indexed_columns": [
            "order_id",
            "customer_id",
            "product_id"
        ]
    }
}


def extract_features(query, table_name):

    sql_features = analyze_query(query)

    table_name = table_name.strip().lower()

    try:
        table_size = get_table_size(table_name)
        indexed_columns = get_indexed_columns(table_name)

    except Exception:
        # Use sample metadata when no online database exists
        table_info = DEMO_TABLES.get(
            table_name,
            {
                "rows": 100,
                "indexed_columns": []
            }
        )

        table_size = table_info["rows"]
        indexed_columns = table_info["indexed_columns"]

    index_available = (
        1 if indexed_columns else 0
    )

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
