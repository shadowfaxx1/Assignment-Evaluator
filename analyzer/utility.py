import PyPDF2
from io import BytesIO
import os
import time 
import os 
from docx import Document
import fitz  # PyMuPDF
import platform
import secrets
import io,random
import plotly.express as px # to create visualisations at the admin session
import plotly.graph_objects as go
import os 
import requests
import json
from analyzer.sentimentanalyzer import evaluator
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from PIL import Image

from db.resultdb import create_conn,saving,save_student_result
from datetime import datetime

class utility():
    def __init__(self):
        # Define weights for each feature
        self.weights = {
            "Positive_Sentences": 0.1,
            "Negative_Sentences": -0.1,
            "Polarity": 0.2,
            "Subjectivity": 0.2,
            "Average_Sentence_Length": 0.1,
            "Complex_Word_Percentage": 0.1,
            "Fog_Index": 0.2,
            "Average_Word_Length": 0.1,
            "Complex_Word_Count": 0.1,
            "Word_Count": 0.05,
            "Syllable_Count": 0.05,
            "Personal_Pronouns": -0.1,
            "Plagiarism_Percentage": -0.2  # Negative weight for plagiarism
        }

    def evaluate_assignment(self, assignment_features):
        total_score = 0
        if(assignment_features.get("Plagiarism_Percentage", 0)):
            if assignment_features.get("Plagiarism_Percentage", 0) > 25:
                self.weights["Plagiarism_Percentage"] = -0.4  # Increase the weight
        for feature, value in assignment_features.items():
            # Provide a default value of 0 if value is None
            value = value if value is not None else 0
            total_score += self.weights.get(feature, 0) * value
        total_score = max(0, min(total_score, 100))
        return total_score
    
    @staticmethod
    def read_text_from_file(file_path):
        file_extension = file_path.split('.')[-1].lower()
        if file_extension == 'pdf':
            return utility.pdf_reader(file_path)
        elif file_extension == 'docx':
            return utility.read_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
    @staticmethod
    def pdf_reader(file):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(file, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                        caching=True,
                                        check_extractable=True):
                page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
        converter.close()
        fake_file_handle.close()
        return text
    @staticmethod
    def read_docx(file_path):
        doc = Document(file_path)
        paragraphs = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(paragraphs)

    def analyze_sentiment(self, destination , topic, enrollment,name):
        x=[]
        content = self.read_text_from_file(destination)
        analysis = evaluator()
        analysis.initialization()
        x=analysis.gathering_info(content,enrollment)
        plagiarism =self.plagiarismbot(content)
        scorejsonentail,scorejsoncontra = self.relevancescore(content,topic)
        scorejsonentail=float(scorejsonentail)
        scorejsoncontra=float(scorejsoncontra)
        x.append(plagiarism)
        print(x)
        print(type(x))

        keys = ["Positive_Sentences", "Negative_Sentences", "Polarity", "Subjectivity",
                "Average_Sentence_Length", "Complex_Word_Percentage", "Fog_Index",
        "Average_Word_Length", "Complex_Word_Count", "Word_Count",
        "Syllable_Count", "Personal_Pronouns", "Plagiarism_Percentage"]
        featurecombined= dict(zip(keys, x))
        if(x):
            structure = self.structure(x[9],x[4],x[11])
            sentiment = self.sentiment(x[0],x[1],x[2],x[3])
            language_complexity = self.analyze_language_complexity(x[4],x[5],x[6],x[7])
            complexwords = int(x[8])
            wordcount =int(x[9])
        else:
            structure = None
            sentiment = None
            language_complexity = None
            complexwords = None
            wordcount=None
        conn = create_conn()
        if conn:
            print(scorejsonentail,scorejsoncontra)
            saving(conn,name, enrollment, plagiarism, scorejsonentail,scorejsoncontra, sentiment, language_complexity,structure,wordcount)
            print("saved result in db")
            conn.close()
        
        final_score = self.evaluate_assignment(dict(zip(keys, x)))
        zonn  = create_conn()
        if zonn and final_score:
            save_student_result(zonn,name,enrollment,final_score)
            print("saved final score to access")
            zonn.close()
            print("Final Score:", final_score)
        else:
            print("error parsing")
            


    @staticmethod
    def structure(word_count, avg_sentence_length, pc):
    # Define thresholds for assignment structure labels
        high_word_count_threshold = 800
        low_avg_sentence_length_threshold = 20
        low_pc_threshold = 3

        # Analyze structure based on thresholds
        if word_count > high_word_count_threshold:
            return "Extensive Content"
        elif avg_sentence_length < low_avg_sentence_length_threshold or pc > low_pc_threshold:
            return "Poor Organization"
        else:
            return "Well-Structured"
        
    @staticmethod
    def analyze_language_complexity(avg_sentence_length, complex_word_percentage, fog_index, avg_word_length):
    # Define thresholds for language complexity labels
        high_complexity_threshold = 80
        moderate_complexity_threshold = 50
        if fog_index > high_complexity_threshold or complex_word_percentage/100 > high_complexity_threshold:
            return "High Complexity"
        elif fog_index > moderate_complexity_threshold or complex_word_percentage/100 > moderate_complexity_threshold:
            return "Moderate Complexity"
        else:
            return "Low Complexity"   
           
    @staticmethod
    def sentiment(pos_score, neg_score, polarity, subjectivity):
        positive_threshold = 0.5  # Adjust as needed
        negative_threshold = -0.5  # Adjust as needed
        polarity_threshold = 0.1  # Adjust as needed
        subjectivity_threshold = 0.3  # Adjust as needed

        # Analyze sentiment based on thresholds
        if pos_score > neg_score and polarity > positive_threshold and subjectivity > subjectivity_threshold:
            return "Positive Sentiment"
        elif neg_score > pos_score and polarity < negative_threshold and subjectivity > subjectivity_threshold:
            return "Negative Sentiment"
        elif abs(polarity) < polarity_threshold and subjectivity <= subjectivity_threshold:
            return "Neutral Sentiment"
        else:
            return "Uncertain Sentiment"

    @staticmethod
    def plagiarismbot(test):
        try:
            url = "https://plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com/plagiarism"
            length=0
            if len(test)<10000:
                length=len(test)
            else:
                length=10000
            payload = {
                "text":test[:length],
                "language": "en",
                "includeCitations": False,
                "scrapeSources": False
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": "3e601078f0msh68d15a818fa4eb7p1a5625jsnf599a1b10a08",
                "X-RapidAPI-Host": "plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com"
            }
            response = requests.post(url, json=payload, headers=headers)
            x = response.json()
            return x['percentPlagiarism']

        except:
            return None
    @staticmethod
    def relevancescore(premise,topic):

        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

        model_name = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)

        hypothesis = "The assignment is well-researched and informative. and relevant to {topic} "

        input = tokenizer(premise, hypothesis, truncation=True, return_tensors="pt")
        output = model(input["input_ids"].to(device))  # device = "cuda:0" or "cpu"
        prediction = torch.softmax(output["logits"][0], -1).tolist()
        label_names = ["entailment", "neutral", "contradiction"]
        prediction = {name: round(float(pred) * 100, 1) for pred, name in zip(prediction, label_names)}
        # print(prediction['entailment'])
        return prediction['entailment'], prediction['contradiction']
    