import tkinter as tk
from tkinter import ttk
from Enums import Coluna
from Controlador import Controlador

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

# Treeview
tree = ttk.Treeview(frame_tabela, columns=[col.value for col in Coluna], show='headings', yscrollcommand=scrollbar.set)

controlador = Controlador(UPDATE_TIME,Coluna.PID.value,tree,root)

tree.heading(Coluna.PID.value, text="PID", command=lambda: controlador.ordenar_coluna(Coluna.PID.value))
tree.heading(Coluna.NOME.value, text="Nome", command=lambda: controlador.ordenar_coluna(Coluna.NOME.value))
tree.heading(Coluna.CPU.value, text="CPU%", command=lambda: controlador.ordenar_coluna(Coluna.CPU.value))
tree.heading(Coluna.MEMORIA.value, text="Memória (MB)", command=lambda: controlador.ordenar_coluna(Coluna.MEMORIA.value))
tree.heading(Coluna.DISCO.value, text="Disco", command=lambda: controlador.ordenar_coluna(Coluna.DISCO.value))
tree.heading(Coluna.REDE.value, text="Rede", command=lambda: controlador.ordenar_coluna(Coluna.REDE.value))

tree.column(Coluna.PID.value, width=80)
tree.column(Coluna.NOME.value, width=250)
tree.column(Coluna.CPU.value, width=100)
tree.column(Coluna.MEMORIA.value, width=100)
tree.column(Coluna.DISCO.value, width=100)
tree.column(Coluna.REDE.value, width=100)

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
