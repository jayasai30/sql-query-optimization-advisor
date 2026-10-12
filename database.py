import mysql.connector


# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="",
        database="sql_optimizer"
    )


# -------------------------------------------------
# GET TABLE ROW COUNT
# -------------------------------------------------

def get_table_size(table_name):

    connection = get_connection()
    cursor = connection.cursor()

    query = f"SELECT COUNT(*) FROM `{table_name}`"

    cursor.execute(query)

    result = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return result


# -------------------------------------------------
# CHECK TABLE INDEXES
# -------------------------------------------------

def check_indexes(table_name):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(f"SHOW INDEX FROM `{table_name}`")

    indexes = cursor.fetchall()

    cursor.close()
    connection.close()

    return indexes


# -------------------------------------------------
# GET INDEXED COLUMN NAMES
# -------------------------------------------------

def get_indexed_columns(table_name):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(f"SHOW INDEX FROM `{table_name}`")

    indexes = cursor.fetchall()

    cursor.close()
    connection.close()

    columns = []

    for index in indexes:

        column_name = index[4]

        if column_name not in columns:
            columns.append(column_name)

    return columns


# -------------------------------------------------
# GET FOREIGN KEYS
# -------------------------------------------------

def get_foreign_keys(table_name):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        COLUMN_NAME,
        REFERENCED_TABLE_NAME,
        REFERENCED_COLUMN_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA = 'sql_optimizer'
    AND TABLE_NAME = %s
    AND REFERENCED_TABLE_NAME IS NOT NULL
    """

    cursor.execute(query, (table_name,))

    foreign_keys = cursor.fetchall()

    cursor.close()
    connection.close()

    return foreign_keys


# -------------------------------------------------
# MYSQL EXPLAIN ANALYSIS
# -------------------------------------------------

def explain_query(query):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Remove unnecessary semicolon
    query = query.strip().rstrip(";")

    explain_sql = "EXPLAIN " + query

    cursor.execute(explain_sql)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


# -------------------------------------------------
# TEST DATABASE FUNCTIONS
# -------------------------------------------------

if __name__ == "__main__":

    table = "orders"

    print("\nADVANCED DATABASE ANALYSIS")
    print("--------------------------------")

    print("Table:", table)

    print(
        "Row Count:",
        get_table_size(table)
    )

    print(
        "Indexed Columns:",
        get_indexed_columns(table)
    )

    print(
        "Foreign Keys:",
        get_foreign_keys(table)
    )


    # Test SQL query

    test_query = """
    SELECT c.customer_name, o.amount
    FROM customers c
    JOIN orders o
    ON c.customer_id = o.customer_id
    WHERE c.city = 'Chennai'
    ORDER BY o.amount DESC;
    """


    print("\nMYSQL EXPLAIN ANALYSIS")
    print("--------------------------------")


    try:

        explain_result = explain_query(test_query)

        for row in explain_result:

            print(row)


    except Exception as e:

        print("EXPLAIN Error:", e)