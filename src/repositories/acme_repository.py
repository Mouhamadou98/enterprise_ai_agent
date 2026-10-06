# Importations des modules nécessaires
from pathlib import Path
import json 
from datetime import datetime

import pandas as pd

DATA_DIR = Path("data/acme_logistics")

class AcmeRepository:

    """
        Le Repository est responsable de :
            « Comment récupérer les données ? » 
    """

    def __init__(self):
        self.customers = pd.read_csv(DATA_DIR / "customers.csv")
        self.orders = pd.read_csv(DATA_DIR / "orders.csv")
        self.deliveries = pd.read_csv(DATA_DIR / "deliveries.csv")
        self.incidents = pd.read_csv(DATA_DIR / "incidents.csv")
        self.invoices = pd.read_csv(DATA_DIR / "invoices.csv")
        self.tickets = pd.read_csv(DATA_DIR / "tickets.csv")

    def get_customer(self, customer_id: str):
        """
        Récupère les informations d'un client à partir de son identifiant.
        """
        results = self.customers[self.customers['customer_id'] == customer_id]
        if results.empty:
            return None
        
        return results.iloc[0].to_dict()
    
    def get_order(self, order_id: str):
        """
        Récupère les informations d'une commande à partir de son identifiant.
        """
        results = self.orders[
            self.orders['order_id'] == order_id
        ]
        if results.empty:
            return None
        
        return results.iloc[0].to_dict()
    
    def get_delivery(self, order_id: str):
        """
        Récupère les informations d'une livraison à partir de son identifiant.
        """
        results = self.deliveries[
            self.deliveries['order_id'] == order_id
        ]
        if results.empty:
            return None
        
        # return results.iloc[0].to_dict()
        return json.loads(results.iloc[[0]].to_json(orient="records", date_format="iso"))[0]
    
    def get_customer_incidents(self, customer_id: str):
        """
        Récupère les informations d'incidents pour un client à partir de son identifiant.
        """
        results = self.incidents[
            self.incidents['customer_id'] == customer_id
        ]
        # if results.empty:
        #     return None
        
        return results.to_dict(orient="records")
    
    def get_order_incidents(self, order_id: str):
        """
        Récupère les informations d'incidents pour une commande à partir de son identifiant.
        """
        results = self.incidents[
            self.incidents["order_id"] == order_id
        ]

        return results.to_dict(orient="records")
    
    def get_invoice(self, order_id: str):
        """
        Récupère les informations d'une facture à partir de la commande.
        """
        results = self.invoices[
            self.invoices['order_id'] == order_id
        ]
        if results.empty:
            return None
        
        return results.iloc[0].to_dict()

    def create_ticket(self, customer_id: str, order_id: str, incident_id: str, subject: str, priority: str = "MEDIUM") -> dict:
        
        ticket = {
        "ticket_id": f"TKT{len(self.tickets) + 1:05d}",
        "customer_id": customer_id,
        "order_id": order_id,
        "incident_id": incident_id,
        "subject": subject,
        "priority": priority,
        "status": "OPEN",
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        }


        self.tickets = self.tickets._append(ticket, ignore_index=True)

        return ticket
