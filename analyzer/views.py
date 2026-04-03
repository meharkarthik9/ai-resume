from django.shortcuts import render
from .models import Resume
from .utils.parser import extract_text_from_pdf
from .utils.skills import extract_skills
from .utils.matcher import (
    skill_match_score,
    semantic_match_score,
    normalize_skills
)


def home(request):
    if request.method == 'POST':
        file = request.FILES.get('resume')
        jd = request.POST.get('jd')

        if file:
            obj = Resume.objects.create(file=file)

            file_path = obj.file.path
            extracted_text = extract_text_from_pdf(file_path)

            # Extract and normalize skills
            skills = normalize_skills(extract_skills(extracted_text))

            jd_skills = []
            skill_score = None
            semantic_score = None
            missing_skills = []

            if jd:
                jd_skills = normalize_skills(extract_skills(jd))

                # 🚨 Check AFTER extraction
                if not jd_skills:
                    missing_skills = ["No recognizable skills found in job description"]
                    skill_score = 0
                    semantic_score = semantic_match_score(extracted_text, jd)

                else:
                    # Skill match
                    skill_score = skill_match_score(skills, jd_skills)

                    # Semantic match
                    semantic_score = semantic_match_score(
                        " ".join(skills),
                        " ".join(jd_skills)
                    )

                    # Missing skills
                    missing_skills = list(set(jd_skills) - set(skills))

            return render(request, 'analyzer/home.html', {
                'message': 'Uploaded Successfully',
                'text': extracted_text,
                'skills': skills,
                'score': skill_score,
                'semantic_score': semantic_score,
                'missing_skills': missing_skills
            })

    return render(request, 'analyzer/home.html')