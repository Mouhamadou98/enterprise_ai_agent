Fast APi et Pydantic

ChatRequest
     ↓
┌─────────────────┐
│ message         │
│ conversation_id │
└─────────────────┘
     ↓
   Agent
     ↓
ChatResponse
┌─────────────────┐
│ conversation_id │
│ message         │
│ status          │
└─────────────────┘

Pourquoi commencer par la commande ?

Parce que la commande nous donne le :

Order
  │
  ├── customer_id ──→ Customer
  │                       │
  │                       └──→ Incidents
  │
  ├── order_id ─────→ Delivery
  │
  └── order_id ─────→ Invoice
