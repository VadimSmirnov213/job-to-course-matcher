from celery import Celery
from config import REDIS_NAME, REDIS_PORT, REDIS_HOST
from ml.main import process_data, calculate_similarity, np
from ml.vaca import DataCollector
celery = Celery('tasks', broker=F'{REDIS_NAME}://{REDIS_HOST}:{REDIS_PORT}', backend=F'{REDIS_NAME}://{REDIS_HOST}:{REDIS_PORT}')

@celery.task
def get_recommendations(courses, vacancy, top_n=3):
    """Генерация рекомендаций на основе расчетного сходства"""
    course_desc, vacancy_keys = process_data(courses, vacancy)
    similarity_scores = calculate_similarity(course_desc, vacancy_keys)
    course_indices = np.argsort(similarity_scores[0])[::-1][:top_n]
    recommendations = {
        'vacancy_id': vacancy.get('Ids', ''),
        'vacancy_name': vacancy.get('Name', ''),
        'recommendations': [
            {
                'course_id': courses[i].get('_id', ''),
                'course_name': courses[i].get('name', ''),
                'course_description': courses[i].get('desc', ''),
                'course_rating': courses[i].get('rating', 'Not rated'),
                'similarity_score': similarity_scores[0][i]
            } for i in course_indices
        ]
    }
    return recommendations

@celery.task
def get_dict(url):
    dc = DataCollector(exchange_rates={"USD": 0.01264, "EUR": 0.01083, "RUR": 1.00000})
    def F(url):
        start = url.rfind('/') + 1
        end = url.find('?')
        number = url[start:end]
        return number
    keys = ['Ids', 'Name', 'Employer', 'VacancyOpen', 'Salary', 'Currency', 'Experience',
            'Schedule', 'Keys', 'Description']
    job_dict = dict(zip(keys, dc.get_vacancy(F(url))))
    return job_dict
