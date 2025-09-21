import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional  # Add all necessary typing imports

class DatabaseManager:
    def __init__(self, db_path="resume_evaluation.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self):
        # Create evaluation results table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_name TEXT,
                jd_name TEXT,
                relevance_score REAL,
                keyword_score REAL,
                semantic_score REAL,
                skill_score REAL,
                verdict TEXT,
                missing_skills TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def save_evaluation_result(self, resume_name: str, jd_name: str, result: Dict):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO evaluations (resume_name, jd_name, relevance_score, keyword_score, 
                                   semantic_score, skill_score, verdict, missing_skills)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            resume_name, 
            jd_name, 
            result["relevance_score"],
            result["keyword_score"],
            result["semantic_score"],
            result["skill_score"],
            result["verdict"],
            json.dumps(result["missing_skills"])
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_evaluation_results(self, filters: Dict = None):
        query = "SELECT * FROM evaluations"
        params = []
        
        if filters:
            conditions = []
            if "jd_name" in filters and filters["jd_name"]:
                conditions.append("jd_name LIKE ?")
                params.append(f"%{filters['jd_name']}%")
            if "min_score" in filters and filters["min_score"] is not None:
                conditions.append("relevance_score >= ?")
                params.append(filters["min_score"])
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY created_at DESC"
        
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "resume_name": row[1],
                "jd_name": row[2],
                "relevance_score": row[3],
                "keyword_score": row[4],
                "semantic_score": row[5],
                "skill_score": row[6],
                "verdict": row[7],
                "missing_skills": json.loads(row[8]),
                "created_at": row[9]
            })
        
        return results