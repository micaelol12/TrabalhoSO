import psutil
import tkinter as tk
from tkinter import ttk
from Controlador import Controlador
from tkinter import messagebox


class Prioridade:
    def __init__(self, root, controlador: Controlador):
        self.controlador = controlador
        self.root = root
        self.janela: tk.Toplevel = None
        self.prioridades = {
            "Tempo real": psutil.REALTIME_PRIORITY_CLASS,
            "Alta": psutil.HIGH_PRIORITY_CLASS,
            "Acima do normal": psutil.ABOVE_NORMAL_PRIORITY_CLASS,
            "Normal": psutil.NORMAL_PRIORITY_CLASS,
            "Abaixo do normal": psutil.BELOW_NORMAL_PRIORITY_CLASS,
            "Baixa": psutil.IDLE_PRIORITY_CLASS
        }
        self.var: tk.StringVar = None

    def mudar_prioridade(self):
        try:
            self.controlador.mudar_prioridade(self.prioridades[self.var.get()])
            self.janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alterar prioridade: {e}")

    def pode_alterar_prioridade(self) -> bool:
        try:
            pid = self.controlador.processo_selecionado.pid
            processo = self.controlador.processo_selecionado
            atual = processo.nice()  # Tenta ler a prioridade atual
            # Tenta reatribuir o mesmo valor (só pra testar permissão)
            processo.nice(atual)
            return True
        except psutil.AccessDenied:
            messagebox.showerror(
                "Erro", f"Permissão negada para alterar prioridade do processo {pid}.")
            return False
        except psutil.NoSuchProcess:
            messagebox.showerror("Erro", f"O processo {pid} não existe mais.")
            return False
        except Exception as e:
            messagebox.showerror("Erro", e)
            return False

    def get_prioridade_nome(self, valor):
        for chave, val in self.prioridades.items():
            if val == valor:
                return chave
        return "Desconhecido"

    def mudar_prioridade_dialog(self):
        if not self.pode_alterar_prioridade():
            return

        self.janela = tk.Toplevel(self.root, padx=10, pady=10)
        self.janela.title("Mudar Prioridade")
        self.janela.grab_set()

        label = tk.Label(
            self.janela, text=f"Selecionado PID: {self.controlador.processo_selecionado.pid}\nEscolha a nova prioridade:")
        label.pack(pady=10)

        self.var = tk.StringVar(self.janela)
        dropdown = ttk.Combobox(self.janela, textvariable=self.var, values=list(
            self.prioridades.keys()), state="readonly")
        dropdown.pack(pady=5)

        # Define valor inicial de acordo com a prioridade atual
        nivel_atual = self.controlador.get_prioridade()
        nome_prioridade = self.get_prioridade_nome(nivel_atual)
        self.var.set(nome_prioridade)

        # Botão aplicar: só vai pegar o valor no momento do clique
        btn = tk.Button(
            self.janela,
            text="Aplicar",
            command=self.mudar_prioridade
        )

        btn.pack(pady=10)
