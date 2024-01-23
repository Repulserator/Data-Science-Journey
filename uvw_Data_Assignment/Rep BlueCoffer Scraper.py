#Import necessary
import os
import nltk
import pyphen
import requests
import pandas as pd
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from tqdm import tqdm, tqdm_pandas
from textblob import TextBlob
from pathlib import Path
import string
import spacy

global stopwords_folder
stopwords_folder = 'StopWords'


def scrape_article(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1', class_='entry-title').get_text(strip=True)
            content = soup.find(class_='td-main-content').get_text(separator=' ', strip=True)
            return title, content
        else:
            return pd.Series([None, None])

    except:
        return pd.Series([None, None])


#Read Stopwords from file
def read_stopwords(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        stopwords = {line.strip().lower() for line in file}
    return stopwords

#Load all stopwords from the file and combine them too
def load_stopwords(folder_path):
    combined_stopwords = set()
    folder = Path(folder_path)
    for file_path in folder.iterdir():
        if file_path.is_file():
            combined_stopwords.update(read_stopwords(file_path))
    return combined_stopwords

def custom_tokenize(text, stopwords):
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word.lower() not in stopwords]
    return filtered_tokens


def load(file_path):
    with open(file_path, 'r') as file:
        return set(word.strip().lower() for word in file.readlines())


#Since the context was not mentioned, Some operations use preprocessed text and others use the original article
def all(sent):

    global stopwords_folder
    
    #Load Stopwords
    try:
        all_stopwords
    except:
        all_stopwords = load_stopwords(stopwords_folder)


    #Check for Nan entries
    if pd.isna(sent):
        return [pd.NA] * 14
    else:
        pass

    # Tokenize sentences and words
    sentences = nltk.sent_tokenize(sent.lower())
    word_tok = " ".join(custom_tokenize(sent, all_stopwords))
    #Usually I would just use nltk tokenize but since the stopwords folder was given, I utilized that instead.
    #I also got rid of the punctations and lower cased it just in case
    #However for sentences i decided to move forward with nltk

    #Stop Check to ensure program works seamlessly from anywhere   
    stopwords_folder = os.path.dirname(stopwords_folder) + '/' if os.path.dirname(stopwords_folder) != '' else ''

    # Load positive and negative words
    positive_words = load(stopwords_folder + 'MasterDictionary/positive-words.txt')
    negative_words = load(stopwords_folder + 'MasterDictionary/negative-words.txt')


    #Positive and Negative Scores
    words = word_tok.split()
    positive_score = sum(1 for word in words if word.lower() in positive_words)
    negative_score = sum(1 for word in words if word.lower() in negative_words)
    
    #Polarity and Subjectivity
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score)/(len(words) + 0.000001)

    #Average Length per Sentence
    total_words = 0
    for sentence in sentences:
        total_words += len(sentence.split())
    avg_sentence_length = total_words / len(sentences) if sentences else 0

    #Complex words
    dic = pyphen.Pyphen(lang='en')
    complex_words = [word for word in words if len(dic.inserted(word).split('-')) >= 3]

    #Percentage of complex words
    percentage_complex_words = len(complex_words) / len(words) * 100

    #Fog Index
    fog_index = 0.4 * (avg_sentence_length + 100 * (len(complex_words) / len(words)))


    # Count the number of words in each sentence
    words_per_sentence = [len(sentence.split()) for sentence in sentences]
    #Average words per sentence
    avg_words_per_sentence = sum(words_per_sentence) / len(sentences) if sentences else 0


    #Syllable per word
    syllable_per_word = [dic.inserted(word).count('-') + 1 for word in words]
    avg_syllable_per_word = sum(syllable_per_word) / len(syllable_per_word) if syllable_per_word else 0


    #Personal Pronoun count 
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sent)
    personal_pronouns = len([token.text for token in doc if token.pos_ == "PRON"])
    
    #Average Word Length
    avg_word_length = sum(len(word) for word in words) / len(words)

    return word_tok,positive_score,negative_score,polarity_score,subjectivity_score,avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, len(complex_words), len(words), avg_syllable_per_word, personal_pronouns, avg_word_length


#To check and find if the structure is similar, if all else fails will ask for directory and continue
try:
    if "StopWords_Auditor.txt" in os.listdir(stopwords_folder):
        print(":)")
    else:
        raise ValueError("Breaking")
except:
    stopwords_folder = input("Enter the folder path: [Ideally its the same structure as the google drive]\n")
    if '\\' in stopwords_folder:
        stopwords_folder = stopwords_folder.replace('\\', '/')+'/StopWords'



#Loads Input file
try:
    df = pd.read_excel(os.path.dirname(stopwords_folder)+'/input.xlsx')
except:
    df = pd.read_excel(os.path.dirname(stopwords_folder)+'input.xlsx')

#Lets you waste less time
while True:
  choice = input('Quick or Full (Runs code on only first 10 entries for the sake of testing)\n1. Quick\n2. Full\n')
  
  if choice == '1':
    print('Running Quick Test')
    df = df.head(10)
    # Run quick code
    break
  elif choice == '2':   
    print('Running Full Test')
    # Run full code
    break
  else:
    print('Invalid option, please enter 1 or 2')
    
print('Test complete!')


# Apply the function to each row
tqdm_pandas(tqdm())
df[['Title', 'Content']] = df['URL'].progress_apply(lambda x: pd.Series(scrape_article(x)))

tqdm_pandas(tqdm())
df[['Pre Process','Positive Score','Negative Score','Polarity Score','Subjectivity Score','Average Sentence Length', 'Complex Words %', 'Fog Index','Average Words Per Sentence', 'Complex Words Count', 'Word Count', 'Syllable Per Word','Personal Pronouns','Average Word Length']] = df.progress_apply(lambda row: all(row['Content']), axis=1, result_type='expand')
print(df)

#Finally Writes to excel file [2 files are created 1, is with the title and pre processed and the otehr one strictly adhering to what the assessment asked]
#I am aware that title was not included in any of the statistics
try:
    df.to_excel(stopwords_folder+"output.xlsx")
    df2 = df.drop(columns=['Pre Process', 'Title']) 
    df2.to_excel(stopwords_folder +"output final.xlsx")
except:
    print("Error in writing")


##GG