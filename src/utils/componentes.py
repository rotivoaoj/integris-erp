import tkinter as tk
from src.utils.cores import *

def botao_padrao(parent, texto, comando, cor=ACCENT):
    return tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=cor,
        fg="white",
        font=("Arial", 10, "bold"),
        bd=0,
        padx=10,
        pady=5,
        cursor="hand2"
    )