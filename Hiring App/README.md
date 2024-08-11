
# Hiring Application

This repository contains two Python scripts that work together to assist in the hiring process by matching job seekers with job descriptions. The `Resume_Data_Preparer.py` script preprocesses resume data and calculates similarity scores between resumes and a job description. The `hiringapp.py` script then uses the resulting vectors to further analyze and identify the most suitable candidates.

## Workflow

1. **Resume Data Preparation**: Run `Resume_Data_Preparer.py` to preprocess resume data and compute similarity scores.
2. **Candidate Selection**: Run `hiringapp.py` to analyze the preprocessed data and select top candidates.

## Prerequisites

- Python 3.x
- Required Libraries: `pandas`, `nltk`, `scikit-learn`

## Installation

Install the required libraries using the following command:

```bash
pip install pandas nltk scikit-learn
```

Before running the scripts, download the necessary NLTK data:

```python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
```

## Usage

### 1. Prepare Resume Data:

- Place the resume data in a CSV file (e.g., `Accurate_Descriptions.csv`) and job descriptions in an Excel file (e.g., `Job_data_cleaned.xlsx`).
- Run the `Resume_Data_Preparer.py` script:
  - This will generate a new CSV file (e.g., `Resume_Vectorz.csv`) containing the preprocessed and vectorized resume data.

### 2. Run the Hiring Application:

- Ensure that the output CSV file from the previous step is available.
- Run the `hiringapp.py` script:
  - Follow any additional instructions provided by the script to complete the candidate selection process.

## Steps

1. **Install Prerequisites**:
   - Install the necessary Python libraries:
     ```bash
     pip install pandas nltk scikit-learn
     ```
   - Download the required NLTK data:
     ```python
     import nltk
     nltk.download('stopwords')
     nltk.download('wordnet')
     ```

2. **Prepare Resume Data**:
   - Place your resume data in a CSV file (e.g., `Accurate_Descriptions.csv`).
   - Place your job descriptions in an Excel file (e.g., `Job_data_cleaned.xlsx`).
   - Run the `Resume_Data_Preparer.py` script to preprocess and vectorize the resume data:
     ```bash
     python Resume_Data_Preparer.py
     ```

3. **Run the Hiring Application**:
   - Ensure that the output CSV file from the previous step (`Resume_Vectorz.csv`) is available.
   - Run the `hiringapp.py` script to select the top candidates:
     ```bash
     python hiringapp.py
     ```

Follow these steps to complete the hiring process using this application.
