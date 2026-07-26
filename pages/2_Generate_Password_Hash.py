import streamlit as st
import bcrypt

st.title("🔑 Generate a Password Hash")
st.write("Type a plain password, get the hashed version. Paste that hash into `config.yaml` under the matching username.")

plain_password = st.text_input("Plain text password", type="password")

if st.button("Generate Hash"):
    if plain_password:
        hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()
        st.success("Copy this into config.yaml:")
        st.code(hashed)
    else:
        st.warning("Type a password first.")
