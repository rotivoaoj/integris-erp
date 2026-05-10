import tkinter as tk
import os

from src.ui.tela_inicio import TelaInicio
from src.ui.tela_produtos import TelaProdutos
from src.ui.tela_movimentacoes import TelaMovimentacoes
from src.ui.tela_vendas import TelaVendas
from src.ui.tela_configuracoes import TelaConfiguracoes
#from src.ui.version import VERSAO

from src.utils.cores import *
from src.utils.formatacao import moeda


from src.settings.config import VERSAO, AMBIENTE


class TelaPrincipal(tk.Frame):

    def __init__(self, master, tema):
        super().__init__(master)
    
        self.botoes_menu = []
        self.botao_ativo = None
        
        self.root = master  # 🔥 CORREÇÃO AQUI
    
        self.tema = tema
        self.root.title("INTEGRIS")
        self.root.geometry("1200x600")
    
        self.root.configure(bg=PRIMARY)

        # =========================
        # MENU LATERAL
        # =========================
        self.menu_lateral = tk.Frame(self, width=200, bg="#2c3e50")
        self.menu_lateral.pack(side="left", fill="y")

        # =========================
        # AREA PRINCIPAL
        # =========================
        self.frame_principal = tk.Frame(self)
        self.frame_principal.pack(side="right", fill="both", expand=True)

        # 🔥 ADICIONE AQUI
        self.pack(fill="both", expand=True)

        # =========================
        # CRIAR MENU
        # =========================
        self.criar_menu()

    # =========================
    # MENU
    # =========================
    def criar_menu(self):

        titulo = tk.Label(
            self.menu_lateral,
            text="INTEGRIS",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=20)

        self.criar_botao_menu("🏠 Início", self.abrir_inicio)
        self.criar_botao_menu("📦 Produtos", self.abrir_produtos)
        self.criar_botao_menu("💰 Vendas", self.abrir_vendas)
        self.criar_botao_menu("📊 Relatórios", self.abrir_movimentacoes)
        self.criar_botao_menu("⚙️ Configurações", self.abrir_configuracoes)
        
        self.ativar_botao(self.botoes_menu[0], self.abrir_inicio)
        
        # =========================
        # RODAPÉ (VERSÃO)
        # =========================

        rodape = tk.Frame(self.menu_lateral, bg="#2c3e50")
        rodape.pack(side="bottom", fill="x", pady=(0, 15))
        
        cor_ambiente = "#22c55e" if AMBIENTE == "PROD" else "#E9E9E9"

        label_versao = tk.Label(
            rodape,
            text=f"{VERSAO} • {AMBIENTE}",
            bg="#2c3e50",
            fg=cor_ambiente,
            #fg="#9ca3af",  # cinza suave
            font=("Segoe UI", 8, "bold")
        )

        label_versao.pack()
        
    def criar_botao_menu(self, texto, comando):

        btn = tk.Button(
            self.menu_lateral,
            text=texto,
            font=10,
            bg="#1f2937",
            fg="white",
            relief="flat",
            anchor="w",
            padx=35,
            pady=10,
            cursor="hand2"
        )

        btn.pack(fill="x")

        btn.bind("<Button-1>", lambda e, b=btn, cmd=comando: self.ativar_botao(b, cmd))

        self.botoes_menu.append(btn)
        
        def on_enter(e):
            if btn != self.botao_ativo:
                btn.config(bg="#50688a")

        def on_leave(e):
            if btn != self.botao_ativo:
                btn.config(bg="#2c3e50")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        #btn.bind("<Enter>", lambda e: btn.config(bg="#34495e"))
        #btn.bind("<Leave>", lambda e: btn.config(bg="#2c3e50"))
        
    def ativar_botao(self, botao, comando):

        # RESETAR TODOS
        for b in self.botoes_menu:
            b.config(bg="#2c3e50")

        # DESTACAR ATIVO
        botao.config(bg="#415d8a")

        # SALVAR ATIVO
        self.botao_ativo = botao

        # EXECUTAR TELA
        comando()

    # =========================
    # LIMPAR TELA
    # =========================
    def limpar_tela(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        self.frame_principal.update()
    # =========================
    # ABRIR TELAS
    # =========================

    def abrir_inicio(self):
    # limpa tela
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    # recria tela (força atualização)
        tela = TelaInicio(self.frame_principal, self.tema)

    def abrir_produtos(self):
        self.limpar_tela()
        tela = TelaProdutos(self.frame_principal, self.tema)
        tela.pack(fill="both", expand=True)

    def abrir_movimentacoes(self):
        self.limpar_tela()
        tela = TelaMovimentacoes(self.frame_principal, self.tema)
        tela.pack(fill="both", expand=True)

    def abrir_vendas(self):
        self.limpar_tela()
        tela = TelaVendas(self.frame_principal, self.tema)
        tela.pack(fill="both", expand=True)

    def abrir_configuracoes(self):
        self.limpar_tela()
        tela = TelaConfiguracoes(self.frame_principal, self.tema)
        tela.pack(fill="both", expand=True)