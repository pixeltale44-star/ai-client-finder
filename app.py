import streamlit as st
from scraper import scrape_gmaps_no_website
from site_generator import create_demo_site

st.title("AI Client Finder & Site Generator")

niche = st.text_input("Niche (e.g. Plumbers)", "Plumbers")
city = st.text_input("City", "Bentonville AR")

if "leads" not in st.session_state:
    st.session_state.leads = []

if st.button("Find Leads Without Websites"):
    st.info("Scanning Google Maps... this can take 20-40 seconds.")
    query = f"{niche} in {city}"
    st.session_state.leads = scrape_gmaps_no_website(query)
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
