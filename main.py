import streamlit as st
from streamlit_ace import st_ace

from sql_transpiler_dev.constants import SQLGLOT_SUPPORTED_DB
from sql_transpiler_dev.transpiler_main import transpile_sql_code

# CSS to arrange dropdowns side by side
st.markdown(
    """
    <style>
    .dropdown-container {
        display: flex;
        justify-content: space-between;
    }
    .dropdown-container > div {
        flex: 1;
        margin-right: 10px;
    }
    .dropdown-container > div:last-child {
        margin-right: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state variables if not already set
if 'code_area' not in st.session_state:
    st.session_state['code_area'] = ""

if 'converted_code_area' not in st.session_state:
    st.session_state['converted_code_area'] = ""

# Create a container for the dropdowns to place them side by side
with st.container():
    st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
    convert_from_label = st.selectbox("Convert from:", options=list(SQLGLOT_SUPPORTED_DB.keys()), index=25)
    convert_to_label = st.selectbox("Convert to:", options=list(SQLGLOT_SUPPORTED_DB.keys()), index=18)
    st.markdown('</div>', unsafe_allow_html=True)

# Create the first Ace editor for the user to input code
code = st_ace(value=st.session_state['code_area'], language='sql', theme='github', key="code_area_editor")

# Update the session state with the current value of the Ace editor
st.session_state['code_area'] = code

# Get the actual values from the dictionaries
convert_from = SQLGLOT_SUPPORTED_DB[convert_from_label]
convert_to = SQLGLOT_SUPPORTED_DB[convert_to_label]

# Create a button for the user to submit the code
submit = st.button("Submit")

# If the user clicks the submit button, convert the code and display the result
if submit:
    converted_code = transpile_sql_code(
        sql_query=st.session_state['code_area'],
        __convert_from=convert_from,
        __convert_to=convert_to
    )
    st.session_state['converted_code_area'] = converted_code
    st_ace(
        value=st.session_state['converted_code_area'],
        language='sql',
        theme='github',
        key="converted_code_area_editor"
    )

# Create buttons to clear both text areas
clear_code_area = st.button("Clear code area")
clear_converted_code_area = st.button("Clear converted code area")

# Clear the first text area if the clear button is clicked
if clear_code_area:
    st.session_state['code_area'] = ""
    st.experimental_rerun()  # Rerun the script to reflect the changes

# Clear the second text area if the clear button is clicked
if clear_converted_code_area:
    st.session_state['converted_code_area'] = ""
    st.experimental_rerun()  # Rerun the script to reflect the changes
