import streamlit as st
import requests

st.title("Mini-RAG Demo")

query = st.text_input("Enter your query:")

if st.button("Search"):
    # Call your backend API (replace with your actual endpoint)
    response = requests.post("http://localhost:5000/ask", json={"q": query})
    data = response.json()

    st.subheader("Results")
    for r in data["results"]:
        st.markdown(f"**Doc:** {r['doc_name']} | **Score:** {r['score']:.2f}")
        st.write(r["text"][:400] + " ...")  # show first 400 chars
        st.divider()
