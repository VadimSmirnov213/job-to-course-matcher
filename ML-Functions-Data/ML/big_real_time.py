import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import defaultdict

class AdvancedRecommendationSystem:
    def __init__(self, num_features=100, max_words=5000, max_sequence_length=150):
        self.vectorizer = TfidfVectorizer(max_features=num_features)
        self.svd = TruncatedSVD(n_components=50)
        self.cluster_model = KMeans(n_clusters=10)
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.tokenizer = Tokenizer(num_words=max_words)
        self.model = self.build_lstm_model(max_words, max_sequence_length)
        self.user_profiles = defaultdict(lambda: {'interests': np.zeros(50), 'ratings': {}})
        self.course_metadata = {}
        self.scaler = MinMaxScaler()

    def build_lstm_model(self, vocab_size, max_sequence_length):
        model = Sequential([
            Embedding(vocab_size, 128, input_length=max_sequence_length),
            LSTM(64, return_sequences=True),
            LSTM(32),
            Dense(10, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def preprocess_courses(self, courses):
        descriptions = [course['description'] for course in courses]
        tfidf_matrix = self.vectorizer.fit_transform(descriptions)
        reduced_matrix = self.svd.fit_transform(tfidf_matrix)
        self.cluster_model.fit(reduced_matrix)
        for idx, course in enumerate(courses):
            self.course_metadata[course['id']] = {
                'vector': reduced_matrix[idx],
                'cluster': self.cluster_model.labels_[idx],
                'keywords': course['keywords'],
                'rating_avg': course['rating_avg']
            }

    def update_user_profile(self, user_id, course_id, rating):
        course_vector = self.course_metadata[course_id]['vector']
        self.user_profiles[user_id]['interests'] += course_vector * rating
        self.user_profiles[user_id]['ratings'][course_id] = rating

    def recommend(self, user_id, num_recommendations=5):
        user_interests = self.user_profiles[user_id]['interests']
        similarities = {course_id: cosine_similarity([user_interests], [meta['vector']])[0][0] for course_id, meta in self.course_metadata.items()}
        sorted_courses = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        return sorted_courses[:num_recommendations]

    def train_sentiment_model(self, texts, labels):
        sequences = self.tokenizer.texts_to_sequences(texts)
        padded_sequences = pad_sequences(sequences, maxlen=150)
        self.model.fit(padded_sequences, labels, epochs=10, batch_size=32)

    def get_sentiment(self, text):
        return self.sentiment_analyzer.polarity_scores(text)['compound']

    def adjust_recommendations_based_on_sentiment(self, recommendations, user_id):
        adjusted = []
        for course_id, _ in recommendations:
            course_reviews = self.fetch_course_reviews(course_id)
            sentiments = [self.get_sentiment(review) for review in course_reviews]
            avg_sentiment = np.mean(sentiments)
            adjusted.append((course_id, self.user_profiles[user_id]['ratings'].get(course_id, 0) * avg_sentiment))
        return sorted(adjusted, key=lambda x: x[1], reverse=True)

# экземпляр системы и использование
rec_system = AdvancedRecommendationSystem()
courses = [{'id': 1, 'description': 'Learn Python', 'keywords': ['python', 'programming'], 'rating_avg': 4.7}, ...]
rec_system.preprocess_courses(courses)
rec_system.update_user_profile('user123', 1, 5)
recommendations = rec_system.recommend('user123')
sentiment_adjusted = rec_system.adjust_recommendations_based_on_sentiment(recommendations, 'user123')
