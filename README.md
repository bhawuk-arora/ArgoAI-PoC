## 🌊 Argo AI: Conversational Ocean Data Explorer

### Project Goal

**Democratizing Oceanographic Data:** Argo AI transforms complex, heterogeneous oceanographic datasets (NetCDF, Argo floats) into an intuitive, accessible conversational interface. It eliminates the need for specialized coding/domain knowledge, allowing researchers and stakeholders to query, explore, and visualize ocean data using **Natural Language**.

---

### 💡 Key Innovation: Intelligent Hybrid Query (RAG + SQL)

The core innovation is an **AI-powered Query Router** that intelligently routes a natural language question to the most efficient backend tool, all accessible via a single **`/query`** endpoint.

| Query Type | Tool Used | Technical Implementation | Purpose |
| :--- | :--- | :--- | :--- |
| **Contextual/Similarity** | **Semantic Search (RAG)** | Sentence Transformers + FAISS Vector Store | Answering descriptive questions like "Find profiles similar to an Arctic deep dive." |
| **Quantitative/Aggregate** | **NL-to-SQL Translation** | LLM Tool-Use (Simulated) + Pandas/Synapse Mock | Answering numerical questions like "What is the average temperature at 200m?" |

This hybrid approach ensures **high accuracy** (using precise SQL for metrics) and **high recall** (using RAG for complex contextual search), delivered through live, interactive visualizations.

---

### 🌐 Scalable Architecture (The Future Vision)

This prototype is built upon a foundation designed for petabyte-scale, real-time data ingestion, aligning with modern cloud data practices:

1.  **Ingestion Layer:** Handles both **NetCDF Batch Files** (via ADLS/Autoloader) and **Real-time Argo Telemetry** (via Event Hub/Structured Streaming).
2.  **Data Lakehouse:** Uses **Databricks Delta Lake** (Bronze, Silver, Gold Layers) for scalable, reliable ETL.
3.  **Unified Query Layer:** Data is served from the Gold layer to two distinct endpoints:
    * **Azure Synapse Analytics:** For high-speed SQL queries (used by NL-to-SQL).
    * **Vector Database (FAISS/Pinecone):** Stores vector embeddings for contextual search (used by Semantic Search).
4.  **FastAPI Agent:** The intelligent orchestration layer that determines the user's intent and executes the correct query tool.

