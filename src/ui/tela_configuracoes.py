import tkinter as tk
from tkinter import messagebox
from tkinter import BooleanVar

from src.modules.db_config import salvar_config, obter_config
from src.utils.formatacao import moeda
from src.utils.cores import PRIMARY, SECONDARY, ACCENT, SUCCESS, WARNING, BG, WHITE


class ToggleButton(tk.Frame):
    """Modern toggle button widget with smooth animation"""
    
    def __init__(self, master, command=None, initial_state=False, **kwargs):
        super().__init__(master, **kwargs)
        
        self.command = command
        self.state = BooleanVar(value=initial_state)
        self.is_on = initial_state
        self.animating = False
        self.current_pos = 18 if initial_state else 2
        
        # Create canvas for toggle switch (smaller size)
        self.canvas = tk.Canvas(
            self,
            width=40,
            height=22,
            bg="white",
            highlightthickness=1,
            highlightbackground="#ddd",
            cursor="hand2"
        )
        self.canvas.pack(side="left", padx=5)
        self.canvas.bind("<Button-1>", self._toggle)
        
        self.update_appearance()
    
    def _toggle(self, event=None):
        if self.animating:
            return
        
        self.is_on = not self.is_on
        self.state.set(self.is_on)
        self._animate()
        if self.command:
            self.command()
    
    def _animate(self):
        """Smooth animation for toggle"""
        self.animating = True
        target_pos = 18 if self.is_on else 2
        step = 1 if self.is_on else -1
        
        def animate_frame():
            if (step > 0 and self.current_pos < target_pos) or (step < 0 and self.current_pos > target_pos):
                self.current_pos += step
                self.update_appearance()
                self.after(15, animate_frame)
            else:
                self.current_pos = target_pos
                self.animating = False
                self.update_appearance()
        
        animate_frame()
    
    def update_appearance(self):
        self.canvas.delete("all")
        
        if self.is_on:
            bg_color = SUCCESS
        else:
            bg_color = "#ccc"
        
        # Draw rounded background manually
        radius = 11
        self.canvas.create_oval(0, 0, radius * 2, 22, fill=bg_color, outline=bg_color)
        self.canvas.create_oval(40 - radius * 2, 0, 40, 22, fill=bg_color, outline=bg_color)
        self.canvas.create_rectangle(radius, 0, 40 - radius, 22, fill=bg_color, outline=bg_color)

        # Draw circle
        circle_size = 18
        self.canvas.create_oval(
            self.current_pos,
            2,
            self.current_pos + circle_size,
            20,
            fill=WHITE,
            outline=WHITE
        )
    
    def get(self):
        return self.is_on
    
    def set(self, value):
        self.is_on = value
        self.state.set(value)
        self.current_pos = 18 if value else 2
        self.update_appearance()


class TelaConfiguracoes(tk.Frame):

    def __init__(self, master, tema):
        super().__init__(master)

        self.pack(fill="both", expand=True)
        self.tema = tema
        self.configure(bg=BG)

        # Header
        header = tk.Label(
            self,
            text="Configurações do Sistema",
            font=("Arial", 18, "bold"),
            bg=BG,
            fg=PRIMARY
        )
        header.pack(pady=(15, 20), padx=20)

        # Conteudo da area scrollavel
        canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Roda de scroll do mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 20))
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=(0, 20))

        # ===== SEÇÃO DE ALERTAS =====
        self._create_section_header(scrollable_frame, "🔔 ALERTAS E NOTIFICAÇÕES")

        alerts_frame = tk.Frame(scrollable_frame, bg=WHITE, relief=tk.FLAT, bd=0)
        alerts_frame.pack(fill="x", pady=(0, 20))

        self.var_alerta_estoque = BooleanVar()
        self.var_alerta_entrada = BooleanVar()
        self.var_alerta_saida = BooleanVar()
        self.var_dicas_flutuantes = BooleanVar()

        self.var_alerta_estoque.set(obter_config("alerta_estoque", "1") == "1")
        self.var_alerta_entrada.set(obter_config("alerta_entrada", "1") == "1")
        self.var_alerta_saida.set(obter_config("alerta_saida", "1") == "1")
        self.var_dicas_flutuantes.set(obter_config("dicas_flutuantes", "1") == "1")

        # Alerta 1
        self._create_toggle_item(
            alerts_frame,
            "Alerta visual de estoque baixo",
            "Notifica quando o estoque fica igual/abaixo do mínimo",
            self.var_alerta_estoque
        )

        # Alerta 2
        self._create_toggle_item(
            alerts_frame,
            "Destacar entradas no histórico",
            "Ressalta movimentações de entrada em verde",
            self.var_alerta_entrada
        )

        # Alerta 3
        self._create_toggle_item(
            alerts_frame,
            "Destacar saídas/vendas no histórico",
            "Ressalta movimentações de saída em vermelho",
            self.var_alerta_saida
        )

        self._create_toggle_item(
            alerts_frame,
            "Dicas flutuantes animadas",
            "Mostra balões de dicas no canto inferior direito a cada 5 minutos",
            self.var_dicas_flutuantes
        )

        # ===== SEÇÃO DE ESTOQUE =====
        self._create_section_header(scrollable_frame, "📦 CONFIGURAÇÕES DE ESTOQUE")

        estoque_frame = tk.Frame(scrollable_frame, bg=WHITE, relief=tk.FLAT, bd=0)
        estoque_frame.pack(fill="x", pady=(0, 20))

        # Estoque mínimo input
        input_frame = tk.Frame(estoque_frame, bg=WHITE)
        input_frame.pack(fill="x", padx=15, pady=15)

        label_frame = tk.Frame(input_frame, bg=WHITE)
        label_frame.pack(fill="x", pady=(0, 8))

        tk.Label(
            label_frame,
            text="Estoque Mínimo Padrão",
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=PRIMARY
        ).pack(anchor="w")

        tk.Label(
            label_frame,
            text="Define o limite mínimo padrão para novos produtos",
            font=("Arial", 9),
            bg=WHITE,
            fg=SECONDARY
        ).pack(anchor="w")

        self.entry_minimo = tk.Entry(
            input_frame,
            font=("Arial", 11),
            width=15,
            bd=1,
            relief=tk.SOLID,
            bg=WHITE,
            fg=PRIMARY
        )
        self.entry_minimo.pack(anchor="w", pady=(8, 0))

        self.entry_minimo.insert(0, obter_config("estoque_minimo", "5"))

        # ===== BOTÃO SALVAR (FIXED AT BOTTOM) =====
        button_frame = tk.Frame(self, bg=BG)
        button_frame.pack(fill="x", padx=20, pady=15)

        tk.Button(
            button_frame,
            text="💾 Salvar Configurações",
            bg=SUCCESS,
            fg=WHITE,
            font=("Arial", 11, "bold"),
            command=self.salvar,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground="#229954"
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            button_frame,
            text="❌ Cancelar",
            bg="#95a5a6",
            fg=WHITE,
            font=("Arial", 11, "bold"),
            command=self._cancelar,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground="#7f8c8d"
        ).pack(side="left")

    def _create_section_header(self, parent, text):
        """Cria uma seçao de header com underline"""
        header_frame = tk.Frame(parent, bg=BG)
        header_frame.pack(fill="x", pady=(15, 10))

        tk.Label(
            header_frame,
            text=text,
            font=("Arial", 12, "bold"),
            bg=BG,
            fg=PRIMARY
        ).pack(anchor="w")

        divider = tk.Frame(header_frame, bg=ACCENT, height=2)
        divider.pack(fill="x", pady=(5, 0))

    def _create_toggle_item(self, parent, title, description, var):
        """Cria um item toggle com titulo e descricao"""
        item_frame = tk.Frame(parent, bg=WHITE)
        item_frame.pack(fill="x", padx=15, pady=12)

        # Left side: text
        text_frame = tk.Frame(item_frame, bg=WHITE)
        text_frame.pack(side="left", fill="both", expand=True)

        tk.Label(
            text_frame,
            text=title,
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=PRIMARY
        ).pack(anchor="w")

        tk.Label(
            text_frame,
            text=description,
            font=("Arial", 9),
            bg=WHITE,
            fg=SECONDARY
        ).pack(anchor="w")

        # Right side: toggle
        toggle = ToggleButton(
            item_frame,
            initial_state=var.get(),
            bg=WHITE
        )
        toggle.pack(side="right", padx=(10, 0))

        # Sincroniza o toggle com uma variavel
        def update_var():
            var.set(toggle.get())

        toggle.command = update_var

    def salvar(self):
        minimo = self.entry_minimo.get()

        if not minimo.isdigit():
            messagebox.showerror("Erro", "Digite um número válido para o estoque mínimo")
            return

        salvar_config("estoque_minimo", minimo)
        salvar_config("alerta_estoque", "1" if self.var_alerta_estoque.get() else "0")
        salvar_config("alerta_entrada", "1" if self.var_alerta_entrada.get() else "0")
        salvar_config("alerta_saida", "1" if self.var_alerta_saida.get() else "0")
        salvar_config("dicas_flutuantes", "1" if self.var_dicas_flutuantes.get() else "0")

        parent = self.master
        while parent is not None:
            if hasattr(parent, "_configurar_dicas_flutuantes"):
                parent._configurar_dicas_flutuantes()
                break
            parent = getattr(parent, "master", None)

        messagebox.showinfo("Sucesso", "✓ Configurações salvas com sucesso!")

    def _cancelar(self):
        """Cancela e retorna pra tela principal"""
        parent = getattr(self.master, "master", None)
        if parent and hasattr(parent, "abrir_inicio"):
            parent.abrir_inicio()
        else:
            messagebox.showwarning("Atenção", "Não foi possível retornar à tela principal.")