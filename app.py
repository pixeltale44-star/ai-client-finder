import subprocess
import sys
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

from scraper import scrape_gmaps_no_website
from site_generator import create_demo_site

# --- One-time Chromium install fix for Streamlit Cloud ---
@st.cache_resource
def install_playwright_browser():
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
    return True

install_playwright_browser()

# --- Login setup ---
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error('Username or password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please log in on the left to use the tool. New here? Check the Pricing page in the sidebar.')
elif st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    username = st.session_state["username"]
    user_plan = config['credentials']['usernames'][username].get('plan', 'free')

    st.sidebar.write(f"Plan: **{user_plan.title()}**")
    st.title("AI Client Finder & Site Generator")

    max_leads = 5 if user_plan == "free" else 25

    niche = st.text_input("Niche (e.g. Plumbers)", "Plumbers")
    city = st.text_input("City", "Bentonville AR")

    if "leads" not in st.session_state:
        st.session_state.leads = []

    if st.button("Find Leads Without Websites"):
        st.info("Scanning Google Maps... this can take 20-40 seconds.")
        query = f"{niche} in {city}"
        st.session_state.leads = scrape_gmaps_no_website(query, max_results=max_leads)
        st.success(f"Found {len(st.session_state.leads)} leads without a website.")

    for i, lead in enumerate(st.session_state.leads):
        st.subheader(lead['name'])
        st.write(f"📞 Phone: {lead['phone']}")
        st.warning("⚠️ No Website Detected")

        if st.button(f"Generate Preview Site", key=f"gen_{i}"):
            site_path = create_demo_site(lead)
            st.success(f"Site generated! Saved at: {site_path}")
            st.code(
                f"Hey! I noticed {lead['name']} doesn't have a website yet — "
                f"I put together a quick preview of what one could look like. Want me to send it over?"
            )
