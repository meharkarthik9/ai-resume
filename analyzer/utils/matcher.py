import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text


def calculate_match_score(resume_text, job_description):
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([resume_text, job_description])

    score = cosine_similarity(vectors[0], vectors[1])
    return round(float(score[0][0]) * 100, 2)


def normalize_skills(skills):
    mapping = {
        "js": "javascript",
        "ml": "machine learning",
        "dl": "deep learning",
        "dsa": "data structures"
    }

    return list(set(mapping.get(skill, skill) for skill in skills))


def skill_match_score(resume_skills, jd_skills):
    if not jd_skills:
        return 0

    matched = set(resume_skills).intersection(set(jd_skills))
    return round((len(matched) / len(jd_skills)) * 100, 2)



def semantic_match_score(a, b):
    return round(SequenceMatcher(None, a, b).ratio() * 100, 2)