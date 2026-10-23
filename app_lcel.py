"""Alias de compatibilidade: mesmo núcleo LCEL de app.py."""
from app import main

if __name__ == '__main__':
    raise SystemExit(main())
