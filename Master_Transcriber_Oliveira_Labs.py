# =================================================================
# 🎙️ MASTER TRANSCRIBER PRO - OLIVEIRA LABS EDITION
# Developed by: Oliveira Labs
# Methodology: Prompt Master MBA
# Purpose: High-performance audio transcription with GUI
# =================================================================

import os
import time
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading

try:
    from faster_whisper import WhisperModel
    HAS_FASTER = True
except ImportError:
    import whisper
    HAS_FASTER = False

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_rem = seconds % 60
    ms = int((seconds_rem - int(seconds_rem)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds_rem):02d},{ms:03d}"

class TranscriberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Master Transcriber Pro")
        self.root.geometry("750x600")
        self.root.configure(bg="#f0f0f0")
        
        self.audio_path = ""
        self.full_srt = ""
        self.full_txt = ""
        
        self.setup_ui()

    def setup_ui(self):
        # Header Branding
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=40)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text=" MASTER TRANSCRIBER PRO", bg="#2c3e50", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=10)
        tk.Label(header_frame, text="Developed by Oliveira Labs ", bg="#2c3e50", fg="#ecf0f1", font=("Segoe UI", 9, "italic")).pack(side=tk.RIGHT, padx=10)

        # File Selection
        file_frame = tk.LabelFrame(self.root, text=" 1. Selecionar Arquivo ", bg="#f0f0f0", font=("Segoe UI", 9, "bold"))
        file_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.btn_select = ttk.Button(file_frame, text="Procurar Áudio...", command=self.select_file)
        self.btn_select.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.lbl_file = tk.Label(file_frame, text="Nenhum arquivo selecionado", bg="#f0f0f0", fg="#7f8c8d", wraplength=500, justify="left")
        self.lbl_file.pack(side=tk.LEFT, padx=10)

        # Progress
        prog_frame = tk.LabelFrame(self.root, text=" 2. Progresso ", bg="#f0f0f0", font=("Segoe UI", 9, "bold"))
        prog_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(prog_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=10, pady=10)
        
        self.lbl_status = tk.Label(prog_frame, text="Aguardando início...", bg="#f0f0f0", fg="#2980b9")
        self.lbl_status.pack()

        # Log/Output Area
        self.log_area = scrolledtext.ScrolledText(self.root, height=12, font=("Consolas", 9), bg="white")
        self.log_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Action Buttons
        actions_frame = tk.Frame(self.root, bg="#f0f0f0")
        actions_frame.pack(fill=tk.X, padx=20, pady=10)

        # Copy Buttons
        copy_label = tk.Label(actions_frame, text="Copiar para ClipBoard:", bg="#f0f0f0", font=("Segoe UI", 8, "bold"))
        copy_label.grid(row=0, column=0, columnspan=2, sticky="w")
        
        self.btn_copy_srt = ttk.Button(actions_frame, text="Copiar com Tempos (SRT)", command=lambda: self.copy_to_clip(self.full_srt))
        self.btn_copy_srt.grid(row=1, column=0, padx=2, pady=5, sticky="ew")
        
        self.btn_copy_txt = ttk.Button(actions_frame, text="Copiar apenas Texto", command=lambda: self.copy_to_clip(self.full_txt))
        self.btn_copy_txt.grid(row=1, column=1, padx=2, pady=5, sticky="ew")

        # Save Buttons
        save_label = tk.Label(actions_frame, text="Salvar Arquivos:", bg="#f0f0f0", font=("Segoe UI", 8, "bold"))
        save_label.grid(row=0, column=2, columnspan=2, sticky="w", padx=20)

        self.btn_save_srt = ttk.Button(actions_frame, text="Salvar .SRT", command=lambda: self.manual_save(".srt", self.full_srt))
        self.btn_save_srt.grid(row=1, column=2, padx=2, pady=5, sticky="ew")
        
        self.btn_save_txt = ttk.Button(actions_frame, text="Salvar .TXT", command=lambda: self.manual_save(".txt", self.full_txt))
        self.btn_save_txt.grid(row=1, column=3, padx=2, pady=5, sticky="ew")

        # Start Button
        self.btn_start = tk.Button(self.root, text="INICIAR TRANSCRIÇÃO", bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), command=self.start_thread)
        self.btn_start.pack(pady=10, fill=tk.X, padx=20)

    def select_file(self):
        file = filedialog.askopenfilename(filetypes=[("Arquivos de Áudio", "*.mp3 *.wav *.m4a *.ogg *.flac"), ("Todos os arquivos", "*.*")])
        if file:
            self.audio_path = file
            self.lbl_file.config(text=os.path.basename(file), fg="black")
            self.log_area.delete('1.0', tk.END)
            self.log(f"Arquivo selecionado: {file}")

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def copy_to_clip(self, content):
        if not content:
            messagebox.showwarning("Aviso", "Ainda não há conteúdo para copiar!")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Sucesso", "Copiado para a área de transferência!")

    def manual_save(self, ext, content):
        if not content:
            messagebox.showwarning("Aviso", "Ainda não há conteúdo para salvar!")
            return
        file = filedialog.asksaveasfilename(defaultextension=ext, filetypes=[(f"Arquivo {ext.upper()}", f"*{ext}")])
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Sucesso", f"Arquivo salvo em: {file}")

    def start_thread(self):
        if not self.audio_path:
            messagebox.showerror("Erro", "Por favor, selecione um arquivo de áudio primeiro!")
            return
        self.btn_start.config(state=tk.DISABLED)
        self.btn_select.config(state=tk.DISABLED)
        self.full_srt = ""
        self.full_txt = ""
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        try:
            self.lbl_status.config(text="Carregando modelos de IA...", fg="#d35400")
            if HAS_FASTER:
                model = WhisperModel("base", device="cpu", compute_type="int8")
                segments, info = model.transcribe(self.audio_path, beam_size=5)
                total_duration = info.duration
            else:
                model = whisper.load_model("base")
                result = model.transcribe(self.audio_path, verbose=False)
                segments = result['segments']
                total_duration = result.get('duration', 1)

            self.lbl_status.config(text="Transcrevendo...", fg="#27ae60")
            
            for i, segment in enumerate(segments, start=1):
                start_val = segment.start if HAS_FASTER else segment['start']
                end_val = segment.end if HAS_FASTER else segment['end']
                text_val = segment.text.strip() if HAS_FASTER else segment['text'].strip()
                
                start = format_timestamp(start_val)
                end = format_timestamp(end_val)
                
                # Update Internal Storage
                current_srt = f"{i}\n{start} --> {end}\n{text_val}\n\n"
                self.full_srt += current_srt
                self.full_txt += text_val + "\n\n"  # Adiciona quebra de linha dupla para legibilidade
                
                # UI Updates
                self.log(f"[{start}] {text_val}")
                percent = (end_val / total_duration) * 100
                self.progress_var.set(percent)
                self.root.update_idletasks()

            self.lbl_status.config(text="CONCLUÍDO!", fg="#2c3e50")
            messagebox.showinfo("Fim", "Transcrição finalizada com sucesso!")
            
        except Exception as e:
            self.log(f"ERRO: {str(e)}")
            messagebox.showerror("Erro Crítico", f"Falha no processo: {e}")
        finally:
            self.btn_start.config(state=tk.NORMAL)
            self.btn_select.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriberApp(root)
    root.mainloop()
