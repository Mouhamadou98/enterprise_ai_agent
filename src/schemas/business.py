from datetime import date

from pydantic import BaseModel, Field

class Customer(BaseModel):
    customer_id: str
    name: str
    email: str
    segment: str
    city: str
    created_at: date
    account_status: str

class Order(BaseModel):
    order_id: str
    customer_id: str
    order_date: date
    status: str
    amount_eur: float
    currency: str
    carrier: str
    expected_delivery: date

class Delivery(BaseModel):
    delivery_id: str
    order_id: str
    carrier: str
    tracking_number: str
    status: str
    estimated_delivery: date
    actual_delivery: date | None
    last_location: str

class Incident(BaseModel):
    incident_id: str
    customer_id: str
    order_id: str
    type: str
    priority: str
    status: str
    created_at: date
    description: str

class Invoice(BaseModel):
    invoice_id: str
    order_id: str
    customer_id: str
    amount_eur: float
    status: str
    due_date: date

class OrderContext(BaseModel):
    customer: Customer
    order: Order
    delivery: Delivery | None
    order_incidents: list[Incident]
    invoice: Invoice | None
    customer_history: list[Incident]