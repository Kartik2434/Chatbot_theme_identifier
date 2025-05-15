import streamlit as st
import requests

API_URL = "http://localhost:8000/api"

st.title("Research Chatbot with Theme Identification")

# --- Document Upload ---
st.header("Upload Document")
uploaded_file = st.file_uploader("Choose a file (PDF, image, or text)")
if uploaded_file is not None:
    with st.spinner("Uploading and processing..."):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post(f"{API_URL}/upload/", files=files)
        if response.ok:
            st.success(f"Uploaded: {uploaded_file.name}")
        else:
            st.error("Upload failed.")

# --- List Documents ---
st.header("Uploaded Documents")
docs_resp = requests.get(f"{API_URL}/documents/")
if docs_resp.ok:
    docs = docs_resp.json()["documents"]
    if docs:
        st.table(docs)
    else:
        st.info("No documents uploaded yet.")
else:
    st.error("Could not fetch documents.")

# --- Query Section ---
st.header("Ask a Research Question")
query = st.text_input("Enter your question:")
if st.button("Submit Query") and query:
    with st.spinner("Searching and synthesizing themes..."):
        resp = requests.post(f"{API_URL}/query/", data={"query": query})
        if resp.ok:
            data = resp.json()
            st.subheader("Relevant Extracted Answers:")
            if data["results"]:
                for ans in data["results"]:
                    st.markdown(f"**Doc:** {ans['doc_id']} | **Location:** {ans['location']}\n\n{ans['text']}")
                    st.markdown("---")
            else:
                st.info("No relevant answers found.")
            st.subheader("Synthesized Themes:")
            st.markdown(data["synthesized"])
        else:
            st.error("Query failed.") 