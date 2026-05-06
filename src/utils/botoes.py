import tkinter as tk

# =========================
# CORES BASE
# =========================
CORES = {
    "primary": "#3b82f6",
    "primary_hover": "#2563eb",

    "success": "#22c55e",
    "success_hover": "#16a34a",

    "danger": "#ef4444",
    "danger_hover": "#dc2626",

    "warning": "#f59e0b",
    "warning_hover": "#d97706",

    "secondary": "#374151",
    "secondary_hover": "#1f2937",

    "default": "#494949",
    "default_hover": "#383838",
    
    "disabled": "#9ca3af"
}


# =========================
# BOTÃO MODERNO
# =========================
def botao_moderno(master, texto, comando, tipo="primary", largura=12):

    cor = CORES.get(tipo, CORES["primary"])
    cor_hover = CORES.get(f"{tipo}_hover", cor)

    btn = tk.Button(
        master,
        text=texto,
        command=comando,
        bg=cor,
        fg="white",
        activebackground=cor_hover,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 10),
        width=largura,
        padx=10,
        pady=6
    )
    
     # =========================
    # HOVER
    # =========================
    def on_enter(e):
        btn.config(bg=cor_hover)

    def on_leave(e):
        btn.config(bg=cor)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    # =========================
    # CLICK (efeito pressionado)
    # =========================
    def on_press(e):
        btn.config(bg="#111827")

    def on_release(e):
        btn.config(bg=cor_hover)

    btn.bind("<ButtonPress-1>", on_press)
    btn.bind("<ButtonRelease-1>", on_release)

    return btn
    
def botao_menor(master, texto, comando, tipo="default", largura=8):

    cor = CORES.get(tipo, CORES["default"])
    cor_hover = CORES.get(f"{tipo}_hover", cor)

    btn = tk.Button(
        master,
        text=texto,
        command=comando,
        bg=cor,
        fg="white",
        activebackground=cor_hover,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 10),
        width=largura,
        padx=6,
        pady=4
    )

    # =========================
    # HOVER
    # =========================
    def on_enter(e):
        btn.config(bg=cor_hover)

    def on_leave(e):
        btn.config(bg=cor)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    # =========================
    # CLICK (efeito pressionado)
    # =========================
    def on_press(e):
        btn.config(bg="#111827")

    def on_release(e):
        btn.config(bg=cor_hover)

    btn.bind("<ButtonPress-1>", on_press)
    btn.bind("<ButtonRelease-1>", on_release)

    return btn


# =========================
# DESABILITAR BOTÃO
# =========================
def desabilitar(btn):
    btn.config(
        state="disabled",
        bg=CORES["disabled"],
        cursor="arrow"
    )


def habilitar(btn, tipo="primary"):
    cor = CORES.get(tipo, CORES["primary"])
    btn.config(
        state="normal",
        bg=cor,
        cursor="hand2"
    )