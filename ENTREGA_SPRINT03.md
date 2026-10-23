# ENTREGA — FIAP × GoodWe | Sprint 03 (2026.2)

## Produto
SmartHub Assistant / ChargeGrid Intelligence, continuação do chatbot das Sprints 1 e 2.
Esta entrega implementa o **Módulo 1 (aulas 01–04)**, como exige o documento da Sprint 03. O material de aulas 11–14 **não** é parte obrigatória desta avaliação.

## Correspondência com a rubrica

| Bloco | Evidência no repositório | Situação |
|---|---|---|
| A — 40 pontos: LCEL | `src/chain/builder.py`, `src/chain/service.py` | Código entregue; validação real do Ollama pendente |
| A — memória/sessões | `src/chain/memoria.py`, `tests/` | Implementado; teste integrado com modelo falso |
| A — Pydantic v2 | `src/schemas/consulta_recarga.py` | Implementado e testado |
| B — 25 pontos: prompts | `prompts/system_prompt_v1.md`, `system_prompt_v2.md`, `prompts/README.md` | Versionados; ganho numérico pendente |
| B — comparação de modelos | `docs/relatorio_modelos.md`, `evals/benchmark_models.py` | Protocolo implementado; medições reais pendentes |
| C — 15 pontos: guardrails | `src/guardrails/`, `evals/offline_guardrails.json` | Implementados com testes offline |
| D — 20 pontos: avaliação | `evals/`, `docs/relatorio_evolucao.pdf` | Material entregue; comparação com medições reais pendente |
| Bônus +1 | Multi-provider (dois provedores distintos) | Não implementado/não reivindicado |

## Executar no Windows

1. Instale o Python 3.10+ e Ollama.
2. No terminal, execute `ollama pull qwen3:4b`.
3. Abra `INICIAR_CHATBOT.bat` ou execute `python -m pip install -r requirements.txt` e `python app.py --model qwen3:4b`.
4. Rode `baixar_segundo_modelo.bat` e `executar_avaliacao_completa.bat`. A última etapa mede desempenho, compara arquiteturas, modelos, prompts e produz o PDF atualizado.
5. Confira `docs/relatorio_evolucao.pdf` (máximo 5 páginas) e as evidências JSON.

## Observações para a entrega oficial

- **Não inventar medições**: campos N/D indicam que não houve teste real do Ollama no ambiente atual. Checks offline e testes com modelo falso não provam qualidade de respostas em produção.
- **Comparativo histórico**: o baseline com Ollama é *reconstruído* a partir do código legado; não equivale a nova execução histórica do Gemini da Sprint 2.
- **Time**: nomes e RMs em `integrantes.txt` foram preservados; turma, atribuições efetivas na Sprint 03 e commits devem ser confirmados pelos participantes.
- **GitHub**: a publicação em repositório público e os commits individuais são atos externos que o ZIP não comprova. Entregar URL do repositório e `integrantes.txt`.
- **Segurança**: exemplo de ambiente sem chaves; não subir `.env`. Se houve credencial exposta antes, revogá-la.
