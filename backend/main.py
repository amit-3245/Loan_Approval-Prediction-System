from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Loan Approval Prediction API")

# Load trained pipeline
model = joblib.load("../model/model.pkl")

class LoanRequest(BaseModel):
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str

@app.get("/")
def health_check():
    return {"status": "API running successfully"}

@app.post("/predict")
def predict_loan(data: LoanRequest):
    try:
        input_df = pd.DataFrame([data.dict()])
        prediction = model.predict(input_df)[0]

        return {
            "loan_status": "Approved" if prediction == 1 else "Rejected"
        }

    except Exception as e:
        return {"error": str(e)}
