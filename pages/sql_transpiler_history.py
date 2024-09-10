import sqlite3

import streamlit as st
from annotated_text import annotated_text

from database.sqlite_db_api import db_ops
from database.sqlite_db_config import FULL_DIRECTORY_WITH_DB_NAME, HISTORY_TABLE_NAME


def convert_to_timestamp_start(date_str):
    """Convert date string from 'YYYY-MM-DD' to 'YYYYMMDD_000000_000000000'."""
    return date_str.replace("-", "") + "_000000_000000000"


def convert_to_timestamp_end(date_str):
    """Convert date string from 'YYYY-MM-DD' to 'YYYYMMDD_235959_999999999'."""
    return date_str.replace("-", "") + "_235959_999999999"


@db_ops
def sql_transpiler_history_page():
    # Page Config
    st.set_page_config(page_title="Transpiler History", layout="wide")
    # Title of the page
    st.markdown("# SQL Transpiler History")

    # Connect to the SQLite database
    db_path = FULL_DIRECTORY_WITH_DB_NAME
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Timestamp filter
    st.sidebar.header("Filter by Timestamp")
    start_date = st.sidebar.date_input("From", value=None)
    end_date = st.sidebar.date_input("To", value=None)

    # Build the WHERE clause for filtering by timestamp
    where_clause = ""
    params = []
    if start_date:
        start_timestamp = convert_to_timestamp_start(str(start_date))
        where_clause += "timestamp >= ?"
        params.append(start_timestamp)
    if end_date:
        end_timestamp = convert_to_timestamp_end(str(end_date))
        if where_clause:
            where_clause += " AND "
        where_clause += "timestamp <= ?"
        params.append(end_timestamp)

    # Pagination logic
    items_per_page = 5
    query = f"SELECT COUNT(*) FROM {HISTORY_TABLE_NAME}"
    if where_clause:
        query += f" WHERE {where_clause}"
    cursor.execute(query, params)
    total_items = cursor.fetchone()[0]
    total_pages = (total_items + items_per_page - 1) // items_per_page
    min_value = 1
    # Page navigation
    current_page = st.number_input(
        "Page",
        min_value=0 if total_pages <= 0 else 1,
        max_value=total_pages,
        step=1
    )

    # Calculate the offset for the current page
    offset = (current_page - 1) * items_per_page

    # Load history data for the current page from the SQLite database
    query = f"""
        SELECT * FROM {HISTORY_TABLE_NAME} 
        """
    if where_clause:
        query += f" WHERE {where_clause}"
    query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
    params.extend([items_per_page, offset])
    cursor.execute(query, params)
    history_items = cursor.fetchall()

    # Display the pagination info
    end_index = min(offset + items_per_page, total_items)
    start_index = offset + 1 if end_index > 0 else 0
    _show_no_of_items = f"Showing {start_index} - {end_index} / {total_items} items (Page {current_page} of {total_pages})"
    st.subheader(_show_no_of_items, divider="grey")

    # Display the history for the current page
    if history_items:
        for item in history_items:
            st.write(f"**Timestamp:** {item[1]}")  # Assuming timestamp is in the second column
            annotated_text(
                (f"{item[2].upper()}", "Base Query Type")
            )  # Assuming base_query_type is in the 4th column
            st.code(f"{item[3]}", language="sql", line_numbers=True)  # Assuming base_query is in the 3rd column
            annotated_text(
                (f"{item[4].upper()}", "Transformed Query Type")
            )  # Assuming transformed_query_type is in the 6th column
            st.code(f"{item[5]}", language="sql",
                    line_numbers=True)  # Assuming transformed_query is in the 5th column
            st.write("---")
    else:
        st.write("No history available.")

    # Option to clear history (for demonstration purposes)
    # if st.button("Clear History"):
    #     cursor.execute("DELETE FROM queries_log")
    #     conn.commit()
    #     st.rerun()

    # Close the database connection
    conn.close()


# to display the page
if __name__ == "__main__":
    sql_transpiler_history_page()