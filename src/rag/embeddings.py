from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)

    # Vectorise une liste de Documents et retourne une liste de vecteurs
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    # Vectorise une requête et retourne un vecteur
    def embed_query(self, text: str) -> list[float]:

        return self.model.encode(text, convert_to_numpy=True,).tolist()
        