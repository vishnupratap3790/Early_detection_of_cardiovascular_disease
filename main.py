import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from transformers import pipeline 


os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")



working_dir = os.path.dirname(os.path.abspath(__file__))


heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))



chatbot_pipeline = pipeline("text-generation", model="gpt2")
def chatbot(message):
    response = chatbot_pipeline(message, max_length=50, num_return_sequences=1)[0]['generated_text']
    return response.strip()


diseases_symptoms = [
   "Chest pain", "Shortness of breath", "Dizziness"
]


 
doctors_info = {
    "Chest pain": [("Dr. John Doe", "123-456-7890"), ("Dr. Jane Smith", "987-654-3210")],
    "Shortness of breath": [("Dr. Michael Johnson", "456-789-0123"), ("Dr. Emily Brown", "321-654-0987")],
    "Dizziness": [("Dr. Sarah Lee", "789-012-3456"), ("Dr. David Wilson", "543-210-9876")]
}

symptoms_medicines = {
    "Chest pain": ["Aspirin", "Nitroglycerin", "Atenolol"],
    "Shortness of breath": ["Albuterol", "Prednisone", "Oxygen therapy"],
    "Dizziness": ["Meclizine", "Dimenhydrinate", "Scopolamine"]
}

# Function to recommend doctors and suggest medicines
def recommend_doctors_and_medicines():
    st.title("Doctor Recommendation and Medicine Suggestion")

   
    selected_disease = st.selectbox("Select Disease:", list(diseases_symptoms))

     
    if selected_disease in doctors_info:
        st.subheader(f"Recommended doctors for {selected_disease}:")
        for doctor, contact_number in doctors_info[selected_disease]:
            st.write(f"**Name:** {doctor}")
            st.write(f"**Contact Number:** {contact_number}")
            st.markdown("---")   
    else:
        st.write("No doctors found for the selected disease.")

    if selected_disease in diseases_symptoms:
        st.subheader(f"Suggested medicines for {selected_disease}:")
        for medicine in symptoms_medicines[selected_disease]:
            st.write(f"- {medicine}")
    else:
        st.write("No medicines found for the selected symptom.")

         


# Sidebar for navigation
with st.sidebar:
    selected = option_menu('Cardiovascular Disease Prediction System',
                           ['Cardiovascular Disease Prediction', 'Chatbot','Doctor Recommendation and Medicine Suggestion'],
                           menu_icon='hospital-fill',
                           icons=['heart', 'chat', 'capsule-pill'],
                           default_index=0)

 
# Heart Disease Prediction Page
if selected == 'Cardiovascular Disease Prediction':

   
    st.title('Cardiovascular Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.selectbox('Sex', ['Male', 'Female'])

    with col3:
        cp = st.selectbox('Chest Pain types', ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'])

    with col1:
        trestbps = st.text_input('Resting Blood Pressure (mmHg)')

    with col2:
        chol = st.text_input('Serum Cholestoral (mg/dl)')

    with col3:
        fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', ['False', 'True'])

    with col1:
        restecg = st.selectbox('Resting Electrocardiographic results', ['Normal', 'ST-T wave abnormality', 'Left ventricular hypertrophy'])

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')

    with col3:
        exang = st.selectbox('Exercise Induced Angina', ['No', 'Yes'])

    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')

    with col2:
        slope = st.selectbox('Slope of the peak exercise ST segment', ['Upsloping', 'Flat', 'Downsloping'])

    with col3:
        ca = st.text_input('Number of Major vessels colored by flourosopy')

    with col1:
        thal = st.selectbox('Thal', ['Normal', 'Fixed Defect', 'Reversible Defect'])

  
    heart_diagnosis = ''

    
    if st.button('Heart Disease Test Result'):

        
        try:
            user_input = [float(age), 1 if sex == 'Male' else 0, ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'].index(cp),
                          float(trestbps), float(chol), 1 if fbs == 'True' else 0,
                          ['Normal', 'ST-T wave abnormality', 'Left ventricular hypertrophy'].index(restecg),
                          float(thalach), 1 if exang == 'Yes' else 0, float(oldpeak),
                          ['Upsloping', 'Flat', 'Downsloping'].index(slope), float(ca), ['Normal', 'Fixed Defect', 'Reversible Defect'].index(thal)]
        except ValueError:
            st.error("Please enter valid numerical values for all input fields.")
            st.error(str(ValueError))
            raise ValueError("Invalid input values")

        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is predicted to have heart disease.'
            st.warning(heart_diagnosis)
        else:
            heart_diagnosis = 'The person is predicted to be healthy without any heart disease.'
            st.success(heart_diagnosis)
            


if selected == 'Chatbot':
    st.title('🤖 Chatbot')
    st.markdown("""
    <style>
    .chat-container {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .chatbot-header {
        font-size: 24px;
        font-weight: bold;
        color: #4CAF50;
    }
    .user-input {
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .chatbot-response {
        background-color: #e8f5e9;
        padding: 10px;
        border-radius: 10px;
        color: #000;
    }
    </style>
    
    """, unsafe_allow_html=True)

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('<div class="chatbot-header">Ask me anything! I\'m here to help with your health-related queries.</div>', unsafe_allow_html=True)

    user_input = st.text_input("You:", "", key="user_input", help="Type your message here")

    if st.button('Submit'):
        if user_input!="":
            chatbot_response = chatbot(user_input)
            st.markdown('<div class="chatbot-response focus" id="chatbot_response">', unsafe_allow_html=True)
            st.text_area("Chatbot:", chatbot_response, height=200, key="chatbot_response", disabled=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.warning("Please enter a message.")
    
    st.markdown('</div>', unsafe_allow_html=True)

        
    


if selected == 'Doctor Recommendation and Medicine Suggestion':
    recommend_doctors_and_medicines()
     
    
