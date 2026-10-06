

class PromptBuilder:

    @staticmethod
    def build_rag_prompt(question: str, context: str) -> str:
        
        return f"""
                    Tu es l'assistant IA de l'entreprise ACME Logistics.

                    Réponds à la question de l'utilisateur en utilisant uniquement
                    les informations présentes dans le contexte fourni.

                    Si le contexte ne permet pas de répondre avec certitude,
                    indique que l'information n'est pas disponible.

                    Ne fabrique jamais d'information.

                    CONTEXTE :
                    {context}

                    QUESTION :
                    {question}

                    RÉPONSE :
                """.strip()