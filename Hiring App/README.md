Hiring Application
Overview
This repository contains two Python scripts that work together to assist in the hiring process by matching job seekers with job descriptions. The Resume_Data_Preparer.py script preprocesses resume data and calculates similarity scores between resumes and a job description. The hiringapp.py script then uses the resulting vectors to further analyze and identify the most suitable candidates.
Workflow
Resume Data Preparation: Run Resume_Data_Preparer.py to preprocess resume data and compute similarity scores.
Candidate Selection: Run hiringapp.py to analyze the preprocessed data and select top candidates.
Prerequisites
Python 3.x
Libraries: pandas, nltk, sklearn
Installation
Install the required libraries using the following command:
bashCopy codepip install pandas nltk scikit-learn
Before running the scripts, download the necessary NLTK data:
pythonCopy codeimport nltk
nltk.download('stopwords')
nltk.download('wordnet')
Usage
Prepare Resume Data:
Place the resume data in a CSV file (e.g., Accurate_Descriptions.csv) and job descriptions in an Excel file (e.g., Job_data_cleaned.xlsx).
Run the Resume_Data_Preparer.py script:
This will generate a new CSV file (e.g., Resume_Vectorz.csv) containing the preprocessed and vectorized resume data.
Run the Hiring Application:
Ensure that the output CSV file from the previous step is available.
Run the hiringapp.py script:
Follow any additional instructions provided by the script to complete the candidate selection process.
bashCopy codepython hiringapp.py
bashCopy codepython Resume_Data_Preparer.py
