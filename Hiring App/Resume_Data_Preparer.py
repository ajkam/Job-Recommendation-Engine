#%%
import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read data
resume_df = pd.read_csv("Accurate_Descriptions_v1.csv", encoding="latin1")

# Preprocessing
def preprocess_text(text):
    # Clean text
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).lower().strip()
    # Tokenize and remove stopwords
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(word) for word in tokens])

resume_df['Combined'] = resume_df['Skills'] + resume_df['Past Job Summary']
resume_df['Cleaned_Description'] = resume_df['Combined'].astype(str).apply(preprocess_text)

# Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(resume_df['Cleaned_Description'])
resume_df['Vector'] = list(X.toarray())

#Exporting Resume Data
resume_df.to_csv('Resume_Vectorz.csv', index=False)
