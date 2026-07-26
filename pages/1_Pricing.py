import streamlit as st

st.title("AI Client Finder — Plans")
st.write("Find local businesses without a website, and auto-generate a demo site to pitch them, in seconds.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Free")
    st.write("₹0 / month")
    st.write("- 5 leads per search")
    st.write("- Manual demo generation")
    st.write("- 1 niche/city at a time")

with col2:
    st.subheader("Pro")
    st.write("₹999 / month")
    st.write("- Unlimited leads per search")
    st.write("- Priority support")
    st.write("- Multiple saved searches")

with col3:
    st.subheader("Agency")
    st.write("₹2,999 / month")
    st.write("- Everything in Pro")
    st.write("- White-label demo sites")
    st.write("- 5 team logins")

st.divider()
st.write("To subscribe, message us and we'll set up your login within 24 hours.")
st.write("📧 your-email@example.com")
