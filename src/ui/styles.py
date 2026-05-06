import tkinter as tk
from tkinter import ttk


def aplicar_estilo(root):

    # =========================
    # CORES PADRÃO
    # =========================
    cor_fundo = "#111827"
    cor_card = "#ffffff"
    cor_texto = "#000000"
    cor_secundaria = "#9ca3af"
    cor_primaria = "#22c55e"
    cor_erro = "#ef4444"

    root.configure(bg=cor_fundo)

    # =========================
    # FONTES
    # =========================
    fonte_padrao = ("Segoe UI", 10)
    fonte_titulo = ("Segoe UI", 16, "bold")

    # =========================
    # STYLE (TTK)
    # =========================
    style = ttk.Style()
    style.theme_use("clam")

    # BOTÃO
    style.configure(
        "TButton",
        font=fonte_padrao,
        padding=8,
        background=cor_card,
        foreground=cor_texto,
        borderwidth=0
    )

    style.map(
        "TButton",
        background=[("active", cor_primaria)]
    )

    # ENTRY
    style.configure(
        "TEntry",
        padding=6
    )

    # TREEVIEW
    style.configure(
        "Treeview",
        background=cor_card,
        foreground=cor_texto,
        rowheight=28,
        fieldbackground=cor_card
    )

    style.configure(
        "Treeview.Heading",
        font=fonte_padrao,
        background="#374151",
        foreground="white"
    )

    return {
        "bg": cor_fundo,
        "card": cor_card,
        "text": cor_texto,
        "primary": cor_primaria,
        "error": cor_erro,
        "font": fonte_padrao,
        "title": ("Arial", 16, "bold")
    }

def botao_primario(master, texto, comando):
    return tk.Button(
        master,
        text=texto,
        command=comando,
        bg="#22c55e",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padx=10,
        pady=5
    )