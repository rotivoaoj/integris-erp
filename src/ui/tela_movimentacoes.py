import tkinter as tk
from tkinter import ttk

from src.modules.db_config import obter_config
from src.modules.estoque import historico_movimentacoes_paginado, contar_movimentacoes, historico_movimentacoes_filtrado, contar_movimentacoes_filtrado
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
        # BARRA DE FILTRO
        # ==========================

        frame_filtro = tk.Frame(self, bg=BG)
        frame_filtro.pack(fill="x", padx=10, pady=10)

        tk.Label(
            frame_filtro,
            text="Filtrar por Produto:",
            font=("Arial", 10),
            bg=BG
        ).pack(side="left", padx=5)

        self.entry_produto = tk.Entry(frame_filtro, width=20)
        self.entry_produto.pack(side="left", padx=5)

        tk.Label(
            frame_filtro,
            text="Data (dd/mm/aaaa):",
            font=("Arial", 10),
            bg=BG
        ).pack(side="left", padx=5)

        self.entry_data = tk.Entry(frame_filtro, width=15)
        self.entry_data.pack(side="left", padx=5)

        btn_filtrar = botao_menor(
            frame_filtro,
            "🔍 Filtrar",
            self.aplicar_filtro,
            "default"
        )
        btn_filtrar.pack(side="left", padx=5)

        btn_limpar = botao_menor(
            frame_filtro,
            "✕ Limpar",
            self.limpar_filtro,
            "default"
        )
        btn_limpar.pack(side="left", padx=5)

        self.filtro_produto = ""
        self.filtro_data = ""
        self.filtro_ativo = False

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
        
        self.tabela.tag_configure("entrada", background="#92a3e6")
        self.tabela.tag_configure("saida", background="#c45d67")
        
        # ==========================
        # PAGINAÇÃO
        # ==========================
        
        frame_paginacao = tk.Frame(self)
        frame_paginacao.pack(pady=10)

        self.btn_anterior = botao_menor(
            frame_paginacao,
            "Anterior",
            self.pagina_anterior,
            "default"
        )
        self.btn_anterior.pack(side="left", padx=5)
        
        self.label_pagina = tk.Label(
            frame_paginacao,
            text="Página 1",
            font=("Arial", 10, "bold")
        )
        self.label_pagina.pack(side="left", padx=10)

        self.btn_proximo = botao_menor(
            frame_paginacao,
            "Próxima",
            self.proxima_pagina,
            "default"
        )
        self.btn_proximo.pack(side="left", padx=5)
        
        
        self.pagina_atual = 0
        self.limite = 20
        self.total_registros = 0

        # carregar dados
        self.carregar_movimentacoes()

    # ==========================
    # CARREGAR MOVIMENTAÇÕES
    # ==========================

    def carregar_movimentacoes(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        offset = self.pagina_atual * self.limite

        # Se há filtro ativo, usar função de filtragem
        if self.filtro_ativo:
            self.total_registros = contar_movimentacoes_filtrado(self.filtro_produto, self.filtro_data)
            dados = historico_movimentacoes_filtrado(self.filtro_produto, self.filtro_data, self.limite, offset)
        else:
            self.total_registros = contar_movimentacoes()
            dados = historico_movimentacoes_paginado(self.limite, offset)

        for d in dados:
            tipo = d[2]
            alerta_entrada = obter_config("alerta_entrada", "1")

            tags = ()

            if alerta_entrada == "1":
                tags = ("entrada",)
            self.tabela.insert("", "end", values=d, tags=tags)
            
            alerta_saida = obter_config("alerta_saida", "1")
            
            if alerta_saida == "1" and tipo == "saida":
                self.tabela.item(self.tabela.get_children()[-1], tags=("saida",))
            
        self.atualizar_label_pagina()
        self.atualizar_botoes_paginacao()

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
        total_paginas = (self.total_registros + self.limite - 1) // self.limite
        if self.pagina_atual < total_paginas - 1:
            self.pagina_atual += 1
            self.carregar_movimentacoes()

    def pagina_anterior(self):
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.carregar_movimentacoes()
            
    def atualizar_label_pagina(self):
        total_paginas = (self.total_registros + self.limite - 1) // self.limite
        self.label_pagina.config(text=f"Página {self.pagina_atual + 1} de {total_paginas}")
        
    def atualizar_botoes_paginacao(self):
        total_paginas = (self.total_registros + self.limite - 1) // self.limite
        
        # Desabilitar botão anterior se estiver na primeira página
        if self.pagina_atual == 0:
            self.btn_anterior.config(state="disabled")
        else:
            self.btn_anterior.config(state="normal")
        
        # Desabilitar botão próximo se estiver na última página
        if self.pagina_atual >= total_paginas - 1:
            self.btn_proximo.config(state="disabled")
        else:
            self.btn_proximo.config(state="normal")

    def aplicar_filtro(self):
        self.filtro_produto = self.entry_produto.get().strip()
        self.filtro_data = self.entry_data.get().strip()
        self.filtro_ativo = bool(self.filtro_produto or self.filtro_data)
        self.pagina_atual = 0
        self.carregar_movimentacoes()

    def limpar_filtro(self):
        self.entry_produto.delete(0, "end")
        self.entry_data.delete(0, "end")
        self.filtro_produto = ""
        self.filtro_data = ""
        self.filtro_ativo = False
        self.pagina_atual = 0
        self.carregar_movimentacoes()
