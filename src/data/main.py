import os 
import streamlit as st

APP_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data_path():
    '''Returns the path of the data folder'''
    return os.path.join(APP_PATH, "data")

def main():
    st.set_page_config(page_title= "MedDesk", page_icon = "🏥", layout = "wide")

    #initialize session state
    if 'logged in' not in st.session_state:
        st.session_state.logged_in = False
    if 'role' not in st.session_state:
        st.sessions_state.role = None
    if 'patient_id' not in st.session_state:
        st.session_state.patient_id = None
    if 'show_admin_login' not in st.session_state:
        st.session_state.show_admin_login = False

    #if already logged in redirect
    if st.session_state.logged_in:
        if st.session_state.role == 'admin':
            st.switch_page("pages/admin_view.py")
        else:
            st.switch_page("pages/patient_view.py")
        return
    
    