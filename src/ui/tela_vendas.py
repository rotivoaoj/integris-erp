import tkinter as tk
from tkinter import ttk, messagebox

from src.modules.vendas import buscar_produto_por_codigo, registrar_venda, faturamento_do_dia
from src.utils.cores import *
from src.utils.componentes import botao_padrao
from src.utils.botoes import botao_moderno, botao_menor
from src.utils.formatacao import moeda

class TelaVendas(tk.Frame):

    def __init__(self, master, tema):
        super().__init__(master)
        self.tema = tema
        self.label_faturamento = tk.Label(
        self,
        text="Faturamento hoje: R$ 0.00",
        font=("Arial", 12, "bold"),
        fg="#2c3e50"
        )

        self.configure(bg=BG)
        
        self.label_faturamento.pack()
    
        self.pack(fill="both", expand=True)
        
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

        self.carrinho = []
        
        # =========================
        # TOPO
        # =========================

        frame_topo = tk.Frame(self)
        frame_topo.pack(fill="x", padx=10, pady=10)
        
        tk.Label(frame_topo, text="Qtd").pack(side="left")

        self.entry_qtd = tk.Entry(frame_topo, width=5)
        self.entry_qtd.insert(0, "1")
        self.entry_qtd.pack(side="left", padx=5)

        tk.Label(frame_topo, text="Código do Produto").pack(side="left")

        self.entry_codigo = tk.Entry(frame_topo)
        self.entry_codigo.pack(side="left", padx=5)

        btn_add = botao_menor(
            frame_topo,
            "+ Adicionar",
            self.adicionar_produto,
            "default"
        )
        btn_add.pack(side="left")

        # =========================
        # TABELA CARRINHO
        # =========================

        self.tabela = ttk.Treeview(
            self,
            columns=("produto","quantidade","preco","subtotal"),
            show="headings"
        )

        self.tabela.heading("produto", text="Produto")
        self.tabela.heading("quantidade", text="Qtd")
        self.tabela.heading("preco", text="Preço")
        self.tabela.heading("subtotal", text="Subtotal")

        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

        # =========================
        # TOTAL
        # =========================

        frame_total = tk.Frame(self)
        frame_total.pack(fill="x", padx=10)

        self.label_total = tk.Label(
            frame_total,
            text="Total: R$ 0.00",
            font=("Arial", 16, "bold")
        )

        self.label_total.pack(side="right")

        # =========================
        # BOTÃO FINALIZAR
        # =========================

        btn_finalizar = botao_moderno(
            self,
            "Finalizar Venda",
            self.finalizar_venda,
            "primary"
        )

        btn_finalizar.pack(pady=10)
        
        btn_remover = botao_moderno(
            self,
            "Remover Item",
            self.remover_item,
            "danger"
        )

        btn_remover.pack(pady=5)
        
        btn_relatorio = botao_moderno(
            self,
            "📄 Relatório do Dia",
            self.exportar_relatorio_dia,
            "default"
        )

        btn_relatorio.pack(pady=5)
        
        total_hoje = faturamento_do_dia()
        self.label_faturamento.config(text=f"Faturamento hoje: R$ {total_hoje:.2f}")

    # =========================
    # ADICIONAR PRODUTO
    # =========================

    def adicionar_produto(self):

        codigo = self.entry_codigo.get().strip()
        quantidade = int(self.entry_qtd.get())

        if not codigo:
            return

        produto = buscar_produto_por_codigo(codigo)

        if not produto:
           messagebox.showerror("Erro","Produto não encontrado")
           return

        produto_id, nome, preco, estoque = produto

    # valida estoque
        if quantidade > estoque:
            messagebox.showerror("Erro", "Estoque insuficiente")
            return

    # 🔥 VERIFICA SE JÁ EXISTE NO CARRINHO
        for item in self.carrinho:
            if item["id"] == produto_id:
                item["quantidade"] += quantidade
                self.atualizar_tabela()
                self.atualizar_total()
                return

    # adiciona novo
        self.carrinho.append({
            "id": produto_id,
            "nome": nome,
            "quantidade": quantidade,
            "preco": preco  # Store raw numeric price
        })

        self.atualizar_tabela()
        self.atualizar_total()

    # =========================
    # ATUALIZAR TOTAL
    # =========================

    def atualizar_tabela(self):

        self.tabela.delete(*self.tabela.get_children())

        for item in self.carrinho:
            subtotal = item["preco"] * item["quantidade"]

            self.tabela.insert(
                "",
                "end",
                values=(
                    item["nome"],
                    item["quantidade"],
                    moeda(item["preco"]),  # Format price for display
                    moeda(subtotal)        # Format subtotal for display
            )
        )
    # =========================
    # FINALIZAR VENDA
    # =========================

    def finalizar_venda(self):

        if not self.carrinho:
            messagebox.showwarning("Aviso","Nenhum item na venda")
            return

        registrar_venda(self.carrinho)

        messagebox.showinfo("Sucesso","Venda registrada!")

        self.tabela.delete(*self.tabela.get_children())
        self.carrinho.clear()

        self.atualizar_total()
        
        total_hoje = faturamento_do_dia()
        self.label_faturamento.config(text=f"Faturamento hoje: R$ {total_hoje:.2f}")
        
        self.atualizar_resumo()
        
    def remover_item(self):

        selecionado = self.tabela.selection()

        if not selecionado:
            return

        index = self.tabela.index(selecionado)

        del self.carrinho[index]

        self.atualizar_tabela()
        self.atualizar_total()
        
    def atualizar_total(self):

        total = 0

        for item in self.carrinho:
            total += item["preco"] * item["quantidade"]

        self.label_total.config(text=f"Total: {moeda(total)}")
        
    def atualizar_resumo(self):

        faturamento = faturamento_do_dia()

        self.label_faturamento.config(text=f"R$ {faturamento:.2f}")
        
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