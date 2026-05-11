import os
import streamlit as st
import pandas as pd
#import matplotlib as plt

APP_PATH = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))

def get_data_path(filename: str) -> str:
    return os.path.join(APP_PATH, "data", filename)

def load_data():
    #load data from csv files
    patients = pd.read_csv(get_data_path("patients.csv"))
    appointments = pd.read_csv(get_data_path("appointments.csv"))
    doctors = pd.read_csv(get_data_path("doctors.csv"))
    billing = pd.read_csv(get_data_path("billing.csv"))
    return patients, appointments, doctors, billing

def main():
    #redirect if not logged in as admin
    if not st.session_state("logged_in") or st.session_state.get("role") != "admin":
        st.warning("Access denies. Please log in as admin")
        st.stop
    
    st.title("🏥 MedDesk - Admin Panel")

#logout button
if st.button("Logout", key = "admin_logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.switch_page("main.py")
    
st.divider()

#tabs for different secionts the admin can look and view
tab1, tab2, tab3, tab4, tab5 = st.stabs([
    "Patients"
    "Appointments"
    "Billing"
    "Analytics"
    "Doctors"
])

# Tab 1: Patients

# Tab 2: Appointments

# Tab 3: Billing

# Tab 4: Analytics

# Tab 5: Doctors