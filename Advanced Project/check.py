import streamlit as st
from glassdoorapi import GlassdoorJobSearch  # your class file


def main():
    st.set_page_config(layout="wide")

    # Check which page we are on
    current_page = st.session_state.get("current_page", "Home")

    if current_page == "Home":
        # CSS for main page (full-bleed split screen)
        st.markdown("""
        <style>
        .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
        [data-testid="stHorizontalBlock"] {min-height: 100vh; margin: 0 !important;}
        [data-testid="stHorizontalBlock"] > div:first-of-type {
            background-color: #191970; color: white; display: flex;
            flex-direction: column; align-items: center; justify-content: center;
            text-align: center; padding: 50px; height: 100vh; min-height: 100vh;
        }
        [data-testid="stHorizontalBlock"] > div:first-of-type h1 {
            margin: 150px 0 0 0 !important; padding: 0 !important; text-align: center !important;
        }
        [data-testid="stHorizontalBlock"] > div:last-of-type {
            background-color: #FFD700; display: flex; flex-direction: column;
            align-items: center; justify-content: center; padding: 100px 100px 50px 100px;
        }
        [data-testid="stForm"] {width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;}
        .stForm {background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important;
                max-width: 450px; width: 90%;}
        label {font-weight: bold !important; color: black !important; display: block; text-align: left; margin-top: 10px;}
        .stTextInput input, .stTextArea textarea {color: black; background-color: white; border-radius: 8px; padding: 8px; width: 100%;}
        .stButton > button {display: block; margin: 25px auto 0 auto; border-radius: 10px; padding: 10px 20px; font-weight: bold;}
        </style>
        """, unsafe_allow_html=True)
    else:
        # CSS for other pages (bring padding back so titles aren’t stuck to the top)
        st.markdown("""
        <style>
        .block-container {padding-top: 2rem !important;}
        </style>
        """, unsafe_allow_html=True)

    # --- UI code for the home page ---
    gd = GlassdoorJobSearch()

    col1, col2 = st.columns([2, 3])
    with col1:
        st.title("💼 Welcome to Glassdoor Job Search!")
    with col2:
        with st.form("job_search"):
            query = st.text_input("Enter the job title or keyword:", "")
            country = st.text_input("Enter the country:", "")
            state_or_city = st.text_input("Enter the state or city (optional):", "")
            submitted = st.form_submit_button("Search Jobs")

        if submitted:
            if not query or not country:
                st.warning("Please fill in both the job query and the country.")
                return
            location_id = gd.find_location_id(country, state_or_city if state_or_city else None)
            if not location_id:
                st.error("Could not find a valid location ID.")
                return
            st.success(f"Using location ID: {location_id}")
            data = gd.search_jobs(query, location_id)
            if not data:
                st.warning("No data returned from job search.")
                return
            jobs = data.get("data", {}).get("jobListings", [])
            if not jobs:
                st.warning("No job listings found.")
                return
            df_jobs = gd.jobs_to_dataframe(jobs)
            st.session_state["job_results"] = df_jobs
            st.success("✅ Jobs found! Go to **Job Listings** page from the sidebar.")


if __name__ == "__main__":
    # Mark that this is the main page
    st.session_state["current_page"] = "Home"
    main()
