"""Entrada oficial Sprint 03: LCEL por padrão. --demo não requer dependências."""
import argparse
import json
from src.simulator import Simulation
from src.ollama_client import OllamaClient, OllamaError


def main(argv=None):
    parser = argparse.ArgumentParser(description='SmartHub Assistant | Sprint 03 LCEL')
    parser.add_argument('--model', default='qwen3:4b')
    parser.add_argument('--session', default='operador-demo')
    parser.add_argument('--prompt-version', choices=['v1', 'v2'], default='v2')
    parser.add_argument('--demo', action='store_true', help='simulação ilustrativa, sem IA')
    args = parser.parse_args(argv)
    simulation = Simulation().run()
    if args.demo:
        print(json.dumps(simulation, ensure_ascii=False, indent=2))
        return 0
    try:
        from src.chain import LCELAssistant
    except ImportError as exc:
        print('Faltam dependências OBRIGATÓRIAS da Sprint 03. Instale: pip install -r requirements.txt')
        print('Detalhe:', exc)
        return 1
    try:
        installed = OllamaClient(model=args.model).installed_models()
    except OllamaError as exc:
        print('Ollama inacessível:', exc)
        return 1
    if args.model not in installed:
        print(f'Modelo {args.model!r} ausente. Instalados: {installed}. Use --model com o nome exato de ollama list.')
        return 1
    try:
        bot = LCELAssistant(model=args.model, prompt_version=args.prompt_version)
    except ImportError as exc:
        print('Dependências LangChain obrigatórias ausentes. Execute: python -m pip install -r requirements.txt')
        print('Detalhe:',exc)
        return 1
    print('SmartHub Assistant | Operador COMERCIAL | Sprint 03 LangChain LCEL')
    print('Comandos: /simular (dados fictícios), /limpar, /sair')
    while True:
        try:
            question = input('Operador: ').strip()
        except (EOFError, KeyboardInterrupt):
            return 0
        if question.lower() in ('/sair', 'sair'):
            return 0
        if question == '/simular':
            print(json.dumps(simulation, ensure_ascii=False, indent=2))
            continue
        if question == '/limpar':
            bot.clear(args.session)
            print('Histórico da sessão apagado.')
            continue
        if not question:
            continue
        try:
            answer, _outcome = bot.reply(question, args.session)
            print('SmartHub:', answer)
        except Exception as exc:
            print('Falha na inferência (não foi gerada resposta):', exc)
    

if __name__ == '__main__':
    raise SystemExit(main())
