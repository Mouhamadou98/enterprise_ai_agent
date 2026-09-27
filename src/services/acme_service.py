# Importations des modules nécessaires
from src.repositories.acme_repository import AcmeRepository

class AcmeService:

    """
        Le Service est responsable de :
            « Comment traiter les données ? » 
    """

    def __init__(self, repository: AcmeRepository):
        self.repository = repository

    def get_customer(self, customer_id: str):
        """
        Récupère les informations d'un client à partir de son identifiant.
        """
        return self.repository.get_customer(customer_id)

    def get_order(self, order_id: str):
        """
        Récupère les informations d'une commande à partir de son identifiant.
        """
        return self.repository.get_order(order_id)

    def get_delivery(self, order_id: str):
        """
        Récupère les informations d'une livraison à partir de son identifiant.
        """
        return self.repository.get_delivery(order_id)

    def get_customer_incidents(self, customer_id: str):
        """
        Récupère les informations d'incidents pour un client à partir de son identifiant.
        """
        customer = self.repository.get_customer(customer_id)

        if customer is None:
            return None
        return self.repository.get_customer_incidents(customer_id)
    
    def get_order_context(self, order_id: str):
        """
        Récupère le contexte métier complet d'une commande.

        Le contexte comprend :
        - les informations du client ;
        - les informations de la commande ;
        - les informations de livraison ;
        - les incidents liés à la commande ;
        - la facture associée ;
        - l'historique des incidents du client.
        """
        order = self.repository.get_order(order_id)
        if order is None:
            return None

        customer = self.repository.get_customer(order['customer_id'])
        if customer is None:
            return None
        
        delivery = self.repository.get_delivery(order_id)
        order_incidents = self.repository.get_order_incidents(order_id)
        invoice = self.repository.get_invoice(order_id)
        customer_history = self.repository.get_customer_incidents(order['customer_id'])

        context = {
            "customer": customer,
            "order": order,
            "delivery": delivery,
            "order_incidents": order_incidents,
            "invoice": invoice,
            "customer_history": customer_history
        }

        return context