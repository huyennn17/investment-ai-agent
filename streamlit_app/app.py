import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

# Initialize user_id once per session
if "user_id" not in st.session_state:
    try:
        res = requests.get(f"{BASE_URL}/user/get_id")
        st.session_state.user_id = res.json().get("user_id")
    except Exception as e:
        st.error("Failed to connect to backend.")
        st.stop()

st.title("InvestmentAI Assistant")

if "user_id" not in st.session_state:
    r = requests.get(f"{BASE_URL}/user/get_id")
    st.session_state.user_id = r.json()["user_id"]

# Fetch all chat history across all services
history_response = requests.get(f"{BASE_URL}/chat/history/{st.session_state.user_id}")
if history_response.status_code == 200:
    st.subheader("Chat History")
    history_data = history_response.json()
    for chat in history_data:
        st.markdown(f"**You:** {chat['message']}")
        st.markdown(f"**AI:** {chat['response']}")
        st.markdown("---")
else:
    st.warning("Could not fetch chat history.")

tab = st.selectbox("Choose a service", ["Budget", "Invest", "PDF Q&A", "General Q&A", "Chat History"])

if tab == "Budget":
    st.subheader("Budget Planning")
    user_input = st.text_area("Describe your budget situation:")
    if st.button("Get Budget Plan"):
        response = requests.post(
            f"{BASE_URL}/budget/",
            json={"user_input": user_input},
            params={"user_id": st.session_state.user_id}
        )
        st.json(response.json())

elif tab == "Invest":
    st.subheader("Investment Advice")

    name = st.text_input("Name", value="client")
    risk = st.selectbox("Risk Tolerance", ["low", "medium", "high"])
    sector = st.text_input("Preferred Sector (e.g. tech, healthcare)")
    investment_horizon = st.selectbox("Investment Horizon", ["short-term", "long-term"])
    capital_amount = st.number_input("Capital Amount", min_value=0.0)
    income_stability = st.selectbox("Income Stability", ["stable", "fluctuating"])
    experience_level = st.selectbox("Investment Experience", ["beginner", "intermediate", "expert"])
    location = st.text_input("Location (e.g. US, Asia)")

    if st.button("Get Investment Advice"):
        response = requests.post(
            f"{BASE_URL}/invest/",
            json={
                "name": name,
                "risk": risk,
                "sector": sector,
                "investment_horizon": investment_horizon,
                "capital_amount": capital_amount,
                "income_stability": income_stability,
                "experience_level": experience_level,
                "location": location
            },
            params={"user_id": st.session_state.user_id}
        )
        st.json(response.json())

elif tab == "PDF Q&A":
    st.subheader("Ask a Question about a PDF")
    question = st.text_input("Your question:")
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
    if pdf_file and st.button("Ask"):
        files = {"file": (pdf_file.name, pdf_file)}
        data = {"question": question}
        response = requests.post(
            f"{BASE_URL}/pdf/",
            files=files,
            data=data,
            params={"user_id": st.session_state.user_id}
        )
        st.json(response.json())

elif tab == "General Q&A":
    st.subheader("Ask a General Finance Question")
    user_input = st.text_area("Ask anything:")
    if st.button("Ask"):
        response = requests.post(
            f"{BASE_URL}/general/",
            json={"user_input": user_input},
            params={"user_id": st.session_state.user_id}
        )
        st.json(response.json())

elif tab == "Chat History":
    st.subheader("Chat History for This Session")
    response = requests.get(f"{BASE_URL}/chat/history/{st.session_state.user_id}")
    history = response.json()
    for chat in history:
        st.markdown(f"**You:** {chat['message']}")
        st.markdown(f"**AI ({chat['source']}):** {chat['response']}")
        st.markdown("---")
