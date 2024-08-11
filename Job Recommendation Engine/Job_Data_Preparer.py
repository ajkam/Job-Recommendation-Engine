import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Read data
job_df = pd.read_excel('Job_data.xlsx')

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

job_df['Cleaned_Description'] = job_df['Job Description'].astype(str).apply(preprocess_text)

# Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(job_df['Cleaned_Description'])
job_df['Vector'] = list(X.toarray())

# Exporting
job_df.drop(columns=['Education and Training'], inplace=True)
job_df.to_excel('Prepared_Job_Data.xlsx', index=False)
