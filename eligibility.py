import streamlit as st
import mysql.connector
connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="placement"
)
cursor=connection.cursor(dictionary=True)
st.header("Company Placement Analysis")
st.divider()
query="""SELECT user_name,unique_id FROM user_info"""
cursor.execute(query)
result=cursor.fetchone()
st.subheader(f"User Name : {result["user_name"]}")
st.subheader(f"Unique ID : {result["unique_id"]}")
st.divider()
#student data collection and insertion
if "check_eligible" not in st.session_state:
    st.session_state.check_eligible=False
company=st.selectbox(
    "Which company are you interested to check your eligibility ?",
    ["TCS","Wipro","Infosys","Accenture","Google"]
)
cgpa=st.number_input("What is your current cgpa ?")
branch=st.radio(
    "Select your branch :",
    ["CS","IT","AIML","CSE"]
)
backlogs=st.number_input("How many backlogs you have ?")
percentage=st.number_input("How much is your percentage ?")
if "data_insert" not in st.session_state:
    st.session_state.data_insert=False
if(st.button("Check Your Eligibility",type="primary")):
     st.session_state.check_eligible=True
if st.session_state.check_eligible:
    try:
        query="""INSERT INTO student(Name,UserID)
        SELECT user_name,unique_id 
        FROM user_info"""
        cursor.execute(query)      
        connection.commit()
        query="""UPDATE student
        SET CompanySelected=%s,CGPA=%s,Backlogs=%s,Branch=%s,Percentage=%s
        WHERE UserID=%s"""
        cursor.execute(query,(company,cgpa,backlogs,branch,percentage,result["unique_id"]))
        connection.commit()
        st.success("Your details are saved successfully..!")
        st.session_state.data_insert=True
    except Exception as e:
        st.error(f"Details couldn't be saved..!.ERROR : {e}")
        st.session_state.data_insert=False
    if st.session_state.data_insert:
        query="""SELECT CGPA,Backlogs,Percentage
        FROM companies
        WHERE Company=%s"""
        cursor.execute(query,(company,))
        results=cursor.fetchall()
        percent_approve=False
        backlog_approve=False
        cgpa_approve=False
        for result1 in results:
            if(percentage>=result1["Percentage"]):
                percent_approve=True
            if(backlogs==result1["Backlogs"]):
                backlog_approve=True
            if(cgpa>=result1["CGPA"]):
                cgpa_approve=True
            if percent_approve and backlog_approve and cgpa_approve:
                query="""UPDATE student
                SET `Eligible/Not Eligible`="Eligible"
                WHERE UserID=%s"""
                cursor.execute(query,(result["unique_id"],))
                connection.commit()
            else:
                query="""UPDATE student
                SET `Eligible/Not Eligible`="Not Eligible"
                WHERE UserID=%s"""
                cursor.execute(query,(result["unique_id"],))
                connection.commit()
            query="""SELECT `Eligible/Not Eligible` from student
            WHERE UserID=%s"""
            cursor.execute(query,(result["unique_id"],))
            select=cursor.fetchone()
            st.write(f"<b>{select["Eligible/Not Eligible"]}</b>",unsafe_allow_html=True)