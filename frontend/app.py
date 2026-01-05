import streamlit as st
import requests

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Loan Approval Predictor",
    page_icon="🏦",
    layout="centered"
)

# -------------------------------
# Custom CSS for Modern UI
# -------------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.block-container {
    padding: 2rem;
}
h1 {
    color: #2c3e50;
    text-align: center;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}
.stButton > button {
    background-color: #2e86de;
    color: white;
    font-size: 16px;
    border-radius: 8px;
    height: 45px;
    width: 100%;
}
.stButton > button:hover {
    background-color: #1b4f72;
}
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Title Section
# -------------------------------
st.markdown("<h1>🏦 Loan Approval Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Check your loan approval status using AI</p>", unsafe_allow_html=True)

# -------------------------------
# Card Layout
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

with st.form("loan_form"):
    col1, col2 = st.columns(2)

    with col1:
        Gender = st.selectbox("Gender", ["Male", "Female"])
        Married = st.selectbox("Married", ["Yes", "No"])
        Dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
        Education = st.selectbox("Education", ["Graduate", "Not Graduate"])
        Self_Employed = st.selectbox("Self Employed", ["Yes", "No"])

    with col2:
        ApplicantIncome = st.number_input("Applicant Income (₹)", min_value=0, step=1000)
        CoapplicantIncome = st.number_input("Coapplicant Income (₹)", min_value=0, step=1000)
        LoanAmount = st.number_input("Loan Amount (₹ thousands)", min_value=0, step=10)
        Loan_Amount_Term = st.number_input("Loan Term (Months)", value=360)
        Credit_History = st.selectbox("Credit History", [1.0, 0.0])
        Property_Area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

    submit = st.form_submit_button(" Predict Loan Status")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# Prediction Logic
# -------------------------------
if submit:
    payload = {
        "Gender": Gender,
        "Married": Married,
        "Dependents": Dependents,
        "Education": Education,
        "Self_Employed": Self_Employed,
        "ApplicantIncome": ApplicantIncome,
        "CoapplicantIncome": CoapplicantIncome,
        "LoanAmount": LoanAmount,
        "Loan_Amount_Term": Loan_Amount_Term,
        "Credit_History": Credit_History,
        "Property_Area": Property_Area
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload,
            timeout=10
        )
        result = response.json()

        st.markdown("---")
        if response.status_code == 200 and "loan_status" in result:
            if result["loan_status"] == "Approved":
                st.success(" Congratulations! Your loan is **APPROVED**")
            else:
                st.error(" Sorry! Your loan is **REJECTED**")
        else:
            st.error(" API Error")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error(" Backend API is not running. Please start FastAPI.")
