import tkinter as tk
#from src.database.database import criar_tabelas
from src.database.init_db import criar_tabelas
from src.ui.splash import SplashScreen
from src.ui.tela_principal import TelaPrincipal
from src.ui.styles import aplicar_estilo

def centralizar_janela(root, largura=1200, altura=600):

    root.update_idletasks()

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    x = (screen_w // 2) - (largura // 2)
    y = (screen_h // 2) - (altura // 2)

    root.geometry(f"{largura}x{altura}+{x}+{y}")

def iniciar_sistema(root, splash, tema):

    splash.root.destroy()

    root.deiconify()
    root.overrideredirect(False)
    centralizar_janela(root, 1200, 600)

    TelaPrincipal(root, tema)


def main():
    # cria banco
    criar_tabelas()

    root = tk.Tk()
    tema = aplicar_estilo(root)

    root.withdraw()

    splash = SplashScreen(root)

    root.after(2500, lambda: iniciar_sistema(root, splash, tema))
    root.mainloop()


if __name__ == "__main__":
    main()