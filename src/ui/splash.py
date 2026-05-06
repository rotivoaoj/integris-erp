import tkinter as tk
from tkinter import ttk
import os

class SplashScreen:

    def __init__(self, root):

        self.root = tk.Toplevel(root)
        self.root.overrideredirect(True)

        self.root.lift()
        self.root.attributes("-topmost", True)
        
        largura = 410
        altura = 520
        caminho = os.path.join("assets", "logo_integris.png")

        self.root.update_idletasks()

        x = (self.root.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.root.winfo_screenheight() // 2) - (altura // 2)

        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

        # =========================
        # FRAME PRINCIPAL
        # =========================
        self.frame = tk.Frame(self.root, bg="#111827")
        self.frame.pack(expand=True, fill="both")

        # =========================
        # LOGO
        # =========================

        caminho_logo = os.path.join("assets", "logo_integris.png")
        self.logo = tk.PhotoImage(file=caminho_logo)

        tk.Label(
            self.frame,
            image=self.logo,
            bg="#111827"
        ).pack(pady=(30, 10))

        # =========================
        # TEXTO STATUS
        # =========================
        self.label_status = tk.Label(
            self.frame,
            text="Iniciando sistema...",
            fg="#9ca3af",
            bg="#111827",
            font=("Arial", 10)
        )
        self.label_status.pack(pady=5)

        # =========================
        # PORCENTAGEM
        # =========================
        self.label_porcentagem = tk.Label(
            self.frame,
            text="0%",
            fg="white",
            bg="#111827",
            font=("Arial", 12, "bold")
        )
        self.label_porcentagem.pack()

        # =========================
        # ESTILO DA BARRA
        # =========================
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TProgressbar",
            thickness=10,
            troughcolor="#1f2937",
            background="#22c55e",
            bordercolor="#22c55e",
            lightcolor="#4ade80",
            darkcolor="#16a34a"
        )

        # =========================
        # BARRA
        # =========================
        self.barra = ttk.Progressbar(
            self.frame,
            orient="horizontal",
            length=300,
            mode="determinate",
            style="TProgressbar"
        )
        self.barra.pack(pady=20)


        # inicia animação
        self.progresso = 0
        self.animar()

    # =========================
    # ANIMAÇÃO SUAVE
    # =========================
    def animar(self):

        if self.progresso < 100:

            self.progresso += 1

            self.barra["value"] = self.progresso
            self.label_porcentagem.config(text=f"{self.progresso}%")

            # textos dinâmicos
            if self.progresso < 30:
                self.label_status.config(text="Carregando módulos...")
            elif self.progresso < 60:
                self.label_status.config(text="Conectando ao banco...")
            elif self.progresso < 90:
                self.label_status.config(text="Inicializando interface...")
            elif self.progresso == 100:
                self.label_status.config(text="Concluído")

            # velocidade da animação
            self.root.after(20, self.animar)
            
    def atualizar(self, valor, texto):

        self.barra["value"] = valor
        self.label_porcentagem.config(text=f"{valor}%")
        self.label_status.config(text=texto)

        self.root.update_idletasks()
