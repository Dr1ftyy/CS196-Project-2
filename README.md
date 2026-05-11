# MedDesk 🏥

A Python/Streamlit data application designed from the perspective of a hospital secretary. MedDesk allows staff to manage patient records, appointments, billing, and doctor schedules — all from a clean, interactive web interface. Patients can also log in to view their own records, schedule appointments, and update their information.

---

## How to Run

Make sure you have the required libraries installed:

```bash
python3 -m pip install streamlit pandas matplotlib
```

Then run the app:

```bash
streamlit run dist/main.py
```

---

## Login Credentials

**Patient Login:** Enter your Patient ID (e.g. `P001`, `P002`, `P003`)
New patients can register directly from the login screen.

**Admin Login:** Password is `admin123`

---

## Controls & Features

### Patient View
- View personal information (DOB, insurance, condition)
- View all appointments with doctor notes and status
- View billing records with insurance breakdown and out-of-pocket costs
- Schedule new appointments with doctor, date, time, and reason
- Update personal information (phone, email, insurance, condition)
- Fill out a health questionnaire before visits

### Admin View (Secretary)
- **Patients tab** — search, add, and delete patient records
- **Appointments tab** — view, filter, update notes/status, and delete appointments
- **Billing tab** — view all billing records, add new billing entries
- **Analytics tab** — charts showing patients per doctor and conditions breakdown, plus summary metrics
- **Doctors tab** — view and add doctors to the system

---

## Data & Save/Load

All data is stored in CSV files inside the `data/` folder. Every time the app is restarted, it reads fresh from the CSVs so all changes are retained. Writing back to CSV happens whenever a user adds, edits, or deletes a record.

---

## AI Usage

Claude (claude.ai) was used during this project for debugging, explaing errors and guidance along with creating this README

---

## Sources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/index.html)