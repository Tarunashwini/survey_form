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
            if write_header:
                csv_writer.writerow(['Have you attended any?', 'Have you participated in any activity?', 'Was it engaging?', 'Do you want to attend more events?', 'Rate your experience:'])
            csv_writer.writerow([answer[0], answer[1], answer[2], answer[3], answer[4]])
        up.upload_to_blob_storage('mnt/data/yes_mydata.csv','yes_response.csv')
    else:  # If there are 2 elements, it means the answer is from the 'no' path
        file_path = 'mnt/data/no_mydata.csv'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
        write_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0  # Check if file is empty or doesn't exist
        with open(file_path, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            if write_header:
                csv_writer.writerow(['Have you attended any?', 'Why didn\'t you attend?'])
            csv_writer.writerow([answer[0], answer[1]])
        up.upload_to_blob_storage('mnt/data/no_mydata.csv','no_response.csv')
    st.write('Your data has been recorded successfully!')

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "survey"

def error():
    st.warning("Please fill all the required questions")

# Navigation logic
if st.session_state.page == "survey":
    # Streamlit app title
    st.title('Welcome to HR Events Survey')

    # Radio button with a default unselected state
    q1 = st.radio("Have you attended any?", ["", "yes", "no"], index=0, format_func=lambda x: "Select an option" if x == "" else x)

    if q1 == "yes":
        # Questions if the user selects "yes"
        q2_yes = st.radio("Have you participated in any activity?", ["", "yes", "no"], index=0, format_func=lambda x: "Select an option" if x == "" else x)
        q3_yes = st.radio("Was it engaging?", ["", "yes", "no"], index=0, format_func=lambda x: "Select an option" if x == "" else x)
        q4_yes = st.radio("Do you want to attend more events?", ["", "yes", "no"], index=0, format_func=lambda x: "Select an option" if x == "" else x)
        q5_yes = st.slider("Rate your experience:", 1, 10)
    elif q1 == "no":
        # Questions if the user selects "no"
        q1_no = st.radio("Why didn't you attend?", ["I was busy", "I was in meetings", "I was on leave", "I work from home", "Other"])
        if q1_no == "Other":
            q1_no = st.text_area('Here you can type your reason!')

    if st.button("Submit"):
        if q1 == "":
            error()
        elif q1 == "yes" and (q2_yes == "" or q3_yes == "" or q4_yes == ""):
            error()
        elif q1 == "no" and q1_no == "":
            error()
        else:
            if q1 == "yes":
                save_data([q1, q2_yes, q3_yes, q4_yes, q5_yes])
            elif q1 == "no":
                save_data([q1, q1_no])
            st.session_state.page = "thankyou"

# Include the thankyou module at the end of the main script
if st.session_state.page == "thankyou":
    import thankyou
