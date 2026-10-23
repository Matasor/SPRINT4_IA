"""Interface simples e responsiva do SmartHub Assistant."""
from __future__ import annotations

import argparse
import json
import os
import queue
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from src.ollama_client import OllamaClient, OllamaError
from src.simulator import Simulation


BG = "#07111f"
PANEL = "#101c2e"
FIELD = "#17263d"
TEXT = "#f1f5f9"
MUTED = "#9fb0c7"
ACCENT = "#2dd4bf"
USER = "#60a5fa"
ERROR = "#fb7185"


class SmartHubGUI:
    """Janela com campo de pergunta sempre editável."""

    def __init__(self, root: tk.Tk, model: str, session_id: str):
        self.root = root
        self.model = model
        self.session_id = session_id
        self.bot = None
        self.busy = False
        self.events: queue.Queue[tuple[str, object]] = queue.Queue()

        self._build()
        self._write("SmartHub", "Digite sua pergunta no campo abaixo e pressione Enter.", "assistant")
        self.entry.focus_force()
        self.root.after(100, self._poll)
        self._check_ollama()

    def _build(self):
        self.root.title("SmartHub Assistant - Chatbot")
        self.root.geometry("920x650")
        self.root.minsize(700, 500)
        self.root.configure(bg=BG)

        header = tk.Frame(self.root, bg=PANEL, padx=22, pady=16)
        header.pack(fill="x")
        tk.Label(header, text="SmartHub Assistant", bg=PANEL, fg=TEXT,
                 font=("Segoe UI Semibold", 18)).pack(anchor="w")
        tk.Label(header, text=f"Chatbot ChargeGrid  |  Modelo: {self.model}  |  LangChain LCEL",
                 bg=PANEL, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(3, 0))

        status_frame = tk.Frame(self.root, bg="#0b1728", padx=22, pady=8)
        status_frame.pack(fill="x")
        self.status_dot = tk.Label(status_frame, text="●", bg="#0b1728", fg="#fbbf24")
        self.status_dot.pack(side="left")
        self.status = tk.Label(status_frame, text="Verificando Ollama...", bg="#0b1728",
                               fg=MUTED, font=("Segoe UI", 9))
        self.status.pack(side="left", padx=(7, 0))

        main = tk.Frame(self.root, bg=BG, padx=22, pady=18)
        main.pack(fill="both", expand=True)

        self.chat = ScrolledText(main, wrap="word", bg=FIELD, fg=TEXT,
                                 insertbackground=TEXT, relief="flat", padx=16, pady=14,
                                 font=("Segoe UI", 10), state="disabled")
        self.chat.pack(fill="both", expand=True)
        self.chat.tag_configure("user_name", foreground=USER, font=("Segoe UI Semibold", 10))
        self.chat.tag_configure("bot_name", foreground=ACCENT, font=("Segoe UI Semibold", 10))
        self.chat.tag_configure("body", foreground=TEXT, spacing3=9)
        self.chat.tag_configure("error", foreground=ERROR, spacing3=9)

        tk.Label(main, text="Sua pergunta:", bg=BG, fg=TEXT,
                 font=("Segoe UI Semibold", 10)).pack(anchor="w", pady=(14, 5))

        input_row = tk.Frame(main, bg=BG)
        input_row.pack(fill="x")
        self.question = tk.StringVar()
        self.entry = tk.Entry(input_row, textvariable=self.question, state="normal",
                              bg="white", fg="#111827", insertbackground="#111827",
                              disabledbackground="white", disabledforeground="#111827",
                              relief="flat", font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="x", expand=True, ipady=11, padx=(0, 10))
        self.entry.bind("<Return>", self._enter_pressed)

        self.send_button = tk.Button(input_row, text="ENVIAR", command=self.send_message,
                                     bg=ACCENT, fg="#052e2b", activebackground="#5eead4",
                                     activeforeground="#052e2b", relief="flat", width=12,
                                     font=("Segoe UI Semibold", 10), cursor="hand2")
        self.send_button.pack(side="right", fill="y")

        tk.Label(main, text="O campo branco permanece liberado para digitação. Enter envia a pergunta.",
                 bg=BG, fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w", pady=(6, 0))

        footer = tk.Frame(self.root, bg=PANEL, padx=22, pady=10)
        footer.pack(fill="x")
        tk.Button(footer, text="Limpar conversa", command=self.clear_chat,
                  bg=FIELD, fg=TEXT, activebackground="#243957", activeforeground=TEXT,
                  relief="flat", padx=12, cursor="hand2").pack(side="left")
        tk.Button(footer, text="Ver simulação fictícia", command=self.show_simulation,
                  bg=FIELD, fg=TEXT, activebackground="#243957", activeforeground=TEXT,
                  relief="flat", padx=12, cursor="hand2").pack(side="left", padx=8)
        tk.Label(footer, text="Sem acesso a telemetria real", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 8)).pack(side="right")

    def _enter_pressed(self, _event):
        self.send_message()
        return "break"

    def _write(self, author: str, text: str, kind: str):
        self.chat.configure(state="normal")
        name_tag = "user_name" if kind == "user" else "bot_name"
        self.chat.insert("end", author + "\n", name_tag)
        self.chat.insert("end", text.strip() + "\n\n", "error" if kind == "error" else "body")
        self.chat.configure(state="disabled")
        self.chat.see("end")

    def _set_status(self, text: str, level: str):
        colors = {"ok": ACCENT, "loading": "#fbbf24", "error": ERROR}
        self.status.configure(text=text)
        self.status_dot.configure(fg=colors[level])

    def _check_ollama(self):
        # O valor do modelo é uma string comum. Nenhum objeto do Tkinter é lido na thread.
        model = self.model
        threading.Thread(target=self._check_worker, args=(model,), daemon=True).start()

    def _check_worker(self, model: str):
        try:
            installed = OllamaClient(model=model, timeout=8).installed_models()
            if model not in installed:
                raise OllamaError(
                    f'Modelo "{model}" não instalado. Execute: ollama pull {model}'
                )
            self.events.put(("status_ok", f"Pronto para responder com {model}"))
        except Exception as exc:
            self.events.put(("status_error", str(exc)))

    def send_message(self):
        # Esta função sempre roda na thread principal do Tkinter.
        text = self.question.get().strip()
        if not text:
            self.entry.focus_force()
            return
        if self.busy:
            self._set_status("Aguarde a resposta atual. Você ainda pode digitar a próxima pergunta.", "loading")
            self.entry.focus_force()
            return

        self.question.set("")
        self._write("Você", text, "user")
        self.busy = True
        self.send_button.configure(state="disabled", text="AGUARDE")
        self._set_status("Gerando resposta...", "loading")
        self.entry.focus_force()  # o campo continua ativo durante a resposta
        threading.Thread(target=self._reply_worker, args=(text,), daemon=True).start()

    def _reply_worker(self, text: str):
        try:
            if self.bot is None:
                installed = OllamaClient(model=self.model, timeout=10).installed_models()
                if self.model not in installed:
                    raise OllamaError(
                        f'Modelo "{self.model}" não instalado. Abra o PowerShell e execute: '
                        f'ollama pull {self.model}'
                    )
                from src.chain import LCELAssistant
                self.bot = LCELAssistant(model=self.model, prompt_version="v2")
            answer, outcome = self.bot.reply(text, self.session_id)
            self.events.put(("answer", (answer, outcome)))
        except Exception as exc:
            self.events.put(("answer_error", str(exc)))

    def _poll(self):
        try:
            while True:
                event, payload = self.events.get_nowait()
                if event == "status_ok":
                    self._set_status(str(payload), "ok")
                elif event == "status_error":
                    self._set_status(str(payload), "error")
                elif event == "answer":
                    answer, outcome = payload
                    self._write("SmartHub", answer, "assistant")
                    label = "Resposta de segurança concluída" if outcome == "blocked" else "Resposta concluída"
                    self._set_status(label, "ok")
                    self._finish()
                elif event == "answer_error":
                    self._write("Erro", str(payload), "error")
                    self._set_status("Falha ao responder. Veja a mensagem no chat.", "error")
                    self._finish()
        except queue.Empty:
            pass
        self.root.after(100, self._poll)

    def _finish(self):
        self.busy = False
        self.send_button.configure(state="normal", text="ENVIAR")
        self.entry.configure(state="normal")
        self.entry.focus_force()

    def clear_chat(self):
        if self.bot is not None:
            self.bot.clear(self.session_id)
        self.chat.configure(state="normal")
        self.chat.delete("1.0", "end")
        self.chat.configure(state="disabled")
        self._write("SmartHub", "Conversa limpa. Digite uma nova pergunta.", "assistant")
        self.entry.configure(state="normal")
        self.entry.focus_force()

    def show_simulation(self):
        data = Simulation().run()
        self._write("Simulação fictícia", json.dumps(data, ensure_ascii=False, indent=2), "assistant")
        self.entry.focus_force()


def main(argv=None):
    parser = argparse.ArgumentParser(description="SmartHub Assistant - interface gráfica")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "qwen3:4b"))
    parser.add_argument("--session", default=os.getenv("SESSION_ID", "interface-sprint3"))
    args = parser.parse_args(argv)
    root = tk.Tk()
    SmartHubGUI(root, args.model, args.session)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
