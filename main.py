import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import matplotlib.pyplot as plt
from enum import Enum

# Criação da janela principal
root = tk.Tk()
root.title("Gerenciador de Processos")
root.geometry("700x400")

# Variáveis globais para ordenação
coluna_ordenada = 'PID'
ordem_reversa = False
tempo_atualizacao = 3000
pid_selecionado = None

# Frame para tabela + scrollbar
frame_tabela = tk.Frame(root)
frame_tabela.pack(fill='both', expand=True)

# Scrollbar vertical
scrollbar = ttk.Scrollbar(frame_tabela, orient='vertical')

class Coluna(Enum):
    PID = 'PID'
    NOME = 'Nome'
    CPU = 'CPU %'
    MEMORIA = 'Memória %'
    DISCO = 'Disco %'
    REDE = 'Rede %'
    
# Treeview
tree = ttk.Treeview(frame_tabela, columns=[col.value for col in Coluna], show='headings', yscrollcommand=scrollbar.set)

tree.heading(Coluna.PID.value, text=Coluna.PID.value, command=lambda: ordenar_coluna(tree, Coluna.PID.value, False))
tree.heading(Coluna.NOME.value, text=Coluna.NOME.value, command=lambda: ordenar_coluna(tree, Coluna.NOME.value, False))
tree.heading(Coluna.CPU.value, text=Coluna.CPU.value, command=lambda: ordenar_coluna(tree, Coluna.CPU.value, False))

tree.heading(Coluna.MEMORIA.value, text=Coluna.MEMORIA.value, command=lambda: ordenar_coluna(tree, Coluna.MEMORIA.value, False))
tree.heading(Coluna.DISCO.value, text=Coluna.DISCO.value, command=lambda: ordenar_coluna(tree, Coluna.DISCO.value, False))
tree.heading(Coluna.REDE.value, text=Coluna.REDE.value, command=lambda: ordenar_coluna(tree, Coluna.REDE.value, False))

tree.column(Coluna.PID.value, width=80)
tree.column(Coluna.NOME.value, width=250)
tree.column(Coluna.CPU.value, width=100)
tree.column(Coluna.MEMORIA.value, width=100)
tree.column(Coluna.DISCO.value, width=100)
tree.column(Coluna.REDE.value, width=100)

scrollbar.config(command=tree.yview)
tree.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

def ordenar_coluna(tv, col, reverse):
    global coluna_ordenada, ordem_reversa
    dados = [(tv.set(k, col), k) for k in tv.get_children('')]

    try:
        dados.sort(key=lambda t: float(t[0]), reverse=reverse)
    except ValueError:
        dados.sort(key=lambda t: t[0].lower(), reverse=reverse)

    for index, (val, k) in enumerate(dados):
        tv.move(k, '', index)

    coluna_ordenada = col
    ordem_reversa = reverse

    tv.heading(col, command=lambda: ordenar_coluna(tv, col, not reverse))


def atualizar_processos():
    # Salva seleção
    global pid_selecionado
    
    selecionado = tree.selection()
    
    if selecionado:
        pid_selecionado = tree.item(selecionado[0])['values'][list(Coluna).index(Coluna.PID)]

    # Limpa e recarrega a lista
    for row in tree.get_children():
        tree.delete(row)

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent','memory_percent']):
        try:
            pid = proc.info['pid']
            nome = proc.info['name']
            cpu = proc.info['cpu_percent']
            memoria = proc.info['memory_percent'],
            tree.insert('', 'end', values=(pid, nome, cpu,memoria))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Reaplica ordenação
    ordenar_coluna(tree, coluna_ordenada, ordem_reversa)
    
    # Restaura seleção
    focaItemSelecionado()
    
    # Reagenda atualização
    root.after(tempo_atualizacao, atualizar_processos)

def focaItemSelecionado():
     if pid_selecionado:
        for item in tree.get_children():
            if tree.item(item)['values'][list(Coluna).index(Coluna.PID)] == pid_selecionado:
                tree.selection_set(item)
                tree.see(item)
                break

def encerrar_processo():
    if not messagebox.askokcancel("Avsio",f"Tem certeza que deseja excluir o processo?"):
        return
    
    
    item = tree.selection()
    if item:
        pid = int(tree.item(item[0])['values'][list(Coluna).index(Coluna.PID)])
        try:
            psutil.Process(pid).terminate()
            messagebox.showinfo("Sucesso", f"Processo {pid} encerrado.")
            atualizar_processos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao encerrar processo {pid}: {e}")
    else:
        messagebox.showwarning("Aviso", "Nenhum processo selecionado.")


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


def exibir_detalhes_processo_selecionado():
    if pid_selecionado:
        processo = psutil.Process(pid_selecionado)
        
        detalhes = f"Nome: {processo.name()}\n"
        detalhes += f"CPU: {processo.cpu_percent()}%\n"
        detalhes += f"Memória: {processo.memory_info().rss / (1024 * 1024)} MB\n"
        detalhes += f"Tempo de execução: {processo.create_time()}"
        
        messagebox.showinfo("Detalhes do Processo", detalhes)

# Botões
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text="Encerrar processo selecionado", command=encerrar_processo).pack(side='left', padx=5)
tk.Button(frame_botoes, text="Mostrar gráfico CPU", command=mostrar_grafico_cpu).pack(side='left', padx=5)
tk.Button(frame_botoes, text="Mostrar detalhes", command=exibir_detalhes_processo_selecionado).pack(side='left', padx=5)

# Inicia atualização automática
atualizar_processos()

# Loop principal
root.mainloop()
