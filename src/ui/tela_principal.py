import os
import random
import tkinter as tk

try:
    import winsound
except ImportError:  # pragma: no cover - ambiente não Windows
    winsound = None

from src.ui.tela_inicio import TelaInicio
from src.ui.tela_produtos import TelaProdutos
from src.ui.tela_movimentacoes import TelaMovimentacoes
from src.ui.tela_vendas import TelaVendas
from src.ui.tela_configuracoes import TelaConfiguracoes
#from src.ui.version import VERSAO

from src.utils.cores import *
from src.utils.formatacao import moeda

from src.modules.db_config import obter_config
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

        self._dica_timer_id = None
        self._baloon_window = None
        self._dicas_ativas = True
        self._dica_intervalo_ms = 300000
        self._alpha_atual = 0.0

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
        self._configurar_dicas_flutuantes()

    def _configurar_dicas_flutuantes(self):
        habilitadas = obter_config("dicas_flutuantes", "1") == "1"
        self._dicas_ativas = habilitadas

        if self._dica_timer_id is not None:
            self.after_cancel(self._dica_timer_id)
            self._dica_timer_id = None

        if self._baloon_window is not None:
            try:
                self._baloon_window.destroy()
            except tk.TclError:
                pass
            self._baloon_window = None

        if habilitadas:
            self._dica_timer_id = self.after(self._dica_intervalo_ms, self._mostrar_dica_aleatoria)

    def _mostrar_dica_aleatoria(self):
        if not self._dicas_ativas:
            return

        if self._baloon_window is not None and self._baloon_window.winfo_exists():
            return

        dicas = [
            "Organize produtos com estoque baixo para evitar faltas.",
            "Revise o histórico de movimentações para acompanhar o fluxo da loja.",
            "Use os relatórios para identificar vendas mais frequentes.",
            "Mantenha as configurações atualizadas para personalizar o sistema.",
            "Cadastre produtos com descrição clara para facilitar buscas futuras."
        ]

        mensagem = random.choice(dicas)
        self._exibir_dica(mensagem)

        self._dica_timer_id = self.after(self._dica_intervalo_ms, self._mostrar_dica_aleatoria)

    def _exibir_dica(self, mensagem):
        if not self._dicas_ativas:
            return

        self.root.update_idletasks()

        self._fechar_dica_flutuante()
        self._baloon_window = tk.Toplevel(self.root)
        self._baloon_window.withdraw()
        self._baloon_window.overrideredirect(True)
        self._baloon_window.attributes("-topmost", True)
        self._baloon_window.configure(bg="#0f172a")

        frame = tk.Frame(self._baloon_window, bg="#111827", bd=0, highlightthickness=0)
        frame.pack(fill="both", padx=10, pady=10)

        content = tk.Frame(frame, bg="#111827")
        content.pack(anchor="w")

        tk.Label(
            content,
            text="💡",
            font=("Segoe UI", 16),
            bg="#111827",
            fg="#fbbf24"
        ).pack(side="left", padx=(0, 8))

        text_frame = tk.Frame(content, bg="#111827")
        text_frame.pack(side="left")

        tk.Label(
            text_frame,
            text="Dica rápida",
            font=("Segoe UI", 10, "bold"),
            bg="#111827",
            fg="#f8fafc"
        ).pack(anchor="w")

        tk.Label(
            text_frame,
            text=mensagem,
            font=("Segoe UI", 10),
            bg="#111827",
            fg="#dbeafe",
            justify="left",
            wraplength=280
        ).pack(anchor="w", pady=(2, 0))

        self._baloon_window.update_idletasks()
        largura = self._baloon_window.winfo_reqwidth()
        altura = self._baloon_window.winfo_reqheight()

        x = self.root.winfo_rootx() + max(20, self.root.winfo_width() - largura - 20)
        y = self.root.winfo_rooty() + max(20, self.root.winfo_height() - altura - 20)
        self._baloon_window.geometry(f"{largura}x{altura}+{x}+{y}")

        try:
            self._baloon_window.attributes("-alpha", 0.0)
        except tk.TclError:
            pass

        self._baloon_window.deiconify()
        self._reproduzir_som_notificacao()
        self._animar_aparecer()
        self.after(4500, self._animar_desaparecer)

    def _animar_aparecer(self):
        if self._baloon_window is None or not self._baloon_window.winfo_exists():
            return

        if self._alpha_atual < 0.9:
            self._alpha_atual = min(0.9, self._alpha_atual + 0.08)
            try:
                self._baloon_window.attributes("-alpha", self._alpha_atual)
            except tk.TclError:
                pass
            self.after(25, self._animar_aparecer)

    def _animar_desaparecer(self):
        if self._baloon_window is None or not self._baloon_window.winfo_exists():
            self._alpha_atual = 0.0
            return

        if self._alpha_atual > 0.0:
            self._alpha_atual = max(0.0, self._alpha_atual - 0.08)
            try:
                self._baloon_window.attributes("-alpha", self._alpha_atual)
            except tk.TclError:
                pass
            self.after(25, self._animar_desaparecer)
        else:
            self._fechar_dica_flutuante()

    def _fechar_dica_flutuante(self):
        if self._baloon_window is not None:
            try:
                self._baloon_window.destroy()
            except tk.TclError:
                pass
        self._baloon_window = None
        self._alpha_atual = 0.0

    def _reproduzir_som_notificacao(self):
        if winsound is None:
            return

        try:
            if hasattr(winsound, "MessageBeep"):
                winsound.MessageBeep()
            elif hasattr(winsound, "Beep"):
                winsound.Beep(1000, 120)
        except Exception:
            pass

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
        self.criar_botao_menu("❓ Ajuda", self.abrir_ajuda)
        
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

    def abrir_ajuda(self):
        self.limpar_tela()

        frame_ajuda = tk.Frame(self.frame_principal, bg=self.tema["card"])
        frame_ajuda.pack(fill="both", expand=True)

        titulo = tk.Label(
            frame_ajuda,
            text="Ajuda",
            font=("Arial", 22, "bold"),
            fg=PRIMARY,
            bg=self.tema["card"]
        )
        titulo.pack(anchor="w", padx=20, pady=(20, 5))

        subtitulo = tk.Label(
            frame_ajuda,
            text="Dicas para usar o sistema de forma simples e eficiente.",
            font=("Arial", 12),
            fg=PRIMARY,
            bg=self.tema["card"]
        )
        subtitulo.pack(anchor="w", padx=20, pady=(0, 20))

        canvas = tk.Canvas(frame_ajuda, bg=self.tema["card"], highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_ajuda, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.tema["card"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 20))
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=(0, 20))

        section_frame = tk.Frame(scrollable_frame, bg=self.tema["card"], bd=0)
        section_frame.pack(fill="x", padx=10, pady=(0, 20))

        header_frame = tk.Frame(section_frame, bg=self.tema["card"])
        header_frame.pack(fill="x", pady=(10, 10), padx=10)

        tk.Label(
            header_frame,
            text="🔎 DICAS RÁPIDAS",
            font=("Arial", 12, "bold"),
            bg=self.tema["card"],
            fg=PRIMARY
        ).pack(anchor="w")

        tk.Frame(header_frame, bg=self.tema["primary"], height=2).pack(fill="x", pady=(5, 0))

        dicas = [
            "1. Use 'Produtos' para cadastrar e editar mercadorias.",
            "2. Em 'Vendas', registre vendas rapidamente e veja o total.",
            "3. Verifique 'Relatórios' para acompanhar movimentações.",
            "4. Ajuste preferências em 'Configurações'.",
            "5. Use o campo de busca em 'Produtos' para encontrar itens rapidamente.",
            "6. Ao cadastrar um produto, preencha todos os campos obrigatórios para evitar erros.",
            "7. Em 'Vendas', selecione o produto e a quantidade correta antes de finalizar a venda.",
            "8. Em 'Relatórios', filtre por datas para visualizar vendas e movimentações específicas.",
            "9. Em 'Configurações', personalize o tema e outras preferências do sistema.",
            "10. Para suporte, entre em contato com o SAC através do telefone ou email fornecido na seção de ajuda.",
            "11. Utilize a função de exportação de relatórios para salvar dados importantes em formatos como CSV ou PDF.",
            "12. Use '.' (ponto) para estabelecer valores decimais."
        ]

        for dica in dicas:
            label = tk.Label(
                section_frame,
                text=dica,
                font=("Arial", 11),
                fg=self.tema["text"],
                bg=self.tema["card"],
                justify="left",
                wraplength=820
            )
            label.pack(anchor="w", padx=20, pady=6)

        contato_section = tk.Frame(scrollable_frame, bg=self.tema["card"], bd=0)
        contato_section.pack(fill="x", padx=10, pady=(0, 20))

        contato_header = tk.Frame(contato_section, bg=self.tema["card"])
        contato_header.pack(fill="x", pady=(10, 10), padx=10)

        tk.Label(
            contato_header,
            text="📞 Suporte ao Cliente (SAC)",
            font=("Arial", 12, "bold"),
            bg=self.tema["card"],
            fg=PRIMARY
        ).pack(anchor="w")

        tk.Frame(contato_header, bg=self.tema["primary"], height=2).pack(fill="x", pady=(5, 0))

        contato = tk.Label(
            contato_section,
            text="Telefone: (35) 98449-8664\nEmail: sac.integris@gmail.com",
            font=("Arial", 11),
            fg=self.tema["text"],
            bg=self.tema["card"],
            justify="left"
        )
        contato.pack(anchor="w", padx=20, pady=(8, 20))

    def abrir_configuracoes(self):
        self.limpar_tela()
        tela = TelaConfiguracoes(self.frame_principal, self.tema)
        tela.pack(fill="both", expand=True)