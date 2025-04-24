
import psutil
import matplotlib.pyplot as plt
from tkinter import  messagebox
from Enums import Coluna

class Controlador:
    coluna_ordenada = None
    tempo_atualizacao = None
    ordem_reversa = False
    pid_selecionado = None
    tree = None
    root = None

    def __init__(self,tempo_atualizacao,coluna_ordenada,tree,root):
        self.tempo_atualizacao = tempo_atualizacao
        self.coluna_ordenada = coluna_ordenada
        self.tree = tree
        self.root = root

    def ordenar_coluna(self, col,change_order = False):
        dados = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]

        try:
            dados.sort(key=lambda t: float(t[0]), reverse=change_order)
        except ValueError:
            dados.sort(key=lambda t: t[0].lower(), reverse=change_order)

        for index, (val, k) in enumerate(dados):
            self.tree.move(k, '', index)

        self.coluna_ordenada = col
        
        self.ordem_reversa = change_order

        self.tree.heading(col, command=lambda: self.ordenar_coluna(col, not change_order))


    def atualizar_processos(self):
        # Salva seleção
        selecionado = self.tree.selection()
        
        if selecionado:
            self.pid_selecionado = self.tree.item(selecionado[0])['values'][list(Coluna).index(Coluna.PID)]

        # Limpa e recarrega a lista
        for row in self.tree.get_children():
            self.tree.delete(row)

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent','memory_percent']):
            try:
                pid = proc.info['pid']
                nome = proc.info['name']
                cpu = proc.info['cpu_percent']
                memoria = proc.info['memory_percent'],
                self.tree.insert('', 'end', values=(pid, nome, cpu,memoria))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Reaplica ordenação
        print(self.coluna_ordenada)
        self.ordenar_coluna(self.coluna_ordenada,self.ordem_reversa)
        
        # Restaura seleção
        self.focaItemSelecionado()
        
        # Reagenda atualização
        self.root.after(self.tempo_atualizacao, self.atualizar_processos)

    def focaItemSelecionado(self):
        if self.pid_selecionado:
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][list(Coluna).index(Coluna.PID)] == self.pid_selecionado:
                    self.tree.selection_set(item)
                    self.tree.see(item)
                    break

    def encerrar_processo(self):
        if not messagebox.askokcancel("Avsio",f"Tem certeza que deseja excluir o processo?"):
            return
        
        
        item = self.tree.selection()
        if item:
            pid = int(self.tree.item(item[0])['values'][list(Coluna).index(Coluna.PID)])
            try:
                psutil.Process(pid).terminate()
                messagebox.showinfo("Sucesso", f"Processo {pid} encerrado.")
                self.atualizar_processos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao encerrar processo {pid}: {e}")
        else:
            messagebox.showwarning("Aviso", "Nenhum processo selecionado.")

    @staticmethod
    def mostrar_grafico_cpu():
        processos = []
        for proc in psutil.process_iter(['name', 'cpu_percent']):
            try:
                cpu = proc.info['cpu_percent']
                if cpu > 0.5:
                    processos.append((proc.info['name'], cpu))
            except:
                continue

        processos.sort(key=lambda x: x[1], reverse=True)
        nomes = [p[0] for p in processos][:10]
        valores = [p[1] for p in processos][:10]

        plt.figure(figsize=(10, 5))
        plt.barh(nomes, valores, color='skyblue')
        plt.xlabel('Uso de CPU (%)')
        plt.title('Top 10 processos por uso de CPU')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()


    def exibir_detalhes_processo_selecionado(self):
        if self.pid_selecionado:
            processo = psutil.Process(self.pid_selecionado)
            
            detalhes = f"Nome: {processo.name()}\n"
            detalhes += f"CPU: {processo.cpu_percent()}%\n"
            detalhes += f"Memória: {processo.memory_info().rss / (1024 * 1024)} MB\n"
            detalhes += f"Tempo de execução: {processo.create_time()}"
            
            messagebox.showinfo("Detalhes do Processo", detalhes)