import streamlit as st
import pickle
import pandas as pd

st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #F4F9FF;
}

/* Input boxes */
.stNumberInput, .stSelectbox, .stSlider {
    background-color: #FFFFFF;
    border-radius: 10px;
    padding: 5px;
}

/* Button styling */
.stButton>button {
    background-color: #2E86C1;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

.stButton>button:hover {
    background-color: #1B4F72;
    color: white;
}


</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Credit & Loan Risk Predictor", layout="wide")


col1, col2 = st.columns([1, 2])

with col1:
    st.image(
        "https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_750,h_394/https://authbridge.com/wp-content/uploads/2025/09/Creadit-Risk-Assessment-blog-image-1024x538.png",
        width=500
    )

with col2:
    st.markdown("""
    <h1 style='color:#2E86C1;'>💳 Credit & Loan Risk Prediction</h1>
    <h4 style='color:gray;'>Smart Credit Decisions using AI</h4>
    <p style='color:#555;'>
    This system analyzes customer financial data to predict the likelihood of loan default. 
    It helps banks and financial institutions make safer and smarter lending decisions.
    </p>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


with open(r"C:\Users\OM\Desktop\Project\project_clg\loan_risk_model.pkl", "rb") as f:
    model = pickle.load(f)

with open(r"C:\Users\OM\Desktop\Project\project_clg\model_columns.pkl", "rb") as f:
    model_columns = pickle.load(f)


st.subheader("📋 Enter Customer Details")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 18, 70)
    income = st.number_input("Annual Income", 10000, 1000000)
    credit_score = st.number_input("Credit Score", 300, 900)
    loan_amount = st.number_input("Loan / Credit Amount", 1000, 500000)

with col2:
    accounts = st.number_input("Active Accounts", 0, 20)
    past_defaults = st.number_input("Past Default Count", 0, 10)
    credit_limit = st.number_input("Credit Limit", 1000, 1000000)
    utilization = st.slider("Utilization Ratio", 0.0, 1.0)


col3, col4, col5 = st.columns(3)

with col3:
    gender = st.selectbox("Gender", ["Male", "Female"])

with col4:
    employment = st.selectbox("Employment Type", ["Salaried", "Self-Employed", "Unemployed"])

with col5:
    application = st.selectbox("Application Type", ["Credit Card", "Home Loan", "Personal Loan"])


input_data = pd.DataFrame(columns=model_columns)
input_data.loc[0] = 0

input_data['Age'] = age
input_data['Annual_Income'] = income
input_data['Credit_Score'] = credit_score
input_data['Loan_or_Credit_Amount'] = loan_amount
input_data['Number_of_Active_Accounts'] = accounts
input_data['Past_Default_Count'] = past_defaults
input_data['Credit_Limit'] = credit_limit
input_data['Utilization_Ratio'] = utilization

input_data['Gender_Male'] = 1 if gender == "Male" else 0

if employment == "Self-Employed":
    input_data['Employment_Type_Self-Employed'] = 1
elif employment == "Unemployed":
    input_data['Employment_Type_Unemployed'] = 1

if application == "Credit Card":
    input_data['Application_Type_Credit Card'] = 1
elif application == "Home Loan":
    input_data['Application_Type_Home Loan'] = 1
elif application == "Personal Loan":
    input_data['Application_Type_Personal Loan'] = 1


st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Predict Risk"):
    prediction = model.predict(input_data)
    prob = model.predict_proba(input_data)

    risk_score = prob[0][1]
    default_status = prediction[0]

    st.subheader("📊 Prediction Result")


    label = "DEFAULT" if default_status == 1 else "NO DEFAULT"
    st.write(f"### Result: **{label}**")

    # Probability
    st.write(f"### Risk Probability: **{risk_score:.2f}**")

    # Risk Level
    if risk_score > 0.7:
        st.error("🔴 High Risk Customer")
    elif risk_score > 0.4:
        st.warning("🟡 Medium Risk Customer")
    else:
        st.success("🟢 Low Risk Customer")
