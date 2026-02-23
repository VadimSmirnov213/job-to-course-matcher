import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class UserProfileBasedRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.user_profiles = {}
        self.course_vectors = None

    def create_course_vectors(self, courses):
        self.course_vectors = self.vectorizer.fit_transform(courses['description'].values)
        self.courses = courses

    def add_user_profile(self, user_id, user_data):
        user_profile_vector = self.vectorizer.transform([user_data['skills']])
        self.user_profiles[user_id] = user_profile_vector

    def recommend_courses(self, user_id, top_n=5):
        user_vector = self.user_profiles[user_id]
        similarity_scores = cosine_similarity(user_vector, self.course_vectors).flatten()
        top_course_indices = np.argsort(similarity_scores)[-top_n:][::-1]
        recommended_courses = self.courses.iloc[top_course_indices]
        return recommended_courses[['course_id', 'description']]

recommender = UserProfileBasedRecommender()

courses = pd.DataFrame({
    'course_id': [1, 2, 3],
    'description': [
        'Introduction to Python for data science',
        'Advanced Machine Learning techniques',
        'Project management fundamentals'
    ]
})

users = {
    'user1': {'skills': 'python, data analysis, machine learning'}
}

recommender.create_course_vectors(courses)
recommender.add_user_profile('user1', users['user1'])

recommended_courses = recommender.recommend_courses('user1')
print(recommended_courses)
