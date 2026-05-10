import tkinter as tk
from tkinter import ttk

from src.modules.db_config import obter_config
from src.modules.estoque import historico_movimentacoes, historico_movimentacoes_paginado
from src.utils.cores import *
from src.utils.botoes import botao_menor
from src.utils.formatacao import moeda


class TelaMovimentacoes(tk.Frame):

    def __init__(self, master, tema):
        super().__init__(master)
        self.tema = tema
        
        
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            rowheight=28,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 11, "bold")
        )

        self.pack(fill="both", expand=True)
        
        self.configure(bg=BG)

        # ==========================
        # TÍTULO
        # ==========================

        titulo = tk.Label(
            self,
            text="Histórico de Movimentações de Estoque",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        # ==========================
        # TABELA
        # ==========================

        frame_tabela = tk.Frame(self)
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabela = ttk.Treeview(
            frame_tabela,
            columns=("id", "produto", "tipo", "quantidade", "motivo", "data"),
            show="headings"
        )

        self.tabela.heading("id", text="ID")
        self.tabela.heading("produto", text="Produto")
        self.tabela.heading("tipo", text="Tipo")
        self.tabela.heading("quantidade", text="Quantidade")
        self.tabela.heading("motivo", text="Motivo")
        self.tabela.heading("data", text="Data")

        self.tabela.column("id", width=50)
        self.tabela.column("produto", width=200)
        self.tabela.column("tipo", width=100)
        self.tabela.column("quantidade", width=100)
        self.tabela.column("motivo", width=200)
        self.tabela.column("data", width=150)

        self.tabela.pack(fill="both", expand=True)
        
        self.tabela.tag_configure("entrada", background="#c8cfec")
        self.tabela.tag_configure("saida", background="#f8d7da")
        
        # ==========================
        # PAGINAÇÃO
        # ==========================
        
        frame_paginacao = tk.Frame(self)
        frame_paginacao.pack(pady=10)

        btn_anterior = botao_menor(
            frame_paginacao,
            "Anterior",
            self.pagina_anterior,
            "default"
        )
        btn_anterior.pack(side="left", padx=5)
        
        self.label_pagina = tk.Label(
            frame_paginacao,
            text="Página 1",
            font=("Arial", 10, "bold")
        )
        self.label_pagina.pack(side="left", padx=10)

        btn_proximo = botao_menor(
            frame_paginacao,
            "Próxima",
            self.proxima_pagina,
            "default"
        )
        btn_proximo.pack(side="left", padx=5)
        
        
        self.pagina_atual = 0
        self.limite = 20

        # carregar dados
        self.carregar_movimentacoes()

    # ==========================
    # CARREGAR MOVIMENTAÇÕES
    # ==========================

    def carregar_movimentacoes(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        offset = self.pagina_atual * self.limite

        dados = historico_movimentacoes_paginado(self.limite, offset)

        for d in dados:
            tipo = d[2]
            #tag = "entrada" if tipo == "entrada" else "saida"
            alerta_entrada = obter_config("alerta_entrada", "1")

            tags = ()

            if alerta_entrada == "1":
                tags = ("entrada",)
            self.tabela.insert("", "end", values=d, tags=tags)
            
            alerta_saida = obter_config("alerta_saida", "1")
            
            if alerta_saida == "1" and tipo == "saida":
                self.tabela.item(self.tabela.get_children()[-1], tags=("saida",))
            
        self.atualizar_label_pagina()

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
        
    def proxima_pagina(self):
        self.pagina_atual += 1
        self.carregar_movimentacoes()

    def pagina_anterior(self):
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.carregar_movimentacoes()
            
    def atualizar_label_pagina(self):
        self.label_pagina.config(text=f"Página {self.pagina_atual + 1}")