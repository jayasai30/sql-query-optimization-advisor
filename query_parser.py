import sqlparse
import re


def analyze_query(query):

    # Convert query to uppercase
    query_upper = query.upper()

    # Remove extra spaces and new lines
    query_clean = " ".join(query_upper.split())

    # Count JOINs
    joins = len(re.findall(r"\bJOIN\b", query_clean))

    # Detect WHERE
    where = 1 if re.search(r"\bWHERE\b", query_clean) else 0

    # Count WHERE conditions
    where_conditions = 0

    if where:
        where_part = query_clean.split("WHERE", 1)[1]

        # Stop at GROUP BY / ORDER BY / LIMIT
        where_part = re.split(
            r"\bGROUP BY\b|\bORDER BY\b|\bLIMIT\b",
            where_part
        )[0]

        where_conditions = (
            len(re.findall(r"\bAND\b|\bOR\b", where_part)) + 1
        )

    # Detect ORDER BY
    order_by = 1 if re.search(r"\bORDER BY\b", query_clean) else 0

    # Detect GROUP BY
    group_by = 1 if re.search(r"\bGROUP BY\b", query_clean) else 0

    # Detect SELECT *
    select_all = 1 if re.search(
        r"\bSELECT\s+\*",
        query_clean
    ) else 0

    # Detect subquery
    subquery = 1 if re.search(
        r"\(\s*SELECT\b",
        query_clean
    ) else 0

    # Detect aggregate functions
    aggregate_functions = len(re.findall(
        r"\b(COUNT|SUM|AVG|MIN|MAX)\s*\(",
        query_clean
    ))

    # Count tables from FROM and JOIN
    tables = re.findall(
        r"\b(?:FROM|JOIN)\s+([A-Z_][A-Z0-9_]*)",
        query_clean
    )

    table_count = len(set(tables))

    # Detect LIMIT
    limit = 1 if re.search(
        r"\bLIMIT\b",
        query_clean
    ) else 0

    features = {
        "joins": joins,
        "where": where,
        "where_conditions": where_conditions,
        "order_by": order_by,
        "group_by": group_by,
        "select_all": select_all,
        "subquery": subquery,
        "aggregate_functions": aggregate_functions,
        "table_count": table_count,
        "limit": limit
    }

    return features


# Test query

query = """
SELECT *
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
WHERE c.city = 'Chennai'
ORDER BY o.amount DESC;
"""


result = analyze_query(query)

print("\nADVANCED SQL QUERY ANALYSIS")
print("--------------------------------")

for name, value in result.items():
    print(f"{name}: {value}")