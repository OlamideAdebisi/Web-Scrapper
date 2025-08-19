import requests
import pandas as pd
import streamlit as st
class GlassdoorJobSearch:
    def __init__(self):
        # --- API credentials ---
        self.api_key = "307779df78mshb912b5b4783343ep17b2e7jsn450cade0db35"
        self.api_host = "glassdoor-real-time.p.rapidapi.com"

        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }

    # --- Get location ID ---
    def find_location_id(self, country: str, state_or_city: str = None) -> str:
        url = f"https://{self.api_host}/jobs/location"
        response = requests.get(url, headers=self.headers, params={"query": country})

        if response.status_code != 200:
            st.error(f"Failed to get location data: {response.status_code} - {response.text}")
            return None

        locations = response.json().get("data", [])
        if not locations:
            st.warning("No location data found.")
            return None

        country_title = country.strip().title()
        city_title = state_or_city.strip().title() if state_or_city else None

        if city_title:
            for loc in locations:
                if loc.get("locationName") == city_title:
                    st.info(f"Found location match for city/state: {city_title}")
                    return loc.get("locationId")

        for loc in locations:
            if loc.get("locationName") == country_title:
                st.info(f"Using country-level location ID: {country_title}")
                return loc.get("locationId")

        st.warning("No exact location match found. Using the first available location ID.")
        return locations[0].get("locationId") if locations else None

    # --- Search jobs ---
    def search_jobs(self, query: str, location_id: str):
        url = f"https://{self.api_host}/jobs/search"
        params = {
            "query": query,
            "locationId": location_id,
            "page": 1
        }

        resp = requests.get(url, headers=self.headers, params=params)
        st.write(f"Job Search response code: {resp.status_code}")

        if resp.status_code != 200:
            st.error(f"Failed to get jobs: {resp.status_code} - {resp.text}")
            return None

        return resp.json()

    # --- Convert job data to DataFrame ---
    def jobs_to_dataframe(self, jobs):
        job_list = []

        for job in jobs:
            jobview = job.get("jobview", {})
            header = jobview.get("header", {})
            employer = header.get("employer", {})
            job_info = jobview.get("job", {})
            indeed_attr = header.get("indeedJobAttribute", {})
            extracted_attrs = indeed_attr.get('extractedJobAttributes', []) if indeed_attr else []

            job_data = {
                "Job Title": job_info.get("jobTitleText"),
                "Company": employer.get("name"),
                "Location": header.get("locationName"),
                "Rating": header.get("rating"),
                "Employment Type": ", ".join([attr.get("value") for attr in extracted_attrs if attr.get("key") == "CF3CP"]),
                "Easy Apply": header.get("easyApply"),
                "Age (Days)": header.get("ageInDays"),
                "Job URL": f"https://www.glassdoor.com{header.get('jobViewUrl')}" if header.get("jobViewUrl") else None
            }

            job_list.append(job_data)

        return pd.DataFrame(job_list)
