# ACME Logistics — Enterprise AI Agent

Enterprise AI Agent built with Python to orchestrate business tools, RAG and LLMs for enterprise use cases.

The project simulates an enterprise environment combining CRM, ERP and internal knowledge management systems.

The objective is to build an AI agent capable of understanding complex business requests, retrieving enterprise information, consulting internal procedures and eventually executing controlled business actions.

---

## 🎯 Project Objective

The agent is designed to handle requests such as:

> "Que se passe-t-il avec la commande ORD001 de Jean Dupont ?  
> Le client a-t-il déjà signalé un problème et quelle procédure devons-nous appliquer ?"

The agent should be able to:

1. Retrieve business information from the ERP/CRM.
2. Search internal documentation.
3. Combine structured and unstructured information.
4. Use LLM reasoning to produce a contextual answer.
5. Call business tools when necessary.
6. Execute controlled actions such as ticket creation.
7. Apply security and governance rules before sensitive actions.

---

## 🏗️ Architecture

Current architecture:

```text
                         User
                           │
                           ▼
                       FastAPI API
                           │
                           ▼
                    Tool Calling Agent
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
             LLM                     Tools
              │                         │
       ┌──────┴──────┐          ┌───────┴────────┐
       │             │          │                │
    Ollama        Future      Business        RAG
                  Providers     Tools          Tools
                                  │                │
                                  ▼                ▼
                              Services       Elasticsearch
                                  │
                                  ▼
                              Repository
                                  │
                                  ▼
                              CSV Data


The project uses an abstraction layer around LLM providers so that the agent is not directly coupled to Ollama.

🚀 Current Features
LLM abstraction
The project defines a common LLMService interface supporting:
- Text generation
- Tool calling
Current provider:
- Ollama
The architecture is designed to support additional providers such as:
- OpenAI
- Mistral
- Gemini
without coupling the agent to a specific provider.

🔧 Business Tools
The agent currently exposes the following tools:
get_order
get_delivery
get_customer_incidents
search_knowledge_base
create_ticket

Tools are implemented using LangChain's @tool decorator.
@tool
def get_delivery(order_id: str) -> dict | None:
    """Retrieve delivery information for an order from the ACME Logistics ERP."""
    return service.get_delivery(order_id)


The LLM does not directly access the database.

LLM
 ↓
Tool Call
 ↓
Tool Executor
 ↓
Business Service
 ↓
Repository

This separation allows business operations to be controlled and validated independently from the LLM.

🔎 RAG Pipeline
The project implements a Retrieval-Augmented Generation pipeline for internal enterprise documentation.

Markdown Documents
        │
        ▼
Document Loader
        │
        ▼
Text Chunking
        │
        ▼
Multilingual Embeddings
        │
        ▼
Elasticsearch
        │
        ├── Vector Search
        │
        └── BM25 Keyword Search
                │
                ▼
           RRF Fusion
                │
                ▼
          Retrieved Context
                │
                ▼
              LLM

Documents
The knowledge base contains synthetic enterprise documentation covering topics such as:
- Delivery policies
- Refund policies
- Commercial gestures
- Ticket creation
- Escalation procedures
- Billing policies
- Data protection
- Agent usage policies
- Return policies
- Service levels

🧠 LLM + RAG
The RAG pipeline can be combined with the LLM:
User Question
      │
      ▼
Retriever
      │
      ├── Vector Search
      └── BM25
      │
      ▼
RRF Fusion
      │
      ▼
Relevant Context
      │
      ▼
Prompt Builder
      │
      ▼
LLM
      │
      ▼
Answer

The prompt instructs the model to use only the retrieved context and avoid fabricating information.

🗄️ Enterprise Data
The project uses a synthetic ACME Logistics dataset.
It simulates:
CRM
 └── Customers
 └── Incidents

ERP
 └── Orders
 └── Deliveries
 └── Invoices

Support
 └── Tickets

GED / Knowledge Base
 └── Internal Markdown documentation

🧪 Testing
The project currently contains automated tests covering:
- Repository
- Services
- RAG loader
- Document splitting
- Embeddings
- Elasticsearch client
- Indexing
- Retrieval
- RRF fusion
- LLM abstraction
- LLM factory
- RAG + LLM
- Business tools
- Tool calling
- Tool execution

Run the complete test suite:
uv run pytest

Current status:
34 passed

⚙️ Installation
Requirements
Python 3.11+
uv
Docker
Ollama
Elasticsearch

Install dependencies
uv pip install -r requirements.txt

Configure environment
Create a .env file:

LLM_PROVIDER=ollama

OPENAI_API_KEY=
MISTRAL_API_KEY=
GEMINI_API_KEY=

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

ELASTICSEARCH_URL=http://localhost:9200

🦙 Ollama
Install and start Ollama.
Pull the model:
ollama pull llama3.2
ollama list

🔎 Elasticsearch
Start Elasticsearch:
docker run -d \
  --name acme-elasticsearch \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "xpack.license.self_generated.type=trial" \
  -v acme-elasticsearch-data:/usr/share/elasticsearch/data \
  docker.elastic.co/elasticsearch/elasticsearch:9.5.4

Verify:
curl http://localhost:9200

📚 Index the Knowledge Base
uv run python -m scripts.index_knowledge_base

▶️ Run the API
Start FastAPI:
uv run uvicorn src.main:app --reload

API documentation:(swagger)
http://localhost:8000/docs

🤖 Test Tool Calling 
Run:
uv run python -m scripts.test_tool_calling
This verifies that the LLM can identify and request a business tool.

🔄 Test the Agent
Run:
uv run python -m scripts.test_agent

This verifies the complete:  LLM → Tool → Tool Result → LLM  workflow.


🛣️ Roadmap

The project is being developed incrementally toward a production-oriented enterprise AI agent.
Completed

Completed
- [v] FastAPI foundation
- [v] Repository / Service architecture
- [v] Synthetic CRM / ERP dataset
- [v] RAG pipeline
- [v] Elasticsearch vector search
- [v] BM25 keyword search
- [v] RRF hybrid retrieval
- [v] LLM abstraction
- [v] Ollama integration
- [v] LangChain tools
- [v] Business tools
- [v] Tool calling
- [v] Tool executor
- [v] LLM → Tool → LLM loop
- [v] Automated tests
In progress / Planned
- [ ] LangGraph agent orchestration
- [ ] Agent state management
- [ ] Multi-step tool execution
- [ ] Conversation memory
- [ ] Human-in-the-Loop
- [ ] Tool permissions and authorization
- [ ] MCP integration
- [ ] Langfuse observability
- [ ] Prometheus / Grafana metrics
- [ ] Kafka event-driven workflows
- [ ] Security and governance
- [ ] PII protection
- [ ] Dockerization
- [ ] Kubernetes deployment
- [ ] CI/CD
- [ ] End-to-end tests
- [ ] Multi-provider production integrations
- [ ] Production deployment architecture