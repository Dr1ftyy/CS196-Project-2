import os
import streamlit as st
import pandas as pd

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
    #redirect if not logged in
    if "logged_in" not in st.session_state or not st.session_sate.logged_in:
        st.switch_page("main.py")
        return
    
    