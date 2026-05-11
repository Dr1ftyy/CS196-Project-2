import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    if not st.session_state.get("logged_in") or st.session_state.get("role") != "admin":
        st.warning("Access denied. Please log in as admin")
        st.stop()
    
    st.title("🏥 MedDesk - Admin Panel")

    col1, col2 = st.columns([8,1])
    with col2:

        #logout button
        if st.button("Logout", key = "admin_logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.show_admin_login = False
            st.switch_page("main.py")
        
    st.divider()

    patients, appointments, doctors, billing = load_data()

    #tabs for different secionts the admin can look and view
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Patients",
        "Appointments",
        "Billing",
        "Analytics",
        "Doctors"
    ])

    # Tab 1: Patients
    with tab1:
        st.subheader("Patient Records")

        #search bar
        search = st.text_input("Search by name or patient ID")
        if search:
            filtered = patients[
                patients['name'].str.contains(search, case=False) |
                patients['patient_id'].str.contains(search, case=False)
            ]
        else: filtered = patients

        st.dataframe(filtered, use_container_width = True)

        st.divider()

        #add a new patient
        st.subheader("Add New Patient")
        with st.form("admin_add_patient"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name")
                dob = st.text_input("Date of Birth (YYYY-MM-DD)")
                phone = st.text_input("Phone")
            with col2:
                email = st.text_input("email")
                insurance = st.selectbox("Insurance", ["BlueCross", "Aetna", "United Healthcare", "Cigna", "Humana", "Other"])
                condition = st.text_input("Primary Condition")
            add_submitted = st.form_submit_button("Add Patient")

            if add_submitted:
                existing_ids = patients['patient_id'].str.replace('P', '').astype(int)
                new_id = f"P{existing_ids.max() + 1:03d}"
                new_row = pd.DataFrame([[new_id, name, dob, phone, email, insurance, condition]],
                                       columns = patients.columns)
                updated = pd.concat([patients, new_row], ignore_index = True)
                updated.to_csv(get_data_path("patients.csv"), index = False)
                st.success(f"Patient added with ID {new_id}!")
                st.rerun()

        st.divider()

        #delete patient
        st.subheader("Delete Patient")
        patient_to_delete = st.selectbox("Select patient to delete",
                                        patients['patient_id'] + " - " + patients['name'],
                                        key = 'delete_patient')
        if st.button("Delete Patient", key = "delete_patient_btn"):
            pid = patient_to_delete.split(" - ")[0]
            updated = patients[patients['patient_id'] != pid]
            updated.to_csv(get_data_path("patients.csv"), index = False)
            st.success(f"Patient {pid} deleted!")
            st.rerun()
        

    # Tab 2: Appointments
    with tab2:
        st.subheader("All Appointments")


    # Tab 3: Billing
    with tab3:
        st.subheader("Billing Records")
        
        merged_billing = billing.merge(patients[['patient_id', 'name']], on = 'patient_id', how = 'left')
        st.dataframe(merged_billing, use_container_width = True)

        st.divider()

        #add billing record
        st.subheader("Add Billing Recod")
        with st.form("add_billing"):
            col1, col2 = st.columns(2)
            with col1:
                bill_patient = st.selectbox("Patient", patients['patient_id'] + " - " + patients['name'])
                procedure = st.text_input("Procedure")
                cost = st.number_input("Total Cost ($)", min_value = 0.0, format = "%.2f")
            with col2:
                appt_options_bill = appointments['appointment_id']
                bill_appt = st.selectbox("Appointment ID", appt_options_bill)
                coverage = st.slider("Insurace Coverage %", 0, 100, 80)
                paid = st.selectbox("Paid?", ["No", "Yes"])
            bill_submitted = st.form_submit_button("Add Billing Record")

        if bill_submitted:
            existing_ids = billing['billing_id'].str.replace('A', '').astype(int)
            new_bill_id = f"A{existing_ids.max() + 1:03d}"
            pid = bill_patient.split(" - ")[0]
            new_bill = pd.DataFrame([new_bill,  pid, bill_appt, procedure, cost, coverage/100, paid],
                                    columns = billing.columns)
            updated_billing = pd.concat([billing, new_bill], ignore_index = True)
            updated_billing.to_csv(get_data_path("billing.csv"), index = False)
            st.success("Billing record added!")
            st.rerun()

    # Tab 4: Analytics
    with tab4:
        st.subheader("Analytics Dashboard")

        col1, col2 = st.columns(2)

        with col1:
            #patients per doctor
            st.markdown("**Patients per Doctor**")
            merged_appts = appointments.merge(doctors[['doctor_id', 'name']], on = 'doctor_id', how = 'left')
            patients_per_doctor = merged_appts.groupby('name')['patient_id'].nunique()
            fig1, ax1 = plt.subplots()
            ax1.bar(patients_per_doctor.index, patients_per_doctor.values, color = 'steelblue')
            ax1.set_xlabel("Doctor")
            ax1.set_ylabel("Unique Patients")
            plt.xticks(rotation = 45, ha = 'right')
            plt.tight_layout()
            st.pyplot(fig1)
        
        with col2:
        #conditions breakdown
            st.markdown("**Conditions per Doctor**")
            conditons = patients['condition'].value_counts()
            fig2, ax2 = plt.subplots()
            ax2.pie(conditons.values, labels = conditons.index, autopct = '%1.1f%%')
            plt.tight_layout()
            st.pyplot(fig2)

        st.divider()

        #summary metrics
        col3, col4, col5 = st.columns(3)
        with col3:
            st.metric("Total Patients", len(patients))
        with col4:
            st.metric("Total Appointments", len(appointments))
        with col5:
            total_billed = billing['cost'].astype(float).sum()
            st.metric("Total Billed", f"${total_billed:,.2f}")


    # Tab 5: Doctors
    with tab5:
        st.subheader("Doctor Directory")
        st.dataframe(doctors, use_container_width = True)

        st.divider()

        st.subheader("Add Doctor")
        with st.form("add_doctor"):
            col1, col2 = st.columns(2)
            with col1:
                doc_name = st.text_input("Doctor's Name")
                specialty = st.text_input("Speciality")
            with col2:
                office = st.text_input("Office")
            doc_submited = st.form_submit_button("Add Doctor")

        if doc_submited:
            existing_ids = doctors['doctor_id'].str.replace('D', '').astype(int)
            new_doc_id = f"D{existing_ids.max() + 1:03d}"
            new_doc = pd.DataFrame([[new_doc_id, doc_name, specialty, office]],
                                   columns = doctors.columns)
            updated_doctors = pd.concat([doctors, new_doc], ignore_index = True)
            updated_doctors.to_csv(get_data_path("doctors.csv"), index = False)
            st.success(f"Doctor added with ID {new_doc_id}!")
            st.rerun()

if __name__ == "__main__":
    main()