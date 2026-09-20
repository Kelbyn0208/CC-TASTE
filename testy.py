import streamlit as st

st.title("Prueba de lectura de secretos")

if "SUPABASE_URL" in st.secrets:
    st.success("¡Leído con éxito!")
    st.write("URL:", st.secrets["SUPABASE_URL"])
else:
    st.error("No se encontró SUPABASE_URL en secrets.toml")