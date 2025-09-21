from typing import Dict, List
from .hard_matcher import HardMatcher
from .semantic_matcher import SemanticMatcher

class ScoringOrchestrator:
    def __init__(self):
        self.hard_matcher = HardMatcher()
        self.semantic_matcher = SemanticMatcher()
    
    def calculate_relevance_score(self, resume_data: Dict, jd_data: Dict) -> Dict:
        # Calculate individual scores
        keyword_score = self.hard_matcher.calculate_keyword_score(
            resume_data["text"], jd_data["text"]
        )
        
        semantic_score = self.semantic_matcher.calculate_semantic_similarity(
            resume_data["text"], jd_data["text"]
        )
        
        # Calculate skill matching score
        skill_score = self.hard_matcher.exact_match_skills(
            resume_data.get("skills", []), jd_data.get("required_skills", [])
        )
        
        # Weighted final score (adjust weights as needed)
        final_score = (keyword_score * 0.3) + (semantic_score * 0.3) + (skill_score * 0.4)
        
        return {
            "relevance_score": round(final_score * 100, 2),  # Convert to 0-100 scale
            "keyword_score": round(keyword_score * 100, 2),
            "semantic_score": round(semantic_score * 100, 2),
            "skill_score": round(skill_score * 100, 2),
            "missing_skills": self._identify_missing_skills(
                resume_data.get("skills", []), jd_data.get("required_skills", [])
            ),
            "verdict": self._get_verdict(final_score)
        }
    
    def _get_verdict(self, score: float) -> str:
        if score >= 0.7:
            return "High"
        elif score >= 0.4:
            return "Medium"
        else:
            return "Low"
    
    def _identify_missing_skills(self, resume_skills: List[str], required_skills: List[str]) -> List[str]:
        return [skill for skill in required_skills if skill not in resume_skills]