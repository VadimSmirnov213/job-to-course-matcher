from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
import numpy as np


def process_data(courses, vacancy):
    """Подготовка данных для векторизации"""
    courses_desc = [" ".join([course.get('desc', '')] + course.get('keywords', [])) for course in courses]
    vacancy_keys = " ".join([vacancy.get('Description', '')] + vacancy.get('Keys', []))
    return courses_desc, [vacancy_keys]


def calculate_similarity(course_desc, vacancy_keys):
    """Расчет сходства"""
    vectorizer = TfidfVectorizer()
    all_texts = vacancy_keys + course_desc
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    k = min(tfidf_matrix.shape) - 1

    u, s, vt = svds(tfidf_matrix, k=k)
    s_matrix = np.diag(s)
    reduced_tfidf = np.dot(u, s_matrix)

    vacancy_vectors = reduced_tfidf[:len(vacancy_keys)]
    course_vectors = reduced_tfidf[len(vacancy_keys):]

    return cosine_similarity(vacancy_vectors, course_vectors)


# def get_recommendations(courses, vacancy, top_n=3):
#     """Генерация рекомендаций на основе расчетного сходства"""
#     course_desc, vacancy_keys = process_data(courses, vacancy)
#     similarity_scores = calculate_similarity(course_desc, vacancy_keys)
#     course_indices = np.argsort(similarity_scores[0])[::-1][:top_n]
#     recommendations = {
#         'vacancy_id': vacancy.get('Ids', ''),
#         'vacancy_name': vacancy.get('Name', ''),
#         'recommendations': [
#             {
#                 'course_id': courses[i].get('_id', ''),
#                 'course_name': courses[i].get('name', ''),
#                 'course_description': courses[i].get('desc', ''),
#                 'course_rating': courses[i].get('rating', 'Not rated'),
#                 'similarity_score': similarity_scores[0][i]
#             } for i in course_indices
#         ]
#     }
#     return recommendations


