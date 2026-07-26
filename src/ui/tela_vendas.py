import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from datetime import datetime

from src.modules.vendas import buscar_produto_por_codigo, registrar_venda, faturamento_do_dia
from src.utils.cores import *
from src.utils.componentes import botao_padrao
from src.utils.botoes import botao_moderno, botao_menor
from src.utils.formatacao import moeda, data_hora_brasileira

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from src.utils.formatacao import data_hora_brasileira

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

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
            "📄 Relatório de Hoje",
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

    def exportar_relatorio_dia(self):

        # Pega vendas do dia
        try:
            from src.modules.vendas import listar_vendas_do_dia
        except Exception:
            messagebox.showerror("Erro", "Não foi possível carregar dados de vendas")
            return

        vendas = listar_vendas_do_dia()

        if not vendas:
            messagebox.showinfo("Relatório", "Nenhuma venda encontrada para hoje")
            return

        # Pergunta onde salvar
        caminho = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Salvar Relatório do Dia"
        )

        if not caminho:
            return

        # Monta documento
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(caminho, pagesize=A4)

        elementos = []

        titulo = Paragraph("<b>INTEGRIS ERP</b><br/>Relatório de Vendas - Hoje", 
                           styles["Title"])
        elementos.append(titulo)
        elementos.append(Spacer(1, 12))

        elementos.append(Paragraph(
            f"Gerado em: {data_hora_brasileira(datetime.utcnow()).replace(' 00:00:00', '')}",
            styles["Normal"]
        ))
        elementos.append(Spacer(1, 12))

        total_geral = 0
        venda_atual = None
        venda_total_atual = 0
        dados_tabela = []

        for venda_id, venda_total, venda_data, produto_id, nome, quantidade, preco_unit, subtotal in vendas:
            if venda_id != venda_atual:
                if venda_atual is not None and len(dados_tabela) > 1:
                    t = Table(dados_tabela, colWidths=[220, 60, 80, 80])
                    t.setStyle(TableStyle([
                        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                        ("ALIGN", (1, 1), (3, -1), "RIGHT")
                    ]))
                    elementos.append(t)
                    elementos.append(Spacer(1, 6))
                    elementos.append(Paragraph(
                        f"Total da venda: R$ {venda_total_atual:.2f}",
                        styles["Normal"]
                    ))
                    elementos.append(Spacer(1, 12))

                venda_atual = venda_id
                venda_total_atual = venda_total or 0
                total_geral += venda_total_atual

                elementos.append(Paragraph(
                    f"<b>Venda #{venda_id}</b> - {data_hora_brasileira(venda_data)}",
                    styles["Heading3"]
                ))
                elementos.append(Spacer(1, 6))

                dados_tabela = [["Produto", "Qtd", "Preço", "Subtotal"]]

            dados_tabela.append([
                nome,
                str(quantidade),
                moeda(preco_unit),
                moeda(subtotal)
            ])

        if venda_atual is not None and len(dados_tabela) > 1:
            t = Table(dados_tabela, colWidths=[220, 60, 80, 80])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("ALIGN", (1, 1), (3, -1), "RIGHT")
            ]))
            elementos.append(t)
            elementos.append(Spacer(1, 6))
            elementos.append(Paragraph(
                f"Total da venda: R$ {venda_total_atual:.2f}",
                styles["Normal"]
            ))
            elementos.append(Spacer(1, 12))

        elementos.append(Paragraph(f"<b>Total do dia:</b> R$ {total_geral:.2f}", styles["Normal"]))

        try:
            doc.build(elementos)
            messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar PDF: {e}")