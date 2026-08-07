import os
import tkinter as tk
from PIL import Image, ImageTk

from src.modules.auth import validar_chave, existe_usuario, criar_usuario_inicial
from src.utils.cores import BG, PRIMARY, WHITE, DANGER


class TelaLogin(tk.Frame):

    def __init__(self, master, tema):
        super().__init__(master)

        self.master = master
        self.tema = tema
        self.configure(bg=BG)
        self.pack(fill="both", expand=True)

        self._construir_interface()

    def _construir_interface(self):
        frame_login = tk.Frame(self, bg=BG)
        frame_login.pack(fill="both", expand=True)
        frame_login.grid_rowconfigure(0, weight=1)
        frame_login.grid_columnconfigure(0, weight=1)
        frame_login.grid_columnconfigure(1, weight=1)

        frame_esquerdo = tk.Frame(frame_login, bg=PRIMARY)
        frame_esquerdo.grid(row=0, column=0, sticky="nsew")
        frame_esquerdo.grid_rowconfigure(0, weight=1)
        frame_esquerdo.grid_columnconfigure(0, weight=1)

        frame_direito = tk.Frame(frame_login, bg=WHITE)
        frame_direito.grid(row=0, column=1, sticky="nsew")
        frame_direito.grid_rowconfigure(0, weight=1)
        frame_direito.grid_columnconfigure(0, weight=1)

        esquerda_interna = tk.Frame(frame_esquerdo, bg=PRIMARY)
        esquerda_interna.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        esquerda_interna.grid_rowconfigure(0, weight=1)
        esquerda_interna.grid_columnconfigure(0, weight=1)

        direita_interna = tk.Frame(frame_direito, bg=WHITE)
        direita_interna.grid(row=0, column=0, sticky="nsew", padx=60, pady=40)
        direita_interna.grid_rowconfigure(0, weight=1)
        direita_interna.grid_columnconfigure(0, weight=1)

        # Logo e texto de branding
        try:
            projeto_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            assets_dir = os.path.normpath(os.path.join(projeto_root, "assets"))
            possiveis_logos = [
                "new_integris.png",
                "icon_integris.png",
                "logo_integris.png",
                "integris.png",
            ]
            caminho_logo = next(
                (os.path.join(assets_dir, nome) for nome in possiveis_logos
                 if os.path.exists(os.path.join(assets_dir, nome))),
                None
            )
            if not caminho_logo:
                raise FileNotFoundError(f"Arquivo de logo não encontrado em {assets_dir}")

            imagem_logo = Image.open(caminho_logo).convert("RGBA")
            imagem_logo = imagem_logo.resize((510, 319), Image.LANCZOS)
            self.logo_imagem = ImageTk.PhotoImage(imagem_logo)
            tk.Label(
                esquerda_interna,
                image=self.logo_imagem,
                bg=PRIMARY,
                justify="center"
            ).pack(pady=(40, 10))
        except Exception as exc:
            print("Erro ao carregar logo de login:", exc)
            tk.Label(
                esquerda_interna,
                text="Bem-vindo(a) ao INTEGRIS",
                font=("Segoe UI", 28, "bold"),
                fg=WHITE,
                bg=PRIMARY
            ).pack(pady=(60, 10))

        tk.Label(
            esquerda_interna,
            text="Desenvolvido por Pimatec Soluções © 2026",
            font=("Segoe UI", 9),
            fg="#d1d5db",
            bg=PRIMARY,
            anchor="center",
            justify="center"
        ).pack(side="bottom", fill="x", padx=20, pady=(10, 0))

        # Campos de login
        titulo = tk.Label(
            direita_interna,
            text="Acesso",
            font=("Segoe UI", 20, "bold"),
            fg=PRIMARY,
            bg=WHITE
        )
        titulo.pack(pady=(40, 12))

        descricao = tk.Label(
            direita_interna,
            text="Digite a sua chave de segurança para entrar no sistema.",
            font=("Segoe UI", 11),
            fg="#475569",
            bg=WHITE,
            wraplength=320,
            justify="left"
        )
        descricao.pack(pady=(0, 20), padx=20)

        self.entry_chave = tk.Entry(
            direita_interna,
            show="*",
            width=32,
            font=("Segoe UI", 12),
            bd=1,
            relief="solid",
            justify="center"
        )
        self.entry_chave.pack(pady=(0, 10), ipady=8, padx=20)
        self.entry_chave.focus_set()

        self.botao_entrar = tk.Button(
            direita_interna,
            text="Entrar",
            bg=PRIMARY,
            fg=WHITE,
            font=("Segoe UI", 11, "bold"),
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
            command=self._on_entrar
        )
        self.botao_entrar.pack(pady=(10, 6), padx=20, fill="x")

        self.botao_registrar = tk.Button(
            direita_interna,
            text="Cadastrar chave inicial",
            bg="#6b7280",
            fg=WHITE,
            font=("Segoe UI", 10),
            bd=0,
            padx=10,
            pady=10,
            cursor="hand2",
            command=self._on_registrar
        )
        self.botao_registrar.pack(pady=(0, 6), padx=20, fill="x")

        self.label_status = tk.Label(
            direita_interna,
            text="",
            font=("Segoe UI", 10),
            fg=DANGER,
            bg=WHITE,
            wraplength=320,
            justify="left"
        )
        self.label_status.pack(padx=20, pady=(10, 0), anchor="w")

        if not existe_usuario():
            self.label_status.configure(
                text="Ainda não há chave configurada. Cadastre a chave inicial abaixo.",
                fg=PRIMARY
            )

    def _on_registrar(self):
        chave = self.entry_chave.get().strip()
        if not chave:
            self.label_status.configure(text="Informe a chave para cadastrar.")
            return

        if existe_usuario():
            self.label_status.configure(text="Já existe uma chave cadastrada.")
            return

        criar_usuario_inicial(chave)
        self.label_status.configure(
            text="Chave inicial registrada com sucesso. Agora faça login.",
            fg=PRIMARY
        )
        self.entry_chave.delete(0, tk.END)

    def _on_entrar(self):
        chave = self.entry_chave.get().strip()
        if not chave:
            self.label_status.configure(text="Informe a chave de segurança.")
            return

        if validar_chave(chave):
            # remove a tela de login primeiro para evitar que os dois frames
            # fiquem visíveis ao mesmo tempo caso haja alguma condição de
            # corrida na geração do evento
            try:
                self.destroy()
            except Exception:
                pass
            self.master.event_generate("<<LoginValido>>")
        else:
            self.label_status.configure(text="Chave inválida. Tente novamente.")
            self.entry_chave.delete(0, tk.END)
