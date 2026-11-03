import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:5001"
st.set_page_config(page_title="SZABIST Student Management", page_icon="🎓")
st.title("Student Management System")
st.caption("Streamlit frontend connected to the Flask REST API")

def api_error(response):
    try:
        return response.json().get("error", response.text)
    except Exception:
        return response.text

try:
    response = requests.get(f"{API}/students", timeout=3)
    response.raise_for_status()
    students = response.json()
except requests.RequestException:
    students = None
    st.error("Cannot connect to Flask API. Start app.py first on port 5001.")

if students is not None:
    st.subheader("All Students")
    if students:
        st.dataframe(pd.DataFrame(students), use_container_width=True, hide_index=True)
    else:
        st.info("No student records yet. Add the first student below.")

    st.divider()
    left, right = st.columns(2)
    with left:
        st.subheader("Add New Student")
        with st.form("add_student", clear_on_submit=True):
            name = st.text_input("Student name")
            department = st.text_input("Department")
            email = st.text_input("Email")
            submitted = st.form_submit_button("Add student")
            if submitted:
                r = requests.post(f"{API}/students", json={
                    "name": name, "department": department, "email": email
                }, timeout=5)
                if r.status_code == 201:
                    st.success("Student added successfully.")
                    st.rerun()
                else:
                    st.error(api_error(r))

    with right:
        st.subheader("Update Existing Student")
        if students:
            ids = [s["id"] for s in students]
            selected = st.selectbox("Select student ID", ids, key="update_id")
            current = next(s for s in students if s["id"] == selected)
            with st.form("update_student"):
                new_name = st.text_input("Name", current["name"])
                new_department = st.text_input("Department", current["department"])
                new_email = st.text_input("Email", current["email"])
                update = st.form_submit_button("Update student")
                if update:
                    r = requests.put(f"{API}/students/{selected}", json={
                        "name": new_name, "department": new_department, "email": new_email
                    }, timeout=5)
                    if r.ok:
                        st.success("Student updated.")
                        st.rerun()
                    else:
                        st.error(api_error(r))
        else:
            st.info("Add a student first to enable editing.")

    st.divider()
    st.subheader("Delete Student")
    if students:
        delete_id = st.selectbox("Choose student to delete", [s["id"] for s in students], key="delete_id")
        if st.button("Delete selected student", type="primary"):
            r = requests.delete(f"{API}/students/{delete_id}", timeout=5)
            if r.ok:
                st.success("Student deleted.")
                st.rerun()
            else:
                st.error(api_error(r))

    if st.button("Refresh records"):
        st.rerun()
