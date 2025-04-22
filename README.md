# TrabalhoSO
Trabalho da disciplina de Sistemas Operacionais


# Ideia para Agregar Valor:

## 🧠 1. Filtros Inteligentes
✅ Por nome do processo (ex: digitar "chrome" e ver só os processos do Chrome).

✅ Por uso de CPU/memória acima de X% (ajuda a encontrar processos pesados).

✅ Por status (running, sleeping, etc.) usando proc.status().

## 📊 2. Mais Gráficos em Tempo Real
Gráfico de uso de memória ao longo do tempo.

Gráfico de uso de CPU por núcleo.

Gráfico de rede por processo (dados enviados/recebidos em tempo real).

Você pode usar matplotlib ou tkinter + canvas para gráficos leves.

## 🧩 3. Detalhes Avançados por Processo
Ao clicar duas vezes em um processo, abrir uma janela com mais informações, como:

Caminho do executável (proc.exe()),

Argumentos da linha de comando (proc.cmdline()),

Tempo de execução (proc.create_time()),

Threads e filhos (proc.threads(), proc.children()),

Usuário que iniciou (proc.username()).

## 💡 4. Modo claro/escuro
Alternância entre modo claro e escuro com um botão (basta trocar cores de fundo/elementos).

## 🧠 5. Otimizações e Segurança
Bloquear encerramento de processos críticos do sistema (ex: PID 0 ou 4).

Confirmar duplamente o encerramento de processos importantes.

Mostrar alerta se o processo for iniciado por outro usuário.

## 🧪 6. Monitoramento de Anomalias
Exibir aviso se um processo estiver:

Consumindo CPU acima de 80% por mais de X segundos.

Aumentando uso de memória rapidamente.

Pode usar threads para isso e dar alertas via messagebox.

## 🔍 7. Busca Global + Destaque
Caixa de busca no topo para digitar o nome e realçar os resultados na tabela.

## 🛠️ 8. Exportar dados
Botão "Exportar CSV" com todos os processos listados.

Botão "Gerar relatório" com resumo de CPU, memória, processos abertos, etc.

## 🎨 9. Interface Moderna
Usar ttk.Style() para deixar o app mais bonito.

Ícones nos botões (ex: 🔍 para buscar, 🗑️ para encerrar).

Adicionar logotipo da universidade/matéria no canto.

## 💬 10. Personalização do Intervalo de Atualização
Um Spinbox para o usuário escolher o intervalo de atualização (ex: 1s, 3s, 5s, 10s...).