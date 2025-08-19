import streamlit as st

def job_listings_page():
    st.set_page_config(layout="wide")

    # CSS fix → bring back padding for non-home pages
    st.markdown("""
    <style>
    .block-container {padding-top: 2rem !important;}
    </style>
    """, unsafe_allow_html=True)

    st.title("📋 Job Listings")

    if "job_results" not in st.session_state:
        st.warning("⚠️ No job results found. Please go back to the Home page and search for jobs first.")
        return

    df_jobs = st.session_state["job_results"]
    st.dataframe(df_jobs, use_container_width=True)


if __name__ == "__main__":
    job_listings_page()
