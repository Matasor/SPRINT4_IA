SmartHub / ChargeGrid — Sprint 04
FIAP | Ciência da Computação — 2º semestre | Prompt and Artificial Intelligence | EV Challenge — GoodWe Brasil
Nota sobre o escopo: este README documenta a evolução experimental do projeto SmartHub/ChargeGrid para as funcionalidades trabalhadas nas aulas 11–14. O enunciado oficial da Sprint 04 não foi fornecido. Portanto, o texto não afirma requisitos, pontuação ou prazo oficial da Sprint 04.

Sobre o projeto
O SmartHub/ChargeGrid é um chatbot acadêmico voltado à mobilidade elétrica e à operação comercial de eletropostos, com integração conceitual ao contexto GoodWe. A Sprint 04 dá continuidade às versões anteriores ao explorar recuperação de documentos (RAG), seleção de ferramentas por agentes, roteamento de intenções, fluxos de estado e uma interface interativa.

Atenção: os dados do simulador são fictícios. Este projeto não se conecta a carregadores físicos, não realiza comando elétrico e não consulta telemetria operacional real da GoodWe.
Objetivos desta evolução
- Integrar a consulta a documentos locais por meio de RAG com ChromaDB e embeddings.
- Utilizar um agente com ferramentas especializadas: consulta documental, busca pública, cálculos e simulação acadêmica.
- Roteamento das perguntas entre caminhos de RAG, cálculo e conversa.
- Modelar um fluxo com LangGraph, memória por thread_id e pontos de revisão humana (HITL).
- Disponibilizar uma demonstração do chatbot em Gradio.
- Documentar requisitos e decisões usando Spec-Driven Development (SDD).
Tecnologias
- Python e LangChain / LangChain Ollama
- Ollama (modelo de linguagem e embeddings)
- ChromaDB para busca vetorial
- LangGraph (StateGraph, arestas condicionais e MemorySaver)
- Gradio para interface
- Pydantic v2, prompts estruturados e guardrails herdados da Sprint 03
- unittest para testes locais
Estrutura principal
SmartHub_Chatbot_DIGITAVEL_V2/
├── app.py                         # Aplicação original
├── app_lcel.py                    # Núcleo conversacional LCEL
├── gradio_ckp03.py                # Demonstração do agente em Gradio
├── modulo4/
│   ├── agent.py                   # Ferramentas e agente
│   ├── router.py                  # Roteamento de intenções
│   └── graph.py                   # Grafo de estado e HITL
├── CKP03_ChargeGrid_SmartHub.ipynb
├── Aula12_Router_ChargeGrid.ipynb
├── Aula13_LangGraph_ChargeGrid.ipynb
├── requirements.txt
├── requirements_aulas11_14.txt
├── spec.md                        # Requisitos e critérios de aceite
├── plan.md                        # Plano técnico
├── tasks.md                       # Tarefas de implementação
├── docs/                          # Documentação do projeto
├── prompts/                       # Prompts versionados
├── src/                           # Núcleo da Sprint 03
└── tests/
    └── test_modulo4.py
Instalação
Pré-requisitos: Python 3.11+, Ollama instalado e em execução. A conexão com a internet é necessária para baixar modelos e utilizar pesquisa pública.
1. Clone ou baixe o repositório e entre na pasta SmartHub_Chatbot_DIGITAVEL_V2.
2. Crie um ambiente virtual e instale as dependências:
python -m venv .venv
No Windows:
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pip install -r requirements_aulas11_14.txt
No Linux/macOS:
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -r requirements_aulas11_14.txt
3. Baixe os modelos de exemplo:
ollama pull qwen3:4b
ollama pull nomic-embed-text
Se os modelos ou o servidor Ollama forem diferentes, ajuste a configuração do projeto. Não publique chaves de API no repositório.
Executar a interface
Com o Ollama ativo:
python gradio_ckp03.py
Abra o endereço local exibido no terminal (normalmente http://127.0.0.1:7860). Para gerar um link público temporário de demonstração, no PowerShell:
$env:GRADIO_SHARE="true"
python gradio_ckp03.py
O link público só existe enquanto a aplicação estiver em execução. Não há uma URL pública permanente fornecida com o projeto.
Testes
Execute a partir da raiz do projeto:
python -m unittest discover -s tests -v
Os testes locais cobrem partes do roteamento, grafo e ferramentas. Testes que dependem do Ollama ou de acesso externo precisam ser executados no ambiente configurado; os resultados não devem ser declarados como aprovados sem execução.
Exemplos de interação
1. Documentos: “O que o projeto SmartHub implementa?”
2. Cálculo: “Quanto custa uma recarga de 35 kWh a R$ 1,20 por kWh?”
3. Pesquisa pública: “Quais são as novidades recentes sobre infraestrutura de recarga elétrica?”
4. Simulação: “Faça uma simulação acadêmica de recarga.”
Esses exemplos são casos de demonstração, não registros de respostas validadas.
Arquitetura de alto nível
Usuário → Interface Gradio → Guardrails → Agente/Roteador
                                         ├── RAG → Documentos + ChromaDB
                                         ├── Pesquisa pública
                                         ├── Calculadora segura
                                         └── Simulador acadêmico
                           └── LangGraph (fluxos de estado e HITL)
O agente e o fluxo LangGraph são componentes demonstrativos disponíveis no projeto; a representação acima é conceitual e não afirma que todos os caminhos são executados em um único pipeline de produção.
Segurança e limitações
- O chatbot deve evitar inventar especificações técnicas da GoodWe ou tratar dados simulados como leituras reais.
- Consultas sobre intervenções elétricas, temas jurídicos e financeiros sensíveis precisam ser encaminhadas a profissionais habilitados.
- O guardrail contra prompt injection é heurístico, portanto não é proteção infalível.
- O MemorySaver é volátil e não constitui armazenamento permanente de produção.
- O Gradio demonstra a resposta progressivamente depois que ela é obtida; não implementa streaming direto de tokens do modelo.
- Busca pública e bibliotecas de agentes dependem de serviços e versões externas e podem apresentar incompatibilidades.
Documentação complementar
- README_AULAS_11_14.md — instruções do complemento das aulas.
- spec.md — requisitos, escopo e aceite.
- plan.md — decisões e plano técnico.
- tasks.md — tarefas divididas em etapas.
- docs/ — documentação herdada do projeto, incluindo evolução da Sprint 03.
Equipe
Preencher com os dados reais da equipe antes da entrega:
Integrante	RM	Responsabilidade
A preencher	A preencher	A preencher


Status
Protótipo acadêmico. Há implementações e notebooks demonstrativos disponíveis; validações de ponta a ponta com Ollama, links públicos e resultados de avaliação precisam ser confirmados no ambiente de execução.
Licença
Consulte o arquivo LICENSE do repositório.
