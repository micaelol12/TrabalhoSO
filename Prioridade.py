import psutil
import tkinter as tk
from tkinter import ttk
from Controlador import Controlador
from tkinter import  messagebox

class Prioridade:
    def __init__(self,root,controlador:Controlador):
        self.controlador = controlador
        self.root = root
        self.prioridades = {
            "Tempo real": psutil.REALTIME_PRIORITY_CLASS,
            "Alta": psutil.HIGH_PRIORITY_CLASS,
            "Acima do normal": psutil.ABOVE_NORMAL_PRIORITY_CLASS,
            "Normal": psutil.NORMAL_PRIORITY_CLASS,
            "Abaixo do normal": psutil.BELOW_NORMAL_PRIORITY_CLASS,
            "Baixa": psutil.IDLE_PRIORITY_CLASS
        }
        
    def mudar_prioridade(self,n,janela:tk.Toplevel):
        try:
         self.controlador.mudar_prioridade(n)
         janela.destroy()
        except Exception as e:
         messagebox.showerror("Erro",f"Erro ao alterar prioridade: {e}")

    
    def pode_alterar_prioridade(self) -> bool:
        try:
            processo = psutil.Process(self.controlador.pid_selecionado)
            atual = processo.nice()  # Tenta ler a prioridade atual
            processo.nice(atual)     # Tenta reatribuir o mesmo valor (só pra testar permissão)
            return True
        except psutil.AccessDenied:
            messagebox.showerror("Erro",f"Permissão negada para alterar prioridade do processo {self.controlador.pid_selecionado}.")
            return False
        except psutil.NoSuchProcess:
            messagebox.showerror("Erro",f"O processo {self.controlador.pid_selecionado} não existe mais.")
            return False
        except Exception as e:
            messagebox.showerror("Erro",e)
            return False
        
    def get_prioridade_nome(self,valor):
        for chave, val in self.prioridades.items():
            if val == valor:
                return chave
        return "Desconhecido"
    
    def mudar_prioridade_dialog(self):
        if self.controlador.pid_selecionado is None:
            print("Nenhum processo selecionado.")
            return

        if not self.pode_alterar_prioridade():
            return

        janela = tk.Toplevel(self.root)
        janela.title("Mudar Prioridade")

        label = tk.Label(janela, text=f"Selecionado PID: {self.controlador.pid_selecionado}\nEscolha a nova prioridade:")
        label.pack(pady=10)

        var = tk.StringVar(janela)
        dropdown = ttk.Combobox(janela, textvariable=var, values=list(self.prioridades.keys()), state="readonly")
        dropdown.pack(pady=5)

        # Define valor inicial de acordo com a prioridade atual
        nivel_atual = self.controlador.get_prioridade()
        nome_prioridade = self.get_prioridade_nome(nivel_atual)
        var.set(nome_prioridade)

        # Botão aplicar: só vai pegar o valor no momento do clique
        btn = tk.Button(
            janela,
            text="Aplicar",
            command=lambda: self.mudar_prioridade(self.prioridades[var.get()], janela)
        )
        
        btn.pack(pady=10)
