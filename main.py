import tkinter as tk
from tkinter import ttk
from Enums import Coluna
from Controlador import Controlador
from Column import Column

# Variáveis
APP_NAME = "Gerenciador de Processos"
WINDOW_SIZE = "700x400"
UPDATE_TIME = 3000

# Criação da janela principal
root = tk.Tk()
root.title(APP_NAME)
root.geometry(WINDOW_SIZE)

# Frame para tabela + scrollbar
frame_tabela = tk.Frame(root)
frame_tabela.pack(fill='both', expand=True)

# Scrollbar vertical
scrollbar = ttk.Scrollbar(frame_tabela, orient='vertical')

colunas = [
    Column(Coluna.PID.value,"PID",80,'pid'),
    Column(Coluna.NOME.value,"Nome",250,'name'),
    Column(Coluna.CPU.value,"CPU %", 100, 'cpu_percent'),
    Column(Coluna.MEMORIA.value,"Memória (MB)",100,'memory_percent'),
    Column(Coluna.STATUS.value,"Status",100,'status'),
    Column(Coluna.USER.value,"Usuário",100,'username')]

# Treeview
tree = ttk.Treeview(frame_tabela, columns=[col.value for col in Coluna], show='headings', yscrollcommand=scrollbar.set)
controlador = Controlador(UPDATE_TIME,tree,root,colunas)

for coluna in colunas:
    print(coluna.Id)
    tree.heading(coluna.Id, text=coluna.Name, command=lambda c = coluna.Id: controlador.ordenar_coluna(c))
    tree.column(coluna.Id, width=coluna.Width,stretch=True)

scrollbar.config(command=tree.yview)
tree.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

# Botões
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)
tk.Button(frame_botoes, text="Encerrar processo selecionado", command=controlador.encerrar_processo).pack(side='left', padx=5)
tk.Button(frame_botoes, text="Mostrar gráfico CPU", command=controlador.mostrar_grafico_cpu).pack(side='left', padx=5)
tk.Button(frame_botoes, text="Mostrar detalhes", command=controlador.exibir_detalhes_processo_selecionado).pack(side='left', padx=5)

# Inicia atualização automática
controlador.atualizar_processos()

# Loop principal
root.mainloop()
