import tkinter as tk

class Pesquisa(tk.Entry):
    def __init__(self, master=None, placeholder="Digite aqui...", cor_placeholder="grey", cor_texto="black", delay=500, ao_parar_digitar=None, **kwargs):
        super().__init__(master, **kwargs)

        # Configurações do placeholder
        self.placeholder = placeholder
        self.cor_placeholder = cor_placeholder
        self.cor_texto = cor_texto

        # Configurações do debounce
        self.delay = delay  # tempo em ms
        self.ao_parar_digitar = ao_parar_digitar  # função para chamar
        self.id_debounce = None

        self.config(fg=self.cor_placeholder)
        self.insert(0, self.placeholder)

        self.bind("<FocusIn>", self._ao_focar)
        self.bind("<FocusOut>", self._ao_perder_foco)
        self.bind("<KeyRelease>", self._ao_digitar)

    def _ao_focar(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.cor_texto)

    def _ao_perder_foco(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.cor_placeholder)

    def _ao_digitar(self, event):
        if self.id_debounce:
            self.after_cancel(self.id_debounce)
        self.id_debounce = self.after(self.delay, self._executar_debounce)

    def _executar_debounce(self):
        if self.ao_parar_digitar:
            self.ao_parar_digitar(self.get_valor())

    def get_valor(self):
        """Retorna o valor real (sem placeholder)."""
        texto = self.get()
        if texto == self.placeholder:
            return ""
        return texto
