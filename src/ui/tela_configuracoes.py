import tkinter as tk
from tkinter import messagebox
from src.modules.db_config import salvar_config, obter_config

class TelaConfiguracoes(tk.Frame):

    def __init__(self, master, tema):
        super().__init__(master)

        self.pack(fill="both", expand=True)
        self.tema = tema
        self.configure(bg="#ecf0f1")

        tk.Label(self, text="Configurações", font=("Arial", 16, "bold")).pack(pady=10)

        # 🔧 ESTOQUE MÍNIMO
        tk.Label(self, text="Estoque mínimo padrão").pack()

        self.entry_minimo = tk.Entry(self)
        self.entry_minimo.pack()

        self.entry_minimo.insert(
            0,
            obter_config("estoque_minimo", "5")
        )

        # 💾 BOTÃO SALVAR
        tk.Button(
            self,
            text="Salvar",
            bg="#27ae60",
            fg="white",
            command=self.salvar
        ).pack(pady=20)


    def salvar(self):

        minimo = self.entry_minimo.get()

        if not minimo.isdigit():
            messagebox.showerror("Erro", "Digite um número válido")
            return

        salvar_config("estoque_minimo", minimo)

        messagebox.showinfo("Sucesso", "Configuração salva!")
        
        def criar_header(self, titulo_texto):

            header = tk.Frame(self, bg="white")
            header.pack(fill="x")

            titulo = tk.Label(
                header,
                text=titulo_texto,
                font=("Arial", 18, "bold"),
                bg="white"
            )
            titulo.pack(side="left", padx=10, pady=10)