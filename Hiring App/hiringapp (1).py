import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 
def calculate_similarity(user_resume, job_description_vectors, vectorizer):
    user_resume_vector = vectorizer.transform([user_resume])
    similarity_scores = cosine_similarity(user_resume_vector, job_description_vectors)
    return (similarity_scores[0])
 
def main():
    st.set_page_config(page_title="DotsLive!", page_icon=":book:", layout="wide")
    st.subheader("Hiring Manager Advisor :book:")
    resume_df = pd.read_csv('Resume_Vectorz.csv')

    vectorizer = TfidfVectorizer()
    resume_df.dropna(subset=['Cleaned_Description'], inplace=True)

    resume_descriptions = resume_df['Cleaned_Description'].tolist()
    X = vectorizer.fit_transform(resume_descriptions)

    job_desc = st.text_area("Paste the job description here")

    if st.button("Submit"):
        resume_df['Similarity'] = calculate_similarity(job_desc, X, vectorizer) 
        resume_df = resume_df.sort_values(by='Similarity', ascending=False)
        filtered_df = resume_df.sort_values(by='Similarity', ascending=False).head(10)
        st.write(filtered_df[['Name', 'Similarity']])


if __name__ == '__main__':
    main()
 