import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import sv_ttk  # Biblioteca para temas modernos

class ModernButton(ttk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style = ttk.Style()
        self.style.configure('Modern.TButton', 
                           font=('Segoe UI', 10),
                           padding=8,
                           relief='flat')
        self.configure(style='Modern.TButton')

class Card(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.style = ttk.Style()
        self.style.configure('Card.TFrame', 
                           background='#2A2D37',
                           borderwidth=0,
                           relief='solid',
                           padding=15)
        self.configure(style='Card.TFrame')
        
        # Efeito de hover
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        self.style.configure('Card.TFrame', background='#323641')
        
    def on_leave(self, e):
        self.style.configure('Card.TFrame', background='#2A2D37')

class IdeaApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.create_db()
        
    def setup_ui(self):
        # Configuração da janela principal
        self.root.title("IdeaFlow SaaS")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Centralizar janela
        self.center_window()
        
        # Configurar tema dark moderno
        sv_ttk.set_theme("dark")
        
        # Fonte moderna
        self.font_normal = ('Segoe UI', 10)
        self.font_bold = ('Segoe UI', 10, 'bold')
        self.font_title = ('Segoe UI', 14, 'bold')
        
        # Layout principal
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = ttk.Frame(self.main_container, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Logo
        self.logo = ttk.Label(self.sidebar, text="🚀 IdeaFlow", font=('Segoe UI', 18, 'bold'))
        self.logo.pack(pady=(20, 30))
        
        # Menu lateral
        self.btn_new = ModernButton(self.sidebar, text="+ Nova Ideia", command=self.show_add_idea)
        self.btn_new.pack(fill=tk.X, pady=5)
        
        self.separator = ttk.Separator(self.sidebar)
        self.separator.pack(fill=tk.X, pady=15)
        
        self.filter_all = ttk.Radiobutton(self.sidebar, text="Todas", value=1, command=self.update_list)
        self.filter_all.pack(anchor=tk.W)
        
        self.filter_active = ttk.Radiobutton(self.sidebar, text="Ativas", value=2, command=self.update_list)
        self.filter_active.pack(anchor=tk.W)
        
        self.filter_completed = ttk.Radiobutton(self.sidebar, text="Concluídas", value=3, command=self.update_list)
        self.filter_completed.pack(anchor=tk.W)
        
        # Área de conteúdo
        self.content = ttk.Frame(self.main_container)
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)
        
        # Barra de ferramentas
        self.toolbar = ttk.Frame(self.content)
        self.toolbar.pack(fill=tk.X, pady=(0, 15))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.toolbar, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.update_list)
        
        self.btn_refresh = ModernButton(self.toolbar, text="Atualizar", command=self.update_list)
        self.btn_refresh.pack(side=tk.LEFT, padx=5)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(self.content, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.content, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to scroll
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Status bar
        self.status = ttk.Label(self.root, text="Pronto", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_db(self):
        self.conn = sqlite3.connect("ideias.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ideias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                notas TEXT,
                concluida INTEGER DEFAULT 0,
                data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        self.update_list()
        
    def show_add_idea(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Nova Ideia")
        self.add_window.geometry("500x300")
        self.center_child_window(self.add_window)
        
        container = ttk.Frame(self.add_window)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(container, text="Nova Ideia", font=self.font_title).pack(pady=(0, 20))
        
        ttk.Label(container, text="Título:", font=self.font_bold).pack(anchor=tk.W)
        self.idea_title = ttk.Entry(container, font=self.font_normal)
        self.idea_title.pack(fill=tk.X, pady=5, ipady=5)
        
        ttk.Label(container, text="Detalhes:", font=self.font_bold).pack(anchor=tk.W, pady=(10, 0))
        self.idea_details = tk.Text(container, font=self.font_normal, height=8, wrap=tk.WORD)
        self.idea_details.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        ModernButton(btn_frame, text="Cancelar", command=self.add_window.destroy).pack(side=tk.RIGHT, padx=5)
        ModernButton(btn_frame, text="Salvar", style='Accent.TButton', command=self.save_idea).pack(side=tk.RIGHT)
        
    def center_child_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
        
    def save_idea(self):
        title = self.idea_title.get()
        details = self.idea_details.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showwarning("Aviso", "O título é obrigatório!")
            return
            
        self.cursor.execute("INSERT INTO ideias (nome, notas) VALUES (?, ?)", (title, details))
        self.conn.commit()
        self.update_list()
        self.add_window.destroy()
        self.show_status("Ideia criada com sucesso!")
        
    def update_list(self, event=None):
        # Limpar cards existentes
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Obter filtro
        filter_type = 1
        if hasattr(self, 'filter_all'):
            if self.filter_all.instate(['selected']):
                filter_type = 1
            elif self.filter_active.instate(['selected']):
                filter_type = 2
            elif self.filter_completed.instate(['selected']):
                filter_type = 3
                
        # Obter termo de busca
        search_term = self.search_var.get().lower()
        
        # Consultar ideias
        if filter_type == 1:
            self.cursor.execute("SELECT id, nome, notas, concluida FROM ideias")
        elif filter_type == 2:
            self.cursor.execute("SELECT id, nome, notas, concluida FROM ideias WHERE concluida = 0")
        else:
            self.cursor.execute("SELECT id, nome, notas, concluida FROM ideias WHERE concluida = 1")
            
        ideas = self.cursor.fetchall()
        
        # Aplicar busca
        if search_term:
            ideas = [idea for idea in ideas if search_term in idea[1].lower() or search_term in (idea[2] or "").lower()]
            
        # Mostrar cards
        if not ideas:
            empty_label = ttk.Label(self.scrollable_frame, text="Nenhuma ideia encontrada", font=self.font_normal)
            empty_label.pack(pady=50)
        else:
            for idea in ideas:
                self.create_idea_card(idea)
                
    def create_idea_card(self, idea):
        card = Card(self.scrollable_frame)
        card.pack(fill=tk.X, pady=5)
        
        # Header
        header = ttk.Frame(card)
        header.pack(fill=tk.X)
        
        title = ttk.Label(header, text=idea[1], font=self.font_bold)
        title.pack(side=tk.LEFT, anchor=tk.W)
        
        # Status badge
        status = ttk.Label(header, text="✔ Concluída" if idea[3] else "◌ Pendente", 
                          foreground="#4CAF50" if idea[3] else "#FF9800")
        status.pack(side=tk.RIGHT, padx=5)
        
        # Content
        if idea[2]:  # Se houver detalhes
            content = ttk.Label(card, text=idea[2], wraplength=700, font=self.font_normal)
            content.pack(fill=tk.X, pady=5, anchor=tk.W)
            
        # Actions
        actions = ttk.Frame(card)
        actions.pack(fill=tk.X, pady=(10, 0))
        
        ModernButton(actions, text="Editar", command=lambda i=idea[0]: self.edit_idea(i)).pack(side=tk.LEFT, padx=2)
        
        if idea[3]:
            ModernButton(actions, text="Reabrir", command=lambda i=idea[0]: self.toggle_idea(i)).pack(side=tk.LEFT, padx=2)
        else:
            ModernButton(actions, text="Concluir", style='Accent.TButton', 
                       command=lambda i=idea[0]: self.toggle_idea(i)).pack(side=tk.LEFT, padx=2)
            
        ModernButton(actions, text="Excluir", command=lambda i=idea[0]: self.delete_idea(i)).pack(side=tk.LEFT, padx=2)
        
    def edit_idea(self, idea_id):
        self.cursor.execute("SELECT nome, notas FROM ideias WHERE id = ?", (idea_id,))
        idea = self.cursor.fetchone()
        
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Editar Ideia")
        self.edit_window.geometry("500x300")
        self.center_child_window(self.edit_window)
        
        container = ttk.Frame(self.edit_window)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(container, text="Editar Ideia", font=self.font_title).pack(pady=(0, 20))
        
        ttk.Label(container, text="Título:", font=self.font_bold).pack(anchor=tk.W)
        self.edit_title = ttk.Entry(container, font=self.font_normal)
        self.edit_title.insert(0, idea[0])
        self.edit_title.pack(fill=tk.X, pady=5, ipady=5)
        
        ttk.Label(container, text="Detalhes:", font=self.font_bold).pack(anchor=tk.W, pady=(10, 0))
        self.edit_details = tk.Text(container, font=self.font_normal, height=8, wrap=tk.WORD)
        self.edit_details.insert("1.0", idea[1] or "")
        self.edit_details.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        ModernButton(btn_frame, text="Cancelar", command=self.edit_window.destroy).pack(side=tk.RIGHT, padx=5)
        ModernButton(btn_frame, text="Salvar", style='Accent.TButton', 
                   command=lambda: self.save_edit(idea_id)).pack(side=tk.RIGHT)
        
    def save_edit(self, idea_id):
        title = self.edit_title.get()
        details = self.edit_details.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showwarning("Aviso", "O título é obrigatório!")
            return
            
        self.cursor.execute("UPDATE ideias SET nome = ?, notas = ? WHERE id = ?", (title, details, idea_id))
        self.conn.commit()
        self.update_list()
        self.edit_window.destroy()
        self.show_status("Ideia atualizada com sucesso!")
        
    def toggle_idea(self, idea_id):
        self.cursor.execute("SELECT concluida FROM ideias WHERE id = ?", (idea_id,))
        current = self.cursor.fetchone()[0]
        new_status = 0 if current else 1
        
        self.cursor.execute("UPDATE ideias SET concluida = ? WHERE id = ?", (new_status, idea_id))
        self.conn.commit()
        self.update_list()
        self.show_status(f"Ideia marcada como {'concluída' if new_status else 'pendente'}!")
        
    def delete_idea(self, idea_id):
        self.cursor.execute("SELECT nome FROM ideias WHERE id = ?", (idea_id,))
        name = self.cursor.fetchone()[0]
        
        if messagebox.askyesno("Confirmar", f"Excluir a ideia '{name}'?", icon='warning'):
            self.cursor.execute("DELETE FROM ideias WHERE id = ?", (idea_id,))
            self.conn.commit()
            self.update_list()
            self.show_status("Ideia excluída com sucesso!")
            
    def show_status(self, message):
        self.status.config(text=message)
        self.root.after(3000, lambda: self.status.config(text="Pronto"))

if __name__ == "__main__":
    root = tk.Tk()
    app = IdeaApp(root)
    root.mainloop()