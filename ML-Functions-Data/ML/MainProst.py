import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def preprocess_text(text, language='russian'):
    """Очистка и предобработка текста"""
    text = re.sub(r'[\W\d]', ' ', text.lower())
    stemmer = SnowballStemmer(language)
    stop_words = set(stopwords.words(language))
    words = nltk.word_tokenize(text)
    return ' '.join([stemmer.stem(word) for word in words if word not in stop_words])

def load_data(filepath, text_columns):
    """Загрузка и предварительная обработка данных из CSV файла"""
    try:
        data = pd.read_csv(filepath)
        for column in text_columns:
            data[column] = data[column].apply(preprocess_text)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()


def get_course_recommendations(vacancy_data, courses_df, top_n=3):
    tfidf_vectorizer = TfidfVectorizer()
    all_texts = vacancy_data['Description'].tolist() + courses_df['description'].tolist()
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_texts)
    
    vacancy_vectors = tfidf_matrix[:len(vacancy_data)]
    course_vectors = tfidf_matrix[len(vacancy_data):]
    
    similarity_scores = cosine_similarity(vacancy_vectors, course_vectors)
    
    recommendations = []
    for idx, vacancy in enumerate(vacancy_data.itertuples()):
        vacancy_recommendations = {
            "vacancy_id": vacancy.Ids,
            "vacancy_name": vacancy.Name,
            "recommended_courses": []
        }
        course_sim_scores = similarity_scores[idx]
        top_courses = sorted(list(enumerate(course_sim_scores)), key=lambda x: x[1], reverse=True)[:top_n]
        
        for course_idx, score in top_courses:
            course_info = {
                "course_name": courses_df.iloc[course_idx]['name'],
                "course_description": courses_df.iloc[course_idx]['description'],
                "similarity_score": score
            }
            vacancy_recommendations["recommended_courses"].append(course_info)
        
        recommendations.append(vacancy_recommendations)
    
    return recommendations

vacancies = load_data('path_to_vacancies.csv', ['Description'])
courses_df = load_data('path_to_courses.csv', ['description'])  # файл с курсами

recommendations = get_course_recommendations(vacancies, courses_df)
json_output = json.dumps(recommendations, indent=4)
print(json_output)
