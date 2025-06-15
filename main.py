import tkinter as tk
from tkinter import ttk
from Enums import Coluna
from Controlador import Controlador
from Column import Column
from Pesquisa import Pesquisa

# Variáveis
APP_NAME = "Gerenciador de Processos"
WINDOW_SIZE = "700x400"
UPDATE_TIME = 3000
colunas = [
    Column(Coluna.PID.value,"PID",80,'pid'),
    Column(Coluna.NOME.value,"Nome",250,'name'),
    Column(Coluna.CPU.value,"CPU %", 50, 'cpu_percent'),
    Column(Coluna.MEMORIA.value,"Memória",80,'memory_info'),
    Column(Coluna.STATUS.value,"Status",80,'status'),
    Column(Coluna.USER.value,"Usuário",100,'username'),
    Column(Coluna.CAMINHO.value,"Caminho",100,'exe')]

# Criação da janela principal
root = tk.Tk()
root.title(APP_NAME)
root.geometry(WINDOW_SIZE)
controlador = Controlador(UPDATE_TIME,root,colunas)

# Pesquisa
frame_pesquisa = tk.Frame(root)
frame_pesquisa.pack(pady=10)
entrada = Pesquisa(
    frame_pesquisa,
    placeholder="Pesquise por Nome,Pid ou Status",
    delay=700,  # 700ms depois de parar de digitar
    ao_parar_digitar=controlador.pesquisar,
    width=30
).pack()

# Frame para tabela + scrollbar
frame_tabela = tk.Frame(root)
frame_tabela.pack(fill='both', expand=True)

# Scrollbar vertical
scrollbar = ttk.Scrollbar(frame_tabela, orient='vertical')

# Treeview
tree = ttk.Treeview(frame_tabela, columns=[col.value for col in Coluna], show='headings', yscrollcommand=scrollbar.set)
controlador.tree = tree

for coluna in colunas:
    tree.heading(coluna.Id, text=coluna.Name, command=lambda c = coluna.Id: controlador.ordenar_coluna(c))
    tree.column(coluna.Id, width=coluna.Width,stretch=True)

#Configura Scrollbar
scrollbar.config(command=tree.yview)
tree.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

# Botões
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text="Encerrar processo selecionado", command=controlador.encerrar_processo).pack(side='left', padx=5)
tk.Button(frame_botoes, text="Mostrar detalhes", command=controlador.exibir_detalhes_processo_selecionado).pack(side='left', padx=5)

# Inicia atualização automática
controlador.atualizar_processos()

# Loop principal
root.mainloop()
