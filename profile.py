import streamlit as st
import re
from pypdf import PdfReader
import mysql.connector
connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="placement"
)
cursor=connection.cursor(dictionary=True)
st.header("Student Profile and Resume Analysis")
st.divider()
if "upload" not in st.session_state:
    st.session_state.upload=False
resume=st.file_uploader("Select your resume : ",type="pdf")
if st.button("Upload",type="primary"):
    st.session_state.upload=True

# four attribute values check:
if "tech_found" not in st.session_state:
    st.session_state.tech_found=False
if "tech_skill" not in st.session_state:
    st.session_state.tech_skill=False
if "prjt" not in st.session_state:
    st.session_state.prjt=False
if "cert" not in st.session_state:
    st.session_state.cert=False

if st.session_state.upload:
    if resume is not None:
        st.success("Resume uploaded successfully..!")
        pdf_reader=PdfReader(resume)
        total_pages=len(pdf_reader.pages)

        for page in range(total_pages):
            pages=pdf_reader.pages[page]
            text=pages.extract_text()
            if text:
                lines=text.splitlines()
                cleaned_word=[word.strip() for word in lines if word.strip()]
                recontruct_text=" ".join(cleaned_word)
        st.divider()

        #using regex to find technical skills from resume
        pattern=r"TECHNICAL SKILLS (.*?)(?=PROJECTS)"
        tech_skill=re.search(pattern,recontruct_text,re.IGNORECASE)
        if tech_skill:
            st.session_state.tech_skill=True
        
        #using regex to find certificate from resume 
        pattern=r"CERTIFICATIONS(.*?)(?=ACHIEVEMENTS)"
        cert=re.search(pattern,recontruct_text,re.IGNORECASE)
        if cert:
            st.session_state.cert=True

        #using regex to find projects from resume
        pattern=r"Projects(.*?)(?=CERTIFICATIONS)"
        prjt=re.search(pattern,recontruct_text,re.IGNORECASE)
        if prjt:
            st.session_state.prjt=True

        #using regex to find technologies from resume
        pattern=r"Technologies\s*:\s*([^-\-]+)"
        tech_found=re.findall(pattern,recontruct_text,re.IGNORECASE)
        if tech_found:
            st.session_state.tech_found=True

        internship=st.radio(
                    "Have you done any internship ?",
                    ["Yes","No"]
                    )
        if "intern" not in st.session_state:
            st.session_state.intern=False
        if "intern_submit" not in st.session_state:
            st.session_state.intern_submit=False
        if(st.button("Internship Choice",type="primary")):
            st.session_state.intern=True
        if st.session_state.intern:
            intern_detail=st.text_area("Provide brief details of your internship (type None if no internship):")
        if(st.button("Submit Internship Details",type="primary",disabled=not st.session_state.intern)):
            st.session_state.intern_submit=True
        if st.session_state.intern_submit:
            if  intern_detail and st.session_state.tech_skill and  st.session_state.tech_found and  st.session_state.cert and  st.session_state.prjt:
                try:
                    query="""INSERT INTO student_skills(UserID,technical_skills,technologies,certificate,project,internship)
                    VALUES(%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(query,(st.session_state.unique_id,tech_skill.group(1),",".join(tech_found),cert.group(1),prjt.group(1),internship))
                    connection.commit()
                    st.success("Insertion succeeds..!")
                except Exception as e:
                    st.error(e)
            query="""SELECT technical_skills,technologies,certificate,project
            FROM company_require
            WHERE company=%s"""
            cursor.execute(query,(st.session_state.company,))
            results_comapny=cursor.fetchall()
            query="""SELECT technical_skills,technologies,certificate,project
            FROM student_skills"""
            cursor.execute(query)
            results_student=cursor.fetchall()
            tech_skills=False
            tech=False
            cert=False
            prjt=False
            if(results_comapny[0]["technical_skills"] in results_student[0]["technical_skills"]):
                tech_skills=True
                if(results_comapny[0]["technologies"] in results_student[0]["technologies"]):
                    tech=True
                    if(results_comapny[0]["certificate"] in results_student[0]["certificate"]):
                        cert=True
                        if(results_comapny[0]["project"] in results_student[0]["project"]):
                            prjt=True
            if tech_skills and tech and cert and prjt:
                st.write(f"<b> Your resume has all necessary skills,tech,certificate,project for {st.session_state.comapny}..!</b>",unsafe_allow_html=True)
            elif(not tech_skills):
                st.write(f"<b> Your resume don't has necessary technicals skills for {st.session_state.company}..!</b>",unsafe_allow_html=True)
            elif(not tech):
                st.write(f"<b> Your resume don't has necessary technologies for {st.session_state.company}..!</b>",unsafe_allow_html=True)
            elif(not cert):
                 st.write(f"<b> Your resume don't has necessary certifications for {st.session_state.company}..!</b>",unsafe_allow_html=True)
            else:
                 st.write(f"<b> Your resume don't has necessary projects for {st.session_state.company}..!</b>",unsafe_allow_html=True)
