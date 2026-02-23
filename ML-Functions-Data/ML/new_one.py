import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, TFBertModel
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, Concatenate

courses = pd.DataFrame({
    'course_id': ['course1', 'course2', 'course3'],
    'description': ['Learn Python basics', 'Advanced Machine Learning', 'Intro to Data Science'],
    'difficulty': ['beginner', 'advanced', 'intermediate'],
    'duration': [10, 20, 15],
    'format': ['video', 'video', 'interactive']
})

users = pd.DataFrame({
    'user_id': ['user1', 'user2', 'user3'],
    'competencies': ['python, data analysis', 'machine learning, python', 'data science, statistics'],
    'learning_pace': ['moderate', 'fast', 'slow']
})

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = TFBertModel.from_pretrained('bert-base-uncased')

def get_course_embeddings(course_descriptions):
    encoded_input = tokenizer(course_descriptions, return_tensors='tf', padding=True, truncation=True)
    outputs = bert_model(encoded_input)
    return outputs.last_hidden_state[:, 0, :]

course_embeddings = get_course_embeddings(courses['description'].tolist())


def match_competencies(user_competencies, course_requirements):
    user_vecs = get_course_embeddings(user_competencies)
    requirement_vecs = get_course_embeddings(course_requirements)
    return cosine_similarity(user_vecs, requirement_vecs)

competency_scores = match_competencies(users['competencies'], courses['description'])


def adaptive_learning_system(user_ids, course_ids, initial_scores):
    inputs = Input(shape=(1,))
    x = Dense(64, activation='relu')(inputs)
    x = Dropout(0.2)(x)
    x = Dense(32, activation='relu')(x)
    outputs = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit([user_ids, course_ids], initial_scores, epochs=10, batch_size=1)
    return model

model_adaptive = adaptive_learning_system(users['user_id'], courses['course_id'], competency_scores)

test_user_ids = np.array([1, 2, 3])
test_course_ids = np.array([1, 2, 3])
predictions = model_adaptive.predict([test_user_ids, test_course_ids])
print(predictions)
