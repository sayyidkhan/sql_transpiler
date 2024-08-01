import streamlit as st


def home_page():
    st.title("Welcome to the SQL Code Transpiler App")

    st.markdown("""
    ## How to Use This App

    This application allows you to transpile SQL code between different SQL dialects. Follow these steps to use the app:

    1. **Navigate to the SQL Transpiler Page**: 
       - Use the navigation menu on the left to go to the "SQL Transpiler" page.

    2. **Select SQL Dialects**:
       - Choose the source SQL dialect from the "Convert from" dropdown menu.
       - Choose the target SQL dialect from the "Convert to" dropdown menu.

    3. **Enter SQL Code**:
       - Enter your SQL code in the provided text area.

    4. **Transpile the SQL Code**:
       - Click the "Submit" button to transpile the SQL code to the target dialect.
       - The converted SQL code will appear in the second text area.

    5. **Clear Code Areas**:
       - Use the "Clear code area" button to clear the input SQL code.
       - Use the "Clear converted code area" button to clear the transpiled SQL code.

    6. **View History**:
       - Navigate to the "History" page to see the history of transpiled SQL code.

    We hope this app helps you with your SQL transpilation needs!
    """)


home_page()
