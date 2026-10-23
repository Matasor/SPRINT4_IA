# SmartHub Assistant - ChargeGrid Intelligence | Sprint 03

Projeto acadêmico FIAP x GoodWe Brasil (2026.2). O chatbot atende o **operador comercial de eletropostos**, usa Ollama local e executa a arquitetura exigida com LangChain LCEL.

## Abrir o chatbot no Windows

1. Instale o [Python 3.10 ou superior](https://www.python.org/downloads/) e marque **Add Python to PATH**.
2. Instale o [Ollama](https://ollama.com/) e confirme que ele está aberto.
3. No PowerShell, instale o modelo: `ollama pull qwen3:4b`.
4. Dê dois cliques em **`INICIAR_CHATBOT.bat`**.

Na primeira abertura, o projeto cria `.venv` e instala as dependências. Aguarde a janela preta concluir a instalação; a janela gráfica será aberta automaticamente. Depois, clique no campo branco **Sua pergunta**, escreva e pressione **Enter**. O campo permanece liberado durante a geração da resposta.

Se preferir o terminal:

```powershell
python -m pip install -r requirements.txt
python app.py --model qwen3:4b
```

Comandos do terminal: `/simular`, `/limpar` e `/sair`.

## O que está implementado

- Interface gráfica Tkinter com envio por Enter, histórico, limpeza e simulação acadêmica.
- Pipeline principal `ChatPromptTemplate | ChatOllama | StrOutputParser` em LCEL.
- Memória separada por `session_id` com `RunnableWithMessageHistory` e `ConversationTokenBufferMemory`.
- Extração estruturada com Pydantic v2 e `field_validator`.
- Prompt v1 preservado e prompt v2 estruturado com XML tagging.
- Guardrails determinísticos antes do modelo: escopo, prompt injection, risco elétrico, telemetria, concorrentes e temas jurídicos/financeiros.
- Avaliações T01-T10, baseline reconstruída, comparação v1/v2, comparação entre modelos, saída estruturada, revisão humana guiada e relatório PDF.
- Simulador acadêmico explicitamente identificado como fictício; não há acesso a IoT, painel GoodWe, pagamentos ou telemetria real.

## Arquitetura

```text
interface.py ou app.py
        |
        v
guardrails determinísticos
        |
        v
prompt XML + histórico por sessão
        |
        v
ChatOllama (LCEL) -> StrOutputParser -> resposta

Pipeline estruturado separado:
prompt -> ChatOllama -> PydanticOutputParser -> ConsultaRecarga
```

O `qwen3:4b` foi adotado por ser compatível com execução local no computador do grupo. O modelo `gpt-oss:120b` citado como possibilidade no material é grande demais para uma demonstração local prática em notebook com RTX 4050. O modelo continua configurável por `--model` ou na própria interface.

## Gerar todas as evidências reais

Os números de latência, tokens proxy e qualidade do modelo dependem do hardware e do Ollama do grupo. Para não inventar resultados, o ZIP contém um fluxo automatizado que coleta tudo no computador da apresentação.

1. Dê dois cliques em **`baixar_segundo_modelo.bat`** uma vez.
2. Dê dois cliques em **`executar_avaliacao_completa.bat`**.
3. Leia as respostas exibidas e marque `s` ou `n` na revisão humana T01-T10.

Esse processo:

1. executa os testes automatizados;
2. valida os guardrails offline;
3. compara baseline reconstruída x LCEL com o mesmo modelo;
4. mede a saída estruturada Pydantic;
5. compara prompts v1 x v2;
6. compara `qwen3:4b` com `qwen3:1.7b`;
7. coleta a avaliação humana sem editar CSV manualmente;
8. atualiza `docs/relatorio_evolucao.md` e `docs/relatorio_evolucao.pdf`.

O processo pode demorar porque realiza várias inferências locais. Ele nunca substitui valores ausentes por métricas fictícias.

Comando equivalente:

```powershell
python avaliar_entrega.py --model qwen3:4b --second-model qwen3:1.7b
```

## Testes rápidos

```powershell
python -m unittest discover -s tests -v
python -m evals.run_evals
```

Os testes de integração utilizam um `FakeChatModel` apenas para provar o encadeamento LCEL, a memória em três turnos e o isolamento de sessões sem depender de rede. As avaliações de conteúdo usam o Ollama real.

## Arquivos principais

```text
interface.py                       interface gráfica funcional
app.py                             interface de terminal LCEL
INICIAR_CHATBOT.bat                atalho principal para abrir o chatbot
abrir_interface.bat                instalação inicial + abertura silenciosa da GUI
avaliar_entrega.py                 fluxo completo de avaliação
src/chain/                         LCEL, memória e serviço
src/schemas/consulta_recarga.py    schema Pydantic v2
src/guardrails/                    regras de segurança e escopo
prompts/                           versões v1 e v2
evals/                             testes T01-T10 e comparações
docs/relatorio_evolucao.pdf        relatório de até cinco páginas
historico_sprint2/                 material original preservado
```

## Segurança e entrega

- Nenhuma chave de API é necessária: a execução usa Ollama local.
- `.env` e ambientes virtuais estão ignorados pelo Git.
- Nunca coloque credenciais reais em `.env.example`, código, ZIP ou repositório.
- O arquivo original recebido continha valores com aparência de credenciais em `.env.example`; eles foram removidos. Por segurança, os responsáveis devem **revogar e recriar essas chaves** nos provedores correspondentes.
- Antes da entrega, publique o repositório, confira a turma, confirme a divisão real do trabalho e os commits de cada integrante. O ZIP não pode produzir essas evidências externas sozinho.

Consulte também `docs/roteiro_video.md`, `docs/mapa_integracao.md` e `docs/relatorio_modelos.md`.
