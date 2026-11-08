import streamlit as st
import mysql.connector
connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password="REDACTED",
    database="placement"
)
cursor=connection.cursor(dictionary=True)
st.header("Company Specific Skill Assessment")
st.divider()
st.subheader(f"Unique ID : {st.session_state.unique_id}")
st.subheader(f"Company : {st.session_state.company}")
st.divider()
if "response" not in st.session_state:
    st.session_state.response=False
if "analyze" not in st.session_state:
    st.session_state.analyze=False
total_score=0
tab1,tab2,tab3,tab4=st.tabs(["Aptitude Assessment","Technical MCQ Assessment","Programming Assessment","SQL Assessment"])
with tab1:
    ques1=st.radio(
        "A product is bought for Rs. 600 and sold at 20% profit. What is selling price ?",
        ["900","920","960","980"]
    )
    ques2=st.radio(
        "A train travels 240 km in 4 hours. What is the average speed ?",
        ["40","50","60","80"]
    )
    ques3=st.radio(
        "Find the next number in the series: 3, 8, 15, 24, 35, ?",
        ["42","46","48",50]
    )
    if(st.button("Save Response",type="primary",key="tab1")):
        query="""INSERT INTO aptitude(UserResponse,QNo)
        VALUES(%s,%s)"""
        cursor.executemany(query,[(ques1,1),(ques2,2),(ques3,3)])
        connection.commit()
        st.success("Response saved..!")
with tab2:
    ques4=st.radio(
        "Which data structure follows FIFO principle ?",
        ["Stack","Queue","Array","Linked List"]
    )
    ques5=st.radio(
        "Which OOPs concept allows class to acquire methods and properties of another class ?",
        ["Abstration","Inheritance","Polymorphism","Encapsulation"]
    )
    ques6=st.radio(
        "Which DBMS property ensures that transaction is completed entirely or not at all ?",
        ["Consistency","Atomicity","Isolation","Durability"]
    )
    if(st.button("Save Response",type="primary",key="key2")):
        query="""INSERT INTO technical(UserResponse,QNo)
        VALUES(%s,%s)"""
        cursor.executemany(query,[(ques4,4),(ques5,5),(ques6,6)])
        connection.commit()
        st.success("Response saved..!")
with tab3:
    ques7=st.radio(
        "Which Python method allows storing list into another list after sorting ?",
        ["sort()","sorted()","arrange()","store()"]
    )
    ques8=st.radio(
        "Which is the correct approach to reverse a string in Python ?",
        ["using list slice","using join,reversed","both of these","none of these"]
    )
    ques9=st.radio(
        "Which python module deals with regular expressions ?",
        ["regex","regular","re","both regex,re"]
    )
    if(st.button("Save Response",type="primary",key="tab3")):
        query="""INSERT INTO program(UserResponse,QNo)
        VALUES(%s,%s)"""
        cursor.executemany(query,[(ques7,7),(ques8,8),(ques9,9)])
        connection.commit()
        st.success("Response saved..!")
with tab4:
    ques10=st.radio(
        "Can a MySQL table have multiple primary keys ?",
        ["Yes","No","Not sure","None of these"]
    )
    ques11=st.radio(
        "How is primary key represented when running the command DESC table_name ?",
        ["Primary","PRIMARY","PRI","All of these"]
    )
    ques12=st.radio(
        "How is unique key represented when running the command DESC table_name ?",
        ["Unique","UNIQUE","UNI","All of these"]
    )
    if(st.button("Save Response",type="primary",key="tab4")):
        query="""INSERT INTO sql_quiz(UserResponse,QNo)
        VALUES(%s,%s)"""
        cursor.executemany(query,[(ques10,10),(ques11,11),(ques12,12)])
        connection.commit()
        st.success("Response saved..!")
if(st.button("Submit Your Response",type="primary")):
    query="""UPDATE aptitude
    SET CorrectResponse=%s
    WHERE QNo=%s"""
    cursor.executemany(query,[("960",1),("60",2),("48",3)])
    connection.commit()

    query="""UPDATE technical
    SET CorrectResponse=%s
    WHERE QNo=%s"""
    cursor.executemany(query,[("Stack",4),("Inheritance",5),("Atomicity",6)])
    connection.commit()

    query="""UPDATE program
    SET CorrectResponse=%s
    WHERE QNo=%s"""
    cursor.executemany(query,[("sorted()",7),("both of these",8),("re",9)])
    connection.commit()

    query="""UPDATE sql_quiz
    SET CorrectResponse=%s
    WHERE QNo=%s"""
    cursor.executemany(query,[("No",10),("PRI",11),("UNI",12)])
    connection.commit()
    st.success("Quiz Ended..!")

    #response evalaution(tab1)
    query="""SELECT QNo FROM aptitude"""
    cursor.execute(query)
    results=cursor.fetchall()
    for result in results:
        query="""SELECT UserResponse, CorrectResponse
        FROM aptitude
        WHERE QNo=%s"""
        cursor.execute(query,(result["QNo"],))
        ans1=cursor.fetchone()
        if(ans1["UserResponse"]==ans1["CorrectResponse"]):
            total_score+=5
            query="""UPDATE aptitude
            SET Status=%s
            WHERE QNo=%s"""
            cursor.execute(query,("Correct",result["QNo"]))
            connection.commit()
        else:
            query="""UPDATE aptitude
            SET Status=%s
            WHERE QNo=%s"""
            cursor.execute(query,("Wrong",result["QNo"]))
            connection.commit()

    #response evalaution(tab2)
    query="""SELECT QNo FROM technical"""
    cursor.execute(query)
    results=cursor.fetchall()
    for result in results:
        query="""SELECT UserResponse, CorrectResponse
        FROM technical
        WHERE QNo=%s"""
        cursor.execute(query,(result["QNo"],))
        ans2=cursor.fetchone()
        if(ans2["UserResponse"]==ans2["CorrectResponse"]):
            total_score+=5
            query="""UPDATE technical
            SET Status=%s
            WHERE QNo=%s"""
            cursor.execute(query,("Correct",result["QNo"]))
            connection.commit()
        else:
            query="""UPDATE technical
            SET Status=%s
            WHERE QNo=%s"""
            cursor.execute(query,("Wrong",result["QNo"]))
            connection.commit()

    #response evalaution(tab3)
    query="""SELECT QNo FROM program"""
    cursor.execute(query)
    results=cursor.fetchall()
    for result in results:
        query="""SELECT UserResponse, CorrectResponse
        FROM program
        WHERE QNo=%s"""
        cursor.execute(query,(result["QNo"],))
        ans3=cursor.fetchone()
        if(ans3["UserResponse"]==ans3["CorrectResponse"]):
            total_score+=5
            query="""UPDATE program
            SET Status=%s
            WHERE QNo=%s"""
            cursor.execute(query,("Correct",result["QNo"]))
            connection.commit()
        else:
            query="""UPDATE program
            SET Status=%s
            WHERE QNo=%s"""
            cursor.execute(query,("Wrong",result["QNo"]))
            connection.commit()

    #response evalaution(tab4)
    query="""SELECT QNo FROM sql_quiz"""
    cursor.execute(query)
    results=cursor.fetchall()
    for result in results:
        query="""SELECT UserResponse, CorrectResponse
        FROM sql_quiz
        WHERE QNo=%s"""
        cursor.execute(query,(result["QNo"],))
        ans4=cursor.fetchone()
        if(ans4["UserResponse"]==ans4["CorrectResponse"]):
            total_score+=5
            query="""UPDATE sql_quiz
            SET Status=%s
            WHERE QNo=%s"""
            cursor.execute(query,("Correct",result["QNo"]))
            connection.commit()
        else:
            query="""UPDATE sql_quiz
            SET Status=%s
            WHERE QNo=%s"""
            cursor.execute(query,("Wrong",result["QNo"]))
            connection.commit()
    st.divider()
    st.subheader(f"Your Overall Score : {total_score}/60")

#performace analysis
if(st.button("Analyze Your Performance",type="primary")):
    st.session_state.analyze=True
if st.session_state.analyze:
    st.write("<u>Aptitude Assessment Analysis :</u>",unsafe_allow_html=True)
    query="""SELECT Status as status, COUNT(*) as count
    FROM aptitude
    GROUP BY Status"""
    cursor.execute(query)
    results=cursor.fetchall()
    for result in results:
        if(result["status"]=="Wrong"):
            st.write(f"Wrong : {result["count"]}")
        elif(result["status"]=="Correct"):
            st.write(f"Correct : {result["count"]}")
    query="""SELECT QNo FROM aptitude
    WHERE Status=%s"""
    cursor.execute(query,("Wrong",))
    results=cursor.fetchall()
    for result in results:
        st.write(f"Wrong Questions : {result["QNo"]}")

    st.write("<u>Technical MCQ Analysis :</u>",unsafe_allow_html=True)
    query="""SELECT Status as status, COUNT(*) as count
    FROM technical
    GROUP BY Status"""
    cursor.execute(query)
    results=cursor.fetchall()
    for result in results:
        if(result["status"]=="Wrong"):
            st.write(f"Wrong : {result["count"]}")
        elif(result["status"]=="Correct"):
            st.write(f"Correct : {result["count"]}")
    query="""SELECT QNo FROM technical
    WHERE Status=%s"""
    cursor.execute(query,("Wrong",))
    results=cursor.fetchall()
    for result in results:
        st.write(f"Wrong Questions : {result["QNo"]}")

    st.write("<u>Programming Assessment Analysis :</u>",unsafe_allow_html=True)
    query="""SELECT Status as status, COUNT(*) as count
    FROM program
    GROUP BY Status"""
    cursor.execute(query)
    results=cursor.fetchall()
    for result in results:
        if(result["status"]=="Wrong"):
            st.write(f"Wrong : {result["count"]}")
        elif(result["status"]=="Correct"):
            st.write(f"Correct : {result["count"]}")
    query="""SELECT QNo FROM program
    WHERE Status=%s"""
    cursor.execute(query,("Wrong",))
    results=cursor.fetchall()
    for result in results:
        st.write(f"Wrong Questions : {result["QNo"]}")

    st.write("<u>SQL Assessment Analysis :</u>",unsafe_allow_html=True)
    query="""SELECT Status as status, COUNT(*) as count
    FROM sql_quiz
    GROUP BY Status"""
    cursor.execute(query)
    results=cursor.fetchall()
    for result in results:
        if(result["status"]=="Wrong"):
            st.write(f"Wrong : {result["count"]}")
        elif(result["status"]=="Correct"):
            st.write(f"Correct : {result["count"]}")
    query="""SELECT QNo FROM sql_quiz
    WHERE Status=%s"""
    cursor.execute(query,("Wrong",))
    results=cursor.fetchall()
    for result in results:
        st.write(f"Wrong Questions : {result["QNo"]}")

if(st.button("Next Page",type="primary")):
    st.switch_page("pages/analysis.py")
if(st.button("Previous Page",type="primary")):
    st.switch_page("pages/profile.py")