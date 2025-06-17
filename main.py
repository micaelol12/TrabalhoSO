import tkinter as tk
from tkinter import ttk
from Enums import Coluna
from Controlador import Controlador
from Column import Column
from Pesquisa import Pesquisa
from Prioridade import Prioridade
from Afinidade import Afinidade

# Variáveis
APP_NAME = "Gerenciador de Processos"
WINDOW_SIZE = "700x400"
UPDATE_TIME = 3000
colunas = [
    Column(Coluna.PID.value, "PID", 80, 'pid'),
    Column(Coluna.NOME.value, "Nome", 250, 'name'),
    Column(Coluna.CPU.value, "CPU %", 50, 'cpu_percent'),
    Column(Coluna.MEMORIA.value, "Memória", 80, 'memory_info'),
    Column(Coluna.STATUS.value, "Status", 80, 'status'),
    Column(Coluna.USER.value, "Usuário", 100, 'username'),
    Column(Coluna.CAMINHO.value, "Caminho", 100, 'exe')]

# Criação da janela principal
root = tk.Tk()
root.title(APP_NAME)
root.geometry(WINDOW_SIZE)
frame_pesquisa = tk.Frame(root)
frame_pesquisa.pack(pady=10)
frame_tabela = tk.Frame(root)
status_bar = tk.Label(root, text="Pronto", anchor='w')
frame_tabela.pack(fill='both', expand=True)
scrollbar = ttk.Scrollbar(frame_tabela, orient='vertical')
tree = ttk.Treeview(frame_tabela, columns=[
                    col.value for col in Coluna], show='headings', yscrollcommand=scrollbar.set)
controlador = Controlador(UPDATE_TIME, root, colunas, tree,status_bar)

# Pesquisa
entrada = Pesquisa(
    frame_pesquisa,
    placeholder="Pesquise por Nome,Pid ou Status",
    delay=700,  # 700ms depois de parar de digitar
    ao_parar_digitar=controlador.pesquisar,
    width=30
).pack()

# Prioridade modal
prioridade = Prioridade(root, controlador)

# Afinidade modal
afinidade = Afinidade(root, controlador)

for coluna in colunas:
    tree.heading(coluna.Id, text=coluna.Name,
                 command=lambda c=coluna.Id: controlador.ordenar_coluna(c))
    tree.column(coluna.Id, width=coluna.Width, stretch=True)

# Configura Scrollbar
scrollbar.config(command=tree.yview)
tree.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

# Botões
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

encerrar_btn = tk.Button(frame_botoes, text="Encerrar processo selecionado",
                         command=controlador.encerrar_processo, state=tk.DISABLED)
details_btn = tk.Button(frame_botoes, text="Mostrar detalhes",
                        command=controlador.exibir_detalhes_processo_selecionado, state=tk.DISABLED)
prioridade_btn = tk.Button(frame_botoes, text="Mudar Prioridade",
                           command=prioridade.mudar_prioridade_dialog, state=tk.DISABLED)
afindiade_btn = tk.Button(frame_botoes, text="Mudar Afinidade",
                          command=afinidade.mudar_afinidade_dialog, state=tk.DISABLED)

encerrar_btn.pack(side='left', padx=5)
details_btn.pack(side='left', padx=5)
prioridade_btn.pack(side='left', padx=5)
afindiade_btn.pack(side='left', padx=5)
status_bar.pack(fill='x', side='bottom')

def tree_select(evento=None):
    controlador.salva_selecao()
    atualizar_estado_botoes()

def atualizar_estado_botoes():
    estado = tk.NORMAL if controlador.processo_selecionado is not None else tk.DISABLED

    encerrar_btn.config(state=estado)
    details_btn.config(state=estado)
    prioridade_btn.config(state=estado)
    afindiade_btn.config(state=estado)


tree.bind("<<TreeviewSelect>>", tree_select)
controlador.atualizar_processos()
root.mainloop()
