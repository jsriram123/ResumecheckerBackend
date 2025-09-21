import re
from typing import Dict, List

class JDParser:
    def parse_jd(self, text: str) -> Dict:
        return {
            "required_skills": self._extract_required_skills(text),
            "preferred_skills": self._extract_preferred_skills(text),
            "education_requirements": self._extract_education_requirements(text),
            "experience_requirements": self._extract_experience_requirements(text)
        }
    
    def _extract_required_skills(self, text: str) -> List[str]:
        # Extract must-have skills using regex patterns
        required_patterns = [
            r"required skills?[:](.*?)(?=preferred|education|experience|$)",
            r"must have[:](.*?)(?=nice to have|education|experience|$)",
            r"requirements?[:](.*?)(?=preferred|education|experience|$)",
            r"qualifications?[:](.*?)(?=preferred|education|experience|$)"
        ]
        
        skills = []
        for pattern in required_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                skills_text = match.group(1)
                # Extract individual skills
                skills.extend(self._extract_individual_skills(skills_text))
        
        return list(set(skills))  # Remove duplicates
    
    def _extract_preferred_skills(self, text: str) -> List[str]:
        # Extract nice-to-have skills
        preferred_patterns = [
            r"preferred skills?[:](.*?)(?=required|education|experience|$)",
            r"nice to have[:](.*?)(?=must have|education|experience|$)",
            r"plus[:](.*?)(?=required|education|experience|$)"
        ]
        
        skills = []
        for pattern in preferred_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                skills_text = match.group(1)
                # Extract individual skills
                skills.extend(self._extract_individual_skills(skills_text))
        
        return list(set(skills))  # Remove duplicates
    
    def _extract_individual_skills(self, text: str) -> List[str]:
        # Common tech skills to look for
        common_skills = [
            'python', 'java', 'javascript', 'c++', 'c#', 'html', 'css', 'sql', 
            'react', 'angular', 'vue', 'node', 'express', 'django', 'flask',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
            'machine learning', 'ai', 'data analysis', 'tableau', 'power bi'
        ]
        
        found_skills = []
        for skill in common_skills:
            if skill.lower() in text.lower():
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_education_requirements(self, text: str) -> List[str]:
        # Extract education requirements
        edu_patterns = [
            r"education[:](.*?)(?=experience|skills|$)",
            r"degree[:](.*?)(?=experience|skills|$)",
            r"qualifications?[:](.*?)(?=experience|skills|$)"
        ]
        
        education = []
        for pattern in edu_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                edu_text = match.group(1)
                # Look for degree types
                degree_types = ['bachelor', 'master', 'phd', 'associate', 'diploma']
                for degree in degree_types:
                    if degree in edu_text.lower():
                        education.append(degree.capitalize() + " degree")
        
        return education
    
    def _extract_experience_requirements(self, text: str) -> List[str]:
        # Extract experience requirements
        exp_pattern = r"(\d+)[+]? years? experience"
        matches = re.findall(exp_pattern, text, re.IGNORECASE)
        
        experience = []
        for match in matches:
            experience.append(f"{match} years of experience")
        
        return experience