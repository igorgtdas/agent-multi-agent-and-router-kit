# langchain-multi-agent-creator

Templates e estrutura minima para criar novos sistemas de agentes.

## Estrutura
- `templates/agents/`: templates de agentes e roteadores
- `templates/tools/`: templates de tools
- `core/` e `tools/`: base minima usada pelos templates
- `chat/`: exemplo de chat para orquestrar via RouterAgent

## Como usar
1) Copie o template desejado para o seu projeto em `agents/` ou `tools/`.
2) Ajuste o `SYSTEM_PROMPT` e o `ResponseFormat`.
3) Registre tools no agente e atualize o roteador (se aplicavel).
4) Copie `chat/chat.py` para seu projeto e ajuste os imports dos agentes.

## Integracao do chat
O `chat/chat.py` assume que existe um `agents/router_agent.py` com `route_and_run`.
Para integrar:
1) Crie seus agentes em `agents/` usando os templates.
2) Garanta que o `RouterAgent` mapeia os agentes no `ROUTE_TO_AGENT`.
3) Rode:
```
python -m chat.chat
```

## Dependencias (recomendado)
```
python -m pip install langchain langgraph langchain-openai langsmith python-dotenv
```
