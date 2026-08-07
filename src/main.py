import tkinter as tk
#from src.database.database import criar_tabelas
from src.database.init_db import criar_tabelas
from src.ui.splash import SplashScreen
from src.ui.tela_principal import TelaPrincipal
from src.ui.tela_login import TelaLogin
from src.ui.styles import aplicar_estilo
from PIL import Image, ImageTk


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

    login_frame = TelaLogin(root, tema)
    root.bind("<<LoginValido>>", lambda event: iniciar_principal(root, login_frame, tema))


def iniciar_principal(root, login_frame, tema):
    # proteja contra tentativa de destruir um frame já destruído
    try:
        if hasattr(login_frame, 'winfo_exists') and login_frame.winfo_exists():
            login_frame.destroy()
    except Exception:
        pass
    TelaPrincipal(root, tema)


def main():
    # cria banco
    criar_tabelas()

    root = tk.Tk()
    
    icone = ImageTk.PhotoImage(Image.open("assets/integris.png"))
    root.iconphoto(True, icone)
    
    tema = aplicar_estilo(root)

    root.withdraw()

    splash = SplashScreen(root)

    root.after(2500, lambda: iniciar_sistema(root, splash, tema))
    root.mainloop()


if __name__ == "__main__":
    main()