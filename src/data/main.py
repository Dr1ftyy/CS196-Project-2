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
    
    #top right admin button
    col1, col2 = st.columns([8, 1])
    with col2:
        if st.buton("Admin"):
            st.session_state.show_admin_login = True
    
    #main login UI
    with col1: st.title("MedDesk")
    st.subheader("Patient Portal")

    st.divider

    #admin login form
    if st.session_state.show_admin_login:
        st.subheader("Admin Login")
        password = st.text_input("Enter Admin Password", type = "Password")
        if password == "admin123":
            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.switch_page("pages/admin_view.py")
        else:
            st.error("Incorrect Password")
    #patient login form
    else:
        st.subheader("Patient Login")
        patient_id = st.text_input("Enter Patient ID")
        if st.button("Login as Patient"):
            #read through data and check if patient id exists
            if patient_id.strip().upper() not in valid_ids:
                st.error("Patient ID not found")
                st.info("Are you a new patient? Register below!")

                #form for the new patient
                with st.form("new patient"):
                    name = st.text_input("Full Name")
                    dob = st.text_input("Date of Birth (YYYY-MM-DD)")
                    phone = st.text_input("Phone Number")
                    email = st.text_input("Email Address")
                    insurance = st.selectbox("Insurace Provider", ["BlueCross", "Aetna", "United Healthcare", "Cigna", "Humana", "Other"])
                    condition = st.text_input("Primary Medical Condition")
                    submitted = st.form_submit_button("Register")

                    if submitted:
                        #auto generate a new patient id
                         new_id = f"P{len(patient_df) + 1:03d}"
                         new_row = pd.DataFrame([[new_id, name, dob, phone, email, insurance, condition]], columns=patient_df.columns)
                         updated_df = pd.concat([patient_df, new_row], ignore_index=True)
                         updated_df.to_csv(get_data_path("patients.csv"), index=False)
                         st.success(f"Registration successful! Your Patient ID is {new_id}. Please use this ID to log in."))



    if __name__ == "__main__":
        main()