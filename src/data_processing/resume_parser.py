import spacy
import re
from typing import Dict, List

class ResumeParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def parse_resume(self, text: str) -> Dict:
        # Basic section detection and normalization
        sections = self._extract_sections(text)
        
        return {
            "skills": self._extract_skills(text),
            "education": self._extract_education(sections.get("education", "")),
            "experience": self._extract_experience(sections.get("experience", "")),
            "projects": self._extract_projects(sections.get("projects", "")),
            "certifications": self._extract_certifications(text)
        }
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        sections = {}
        lines = text.split('\n')
        current_section = "other"
        
        for line in lines:
            line_lower = line.strip().lower()
            if any(keyword in line_lower for keyword in ['education', 'academic']):
                current_section = "education"
                sections[current_section] = line + "\n"
            elif any(keyword in line_lower for keyword in ['experience', 'employment', 'work']):
                current_section = "experience"
                sections[current_section] = line + "\n"
            elif any(keyword in line_lower for keyword in ['project', 'portfolio']):
                current_section = "projects"
                sections[current_section] = line + "\n"
            elif any(keyword in line_lower for keyword in ['skill', 'competence', 'ability']):
                current_section = "skills"
                sections[current_section] = line + "\n"
            elif any(keyword in line_lower for keyword in ['certification', 'certificate']):
                current_section = "certifications"
                sections[current_section] = line + "\n"
            else:
                if current_section in sections:
                    sections[current_section] += line + "\n"
        
        return sections
    
    def _extract_skills(self, text: str) -> List[str]:
        # Simple skill extraction using common tech skills
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
    
    def _extract_education(self, text: str) -> List[str]:
        # Simple education extraction
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'diploma', 'university', 'college']
        lines = text.split('\n')
        education = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in education_keywords):
                education.append(line.strip())
        
        return education
    
    def _extract_experience(self, text: str) -> List[str]:
        # Simple experience extraction
        exp_keywords = ['experience', 'work', 'employment', 'internship']
        lines = text.split('\n')
        experience = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in exp_keywords):
                experience.append(line.strip())
            elif re.search(r'\d+ years?', line.lower()):
                experience.append(line.strip())
        
        return experience
    
    def _extract_projects(self, text: str) -> List[str]:
        # Simple project extraction
        proj_keywords = ['project', 'portfolio', 'developed', 'built', 'created']
        lines = text.split('\n')
        projects = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in proj_keywords):
                projects.append(line.strip())
        
        return projects
    
    def _extract_certifications(self, text: str) -> List[str]:
        # Simple certification extraction
        cert_keywords = ['certification', 'certificate', 'certified', 'aws', 'azure', 'google cloud']
        lines = text.split('\n')
        certifications = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in cert_keywords):
                certifications.append(line.strip())
        
        return certifications