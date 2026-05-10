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
    patient_id = st.session_state.get("patient_id")
    if not patient_id:
        st.error("No patient ID found. Please login again.")
        st.stop()
    
    patients, appointments, doctors, billing = load_data()

    #get this patient's data from the csv files
    match = patients[patients["patient_id"].str.upper() == patient_id.upper()]
    if match.empty:
        st.error("Patient record not found.")
        st.stop()
    patient = match.iloc[0]

    patient_appointments = appointments[appointments['patient_id'] == patient_id]
    patient_billing = billing[billing["patient_id"] == patient_id]

    #header
    st.title(f"Welcome {patient['name']}!")
    st.caption(f"Patient ID: {patient_id}")

    #logout button 
    if st.button("Logout", key="patient_logout_btn"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.patient_id = None
        st.switch_page("main.py")

    st.divider()

    #personal info section
    st.subheader("Your Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Date of Birth", patient['dob'])
    with col2:
        st.metric("Insurance", patient['insurance'])
    with col3:
        st.metric("Condition", patient['condition'])

    st.divider()

    #appointments section
    st.subheader("Your Appointments")
    if patient_appointments.empty:
        st.info("You have no upcoming appointments.")
    else:
        for _, appt in patient_appointments.iterrows():
            doctor = doctors[doctors['doctor_id'] == appt['doctor_id']] .iloc[0]
            status_color = "green" if appt['status'] == "Completed" else "orange"
            with st.expander(f"{status_color} {appt['date']} at {appt['time']} - {doctor['name']}"):
                st.write(f"**Doctor:** {doctor['name']} ({doctor['specialty']})")
                st.write(f"**Office:** {doctor['office']}")
                st.write(f"**Status:** {appt['status']}")
                st.write(f"**Docotor Notes:** {appt['notes']}")
                if appt['status'] == 'Completed':
                    better = appt.get ('getting_better', 'N/A')
                    st.write(f"**Getting Better?** {better}")

    st.divider()

    #billing section
    st.subheader("Your Billing")
    if patient_billing.empty:
        st.info("No billing records found.")
    else:
        total_cost = 0.0
        total_oop = 0.0 #oop stands for out of pocket cost after insurance
        for _, bill in patient_billing.iterrows():
            cost = float(bill['cost'])
            coverage = float(bill['insurance_coverage'])
            oop = cost * (1 - coverage)
            total_cost += cost
            total_oop += oop

            with st.expander(f"{'✅' if bill['paid'] == 'Yes' else '❌'} {bill['procedure']} - ${cost:.2f}"):
                st.write(f"**Procedure:** {bill['procedure']}")
                st.write(f"**Total Cost:** ${cost:.2f}")
                st.write(f"**Insurance Coverage:** {int(coverage * 100)}%")
                st.write(f"**Your Out-of-Pocket Cost:** ${oop:.2f}")
                st.write(f"**Paid:** {bill['paid']}")

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Billed", f"${total_cost:.2f}")
        with col2:
            st.metric("Total Out-of-Pocket", f"${total_oop:.2f}")

    st.divider()

    #schedlue new appointment
    st.subheader("Schedule an Appointment")
    with st.form ("schedule_appt"):
        #build doctor options from doctors data frame
        doctor_options = {f"{row['name']} ({row['specality']}) - {row['office']}": row['doctor_id']
                          for _, row in doctors.iterrows()}
        selected_doctor = st.selectbox("Select a Doctor", list(doctor_options.keys()))
        appt_date = st.date_input("Preffered Date")
        appt_time = st.time_input("Preferred Time")
        reason = st.text_area("Reason for Visit")
        submittetd = st.form_submit_button("Request Appointment")

        if submitted:
            #load a fresh copy of the appts
            all_appointments = pd.read_csv(get_data_path("appointments.csv"))
            new_appt_id = f"A{len(all_appointments) + 1:03d}"
            doctor_id = doctor_options[selected_doctor]
            new_appt = pd.DataFrame([[
                new_appt_id,
            patient_id,
            doctor_id,
            str(appt_date),
            str(appt_time),
            reason,
            "Upcoming",
            ""
        ]], columns=all_appointments.columns)
        updated_appointments = pd.concat([all_appointments, new_appt], ignore_index=True)
        updated_appointments.to_csv(get_data_path("appointments.csv"), index=False)
        st.success(f"Appointment requested for {appt_date} at {appt_time}!")
        st.rerun()

    st.divider()

    #edit personal info
    st.subheader("Update Your Information")
    with st.form("update_info"):

    #patient questionarire
    st.subheader("Health Questionnaire")
    st.caption("Help us understand how you're feeling before your next visit")
    with st.form("questionnaire"):
        pain = st.slider("Pain Level (0 = none, 10 = severe)", 0, 10, 0)
        symptoms = st.text_input("Any new or ongoing symptoms?")
        medication = st.text_input("Current Medications (comma separated)")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Thank you! Your response have been noted for your doctor to review before your next appointment.")

if __name__ == "__main__":
    main()