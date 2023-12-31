import streamlit as st
import reqapi as ra
import pandas as pd
import datetime

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.markdown('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" crossorigin="anonymous">', unsafe_allow_html=True)
    hide_img_fs = '''
    <style>
    button[title="View fullscreen"]{visibility: hidden;}
    div.stActionButton > button[kind="header"]{visibility: hidden;}
    </style>
    '''
    st.markdown(hide_img_fs, unsafe_allow_html=True)

    with st.form("myform"):
        c1, c2, c3 = st.columns([1, 4, 1])
        c1.write("Project #:")
        c2.text_input("Project Number:", key="id", label_visibility="collapsed")
        with c3:
            submit = st.form_submit_button(label="Submit", help="Generate Excel")
        error_n1 = st.empty()
        error_n1.write("&nbsp;", unsafe_allow_html=True)

    if submit:
        st.session_state.ok = 1
        if st.session_state["id"] == '':
            st.session_state.ok = 0
        if st.session_state.ok:
            with st.spinner('Wait for it...'):
                res = ra.getData(st.session_state.id)
            if res['is_ok'] == 1:
                with st.expander("Results", expanded=True):
                    st.subheader(f"Project Number: :blue[{st.session_state['id']}]")
                    c1, c2 = st.columns([2, 3])
                    c1.markdown(f"<i class='bi bi-download'></i> [Download Excel]({res['response']['url']})   ", unsafe_allow_html=True)
                    c2.markdown(f"<i class='bi bi-file-excel'></i> [Preview Excel]({res['response']['preview']})", unsafe_allow_html=True)
                    c1, c2 = st.columns([1, 3])
                    c1.markdown("**Promoter**")
                    c1.markdown("**Last Modified Date**")
                    c2.markdown(f"{res['response']['data']['promoter_name']}")
                    c2.markdown(f"{res['response']['data']['lastModifiedDate']}")

                    df1 = pd.json_normalize(res['response']['data']['completion'])
                    df1 = df1.reindex(['name', 'completion_date'], axis=1)
                    df2 = pd.json_normalize(res['response']['data']['area'])
                    df2 = df2.reindex(['area', 'total_units', 'booked_units', 'available_units'], axis=1)
                    c1, c2 = st.columns([2, 3])
                    c1.dataframe(df1, column_config={"name":"Name","completion_date":"Completion Date"}, hide_index=True)
                    c2.dataframe(df2, column_config={"area":"Area","total_units":"Total Units", "booked_units":"Booked Units", "available_units":"Available Units"}, hide_index=True)
                    st.caption(f"Done in {res['response']['meta']['duration']} sec")

            else:
                error_n1.markdown(f":red[{res['error']}]")

            with st.expander('Details'):
                st.write(res)
        else:
            error_n1.markdown(":red[Project Number could not be empty]")

    with st.expander("All Projects Excel", expanded=False):
        mon = datetime.date.today() - datetime.timedelta(datetime.date.today().weekday())
        st.markdown(f"<i class='bi bi-download'></i> [Download AllProjects.xlsx]({'https://drive.google.com/uc?id=17gfF0RxHXkcWtXvFCSskwmWV3FZIEk6J&export=download'})   ", unsafe_allow_html=True)
        st.markdown(f"<i class='bi bi-file-excel'></i> [Open AllProjects.xlsx]({'https://docs.google.com/spreadsheets/d/17gfF0RxHXkcWtXvFCSskwmWV3FZIEk6J/edit'})", unsafe_allow_html=True)
        st.write(f"Updated: {mon:%d/%m/%Y}")
