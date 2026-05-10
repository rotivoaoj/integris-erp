import tkinter as tk

from src.modules.vendas import faturamento_do_dia, faturamento_do_mes, vendas_por_dia, vendas_mes_anterior_total, vendas_por_dia_mes_atual
from src.modules.produtos import listar_produtos, valor_total_estoque

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.ui.tela_produtos import TelaProdutos

from src.utils.cores import *
from src.utils.formatacao import moeda


class TelaInicio(tk.Frame):

    def __init__(self, master, tema):
        super().__init__(master)
        self.tema = tema
        self.pack(fill="both", expand=True)
        
        self.configure(bg=BG)

        # =========================
        # TÍTULO
        # =========================

        titulo = tk.Label(
            self,
            text="Bem-vindo(a) ao INTEGRIS",
            font=("Arial", 22, "bold"),
            fg="#2c3e50"
        )
        titulo.pack(pady=20)

        subtitulo = tk.Label(
            self,
            text="Sistema de Gestão de Estoque",
            font=("Arial", 14)
        )
        subtitulo.pack(pady=5)

        # =========================
        # CARDS
        # =========================

        frame_cards = tk.Frame(self, bg=self.tema["bg"])
        frame_cards.pack(fill="x", padx=20, pady=15)

        for i in range(4):
            frame_cards.grid_columnconfigure(i, weight=1)
        
        #def formatar_moeda(valor):
         #   return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        faturamento = faturamento_do_dia()
        total_produtos = len(listar_produtos())
        valor_estoque = valor_total_estoque()
        faturamento_mes = faturamento_do_mes()

        self.label_faturamento = self.criar_card(frame_cards, "Faturamento do Dia", f"R$ {faturamento:.2f}", 0, "#4f92ff", "💰")
        self.label_produtos = self.criar_card(frame_cards, "Produtos", total_produtos, 1, "#4f92ff", "📦")
        self.label_estoque = self.criar_card(frame_cards, "Valor em Estoque", f"R$ {valor_estoque:.2f}", 2, "#4f92ff", "🏬")
        self.label_mes = self.criar_card(frame_cards, "Faturamento do Mês", f"R$ {faturamento_mes:.2f}", 3, "#4f92ff", "📈")

        #========================
        # GRÁFICO 
        #========================

        frame_grafico = tk.Frame(self, bg=self.tema["bg"])
        frame_grafico.pack(fill="both", expand=True)

        self.criar_grafico(frame_grafico)
        
        mes_anterior = vendas_mes_anterior_total()
        mes_atual = faturamento_do_mes()  # se já tiver essa função

        variacao = 0
        if mes_anterior > 0:
            variacao = ((mes_atual - mes_anterior) / mes_anterior) * 100

        texto = f"{variacao:.1f}% em relação ao mês anterior"

        cor = "green" if variacao >= 0 else "red"

        label_variacao = tk.Label(
            self,
            text=texto,
            fg=cor,
            bg=self.tema["bg"],
            font=("Segoe UI", 10, "bold")
        )
        label_variacao.pack(pady=5)
    
        # =========================
        # AÇÕES RÁPIDAS
        # =========================

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=20)

        # ✅ INICIA ATUALIZAÇÃO (CORRETO)
        self.after(1000, self.atualizar_cards)

    def criar_card(self, parent, titulo, valor, coluna, cor="#22c55e", icone=""):

        container = tk.Frame(parent, bg="#0f172a")
        container.grid(row=0, column=coluna, padx=12, pady=8)

        card = tk.Frame(
            container,
            bg=self.tema["card"],
            width=220,
            height=120,
            highlightthickness=2,
            highlightbackground="#374151"
        )
        card.pack(padx=3, pady=3)
        card.pack_propagate(False)

    # Barra colorida
        barra = tk.Frame(card, bg=cor, height=8)
        barra.pack(fill="x")

    # Área interna
        conteudo = tk.Frame(card, bg=self.tema["card"])
        conteudo.pack(fill="both", expand=True, padx=10, pady=10)

    # LINHA SUPERIOR (Ícone + título)
        header = tk.Frame(conteudo, bg=self.tema["card"])
        header.pack(fill="x")

        tk.Label(
            header,
            text=icone,
            bg=self.tema["card"],
            fg=self.tema["text"],
            font=("Segoe UI Emoji", 14)
        ).pack(side="left")

        tk.Label(
            header,
            text=titulo,
            bg=self.tema["card"],
            fg="#9ca3af",
            font=("Segoe UI", 10)
        ).pack(side="left", padx=5)

    # VALOR
        label_valor = tk.Label(
            conteudo,
            text=valor,
            fg=self.tema["text"],
            bg=self.tema["card"],
            font=("Segoe UI", 18, "bold")
        )
        label_valor.pack(anchor="w", pady=(10, 0))

        
        def on_enter(e):
            card.config(highlightbackground=cor)

        def on_leave(e):
            card.config(highlightbackground="#374151")

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        return label_valor
    
    def atualizar_cards(self):

        faturamento = faturamento_do_dia()
        produtos = len(listar_produtos())
        valor_estoque = valor_total_estoque()
        faturamento_mes = faturamento_do_mes()

        self.label_faturamento.config(text=f"R$ {faturamento:.2f}")
        self.label_produtos.config(text=f"{produtos}")
        self.label_estoque.config(text=f"R$ {valor_estoque:.2f}")
        self.label_mes.config(text=f"R$ {faturamento_mes:.2f}")

        # loop contínuo
        self.after(2000, self.atualizar_cards)
        
    def limpar_tela(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        self.frame_principal.update()
        
    def abrir_produtos(self):
        self.limpar_tela()
        tela = TelaProdutos(self.frame_principal)
        tela.pack(fill="both", expand=True)
        
    def criar_grafico(self, parent):

        fig = Figure(figsize=(6, 4.5), dpi=100)
        fig.subplots_adjust(bottom=0.2)

        self.ax = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

        # estilo fixo
        fig.patch.set_facecolor('#111827')
        self.ax.set_facecolor('#1f2937')
        self.ax.tick_params(colors='white')
        self.ax.title.set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')

        self.atualizar_grafico()

    def atualizar_grafico(self):

        dias_atual, valores_atual = vendas_por_dia(0)
        dias_ant, valores_ant = vendas_por_dia(-1)

        self.ax.clear()
        
        self.ax.set_facecolor('#1f2937')
        self.ax.tick_params(colors='white')
        self.ax.title.set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')

    # --- mês atual ---
        if dias_atual:
            self.ax.plot(
                dias_atual,
                valores_atual,
                marker='o',
                linewidth=2,
                label="Mês Atual"
            )
            self.ax.fill_between(dias_atual, valores_atual, alpha=0.2)

    # --- mês anterior ---
        if dias_ant:
            self.ax.plot(
                dias_ant,
                valores_ant,
                linestyle='--',
                linewidth=2,
                label="Mês Anterior"
            )

    # --- estilo ---
        self.ax.set_title("Comparativo de Vendas", pad=15)
        self.ax.set_xlabel("Dia")
        self.ax.set_ylabel("R$")

        self.ax.grid(True, linestyle="--", alpha=0.2)
        self.ax.set_xlim(1, 31)
        
        if valores_atual and valores_ant:

            total_atual = sum(valores_atual)
            total_ant = sum(valores_ant)

            if total_ant > 0:
                variacao = ((total_atual - total_ant) / total_ant) * 100

                cor = "green" if variacao >= 0 else "red"
                sinal = "+" if variacao >= 0 else ""

                texto = f"{sinal}{variacao:.1f}%"

                self.ax.text(
                    1,
                    max(valores_atual),
                    texto,
                    color=cor,
                    fontsize=10,
                    fontweight="bold"
                )
            
        self.ax.set_xlim(1, 31)
        
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        
        self.ax.legend(loc="upper right")

        self.canvas.draw()