from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
import numpy as np
from textblob import TextBlob
import pandas as pd
from collections import defaultdict

class DynamicRecommendationModel:
    def __init__(self, num_topics=100):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
        self.lsa = make_pipeline(TruncatedSVD(num_topics), Normalizer(copy=False))
        self.course_vectors = None
        self.user_profiles = defaultdict(dict)
        self.course_metadata = {}
        self.num_topics = num_topics

    def fit_transform_courses(self, courses):
        combined_texts = [course['description'] + ' ' + ' '.join(course['keywords']) for course in courses]
        self.course_vectors = self.lsa.fit_transform(self.vectorizer.fit_transform(combined_texts))
        for idx, course in enumerate(courses):
            self.course_metadata[course['_id']] = idx

    def update_course(self, course):
        combined_text = course['description'] + ' ' + ' '.join(course['keywords'])
        course_vector = self.lsa.transform(self.vectorizer.transform([combined_text]))
        if course['_id'] in self.course_metadata:
            self.course_vectors[self.course_metadata[course['_id']]] = course_vector
        else:
            self.course_vectors = np.vstack([self.course_vectors, course_vector])
            self.course_metadata[course['_id']] = self.course_vectors.shape[0] - 1

    def add_user_feedback(self, user_id, course_id, rating, sentiment_score):
        if course_id in self.course_metadata:
            self.user_profiles[user_id][course_id] = {'rating': rating, 'sentiment': sentiment_score}

    def recommend(self, user_id, num_recommendations=5):
        user_ratings = self.user_profiles[user_id]
        similarity_matrix = cosine_similarity(self.course_vectors)
        user_interest_scores = np.zeros(self.course_vectors.shape[0])
        for course_id, feedback in user_ratings.items():
            course_idx = self.course_metadata[course_id]
            user_interest_scores += (feedback['rating'] + feedback['sentiment']) * similarity_matrix[course_idx]
        recommendations = np.argsort(user_interest_scores)[::-1][:num_recommendations]
        return [list(self.course_metadata.keys())[idx] for idx in recommendations if list(self.course_metadata.keys())[idx] not in user_ratings]

    def analyze_sentiment(self, text):
        return TextBlob(text).sentiment.polarity

courses_data = [{'_id': 'course1', 'description': 'Learn Python', 'keywords': ['programming', 'python', 'coding']}, {'_id': 'course2', 'description': 'Learn Java', 'keywords': ['programming', 'java', 'development']}]
model = DynamicRecommendationModel()
model.fit_transform_courses(courses_data)
model.update_course({'_id': 'course3', 'description': 'Data Science with Python', 'keywords': ['data', 'science', 'python']})
feedback = {'user1': {'course1': {'rating': 5, 'comment': 'Great course!'}, 'course2': {'rating': 4, 'comment': 'Good course, but challenging.'}}}
for user, courses in feedback.items():
    for course_id, details in courses.items():
        sentiment_score = model.analyze_sentiment(details['comment'])
        model.add_user_feedback(user, course_id, details['rating'], sentiment_score)
recommendations = model.recommend('user1', 2)
print(recommendations)
