import streamlit as st
from streamlit_ace import st_ace

from sql_transpiler_dev.constants import SQLGLOT_SUPPORTED_DB
from sql_transpiler_dev.transpiler_main import transpile_sql_code


@st.dialog("Transpiler Config")
def transpiler_config_modal():
    st.write(f"Changes are only updated upon saving. ")

    remove_comments_state = st.toggle("Remove Comments (Default: True)", key="remove_comments_switch", value=True)

    if st.button("Save", key="save_config"):
        st.session_state.transpiler_config = {
            "remove_comments": remove_comments_state,
        }
        # notification for successful updates
        st.rerun()


# Set the page layout to wide
st.set_page_config(page_title="SQL Code Transpiler", layout="wide")

st.markdown("# SQL Transpiler")

# CSS to arrange elements and buttons side by side
st.markdown(
    """
    <style>
    .dropdown-container, .buttons-container {
        display: flex;
        justify-content: space-between;
    }
    .dropdown-container > div, .buttons-container > div {
        flex: 1;
        margin-right: 10px;
    }
    .dropdown-container > div:last-child, .buttons-container > div:last-child {
        margin-right: 0;
    }
    .st-ace .ace_editor {
        width: 100% !important;
    }
    div[data-testid="column"] {
        width: fit-content !important;
        flex: unset;
    }
    div[data-testid="column"] * {
        width: fit-content !important;
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
    st.write("#### Menu Options")

    # column design
    mo1_col1, mo1_col2, mo1_col3 = st.columns(3, gap="small", vertical_alignment="bottom")
    with mo1_col1:
        convert_from_label = st.selectbox("Convert from:", options=list(SQLGLOT_SUPPORTED_DB.keys()), index=25)
    with mo1_col2:
        convert_to_label = st.selectbox("Convert to:", options=list(SQLGLOT_SUPPORTED_DB.keys()), index=18)
    with mo1_col3:
        if st.button('⚙️', key='config_button'):
            transpiler_config_modal()

    # Get the actual values from the dictionaries
    convert_from = SQLGLOT_SUPPORTED_DB[convert_from_label]
    convert_to = SQLGLOT_SUPPORTED_DB[convert_to_label]

    st.session_state['convert_from'] = convert_from
    st.session_state['convert_to'] = convert_to

# Create another container for the first Ace editor and buttons
with st.container():
    # Create a container for the buttons to place them side by side
    st.markdown('<div class="buttons-container">', unsafe_allow_html=True)
    ca1_col1, ca1_col2 = st.columns(2, gap="small")
    with ca1_col1:
        submit = st.button("Submit")

    code = st_ace(
        value=st.session_state['code_area'],
        language='sql',
        theme='github',
        key="code_area_editor",
        auto_update=True
    )

    # Update the session state with the current value of the Ace editor
    st.session_state['code_area'] = code

    st.markdown('</div>', unsafe_allow_html=True)

# If the user clicks the submit button, convert the code and update the session state
if submit:
    converted_code = transpile_sql_code(
        sql_query=st.session_state['code_area'],
        __convert_from=st.session_state['convert_from'],
        __convert_to=st.session_state['convert_to']
    )
    st.session_state['converted_code_area'] = converted_code

# Create another container for the converted code Ace editor and button
with st.container():
    st.markdown('<div class="buttons-container">', unsafe_allow_html=True)
    if st.session_state['converted_code_area']:
        st_ace(
            value=st.session_state['converted_code_area'],
            language='sql',
            theme='github',
            key="converted_code_area_editor"
        )
        clear_converted_code_area = st.button("Clear converted code area")
        # Clear the second text area if the clear button is clicked
        if clear_converted_code_area:
            st.session_state['converted_code_area'] = ""
    st.markdown('</div>', unsafe_allow_html=True)
