import streamlit as st
import csv
import os
import uploadfiles as up

# Define your function to save data
def save_data(answer):
    if len(answer) > 2:  # If there are more than 2 elements, it means the answer is from the 'yes' path
        file_path = 'mnt/data/yes_mydata.csv'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
        write_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0  # Check if file is empty or doesn't exist
        with open(file_path, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([answer[0], answer[1], answer[2], answer[3], answer[4]])
        up.upload_to_blob_storage('mnt/data/yes_mydata.csv', 'yes_response.csv')
    else:  # If there are 2 elements, it means the answer is from the 'no' path
        file_path = 'mnt/data/no_mydata.csv'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
        write_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0  # Check if file is empty or doesn't exist
        with open(file_path, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([answer[0], answer[1]])
        up.upload_to_blob_storage('mnt/data/no_mydata.csv', 'no_response.csv')
    st.write('Your data has been recorded successfully!')

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "survey"
if "answers" not in st.session_state:
    st.session_state.answers = []

def error():
    st.warning("Please fill all the required questions")

# Navigation logic
if st.session_state.page == "survey":
    # Streamlit app title
    st.title('Welcome to HR Events Survey')

    # Question 1
    if len(st.session_state.answers) == 0:
        q1 = st.radio("Have you attended any?", ["", "yes", "no"], index=0, format_func=lambda x: "Select an option" if x == "" else x)
        if q1:
            st.session_state.answers.append(q1)
    
    # Question 2 (if q1 is "yes")
    if len(st.session_state.answers) == 1 and st.session_state.answers[0] == "yes":
        q2_yes = st.radio("Have you participated in any activity?", ["", "yes", "no"], index=0, format_func=lambda x: "Select an option" if x == "" else x)
        if q2_yes:
            st.session_state.answers.append(q2_yes)
    
    # Question 3 (if q2 is "yes")
    if len(st.session_state.answers) == 2 and st.session_state.answers[1] == "yes":
        q3_yes = st.radio("Was it engaging?", ["", "yes", "no"], index=0, format_func=lambda x: "Select an option" if x == "" else x)
        if q3_yes:
            st.session_state.answers.append(q3_yes)
    
    # Question 4 (if q3 is "yes")
    if len(st.session_state.answers) == 3 and st.session_state.answers[2] == "yes":
        q4_yes = st.radio("Do you want to attend more events?", ["", "yes", "no"], index=0, format_func=lambda x: "Select an option" if x == "" else x)
        if q4_yes:
            st.session_state.answers.append(q4_yes)
    
    # Question 5 (if q4 is "yes")
    if len(st.session_state.answers) == 4 and st.session_state.answers[3] == "yes":
        q5_yes = st.slider("Rate your experience:", 1, 10)
        st.session_state.answers.append(q5_yes)

    # Question for "no" response to q1
    if len(st.session_state.answers) == 1 and st.session_state.answers[0] == "no":
        q1_no = st.radio("Why didn't you attend?", ["I was busy", "I was in meetings", "I was on leave", "I work from home", "Other"])
        if q1_no:
            if q1_no == "Other":
                q1_no = st.text_area('Here you can type your reason!')
            st.session_state.answers.append(q1_no)

    if st.button("Submit"):
        if len(st.session_state.answers) == 0 or (st.session_state.answers[0] == "yes" and len(st.session_state.answers) < 5) or (st.session_state.answers[0] == "no" and len(st.session_state.answers) < 2):
            error()
        else:
            save_data(st.session_state.answers)
            st.session_state.page = "thankyou"

# Include the thankyou module at the end of the main script
if st.session_state.page == "thankyou":
    import thankyou
