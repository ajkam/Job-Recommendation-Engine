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

Before running the scripts, download the necessary NLTK data:

import nltk
nltk.download('stopwords')
nltk.download('wordnet')
