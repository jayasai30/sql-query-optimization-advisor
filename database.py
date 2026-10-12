
import re
import mysql.connector
import streamlit as st


def get_connection():
    """Connect to MySQL when database credentials are configured."""
    config = st.secrets.get("mysql", {})

    if not config:
        raise RuntimeError(
            "Online MySQL is not configured. "
            "The application must use demo mode."
        )

    return mysql.connector.connect(
        host=config["host"],
        port=int(config.get("port", 3306)),
        user=config["user"],
        password=config["password"],
        database=config["database"],
        connection_timeout=5
    )


def _validate_table_name(table_name):
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table_name):
        raise ValueError("Invalid table name.")
    return table_name


def get_table_size(table_name):
    table_name = _validate_table_name(table_name)

    connection = get_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT COUNT(*) FROM `{table_name}`"
            )
            return cursor.fetchone()[0]
        finally:
            cursor.close()
    finally:
        connection.close()


def check_indexes(table_name):
    table_name = _validate_table_name(table_name)

    connection = get_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute(f"SHOW INDEX FROM `{table_name}`")
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()


def get_indexed_columns(table_name):
    indexes = check_indexes(table_name)
    return list(dict.fromkeys(index[4] for index in indexes))


def get_foreign_keys(table_name):
    table_name = _validate_table_name(table_name)

    connection = get_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT COLUMN_NAME, REFERENCED_TABLE_NAME,
                       REFERENCED_COLUMN_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = %s
                  AND REFERENCED_TABLE_NAME IS NOT NULL
                """,
                (table_name,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()


def explain_query(query):
    if not query.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries can be analyzed.")

    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("EXPLAIN " + query.strip().rstrip(";"))
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()
