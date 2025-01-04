import streamlit as st

# Create tabs for the profile page
tabs = st.tabs(["Profile", "Candidate Details"])

# Profile page where the user inputs details
with tabs[0]:
    st.header("Profile Page")

    # Profile form
    with st.form(key='profile_form'):
        st.subheader("Basic Information")
        name = st.text_input("Name")
        email = st.text_input("Email")
        mobile = st.text_input("Mobile Number")
        age = st.number_input("Age", min_value=1, max_value=100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        submit_button = st.form_submit_button("Submit")

    if submit_button:
        st.write("### Submitted Information")
        st.write(f"**Name**: {name}")
        st.write(f"**Email**: {email}")
        st.write(f"**Mobile Number**: {mobile}")
        st.write(f"**Age**: {age}")
        st.write(f"**Gender**: {gender}")

# Candidate details tab for extra info
with tabs[1]:
    st.header("Candidate Details (Additional Info)")
    st.subheader("Yoga Preferences")
    experience = st.selectbox("Yoga Experience", ["Beginner", "Intermediate", "Advanced"])
    goals = st.text_area("Yoga Goals", "e.g. Flexibility, Stress Relief, Weight Loss")

    st.write(f"**Yoga Experience**: {experience}")
    st.write(f"**Yoga Goals**: {goals}")
