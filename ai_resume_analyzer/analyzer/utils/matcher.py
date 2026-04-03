import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

# Load model ONCE
model = SentenceTransformer('all-MiniLM-L6-v2')


# -----------------------------
# TEXT CLEANING
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text


# -----------------------------
# TF-IDF MATCHING (baseline)
# -----------------------------


# -----------------------------
# SKILL NORMALIZATION
# -----------------------------
def normalize_skills(skills):
    mapping = {
        "js": "javascript",
        "ml": "machine learning",
        "dl": "deep learning",
        "dsa": "data structures"
    }

    normalized = set()
    for skill in skills:
        normalized.add(mapping.get(skill, skill))

    return list(normalized)


# -----------------------------
# SKILL MATCHING (PRIMARY)
# -----------------------------
def skill_match_score(resume_skills, jd_skills):
    if not jd_skills:
        return 0

    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = resume_set.intersection(jd_set)
    score = (len(matched) / len(jd_set)) * 100

    return round(score, 2)


# -----------------------------
# BERT SEMANTIC MATCHING
# -----------------------------


def semantic_match_score(resume_text, job_description):
    emb1 = model.encode(resume_text)
    emb2 = model.encode(job_description)

    score = util.cos_sim(emb1, emb2)[0][0]
    return round(float(score) * 100, 2)