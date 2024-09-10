import streamlit as st
from streamlit_ace import st_ace

from database.sqlite_db_api import insert_record_into_transpiler_history, db_ops
from sql_transpiler_logic.constants import SQLGLOT_SUPPORTED_DB
from sql_transpiler_logic.transpiler_main import transpile_sql_code
# If not, then initialize it
from sql_transpiler_logic.util.util_datetime import get_curr_date_time_now


@db_ops
def sql_transpiler_page():
    if 'transpiler_config' not in st.session_state:
        st.session_state['transpiler_config'] = {
            "remove_comments": True,
        }

    @st.dialog("Transpiler Config")
    def transpiler_config_modal():
        def validate_remove_comments():
            """
            if there is state management on remove_comments, then use existing state,
            otherwise default is True
            """
            if "transpiler_config" in st.session_state and "remove_comments" in st.session_state.transpiler_config:
                return st.session_state.transpiler_config["remove_comments"]
            else:
                return True

        st.write("Changes are only updated upon saving.")

        # Retrieve the current state of the toggle from session state
        remove_comments_state = st.toggle(
            "Remove Comments (Default: True)",
            key="remove_comments_switch",
            value=validate_remove_comments()
        )

        if st.button("Save", key="save_config"):
            st.session_state.transpiler_config = {
                "remove_comments": remove_comments_state
            }
            st.write("Configuration saved!")  # Optional: Provide feedback to the user
            st.rerun()  # Rerun the app to ensure the state is updated

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
        _base_query_type = st.session_state['convert_from']
        _transformed_query_type = st.session_state['convert_to']
        _base_query = st.session_state['code_area']

        _transformed_query = transpile_sql_code(
            sql_query=_base_query,
            __convert_from=_base_query_type,
            __convert_to=_transformed_query_type,
            # MODAL BOX: transpiler config
            strip_comments=st.session_state.transpiler_config['remove_comments']
        )
        st.session_state['converted_code_area'] = _transformed_query

        """ insert record into the database """
        _curr_timestamp = get_curr_date_time_now(
            display_date=True,
            display_time=True,
            display_nanoseconds=True
        )
        _insert_query = {
            "timestamp": _curr_timestamp,
            "base_query_type": _base_query_type,
            "base_query": _base_query,
            "transformed_query_type": _transformed_query_type,
            "transformed_query": _transformed_query,
        }
        print(_insert_query.keys())
        print(_insert_query.values())
        insert_record_into_transpiler_history(_record=list(_insert_query.values()), _timestamp=_curr_timestamp)
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


# to display the page
if __name__ == "__main__":
    sql_transpiler_page()