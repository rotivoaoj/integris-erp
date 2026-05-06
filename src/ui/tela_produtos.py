import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src.modules.produtos import listar_produtos, inserir_produto, atualizar_produto, excluir_produto, salvar_produto
from src.modules.estoque import entrada_estoque, saida_estoque
from src.modules.db_config import obter_config
from src.utils.cores import *
from src.ui.styles import *
from src.utils.botoes import botao_moderno, botao_menor

class TelaProdutos(tk.Frame):

    def __init__(self, master, tema):
        super().__init__(master)
        
        style = ttk.Style()
        style.theme_use("default")
        self.tema = tema

        style.configure(
            "Treeview",
            rowheight=28,
            font=self.tema["font"]
        )
        style.map(
            "Treeview",
            background=[("selected", "#22c55e")],
            foreground=[("selected", "white")]
        )
        style.configure(
            "Treeview",
            bordercolor=self.tema["primary"],
            relief="flat"
        )
        style.configure(
            "Treeview.Heading",
            font=self.tema["title"]
        )

        self.pack(fill="both", expand=True)
        
        self.configure(bg=self.tema["card"])

        # ===============================
        # BARRA SUPERIOR
        # ===============================

        barra_topo = tk.Frame(self)
        barra_topo.pack(fill="x", padx=10, pady=5)

        # ===============================
        # BARRA DE BUSCA
        # ===============================

        barra_topo = tk.Frame(self, bg=self.tema["card"])
        barra_topo.pack(fill="x", padx=10, pady=5)
        barra_topo.configure(height=50)

        # TÍTULO
        titulo = tk.Label(
            barra_topo,
            text="Produtos",
            fg=self.tema["text"],
            bg=self.tema["card"],
            font=self.tema["title"]
        )
        titulo.pack(side="left", padx=(0, 20))

        # BUSCA
        tk.Label(
            barra_topo,
            bg=self.tema["card"],
            fg=self.tema["text"]
        ).pack(side="left")

        self.entry_busca = tk.Entry(
            barra_topo,
            bg="#ffffff",
            fg="black",
            insertbackground="white",
            width=25
        )
        self.entry_busca.pack(side="left", padx=5)

        btn_buscar = botao_menor(
            barra_topo,
            "Buscar 🔍",
            self.buscar_produto,
            "default"
        )
        btn_buscar.pack(side="left", padx=5)

        # BOTÃO NOVO (fica na direita)
        btn_novo = botao_moderno(barra_topo, "+ Novo Produto", self.novo_produto, "primary")
        btn_novo.pack(side="right", padx=5)

        # ==========================
        # AREA PRINCIPAL
        # ==========================

        frame_conteudo = tk.Frame(self)
        frame_conteudo.pack(fill="both", expand=True)

        # ==========================
        # LISTA PRODUTOS
        # ==========================

        frame_lista = tk.Frame(frame_conteudo, width=700)
        frame_lista.pack(side="left", fill="both", padx=10, pady=10)
        frame_lista.pack_propagate(False)

        self.tabela = ttk.Treeview(
            frame_lista,
            columns=("id","codigo","nome","preco","estoque"),
            show="headings"
        )
        
        self.tabela.tag_configure(
            "estoque_baixo",
            background="#ff4d4d",
            foreground="white"
        )
        style.map(
            "Treeview",
            background=[("selected", "#5a90c2")],
            foreground=[("selected", "white")]
        )

        self.tabela.heading("id", text="ID")
        self.tabela.heading("codigo", text="Código")
        self.tabela.heading("nome", text="Produto")
        self.tabela.heading("preco", text="Preço")
        self.tabela.heading("estoque", text="Estoque")

        self.tabela.column("id", width=50)
        self.tabela.column("codigo", width=120)
        self.tabela.column("nome", width=250)
        self.tabela.column("preco", width=100)
        self.tabela.column("estoque", width=100)

        self.tabela.pack(fill="both", expand=True)
        self.tabela.tag_configure(
            "estoque_baixo",
            background="#7f1d1d",
            foreground="white"
        )

        self.tabela.bind("<<TreeviewSelect>>", self.mostrar_detalhes)

        # ==========================
        # DETALHES
        # ==========================

        frame_detalhes = tk.Frame(
            frame_conteudo,
            width=350,
            bg=self.tema["card"]
        )
        frame_detalhes.pack(side="right", fill="y", padx=10, pady=10)
        frame_detalhes.pack_propagate(False)

        titulo_det = tk.Label(
            frame_detalhes,
            text="Detalhes do Produto",
            font=("Arial", 14, "bold"),
            bg=self.tema["card"]
        )

        titulo_det.pack(pady=10)

        self.label_info = tk.Label(
            frame_detalhes,
            text="Selecione um produto",
            justify="left",
            bg=self.tema["card"],
            font=self.tema["font"]
        )

        self.label_info.pack(padx=10, pady=10)

        # ==========================
        # BOTÕES
        # ==========================

        frame_acoes = tk.Frame(frame_detalhes, bg=self.tema["card"])
        frame_acoes.pack(pady=20, fill="x")

        btn_entrada = botao_moderno(frame_acoes, "Entrada", self.entrada_estoque, "primary")
        btn_entrada.pack(fill="x", pady=5)

        btn_saida = botao_moderno(frame_acoes, "Saída", self.saida_estoque, "warning")
        btn_saida.pack(fill="x", pady=5)
        
        btn_editar = botao_moderno(frame_acoes, "Editar", self.editar_produto,"primary")
        btn_editar.pack(fill="x", pady=5)

        btn_excluir = botao_moderno(frame_acoes, "Excluir", self.excluir_produto, "danger")
        btn_excluir.pack(fill="x", pady=5)


        # CARREGA PRODUTOS
        self.carregar_produtos()

    def carregar_produtos(self):
        
        estoque_minimo_global = obter_config("estoque_minimo", 5)
        estoque_minimo_global = int(estoque_minimo_global)

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        produtos = listar_produtos()

        for p in produtos:

            id_produto = p[0]
            codigo = p[1]
            nome = p[2]
            preco = p[3]
            estoque = p[4]
            estoque_minimo = p[5] if len(p) > 5 else 5

            if estoque is None:
                estoque = 0

            if estoque_minimo is None:
                estoque_minimo = estoque_minimo_global

            if estoque <= estoque_minimo:

                self.tabela.insert(
                    "",
                    "end",
                    values=(id_produto, codigo, nome, preco, estoque),
                    tags=("estoque_baixo",)
                )

            else:

                self.tabela.insert(
                    "",
                    "end",
                    values=(id_produto, codigo, nome, preco, estoque)
                )
            
    def buscar_produto(self):

        termo = self.entry_busca.get().lower()

        for item in self.tabela.get_children(): 
            self.tabela.delete(item)

        produtos = listar_produtos()

        for p in produtos:
            if termo in p[2].lower():
                self.tabela.insert("", "end", values=p)

    def mostrar_detalhes(self, event):

        selecionado = self.tabela.selection()

        if not selecionado:
            return

        item = selecionado[0]
        dados = self.tabela.item(item)["values"]

        texto = f"""
            ID: {dados[0]}
            Código: {dados[1]}
            Produto: {dados[2]}

            Preço: R$ {dados[3]}
            Estoque: {dados[4]}
        """

        self.label_info.config(text=texto)

    def novo_produto(self):

        janela = tk.Toplevel(self)
        janela.title("Cadastro de Produto")
        janela.geometry("350x300")
        janela.grab_set()

        tk.Label(janela, text="Código").pack()
        entry_codigo = tk.Entry(janela)
        entry_codigo.pack()
        entry_codigo.focus()

        tk.Label(janela, text="Nome").pack()
        entry_nome = tk.Entry(janela)
        entry_nome.pack()

        tk.Label(janela, text="Preço").pack()
        entry_preco = tk.Entry(janela)
        entry_preco.pack()

        tk.Label(janela, text="Estoque").pack()
        entry_estoque = tk.Entry(janela)
        entry_estoque.pack()


    # ===============================
    # FUNÇÃO SALVAR
    # ===============================

        def salvar():

            codigo = entry_codigo.get().strip()
            nome = entry_nome.get().strip()
            preco_venda = entry_preco.get().strip()
            estoque = entry_estoque.get().strip()

            # VALIDAÇÃO
            if not codigo or not nome or not preco_venda or not estoque:
                messagebox.showerror(
                    "Erro",
                    "Todos os campos são obrigatórios."
                )
                return

        # VALIDAR NÚMEROS
            try:
                preco_venda = float(preco_venda)
                estoque = int(estoque)
            except ValueError:
                messagebox.showerror(
                    "Erro",
                    "Preço deve ser número e estoque deve ser inteiro."
                )
                return

        # SALVAR NO BANCO
            try:

                inserir_produto(codigo, nome, preco_venda, estoque)

                messagebox.showinfo(
                    "Sucesso",
                    "Produto cadastrado com sucesso!"
                )

                janela.destroy()

                self.carregar_produtos()

            except Exception as e:

                if "UNIQUE constraint" in str(e):

                    messagebox.showerror(
                        "Erro",
                        "Já existe um produto com esse código."
                    )

                else:

                    messagebox.showerror(
                        "Erro",
                        f"Erro ao salvar produto:\n{e}"
                    )

    # BOTÃO SALVAR
        btn_salvar = botao_moderno(
            janela,
            "Salvar",
            salvar,
            "primary"
        )

        btn_salvar.pack(pady=10)

    def editar_produto(self):

        selecionado = self.tabela.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto.")
            return

        item = self.tabela.selection()[0]
        
        dados = self.tabela.item(item)["values"]

        id_produto = dados[0]

        janela = tk.Toplevel(self)
        janela.title("Editar Produto")
        janela.geometry("350x300")
        janela.grab_set()

        tk.Label(janela, text="Código").pack()
        entry_codigo = tk.Entry(janela)
        entry_codigo.pack()
        entry_codigo.insert(0, dados[1])

        tk.Label(janela, text="Nome").pack()
        entry_nome = tk.Entry(janela)
        entry_nome.pack()
        entry_nome.insert(0, dados[2])

        tk.Label(janela, text="Preço").pack()
        entry_preco = tk.Entry(janela)
        entry_preco.pack()
        entry_preco.insert(0, dados[3])

        tk.Label(janela, text="Estoque").pack()
        entry_estoque = tk.Entry(janela)
        entry_estoque.pack()
        entry_estoque.insert(0, dados[4])

        def salvar():

            codigo = entry_codigo.get().strip()
            nome = entry_nome.get().strip()
            preco = entry_preco.get().strip()
            estoque = entry_estoque.get().strip()

            if not codigo or not nome or not preco or not estoque:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
                return

            try:
                preco = float(preco)
                estoque = int(estoque)
            except ValueError:
                messagebox.showerror("Erro", "Preço inválido ou estoque inválido.")
                return

            try:

                atualizar_produto(id_produto, codigo, nome, preco, estoque)

                messagebox.showinfo("Sucesso", "Produto atualizado!")

                janela.destroy()
                self.carregar_produtos()

            except Exception as e:

                messagebox.showerror("Erro", str(e))

        btn_salvar = botao_moderno(
            janela,
            "Salvar Alterações",
            self.salvar,
            "primary"
        )

        btn_salvar.pack(pady=10)
        
    def excluir_produto(self):

        selecionado = self.tabela.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto.")
            return

        item = self.tabela.selection()[0]
        
        dados = self.tabela.item(item)["values"]

        id_produto = dados[0]
        nome_produto = dados[2]

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja excluir o produto:\n\n{nome_produto} ?"
        )

        if not confirmar:
            return

        try:

            excluir_produto(id_produto)

            messagebox.showinfo(
                "Sucesso",
                "Produto excluído com sucesso!"
            )

            self.carregar_produtos()

            self.label_info.config(text="Selecione um produto")

        except Exception as e:

            messagebox.showerror(
                "Erro",
                f"Erro ao excluir produto:\n{e}"
            )
            
    def entrada_estoque(self):

        selecionado = self.tabela.selection()

        if not selecionado:
            return

        item = selecionado[0]
        dados = self.tabela.item(item)["values"]
        produto_id = dados[0]

        quantidade = simpledialog.askinteger(
            "Entrada de Estoque",
            "Quantidade a adicionar:",
            minvalue=1
        )

        if quantidade:

            entrada_estoque(produto_id, quantidade)

            messagebox.showinfo("Sucesso", "Estoque atualizado")

            self.carregar_produtos()
            
    def saida_estoque(self):

        selecionado = self.tabela.selection()

        if not selecionado:
            return

        item = selecionado[0]
        dados = self.tabela.item(item)["values"]
        produto_id = dados[0]

        quantidade = simpledialog.askinteger(
            "Saída de Estoque",
            "Quantidade a retirar:"
        )

        if quantidade:

            saida_estoque(produto_id, quantidade)

            messagebox.showinfo("Sucesso", "Saída registrada")

            self.carregar_produtos()
    
        try:
            saida_estoque(produto_id, quantidade)
            messagebox.showinfo("Sucesso", "Saída registrada!")

        except Exception as e:
            messagebox.showerror("Erro", str(e))
            
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

        btn_novo = botao_moderno(
            header,
            "+ Novo Produto",
            self.novo_produto,
            "sucess"
        )
        btn_novo.pack(side="right")
        
        # ==========================
        # AREA PRINCIPAL
        # ==========================

        frame_conteudo = tk.Frame(self)
        frame_conteudo.pack(fill="both", expand=True)

        # ==========================
        # LISTA PRODUTOS
        # ==========================

        frame_lista = tk.Frame(frame_conteudo, width=700)
        frame_lista.pack(side="left", fill="both", padx=10, pady=10)
        frame_lista.pack_propagate(False)

        self.tabela = ttk.Treeview(
            frame_lista,
            columns=("id","codigo","nome","preco","estoque"),
            show="headings"
        )
        
        self.tabela.tag_configure(
            "estoque_baixo",
            background="#ff4d4d",
            foreground="white"
        )

        self.tabela.heading("id", text="ID")
        self.tabela.heading("codigo", text="Código")
        self.tabela.heading("nome", text="Produto")
        self.tabela.heading("preco", text="Preço")
        self.tabela.heading("estoque", text="Estoque")

        self.tabela.column("id", width=50)
        self.tabela.column("codigo", width=120)
        self.tabela.column("nome", width=250)
        self.tabela.column("preco", width=100)
        self.tabela.column("estoque", width=100)

        self.tabela.pack(fill="both", expand=True)
        self.tabela.tag_configure(
            "estoque_baixo",
            background="#ffcccc"
        )

        self.tabela.bind("<<TreeviewSelect>>", self.mostrar_detalhes)

        # ==========================
        # DETALHES
        # ==========================

        frame_detalhes = tk.Frame(frame_conteudo, width=350, bg="#ecf0f1")
        frame_detalhes.pack(side="right", fill="y", padx=10, pady=10)
        frame_detalhes.pack_propagate(False)

        titulo_det = tk.Label(
            frame_detalhes,
            text="Detalhes do Produto",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1"
        )

        titulo_det.pack(pady=10)

        self.label_info = tk.Label(
            frame_detalhes,
            text="Selecione um produto",
            justify="left",
            bg=self.tema["bg"],
            font=self.tema["text"]
        )

        self.label_info.pack(padx=10, pady=10)

        # BOTÕES

        frame_acoes = tk.Frame(frame_detalhes, bg="#ecf0f1")
        frame_acoes.pack(pady=20)

        btn_editar = tk.Button(
            frame_acoes,
            text="Editar",
            command=self.editar_produto
        )
        btn_editar.pack(side="left", padx=5)

        btn_excluir = tk.Button(
            frame_acoes,
            text="Excluir",
            bg="#e74c3c",
            fg="white",
            command=self.excluir_produto,
            font=self.tema["text"]
        )
        btn_excluir.pack(side="left", padx=5)
        
        btn_entrada = tk.Button(
            frame_acoes,
            text="Entrada",
            bg="#2eaccc",
            fg="white",
            command=self.entrada_estoque
        )
        btn_entrada.pack(side="left", padx=5)

        btn_saida = tk.Button(
            frame_acoes,
            text="Saída",
            bg="#2eaccc",
            fg="white",
            command=self.saida_estoque
        )
        btn_saida.pack(side="left", padx=5)

        # CARREGA PRODUTOS
        self.carregar_produtos()
        
    def atualizar_produto(id, codigo, nome, preco_venda, estoque):

        from src.database.database import conectar

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE produtos
            SET codigo = ?, nome = ?, preco_venda = ?, estoque = ?
            WHERE id = ?
        """, (codigo, nome, preco_venda, estoque, id))

        conn.commit()
        conn.close()