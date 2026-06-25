import streamlit as st

st.set_page_config(
    page_title="AI PolyVerse",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI PolyVerse")
st.subheader("聚智宇宙")

st.write("AI + Plastic Engineering + English Learning")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.button("AI Terms")

with col2:
    st.button("Plastic Engineering")

with col3:
    st.button("AI Scientists")
