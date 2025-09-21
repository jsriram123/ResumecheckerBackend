from sklearn.feature_extraction.text import TfidfVectorizer
import re
from typing import List

class HardMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
    
    def calculate_keyword_score(self, resume_text: str, jd_text: str) -> float:
        # TF-IDF based keyword matching
        try:
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, jd_text])
            similarity = (tfidf_matrix * tfidf_matrix.T).A[0, 1]
            return max(0, min(similarity, 1))  # Ensure between 0 and 1
        except:
            return 0.0
    
    def exact_match_skills(self, resume_skills: List[str], required_skills: List[str]) -> float:
        if not required_skills:
            return 1.0
            
        matched = 0
        for req_skill in required_skills:
            for res_skill in resume_skills:
                if req_skill.lower() == res_skill.lower():
                    matched += 1
                    break
        
        return matched / len(required_skills)
    
    def fuzzy_match_skills(self, resume_skills: List[str], required_skills: List[str]) -> float:
        if not required_skills:
            return 1.0
            
        matched = 0
        for req_skill in required_skills:
            for res_skill in resume_skills:
                # Simple fuzzy matching
                if req_skill.lower() in res_skill.lower() or res_skill.lower() in req_skill.lower():
                    matched += 1
                    break
        
        return matched / len(required_skills)