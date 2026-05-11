import os
import pandas as pd
import streamlit as st

APP_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename: str) -> str:
    '''Returns the path to a data file, given its filename.'''
    return os.path.join(APP_PATH, "data", filename)

def main():
    st.set_page_config(page_title="Welcome to  the MedDesk Portal", page_icon="🏥", layout="wide")

    # initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'patient_id' not in st.session_state:
        st.session_state.patient_id = None
    if 'show_admin_login' not in st.session_state:
        st.session_state.show_admin_login = False

    # if already logged in redirect
    if st.session_state.logged_in:
        if st.session_state.role == 'admin':
            st.switch_page("pages/admin_view.py")
        else:
            st.switch_page("pages/patient_view.py")
        return

    # title at the top
    st.title("🏥 MedDesk Portal")
    st.subheader("Login below")

    st.divider()
    
    tab1, tab2 = st.tabs(["Admin", "Patient Login"])


    # admin login form
    with tab1:
        st.subheader("Admin Login")
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("Login as Admin"):
            if password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = 'admin'
                st.rerun()
            else:
                st.error("Incorrect password")

    # patient login form
    with tab2:
        st.subheader("Patient Login")
        patients_df = pd.read_csv(get_data_path("patients.csv"))
        valid_ids = patients_df['patient_id'].str.upper().tolist()
        patient_id = st.text_input("Enter Patient ID (e.g. P001)")

        if st.button("Login as Patient"):
            if patient_id.strip().upper() in valid_ids:
                st.session_state.logged_in = True
                st.session_state.role = 'patient'
                st.session_state.patient_id = patient_id.strip().upper()
                st.rerun()
            else:
                st.error("Patient ID not found.")
                st.info("Are you a new patient? Register below!")

                with st.form("new_patient"):
                    name = st.text_input("Full Name")
                    dob = st.text_input("Date of Birth (YYYY-MM-DD)")
                    phone = st.text_input("Phone Number")
                    email = st.text_input("Email Address")
                    insurance = st.selectbox("Insurance Provider", ["BlueCross", "Aetna", "United Healthcare", "Cigna", "Humana", "Other"])
                    condition = st.text_input("Primary Medical Condition")
                    submitted = st.form_submit_button("Register")

                    if submitted:
                        new_id = f"P{len(patients_df) + 1:03d}"
                        new_row = pd.DataFrame([[new_id, name, dob, phone, email, insurance, condition]],
                                               columns=patients_df.columns)
                        updated_df = pd.concat([patients_df, new_row], ignore_index=True)
                        updated_df.to_csv(get_data_path("patients.csv"), index = False)
                        st.success(f"Registered! Your Patient ID is {new_id}. Please use this to log in moving forward")


if __name__ == "__main__":
    main()