import re

SKILLS_DB = [
    "python", "java", "c++","ruby"
    "django", "flask",
    "sql", "mysql",
    "machine learning", "ml",
    "deep learning", "dl",
    "nlp",
    "javascript", "js",
    "react", "node",
    "html", "css",
    "data structures", "algorithms", "dsa"
]

def extract_skills(text):
    text = text.lower()
    found = set()

    for skill in SKILLS_DB:
        # 👉 use word boundaries to avoid false matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found.add(skill)

    return list(found)