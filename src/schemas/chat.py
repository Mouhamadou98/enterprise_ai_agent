# Importation des modules nécessaires
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Modèle de requête pour l'API de chat.
    Attributes:
        message (str): Message envoyé par l'utilisateur.
        conversation_id (str | None): Identifiant de la conversation.
    """

    message: str = Field(
        ..., 
        min_length=1, # Une requeête vide n'est pas autorisée
        description="Message envoyé par l'utilisateur."
    )
    conversation_id: str | None = Field(
        default=None, 
        description="Identifiant de la conversation."

        # Note de rappel : L'identifiant de conversation est facultatif : 
        # Pourquoi ?
        # Parce que lors du premier message, l'utilisateur n'a peut-être pas encore de conversation. 
        # Plus tard, notre système pourra générer automatiquement cet ID.
    )

class ChatResponse(BaseModel):
    
    conversation_id: str
    message: str
    status: str