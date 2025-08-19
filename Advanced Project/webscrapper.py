# IGNORE THIS!!!!!!!!!!!
# # import requests
# # import pandas as pd
# # import streamlit as st


# # class GlassdoorJobSearch:
# #     def __init__(self):
# #         # --- API credentials ---
# #         self.api_key = "307779df78mshb912b5b4783343ep17b2e7jsn450cade0db35"
# #         self.api_host = "glassdoor-real-time.p.rapidapi.com"

# #         self.headers = {
# #             "X-RapidAPI-Key": self.api_key,
# #             "X-RapidAPI-Host": self.api_host
# #         }

# #     # --- Get location ID ---
# #     def find_location_id(self, country: str, state_or_city: str = None) -> str:
# #         url = f"https://{self.api_host}/jobs/location"
# #         response = requests.get(url, headers=self.headers, params={"query": country})

# #         if response.status_code != 200:
# #             st.error(f"Failed to get location data: {response.status_code} - {response.text}")
# #             return None

# #         locations = response.json().get("data", [])
# #         if not locations:
# #             st.warning("No location data found.")
# #             return None

# #         country_title = country.strip().title()
# #         city_title = state_or_city.strip().title() if state_or_city else None

# #         if city_title:
# #             for loc in locations:
# #                 if loc.get("locationName") == city_title:
# #                     st.info(f"Found location match for city/state: {city_title}")
# #                     return loc.get("locationId")

# #         for loc in locations:
# #             if loc.get("locationName") == country_title:
# #                 st.info(f"Using country-level location ID: {country_title}")
# #                 return loc.get("locationId")

# #         st.warning("No exact location match found. Using the first available location ID.")
# #         return locations[0].get("locationId") if locations else None

# #     # --- Search jobs ---
# #     def search_jobs(self, query: str, location_id: str):
# #         url = f"https://{self.api_host}/jobs/search"
# #         params = {
# #             "query": query,
# #             "locationId": location_id,
# #             "page": 1
# #         }

# #         resp = requests.get(url, headers=self.headers, params=params)
# #         st.write(f"Job Search response code: {resp.status_code}")

# #         if resp.status_code != 200:
# #             st.error(f"Failed to get jobs: {resp.status_code} - {resp.text}")
# #             return None

# #         return resp.json()

# #     # --- Convert job data to DataFrame ---
# #     def jobs_to_dataframe(self, jobs):
# #         job_list = []

# #         for job in jobs:
# #             jobview = job.get("jobview", {})
# #             header = jobview.get("header", {})
# #             employer = header.get("employer", {})
# #             job_info = jobview.get("job", {})
# #             indeed_attr = header.get("indeedJobAttribute", {})
# #             extracted_attrs = indeed_attr.get('extractedJobAttributes', []) if indeed_attr else []

# #             job_data = {
# #                 "Job Title": job_info.get("jobTitleText"),
# #                 "Company": employer.get("name"),
# #                 "Location": header.get("locationName"),
# #                 "Rating": header.get("rating"),
# #                 "Employment Type": ", ".join([attr.get("value") for attr in extracted_attrs if attr.get("key") == "CF3CP"]),
# #                 "Easy Apply": header.get("easyApply"),
# #                 "Age (Days)": header.get("ageInDays"),
# #                 "Job URL": f"https://www.glassdoor.com{header.get('jobViewUrl')}" if header.get("jobViewUrl") else None
# #             }

# #             job_list.append(job_data)

# #         return pd.DataFrame(job_list)


# # # --- UI code ---
# # def main():
# #     st.set_page_config(layout="wide")

# #     # CSS
# #     st.markdown("""
# #     <style>
# #     .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
# #     [data-testid="stHorizontalBlock"] {min-height: 100vh; margin: 0 !important;}
# #     [data-testid="stHorizontalBlock"] > div:first-of-type {
# #         background-color: #191970; color: white; display: flex;
# #         flex-direction: column; align-items: center; justify-content: center;
# #         text-align: center; padding: 50px; height: 100vh; min-height: 100vh;
# #     }
# #     [data-testid="stHorizontalBlock"] > div:first-of-type h1 {
# #         margin: 150px 0 0 0 !important; padding: 0 !important; text-align: center !important;
# #     }
# #     [data-testid="stHorizontalBlock"] > div:last-of-type {
# #         background-color: #FFD700; display: flex; flex-direction: column;
# #         align-items: center; justify-content: center; padding: 100px 100px 50px 100px;
# #     }
# #     [data-testid="stForm"] {width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;}
# #     .stForm {background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important;
# #              max-width: 450px; width: 90%;}
# #     label {font-weight: bold !important; color: black !important; display: block; text-align: left; margin-top: 10px;}
# #     .stTextInput input, .stTextArea textarea {color: black; background-color: white; border-radius: 8px; padding: 8px; width: 100%;}
# #     .stButton > button {display: block; margin: 25px auto 0 auto; border-radius: 10px; padding: 10px 20px; font-weight: bold;}
# #     </style>
# #     """, unsafe_allow_html=True)

# #     # Initialize class (with API key + host already inside)
# #     gd = GlassdoorJobSearch()

# #     col1, col2 = st.columns([2, 3])
# #     with col1:
# #         st.title("💼 Welcome to Glassdoor Job Search!")
# #     with col2:
# #         with st.form("job_search"):
# #             query = st.text_input("Enter the job title or keyword:", "")
# #             country = st.text_input("Enter the country:", "")
# #             state_or_city = st.text_input("Enter the state or city (optional):", "")
# #             submitted = st.form_submit_button("Search Jobs")

# #         if submitted:
# #             if not query or not country:
# #                 st.warning("Please fill in both the job query and the country.")
# #                 return
# #             location_id = gd.find_location_id(country, state_or_city if state_or_city else None)
# #             if not location_id:
# #                 st.error("Could not find a valid location ID.")
# #                 return
# #             st.success(f"Using location ID: {location_id}")
# #             data = gd.search_jobs(query, location_id)
# #             if not data:
# #                 st.warning("No data returned from job search.")
# #                 return
# #             jobs = data.get("data", {}).get("jobListings", [])
# #             if not jobs:
# #                 st.warning("No job listings found.")
# #                 return
# #             df_jobs = gd.jobs_to_dataframe(jobs)
# #             st.write("### 🧾 Job Listings")
# #             st.dataframe(df_jobs)


# # if __name__ == "__main__":
# #     main()
