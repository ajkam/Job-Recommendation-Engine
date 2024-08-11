
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains import RetrievalQA

import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
 
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text
 
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200, chunk_overlap=450, length_function=len
    )
    return text_splitter.split_text(text)
 
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)
 
def process_pdfs(pdf_docs):
    raw_text = get_pdf_text(pdf_docs)
    if not raw_text:
        return None, "No text found in the uploaded PDFs or no pdf uploaded. Please upload a valid PDF."
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)
    return vectorstore.as_retriever(), ""
 
def extract_information(retriever):
    questions = [
        "What is the name on resume(Just the name, example: John Stuart, Mike Charles)?",
        "A number which will tell the year of work experience on this resume (example: 2, 3, 4)?",
        "What are the skills on resume, just the name of the skill no additional comment (Example: Python, SQL, Project Management)?",
        "What is the current location on the resume, just the city name (Example: New York, San Francisco)?",
        "Extract the exact Job title and description from the resume (DO not make anything up, you may find information in form of bullet points)?",
        "Extract the exact project title and description from the resume (DO not make anything up, you may find information in form of bullet points)?",
    ]
 
    qa = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0, max_tokens=200), chain_type="stuff", retriever=retriever)
    return [qa.invoke(question)['result'] for question in questions]
 
def calculate_similarity(user_resume, job_description_vectors, vectorizer):
    user_resume_vector = vectorizer.transform([user_resume])
    similarity_scores = cosine_similarity(user_resume_vector, job_description_vectors)
    return similarity_scores[0] 
 
def main():
    st.set_page_config(page_title="DotsLive!", page_icon=":book:", layout="wide")
    st.subheader("DotsLive! :book:")
    job_df = pd.read_excel('Prepared_Job_Data.xlsx')
 
    vectorizer = TfidfVectorizer()
    job_df.dropna(subset=['Cleaned_Description'], inplace=True)
 
    job_descriptions = job_df['Cleaned_Description'].tolist()
    X = vectorizer.fit_transform(job_descriptions)
 
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=['Name', 'Work Experience', 'Skills', 'Location', 'Resume_description', 'Project_description'])
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
 
    with st.sidebar:
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                retriever, error_message = process_pdfs(pdf_docs)
                if error_message:
                    st.error(error_message)
                elif retriever:
                    responses = extract_information(retriever)
                    new_data = {
                        'Name': [responses[0]],
                        'Work Experience': [responses[1]],
                        'Skills': [responses[2]],
                        'Location': [responses[3]],
                        'Resume_description': [responses[4]],
                        'Project_description': [responses[5]]
                    }
                    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame(new_data)], ignore_index=True)
 
    if not st.session_state.submitted:
        if not st.session_state.df.empty:
            name = st.text_input("Name", value=st.session_state.df['Name'][0])
            work_experience = st.text_input("Work Experience", value=st.session_state.df['Work Experience'][0])
            skills = st.text_input("Skills", value=st.session_state.df['Skills'][0])
            location = st.text_input("Location", value=st.session_state.df['Location'][0])
            resume_description = st.text_area("Resume Description", value=st.session_state.df['Resume_description'][0])
            project_description = st.text_area("Project Description", value=st.session_state.df['Project_description'][0])
 
            if st.button("Submit"):
                st.session_state.df.loc[0, 'Name'] = name
                st.session_state.df.loc[0, 'Work Experience'] = work_experience
                st.session_state.df.loc[0, 'Skills'] = skills
                st.session_state.df.loc[0, 'Location'] = location
                st.session_state.df.loc[0, 'Resume_description'] = resume_description
                st.session_state.df.loc[0, 'Project_description'] = project_description
                st.session_state.submitted = True
                st.experimental_rerun()
 
    if st.session_state.submitted:
        st.session_state.df['Combined'] = st.session_state.df['Resume_description'] + st.session_state.df['Project_description'] + st.session_state.df['Skills']
        user_resume = st.session_state.df.iloc[0]['Combined']
        job_description_vectors = vectorizer.transform(job_descriptions)
        similarity_scores = calculate_similarity(user_resume, job_description_vectors, vectorizer)
        job_df['Similarity'] = similarity_scores
        filtered_jobs = job_df.sort_values(by='Similarity', ascending=False).head(10)


         
        # Update the Location Match column using RetrievalQA
        vector_store_loc = FAISS.from_texts([location for location in filtered_jobs['Location']], OpenAIEmbeddings())
        retriever_loc = vector_store_loc.as_retriever()
        loc_QA = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0, max_tokens=200), chain_type="stuff", retriever=retriever_loc)
        for index, row in filtered_jobs.iterrows():
            question = f"Is the location {row['Location']} matching with the resume location {st.session_state.df['Location'].iloc[0]}, return just 1 or 0, say 1 if even one values matches, say 1 if the location are in a radius of 100KM, say 1 if the job location has Remote in it, say 0 if no condition is satisfied ,DO Not add addidtional information.?"
            response_loc = loc_QA.invoke(question)
            filtered_jobs.loc[index, 'Location Match'] = response_loc['result']

        # convert the similarity scores to percentage
        max_score = filtered_jobs['Similarity'].max()
        filtered_jobs['Normalized_Similarity']= filtered_jobs['Similarity']/max_score


        similarity_weight = 0.7
        location_match_weight = 0.3
        # Exp = 0.3

        filtered_jobs['Final_Score'] = (similarity_weight * filtered_jobs['Normalized_Similarity']) + (location_match_weight * filtered_jobs['Location Match'].astype(float))*100
        st.write(filtered_jobs[['title', 'Job Description', 'Location', 'Final_Score']].sort_values(by='Final_Score', ascending=False).reset_index(drop=True))
        
            
        

        ### we can add a filter to threshold the final score
        


 
 
 
if __name__ == '__main__':
    main()
 