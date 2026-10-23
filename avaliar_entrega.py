"""Executa as evidências da Sprint 03 e atualiza o relatório final."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

from src.ollama_client import OllamaClient, OllamaError


def run_step(title, *args):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)
    completed = subprocess.run([sys.executable, *args])
    if completed.returncode:
        raise SystemExit(f"Etapa interrompida: {title}")


def main():
    parser = argparse.ArgumentParser(description="Avaliação completa SmartHub Sprint 03")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "qwen3:4b"))
    parser.add_argument("--second-model", default=None)
    parser.add_argument("--skip-human", action="store_true")
    args = parser.parse_args()

    try:
        installed = OllamaClient(model=args.model, timeout=10).installed_models()
    except OllamaError as exc:
        raise SystemExit(str(exc))
    if args.model not in installed:
        raise SystemExit(f"Modelo principal {args.model!r} ausente. Instalados: {installed}")
    second = args.second_model or next((name for name in installed if name != args.model), None)

    run_step("1/8 - Testes automatizados", "-m", "unittest", "discover", "-s", "tests", "-v")
    run_step("2/8 - Avaliação offline dos guardrails", "-m", "evals.run_evals")
    run_step("3/8 - Baseline reconstruída x LCEL", "-m", "evals.compare_architecture", "--model", args.model)
    run_step("4/8 - Saída estruturada Pydantic", "-m", "evals.run_structured_evals", "--model", args.model)
    run_step("5/8 - Prompt v1 x v2", "-m", "evals.compare_prompts", "--model", args.model)

    if second:
        run_step("6/8 - Comparação entre dois modelos", "-m", "evals.benchmark_models",
                 "--models", args.model, second)
    else:
        print("\n6/8 - Comparação entre modelos pendente: só há um modelo instalado.")
        print("Execute baixar_segundo_modelo.bat e rode esta avaliação novamente.")

    if not args.skip_human:
        run_step("7/8 - Revisão humana guiada", "-m", "evals.review_human")
    else:
        print("\n7/8 - Revisão humana ignorada por --skip-human.")
    run_step("8/8 - Consolidação e relatório PDF", "-m", "evals.finalize")

    print("\nAVALIAÇÃO CONCLUÍDA")
    print("Relatório atualizado: docs\\relatorio_evolucao.pdf")
    if not second:
        print("Ainda falta instalar um segundo modelo e repetir para preencher essa comparação.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
