from Controlador import Controlador
import psutil
import tkinter as tk
from Controlador import Controlador
from tkinter import messagebox


class Afinidade:
    def __init__(self, root: tk.Tk, controlador: Controlador):
        self.controlador = controlador
        self.root = root
        self.vars_check = []
        self.janela = None

    def aplicar_afinidade(self):
        nova_afinidade = [cpu for cpu,
                          var in self.vars_check if var.get() == 1]

        if not nova_afinidade:
            messagebox.showwarning("Aviso", "Selecione ao menos um núcleo!")
            return
        try:
            self.controlador.set_afinidade(nova_afinidade)
            messagebox.showinfo(
                "Sucesso", f"Afinidade atualizada para: {nova_afinidade}")
            self.janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def mudar_afinidade_dialog(self):
        pid = self.controlador.processo_selecionado.pid

        try:
            cpus_disponiveis = list(range(psutil.cpu_count()))
            afinidade_atual = self.controlador.get_afinidade()
        except psutil.NoSuchProcess:
            print("Processo não encontrado.")
            return
        except psutil.AccessDenied:
            print("Sem permissão para alterar afinidade.")
            return

        self.janela = tk.Toplevel(self.root)
        self.janela.title(f"Afinidade de CPU - PID {pid}")
        self.vars_check = []

        tk.Label(self.janela, text="Selecione os núcleos que o processo pode usar:").pack(
            pady=5)

        for cpu in cpus_disponiveis:
            value = 1 if cpu in afinidade_atual else 0
            var = tk.IntVar()
            var.set(value)
            chk = tk.Checkbutton(
                self.janela, text=f"CPU {cpu}", variable=var, onvalue=1, offvalue=0)
            chk.pack(anchor='w')
            self.vars_check.append((cpu, var))

        tk.Button(self.janela, text="Aplicar",
                  command=self.aplicar_afinidade).pack(pady=10)
