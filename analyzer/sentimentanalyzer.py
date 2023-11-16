import csv
import string
from bs4 import BeautifulSoup
import requests
import os
import nltk 
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
import re
import pandas as pd
from prettytable import PrettyTable
from db.plotterdb import con_create,save_ass

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
stopwordpath =r"your-path-for-stopword\StopWords"
pospath= r"your-path-for-postivewordlib\positive-words.txt"
negpath =r"your-path-for-negativewords\negative-words.txt"

class evaluator:
    def __init__(self):
        self.dict_p = set()
        self.dict_n = set()
        self.stopw = set()

    def initialization(self, stopword_folder=stopwordpath, dictionary_positive=pospath, dictionary_negative=negpath):
        # Opening stopwords folder to access various files associated and updating the "stopw" set
        for filename in os.listdir(stopword_folder):
            with open(os.path.join(stopword_folder, filename), 'r') as file:
                self.stopw.update([word.lower() for word in file.read().splitlines()])

        # Opening positive and negative dictionaries
        with open(dictionary_negative, "r") as fn:
            self.dict_n.update(fn.read().splitlines()) 

        with open(dictionary_positive, "r") as fz:
            self.dict_p.update(fz.read().splitlines())

    # def write_into_csv(self, x):
    #     columns = ["url", "Positive Sentences", "Negative Sentences", "Polarity", "Subjectivity", 
    #                "Average Sentence Length", "Complex Word Percentage", "Fog Index", "Average Word Length", 
    #                "Complex Word Count", "Word Count", "Syllable Count", "Personal Pronouns"]

    #     with open(r"output.csv", 'w', encoding='utf-8', newline='') as fp:
    #         wr = csv.writer(fp)
    #         wr.writerow(columns)
    #         wr.writerows(x)
    #     fp.close()

    def count_syl(self, w):
        vowels = 'aeiou'
        count = 0
        if w[0] in vowels:
            count += 1
        for i in range(1, len(w)):
            if w[i] in vowels and w[i - 1] not in vowels:
                count += 1
        if w.endswith(('es', 'ed')):
            count -= 1
        return count

    def count_pronouns(self, text):
        pattern = r"\b(I|we|my|ours|us)\b"
        exclude_pattern = r"\bUS\b"
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        matches = [match for match in matches if not re.match(exclude_pattern, match, flags=re.IGNORECASE)]
        count = len(matches)
        return count

    def sentiment_analysis(self, text,enr):
        # Tokenization and lemmatization
        pc = self.count_pronouns(text)
        tokens = nltk.word_tokenize(text.lower())
        tokens = [w for w in tokens if w not in string.punctuation]
        lemmatizer = WordNetLemmatizer()
        lemmas = [lemmatizer.lemmatize(token) for token in tokens]
        lemmatized_text = ' '.join(lemmas)
        tokens = nltk.word_tokenize(lemmatized_text)
        stopwoz = set(stopwords.words('english'))
        tokens = [w for w in tokens if w not in stopwoz]

        # Calculate positives and negatives 
        pos_s = sum(1 for i in tokens if i in self.dict_p)
        neg_s = sum(1 for i in tokens if i in self.dict_n)

        # Polarity 
        polarity = (pos_s - neg_s) / (pos_s + neg_s + 0.000001)
        sentences = nltk.sent_tokenize(text)

        # Calculate the word count 
        word_count = len(tokens)

        # Calculate average number of words per sentence
        avg_words = word_count / len(sentences)

        # Subjectivity
        subjectivity = (pos_s + neg_s) / ((word_count) + 0.000001)

        # Syllable count 
        syl_count = sum(self.count_syl(w) for w in tokens)

        # Complex words 
        complex_count = sum(1 for w in tokens if self.count_syl(w) > 2)

        # Complex percentage 
        cmp_percentage = (complex_count / word_count) * 100

        # Fog Index 
        sum_of_sent = sum(len(nltk.word_tokenize(sentence)) for sentence in sentences)
        avg_sent = sum_of_sent / len(sentences)
        fog_index = 0.4 * (avg_sent) + cmp_percentage
        conn = con_create()
        if conn:
            cursor = conn.cursor()
            save_ass(conn,enr, pos_s, neg_s, polarity, subjectivity, avg_sent, cmp_percentage, fog_index, 
             avg_words, complex_count, word_count, syl_count)
            print("saved result in db")
            conn.close()  
        
        x = [pos_s, neg_s, polarity, subjectivity, avg_sent, cmp_percentage, fog_index, 
             avg_words, complex_count, word_count, syl_count, pc]
        
        print(x)

        return x
    
    def cleaning_file(self, text):
        cleaned_text = ' '.join([word for word in text.split() if word.lower() not in self.stopw])
        return cleaned_text

    def gathering_info(self, text,enr):
        cleaned_file = self.cleaning_file(text)
        print(cleaned_file)
        
        result = self.sentiment_analysis(cleaned_file,enr)
        return result 
    

