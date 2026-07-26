import streamlit as st
import streamlit_authenticator as stauth

st.title("🔑 Generate a Password Hash")
st.write("Type a plain password, get the hashed version. Paste that hash into `config.yaml` under the matching username.")

plain_password = st.text_input("Plain text password", type="password")

if st.button("Generate Hash"):
    if plain_password:
        hashed = stauth.Hasher.hash(plain_password)
        st.success("Copy this into config.yaml:")
        st.code(hashed)
    else:
        st.warning("Type a password first.")
