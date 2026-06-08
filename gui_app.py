# gui_app.py
"""Tkinter GUI for the Flex Lexical Analyzer.

Features:
- Modern dark-themed user interface.
- Tabbed interface: Token Grid (structured table) & Raw Output (console log).
- Code editor pane with syntax template options (e.g., standard if-else, while loop).
- Invokes lexer.exe in the background and processes the printed token stream.
- Export results to CSV.
"""

import subprocess
import sys
import os
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LEXER_EXE = os.path.join(BASE_DIR, "lexer.exe")

# Modern Dark Theme Colors
COLOR_BG = "#1e1e24"          # Main window bg
COLOR_PANEL = "#121214"       # Editor/Console bg
COLOR_TEXT = "#e1e1e6"        # Text color
COLOR_ACCENT = "#6c5ce7"      # Accent purple
COLOR_ACCENT_HOVER = "#5849c7"
COLOR_SUCCESS = "#2ed573"     # Active/Success green
COLOR_WARNING = "#ffa502"     # Warning orange
COLOR_WHITE = "#ffffff"

class LexerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador Léxico - FLEX + Python (MiniLang)")
        self.geometry("950x700")
        self.minsize(800, 600)
        self.configure(bg=COLOR_BG)
        
        # Apply TTK Styles
        self._setup_styles()
        
        # Create Widgets
        self._create_header()
        self._create_main_layout()
        self._create_footer()
        
        # Load default sample code
        self._load_sample_code()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        
        # Configure Frame/Notebook styles
        style.configure(".", background=COLOR_BG, foreground=COLOR_TEXT)
        style.configure("TFrame", background=COLOR_BG)
        style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background="#2a2a35", foreground=COLOR_TEXT, padding=[12, 4], font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", COLOR_ACCENT)], foreground=[("selected", COLOR_WHITE)])
        
        # Treeview (Token Table) Styles
        style.configure("Treeview", background="#1a1a20", fieldbackground="#1a1a20", foreground=COLOR_TEXT, rowheight=26, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#2b2b36", foreground=COLOR_WHITE, borderwidth=1, font=("Segoe UI", 10, "bold"))
        style.map("Treeview.Heading", background=[("active", COLOR_ACCENT)])

    def _create_header(self):
        # Header frame with title and load options
        header_frame = tk.Frame(self, bg=COLOR_BG, height=60)
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        
        title_label = tk.Label(header_frame, text="ANALIZADOR LÉXICO (FLEX + PYTHON)", font=("Segoe UI", 16, "bold"), bg=COLOR_BG, fg=COLOR_WHITE)
        title_label.pack(side=tk.LEFT, anchor=tk.CENTER)
        
        # Template selector
        tpl_label = tk.Label(header_frame, text="Plantilla:", font=("Segoe UI", 10), bg=COLOR_BG, fg=COLOR_TEXT)
        tpl_label.pack(side=tk.RIGHT, padx=5)
        
        self.tpl_var = tk.StringVar(value="Bucle simple")
        tpl_combo = ttk.Combobox(header_frame, textvariable=self.tpl_var, values=["Bucle simple", "Condición If-Else", "Operaciones Aritméticas"], state="readonly", width=18)
        tpl_combo.pack(side=tk.RIGHT, padx=5)
        tpl_combo.bind("<<ComboboxSelected>>", self._on_template_selected)

    def _create_main_layout(self):
        # Main split container: Left (Editor) and Right (Results)
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=COLOR_BG, bd=0, sashwidth=4)
        paned.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # --- LEFT PANEL: Source Code Editor ---
        left_frame = tk.Frame(paned, bg=COLOR_BG)
        paned.add(left_frame, minsize=350)
        
        lbl_editor = tk.Label(left_frame, text="Código de Entrada (MiniLang)", font=("Segoe UI", 11, "bold"), bg=COLOR_BG, fg=COLOR_TEXT)
        lbl_editor.pack(anchor=tk.W, pady=3)
        
        self.source_text = scrolledtext.ScrolledText(left_frame, wrap=tk.NONE, font=("Consolas", 11), bg=COLOR_PANEL, fg="#e1e1e6", insertbackground="#ffffff", bd=0, highlightthickness=1, highlightbackground="#3e3e4a", highlightcolor=COLOR_ACCENT)
        self.source_text.pack(fill=tk.BOTH, expand=True)
        
        # Editor button bar
        btn_bar = tk.Frame(left_frame, bg=COLOR_BG)
        btn_bar.pack(fill=tk.X, pady=10)
        
        btn_open = tk.Button(btn_bar, text="Abrir Archivo", command=self.open_file, bg="#33333e", fg=COLOR_WHITE, activebackground="#454554", bd=0, padx=12, pady=6, font=("Segoe UI", 10))
        btn_open.pack(side=tk.LEFT, padx=3)
        
        btn_clear = tk.Button(btn_bar, text="Limpiar", command=self._clear_editor, bg="#33333e", fg=COLOR_WHITE, activebackground="#454554", bd=0, padx=12, pady=6, font=("Segoe UI", 10))
        btn_clear.pack(side=tk.LEFT, padx=3)
        
        btn_run = tk.Button(btn_bar, text="Analizar Código", command=self.run_lexer, bg=COLOR_ACCENT, fg=COLOR_WHITE, activebackground=COLOR_ACCENT_HOVER, bd=0, padx=18, pady=6, font=("Segoe UI", 10, "bold"))
        btn_run.pack(side=tk.RIGHT, padx=3)
        
        # --- RIGHT PANEL: Results ---
        right_frame = tk.Frame(paned, bg=COLOR_BG)
        paned.add(right_frame, minsize=400)
        
        lbl_results = tk.Label(right_frame, text="Resultado del Análisis", font=("Segoe UI", 11, "bold"), bg=COLOR_BG, fg=COLOR_TEXT)
        lbl_results.pack(anchor=tk.W, pady=3)
        
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Token Grid View
        self.tab_grid = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_grid, text=" Tabla de Tokens ")
        
        cols = ("Token", "Lexema", "Categoría")
        self.tree = ttk.Treeview(self.tab_grid, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("Token", text="Token (Flex)")
        self.tree.heading("Lexema", text="Lexema (Texto)")
        self.tree.heading("Categoría", text="Categoría de Lenguaje")
        
        self.tree.column("Token", width=120, anchor=tk.W)
        self.tree.column("Lexema", width=120, anchor=tk.W)
        self.tree.column("Categoría", width=150, anchor=tk.W)
        
        # Scrollbars for Treeview
        tree_scroll_y = ttk.Scrollbar(self.tab_grid, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll_y.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tab 2: Raw Console Output
        self.tab_raw = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_raw, text=" Salida de Consola (Raw) ")
        
        self.raw_output = scrolledtext.ScrolledText(self.tab_raw, wrap=tk.WORD, font=("Consolas", 10), bg=COLOR_PANEL, fg=COLOR_SUCCESS, state=tk.DISABLED, bd=0)
        self.raw_output.pack(fill=tk.BOTH, expand=True)
        
        # Actions for Right Side
        right_btn_bar = tk.Frame(right_frame, bg=COLOR_BG)
        right_btn_bar.pack(fill=tk.X, pady=10)
        
        btn_export = tk.Button(right_btn_bar, text="Exportar a CSV", command=self.export_csv, bg="#33333e", fg=COLOR_WHITE, activebackground="#454554", bd=0, padx=12, pady=6, font=("Segoe UI", 10))
        btn_export.pack(side=tk.LEFT)

    def _create_footer(self):
        # Footer / Status bar
        self.status_bar = tk.Frame(self, bg="#121214", height=25)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_lbl = tk.Label(self.status_bar, text="Listo | Compilación de Analizador Léxico FLEX exitosa", font=("Segoe UI", 9), bg="#121214", fg="#888899")
        self.status_lbl.pack(side=tk.LEFT, padx=15, pady=2)
        
        self.count_lbl = tk.Label(self.status_bar, text="Tokens: 0", font=("Segoe UI", 9, "bold"), bg="#121214", fg=COLOR_SUCCESS)
        self.count_lbl.pack(side=tk.RIGHT, padx=15, pady=2)

    def _load_sample_code(self):
        sample_code = (
            "// Ejemplo de código MiniLang para analizar\n"
            "if (contador <= 10) {\n"
            "    while (flag == 1) {\n"
            "        x = x + 5;\n"
            "        return x;\n"
            "    }\n"
            "}\n"
            "else {\n"
            "    x = 0 - y;\n"
            "}\n"
        )
        self.source_text.insert(tk.END, sample_code)

    def _on_template_selected(self, event=None):
        tpl = self.tpl_var.get()
        self.source_text.delete('1.0', tk.END)
        
        if tpl == "Bucle simple":
            code = (
                "// Ejemplo Bucle\n"
                "while (contador < 100) {\n"
                "    total = total + step;\n"
                "    contador = contador + 1;\n"
                "}\n"
            )
        elif tpl == "Condición If-Else":
            code = (
                "// Ejemplo If-Else\n"
                "if (valor == 42) {\n"
                "    return 1;\n"
                "} else {\n"
                "    return 0;\n"
                "}\n"
            )
        elif tpl == "Operaciones Aritméticas":
            code = (
                "// Ejemplo Aritmética\n"
                "resultado = (a * b) - (c / d) + 40;\n"
            )
        else:
            code = ""
            
        self.source_text.insert(tk.END, code)

    def _clear_editor(self):
        self.source_text.delete('1.0', tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Código fuente", "*.txt *.l *.c *.cpp"), ("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.source_text.delete('1.0', tk.END)
                self.source_text.insert(tk.END, content)
                self.status_lbl.configure(text=f"Archivo cargado: {os.path.basename(file_path)}", fg=COLOR_SUCCESS)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    def run_lexer(self):
        if not os.path.exists(LEXER_EXE):
            messagebox.showerror("Ejecutable no encontrado", f"No se encontró {LEXER_EXE}.\nPor favor, ejecuta build.bat primero para compilar el analizador.")
            return
            
        # Get source code
        source_code = self.source_text.get('1.0', tk.END).strip()
        if not source_code:
            messagebox.showwarning("Advertencia", "El editor de código está vacío.")
            return

        # Write current source to a temporary file
        temp_path = os.path.join(BASE_DIR, "tmp_input.txt")
        try:
            with open(temp_path, "w", encoding="utf-8") as tmp:
                tmp.write(source_code)
                
            # Run the lexer process
            result = subprocess.run(
                [LEXER_EXE], 
                cwd=BASE_DIR, 
                input=open(temp_path, "rb").read(), 
                capture_output=True, 
                timeout=5
            )
            
            output = result.stdout.decode('utf-8', errors='ignore')
            
            # Update GUI results
            self._update_results(output)
            self.status_lbl.configure(text="Análisis finalizado con éxito.", fg=COLOR_SUCCESS)
            
        except subprocess.TimeoutExpired:
            messagebox.showerror("Límite de tiempo excedido", "El analizador tardó demasiado en responder.")
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la ejecución: {e}")
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

    def _update_results(self, raw_output_text):
        # 1. Clear previous rows in table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 2. Populate raw log text tab
        self.raw_output.configure(state=tk.NORMAL)
        self.raw_output.delete('1.0', tk.END)
        self.raw_output.insert(tk.END, raw_output_text)
        self.raw_output.configure(state=tk.DISABLED)
        
        # 3. Parse output line-by-line and populate Treeview
        lines = raw_output_text.splitlines()
        token_count = 0
        
        for line in lines:
            if not line.strip():
                continue
            
            # Expected formats:
            # - TOKEN_IF
            # - TOKEN_ID lexeme
            parts = line.split(" ", 1)
            token_type = parts[0]
            lexeme = parts[1] if len(parts) > 1 else ""
            
            # Map keyword tokens to clean Lexeme represention if empty
            if token_type == "TOKEN_IF":
                lexeme = "if"
                category = "Palabra Clave (Keyword)"
            elif token_type == "TOKEN_ELSE":
                lexeme = "else"
                category = "Palabra Clave (Keyword)"
            elif token_type == "TOKEN_WHILE":
                lexeme = "while"
                category = "Palabra Clave (Keyword)"
            elif token_type == "TOKEN_RETURN":
                lexeme = "return"
                category = "Palabra Clave (Keyword)"
            elif token_type == "TOKEN_ID":
                category = "Identificador"
            elif token_type == "TOKEN_NUM":
                category = "Constante Numérica"
            elif token_type == "TOKEN_OP":
                category = "Operador"
            elif token_type == "TOKEN_DELIM":
                category = "Delimitador (Puntuación)"
            elif token_type == "TOKEN_UNKNOWN":
                category = "No Reconocido (Error)"
            else:
                category = "Otros"
                
            self.tree.insert("", tk.END, values=(token_type, lexeme, category))
            token_count += 1
            
        self.count_lbl.configure(text=f"Tokens: {token_count}")

    def export_csv(self):
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("Exportar", "No hay datos de tokens para exportar.")
            return
            
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
        if file_path:
            try:
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Token (Flex)", "Lexema", "Categoría"])
                    for item in items:
                        writer.writerow(self.tree.item(item, "values"))
                messagebox.showinfo("Exportar", "Tabla de tokens exportada con éxito.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo CSV: {e}")

if __name__ == "__main__":
    app = LexerGUI()
    app.mainloop()
