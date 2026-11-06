import streamlit as st
import pywhatkit
import mysql.connector
connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password="REDACTED",
    database="placement"
)
cursor=connection.cursor(dictionary=True)
st.header("Company Placement Analyzer Eligibility")
st.divider()

#user details form
#entry for new user

user_type=st.radio(
    "Are you new user or existing user ?",
    ["new user","existing user"]
)
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked=False
if "verify_code" not in st.session_state:
    st.session_state.verify_code=False
if(st.button("Submit User Type",type="primary")):
    st.session_state.button_clicked=True
if  st.session_state.button_clicked:
    if(user_type=="new user"):
        user_name=st.text_input("Enter your name :").lower()
        year=st.selectbox(
            "What is your current year ?",
            ["1st","2nd","3rd","4th"]
        )
        branch=st.radio(
            "Select your branch :",
            ["CS","IT"]
        )
        if "unique_id" not in st.session_state:
            st.session_state.unique_id=0
        phone_number=st.text_input("Enter your 10 digit phone number : ")
        roll_no=st.text_input("Enter your 13 digit roll number ")
        st.session_state.unique_id=f"{user_name}@{roll_no[9:]}:{year}-{branch}"
        if(st.button("Submit",type="primary")):
            pywhatkit.sendwhatmsg_instantly(
                f"+91{phone_number}",
                f"""
                Congratulations! Your unique id is generated.
Don't share it with anyone.
Unique ID : {st.session_state.unique_id}""" 
            )
            st.success(f"Code sent to your phone nummber..!")
            # if "code_sent" not in st.session_state:
            #     st.session_state.code_sent=False
        check_code=st.text_input("Enter the code sent : ")
        if(st.button("Verify Code",type="primary")):
            st.session_state.verify_code=True
        if st.session_state.verify_code:
            if(check_code==st.session_state.unique_id):
                st.success("Congrats, Entry Permitted..!!")
                query="""INSERT INTO user_info
                VALUES(%s,%s)"""
                cursor.execute(query,(user_name,st.session_state.unqiue_id))
                connection.commit()
                st.switch_page("pages/eligibility.py")

            else:
                st.error("Entry Restricted..!!")
    else:
        exist_user=st.text_input("Enter your name : ")
        exist_id=st.text_input("Emter your unique id : ")
        if(st.button("Submit",type="primary")):
            query="""SELECT user_name,unique_id
            FROM user_info"""
            cursor.execute(query)
            results=cursor.fetchone()
            if(results["user_name"]==exist_user.lower() and results["unique_id"]==exist_id):
                st.success("Congrats, Entry Permitted..!!")
                st.session_state.unique_id=results["unique_id"]
                st.switch_page("pages/eligibility.py")
            else:
                st.error("Entry Restricted..!!")
