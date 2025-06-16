
import psutil
import matplotlib.pyplot as plt
from tkinter import  messagebox
from Enums import Coluna

class Controlador:
    coluna_ordenada = None
    tempo_atualizacao = None
    ordem_reversa = False
    pid_selecionado:int = None
    tree = None
    root = None
    colunas = None
    data = []
    filteredData = []
    pesquisa = ""

    def __init__(self,tempo_atualizacao,root,colunas: list[Coluna]):
        self.tempo_atualizacao = tempo_atualizacao
        self.coluna_ordenada = colunas[0].Id
        self.root = root
        self.colunas = colunas

    def ordenar_coluna(self, col: int,change_order = False):
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

    def preencheTabela(self):
        for item in self.filteredData:
            self.tree.insert('', 'end', values=item)

    def getProcessos(self):
        cpuCount = psutil.cpu_count()
        processos = psutil.process_iter([col.ProcessAtribute for col in self.colunas])
        self.data = []

        for proc in processos:
            try:
                values = []
                
                for col in self.colunas:
                    
                    value = proc.info.get(col.ProcessAtribute, '')  # Usa o atributo dinamicamente
                    if col.Id == Coluna.CPU.value:
                            value = round(value / cpuCount, 2)  # CPU ajustado + arredondado
                    elif col.Id == Coluna.MEMORIA.value:
                            value = f"{round(value.rss/1024,2)} K" # Memória em Kilobytes 
                    elif col.Id == Coluna.USER.value:
                            value = "Sistema" if value == None else value   
    
                    values.append(value)
                
                self.data.append(values)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.filtra_dados()

    def filtra_dados(self):
        if self.pesquisa == "":
            self.filteredData = self.data
        else:
            colunas_para_filtrar = [Coluna.NOME, Coluna.PID, Coluna.STATUS]
            pesquisa_lower = self.pesquisa.lower()

            self.filteredData = [
                    processo for processo in self.data
                    if any(
                        pesquisa_lower in str(processo[list(Coluna).index(col)]).lower()
                        for col in colunas_para_filtrar
                    )
                ]

    def atualizar_processos(self):
        self.salvaSelecao()
        
        self.limpaTabela()

        self.getProcessos()
        
        self.preencheTabela()

        self.ordenar_coluna(self.coluna_ordenada,self.ordem_reversa)
        
        self.focaItemSelecionado()
        
        self.root.after(self.tempo_atualizacao, self.atualizar_processos)

    def salvaSelecao(self):
        selecionado = self.tree.selection()
        
        if selecionado:
            self.pid_selecionado = self.tree.item(selecionado[0])['values'][list(Coluna).index(Coluna.PID)]

    def limpaTabela(self):
         for row in self.tree.get_children():
            self.tree.delete(row)

    def focaItemSelecionado(self):
        if self.pid_selecionado != None:
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

    def exibir_detalhes_processo_selecionado(self):
        if self.pid_selecionado:
            processo = psutil.Process(self.pid_selecionado)
            
            detalhes = f"Nome: {processo.name()}\n"
            detalhes += f"CPU: {processo.cpu_percent()}%\n"
            detalhes += f"Memória: {processo.memory_info().rss / (1024 * 1024)} MB\n"
            detalhes += f"Tempo de execução: {processo.create_time()}"
            
            messagebox.showinfo("Detalhes do Processo", detalhes)

    def pesquisar(self,valor):
        self.pesquisa = valor
        self.filtra_dados()
        self.limpaTabela()
        self.preencheTabela()
        self.ordenar_coluna(self.coluna_ordenada, self.ordem_reversa)
    
    def get_prioridade(self) -> int:
        p = psutil.Process(self.pid_selecionado)
        return p.nice()
    
    def mudar_prioridade(self,nivel):
        p = psutil.Process(self.pid_selecionado)
        p.nice(nivel)
        
    def get_afinidade(self):
        p = psutil.Process(self.pid_selecionado)
        return p.cpu_affinity()
    
    def set_afinidade(self,nova_afinidade):
        p = psutil.Process(self.pid_selecionado)
        p.cpu_affinity(nova_afinidade)


