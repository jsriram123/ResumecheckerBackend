from langchain.embeddings import HuggingFaceEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SemanticMatcher:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    def calculate_semantic_similarity(self, resume_text: str, jd_text: str) -> float:
        try:
            # Generate embeddings and calculate cosine similarity
            resume_embedding = self.embeddings.embed_query(resume_text)
            jd_embedding = self.embeddings.embed_query(jd_text)
            
            similarity = cosine_similarity([resume_embedding], [jd_embedding])[0][0]
            return max(0, min(similarity, 1))  # Ensure between 0 and 1
        except Exception as e:
            print(f"Error in semantic matching: {e}")
            return 0.0