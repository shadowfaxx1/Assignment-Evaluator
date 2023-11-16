# Assignment Evaluator 

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![AssignmentEval](https://img.shields.io/badge/Assignment-Eval-purple.svg)](LICENSE)

## Overview
The Assignment Evaluator is an automated system designed to streamline the process of evaluating student assignments. Leveraging natural language processing models, sentiment analysis, and advanced analytics, this tool reduces the manual burden on educators and enhances the accuracy of assessments.

## Features
- **Sentiment Analysis:** The system employs sentiment analysis to evaluate the emotional tone of the assignments. Positive and negative scores, along with polarity and subjectivity, contribute to a comprehensive sentiment assessment.

- **Language Complexity:** Various metrics, including average sentence length, complex word percentage, Fog index, and average word length, gauge the complexity of language used in the assignments.

- **Assignment Structure Analysis:** The tool analyzes word count, sentence length, and paragraph structure to assess the organization and coherence of the assignments.

- **Plagiarism Score:** Utilizing advanced algorithms, the system calculates a plagiarism score to identify potential instances of academic misconduct.

- **Hypothesis Testing (Zero-Shot Classification):** The system employs zero-shot classification from Hugging Face models to evaluate the assignments against predefined hypotheses.

## Usage
1. **Admin Login:** Log in to the admin panel to access the assignment evaluation dashboard.

2. **View Assignments:** The system displays a summary of assignments with key metrics. Clicking on an assignment reveals detailed evaluation results.

3. **Student-wise Report:** Navigate to the student-wise report page to explore individual student performance and metrics.

4. **Evaluation Metrics:** Sentiment analysis, language complexity, assignment structure, plagiarism score, and hypothesis testing contribute to a comprehensive evaluation.

5. **Database Storage:** Assignment details, along with evaluation results, are stored in an SQLite database for future reference.

## System Requirements
- Python 3.x
- Streamlit
- NLTK
- Hugging Face Transformers
- SQLite

## Installation
1. Clone the repository: `git clone <repository_url>`
2. Install required libraries: `pip install -r requirements.txt`
3. Run the Streamlit app: `streamlit run main.py`

## Results and Visualization
The system generates visualizations, including bar charts and scatter plots, to provide a clear overview of assignment metrics and trends over time.

## Database
All assignment details, including evaluation results, are stored in an SQLite database for easy retrieval and analysis.

## Conclusion
The Assignment Evaluator project aims to revolutionize the assignment evaluation process, bringing efficiency, accuracy, and data-driven insights to educators. It serves as a valuable tool for educational institutions seeking to enhance their assessment processes.

---

*This project is licensed under the [MIT License](LICENSE). Feel free to contribute or use this project in your educational endeavors.*
