import streamlit as st
import mysql.connector
connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password="REDACTED",
    database="placement"
)
cursor=connection.cursor(dictionary=True)
st.header("Placement Competitiveness Analysis")
st.divider()
st.subheader(f"UserName : {st.session_state.user_name}")
st.subheader(f"UniqueID : {st.session_state.unique_id}")
st.divider()

st.write("<u>Eligibility Status : </u>",unsafe_allow_html=True)
st.write(f"You selected company to check your eligibility : {st.session_state.company}")
st.write(f"Your current cgpa : {st.session_state.cgpa}")
st.write(f"Your overall percentage : {st.session_state.percent}")
st.write(f"You have {int(st.session_state.back)} backlogs")
query="""SELECT `Eligible/Not Eligible` from student
WHERE UserID=%s"""
cursor.execute(query,(st.session_state.unique_id,))
result=cursor.fetchone()
st.write(f"You are {result["Eligible/Not Eligible"]} for the company : {st.session_state.company}")
st.divider()

st.write("<u>Resume Analysis Result : </u>",unsafe_allow_html=True)
if(st.session_state.all_pre):
    st.write(f"Your resume has all the required skills for the company : {st.session_state.company}")
elif(st.session_state.miss_tech):
    st.write(f"Your resume lacks required technologies for the company : {st.session_state.comapny}")
    query="""SELECT technologies from company_require
    WHERE company=%s"""
    cursor.execute(query,(st.session_state.company,))
    result=cursor.fetchone()
    st.write(f"Work on these technologies : {result["technologies"]}..")
elif(st.session_state.miss_skill):
    st.write(f"Your resume lacks required technical skills for the company : {st.session_state.company}")
    query="""SELECT technical_skills from company_require
    WHERE company=%s"""
    cursor.execute(query,(st.session_state.company,))
    result=cursor.fetchone()
    st.write(f"Work on these technical skills : {result["technical_skills"]}..")
elif(st.session_state.miss_cert):
    st.write(f"Your resume lacks required certifications for the company : {st.session_state.company}")
    query="""SELECT certificate from company_require
    WHERE company=%s"""
    cursor.execute(query,(st.session_state.company,))
    result=cursor.fetchone()
    st.write(f"Work on these certifications : {result["certificate"]}..")
else:
    st.write(f"Your resume lacks required projects for the company : {st.session_state.company}")
    query="""SELECT project from company_require
    WHERE company=%s"""
    cursor.execute(query,(st.session_state.company,))
    result=cursor.fetchone()
    st.write(f"Work on these projects : {result["technical_skills"]}..")
st.divider()
