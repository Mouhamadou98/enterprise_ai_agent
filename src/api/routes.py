# Importations des modules nécessaires
from fastapi import APIRouter, HTTPException, Depends

from src.schemas.chat import ChatRequest, ChatResponse
from src.services.acme_service import AcmeService
# from src.repositories.acme_repository import AcmeRepository
from src.schemas.business import OrderContext
from src.api.dependencies import get_service


router = APIRouter()

# repository = AcmeRepository()
# service = AcmeService(repository)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Endpoint pour gérer les requêtes de chat.
    
    Args:
        chat_request (ChatRequest): Requête contenant le message de l'utilisateur et éventuellement un identifiant de conversation.
    
    Returns:
        ChatResponse: Réponse contenant l'identifiant de la conversation, le message généré par l'IA et le statut de la réponse.
    """
    # Ici, vous pouvez ajouter la logique pour traiter le message de l'utilisateur,
    # interagir avec votre modèle d'IA, et générer une réponse appropriée.

    # Exemple de réponse simulée
    conversation_id = request.conversation_id or "conv-demo"
    response_message = f"Votre demande a bien été reçue"
    
    return ChatResponse(
        conversation_id=conversation_id,
        message=response_message,
        status="success"
    )

@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str, service: AcmeService = Depends(get_service)):
    """
    Endpoint pour récupérer les informations d'un client à partir de son identifiant.
    
    Args:
        customer_id (str): Identifiant du client.
    
    Returns:
        dict: Informations du client ou message d'erreur si le client n'est pas trouvé.
    """
    customer = service.get_customer(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=404, 
            detail="Customer not found"
        )
        
    return customer

@router.get("/orders/{order_id}")
async def get_order(order_id: str, service: AcmeService = Depends(get_service)):
    """
    Endpoint pour récupérer les informations d'une commande à partir de son identifiant.
    
    Args:
        order_id (str): Identifiant de la commande.
    
    Returns:
        dict: Informations de la commande ou message d'erreur si la commande n'est pas trouvée.
    """
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=404, 
            detail="Order not found"
        )
        
    return order

@router.get("/deliveries/{order_id}")
async def get_delivery(order_id: str, service: AcmeService = Depends(get_service)):
    """
    Endpoint pour récupérer les informations d'une livraison à partir de l'identifiant de la commande.
    
    Args:
        order_id (str): Identifiant de la commande.
    
    Returns:
        dict: Informations de la livraison ou message d'erreur si la livraison n'est pas trouvée.
    """
    delivery = service.get_delivery(order_id)
    if delivery is None:
        raise HTTPException(
            status_code=404, 
            detail="Delivery not found"
        )
        
    return delivery

@router.get("/customers/{customer_id}/incidents")
async def get_customer_incidents(customer_id: str, service: AcmeService = Depends(get_service)):
    """
    Récupère les incidents associés à un client.

    Args:
        customer_id: Identifiant du client.

    Returns:
        Liste des incidents du client, ou None si le client n'existe pas.
    """
    incidents = service.get_customer_incidents(customer_id)
    if incidents is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )
        
    return incidents

@router.get("/orders/{order_id}/context", response_model=OrderContext)
def get_order_context(order_id: str, service: AcmeService = Depends(get_service)):
    """
    Récupère le contexte complet d'une commande, y compris les informations sur le client, la commande et la livraison.

    Args:
        order_id: Identifiant de la commande.

    Returns:
        Dictionnaire contenant les informations du client, de la commande, de la livraison, des incidents et des factures.
        Retourne None si la commande n'existe pas.
    """
    context = service.get_order_context(order_id)
    if context is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )
        
    return context
