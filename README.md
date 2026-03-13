# langchain-multi-agent-creator

Templates e estrutura minima para criar novos sistemas de agentes com roteamento.

Templates and minimal structure to create new router-based agent systems.

---

## PT-BR

### Visao geral
Este repositorio oferece uma base minima para:
- criar agentes e roteadores a partir de templates;
- organizar tools e observabilidade;
- integrar um chat simples com roteamento.

### Estrutura
- `templates/agents/`: templates de agentes e roteadores
- `templates/tools/`: templates de tools
- `core/` e `tools/`: base minima usada pelos templates
- `chat/`: exemplo de chat para orquestrar via RouterAgent
- `api/`: exemplo de API FastAPI com RouterAgent como entrypoint

### Como usar os templates
1) Copie o template desejado para o seu projeto em `agents/` ou `tools/`.
2) Ajuste o `SYSTEM_PROMPT` e o `ResponseFormat`.
3) Registre tools no agente e atualize o roteador.
4) Copie `chat/chat.py` para seu projeto e ajuste os imports dos agentes.

### Boas praticas de organizacao
- Crie uma pasta `agents/` para seus agentes e uma pasta `tools/` para suas tools.
- Use o prefixo `tool_` no nome das tools (ex: `tool_search`, `tool_sql_query`).
- Centralize o roteamento no `RouterAgent` e mantenha o mapeamento `ROUTE_TO_AGENT` atualizado.
- Evite logica de IO dentro dos agentes; delegue para tools dedicadas.
- Garanta que o RouterAgent seja a unica porta de entrada em CLI, chat e API.

### Guia rapido: como construir um agente
1) Crie o arquivo do agente em `agents/` a partir de um template.
2) Escreva o `SYSTEM_PROMPT` com objetivo, limites e formato esperado.
3) Defina o `ResponseFormat` para padronizar a saida.
4) Registre as tools relevantes no agente.
5) Adicione o agente ao `RouterAgent` e atualize o roteamento.

### Executar o exemplo
O `chat/chat.py` recebe o agente instanciado pelo entrypoint.
Isso garante que o RouterAgent seja sempre o primeiro a rodar.

Para rodar via CLI:
```
python main.py
```

Para rodar via API (FastAPI):
```
uvicorn api.app:app --reload
```

Endpoint:
- `POST /chat` usa exclusivamente `RouterAgent.route_and_run()`
- Header obrigatório: `X-API-Key` (valor definido em `API_KEY`)

### Dependencias (recomendado)
```
python -m pip install langchain langgraph langchain-openai langsmith python-dotenv
```

### Sugestao de projeto basico (apenas em Markdown)
**Projeto: Assistente de suporte interno**

**Objetivo:** responder perguntas de colaboradores sobre processos internos.

**Agentes sugeridos:**
- `agents/support_agent.py`: responde perguntas gerais.
- `agents/policy_agent.py`: responde sobre politicas e compliance.
- `agents/router_agent.py`: roteia para o agente correto.

**Tools sugeridas:**
- `tools/tool_kb_search.py`: busca em base de conhecimento.
- `tools/tool_policy_lookup.py`: consulta politicas.

**Fluxo proposto:**
1) Usuario pergunta.
2) RouterAgent classifica a intencao.
3) Agente especializado responde usando tools.
4) Resposta padronizada com `ResponseFormat`.

**Proximos passos:**
- Definir fontes de dados (Docs internos, FAQ, Confluence).
- Criar logs e metricas basicas.
- Adicionar testes unitarios para tools.

---

## EN

### Overview
This repository provides a minimal base to:
- create agents and routers from templates;
- organize tools and observability;
- integrate a simple routed chat.

### Structure
- `templates/agents/`: agent and router templates
- `templates/tools/`: tool templates
- `core/` and `tools/`: minimal base used by templates
- `chat/`: chat example orchestrated by RouterAgent
- `api/`: FastAPI example with RouterAgent as entrypoint

### How to use the templates
1) Copy the desired template into `agents/` or `tools/`.
2) Adjust `SYSTEM_PROMPT` and `ResponseFormat`.
3) Register tools in the agent and update the router.
4) Copy `chat/chat.py` into your project and fix imports.

### Best practices
- Create an `agents/` folder for agents and a `tools/` folder for tools.
- Use the `tool_` prefix for tool names (e.g., `tool_search`, `tool_sql_query`).
- Keep routing centralized in `RouterAgent` and maintain `ROUTE_TO_AGENT`.
- Avoid IO logic inside agents; delegate to dedicated tools.
- Ensure RouterAgent is the single entrypoint for CLI, chat, and API.

### Quick guide: build an agent
1) Create the agent file in `agents/` from a template.
2) Write the `SYSTEM_PROMPT` with goal, limits, and expected format.
3) Define `ResponseFormat` to standardize output.
4) Register relevant tools in the agent.
5) Add the agent to `RouterAgent` and update routing.

### Run the example
`chat/chat.py` receives the agent instantiated by the entrypoint.
This guarantees RouterAgent runs first.

Run via CLI:
```
python main.py
```

Run via API (FastAPI):
```
uvicorn api.app:app --reload
```

Endpoint:
- `POST /chat` uses only `RouterAgent.route_and_run()`
- Required header: `X-API-Key` (value set in `API_KEY`)

### Dependencies (recommended)
```
python -m pip install langchain langgraph langchain-openai langsmith python-dotenv
```

### Basic project suggestion (Markdown only)
**Project: Internal support assistant**

**Goal:** answer employee questions about internal processes.

**Suggested agents:**
- `agents/support_agent.py`: handles general questions.
- `agents/policy_agent.py`: handles policy and compliance.
- `agents/router_agent.py`: routes requests to the right agent.

**Suggested tools:**
- `tools/tool_kb_search.py`: knowledge base search.
- `tools/tool_policy_lookup.py`: policy lookup.

**Proposed flow:**
1) User asks a question.
2) RouterAgent classifies intent.
3) Specialized agent responds using tools.
4) Response standardized via `ResponseFormat`.

**Next steps:**
- Define data sources (internal docs, FAQ, Confluence).
- Add basic logging and metrics.
- Add unit tests for tools.
