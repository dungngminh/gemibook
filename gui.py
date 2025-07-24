import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import threading
from stats import count_words, count_characters, get_sorted_character_report, count_word_frequency, calculate_average_word_length
from bookbot.pdf_parser import get_pdf_text

def get_book_text(path):
    """Reads the content of a file at the given path and returns it as a string."""
    if path.lower().endswith('.pdf'):
        return get_pdf_text(path)
    else:
        with open(path, encoding='utf-8') as f:
            return f.read()

def analyze_book(book_path):
    """Analyzes a single book and returns a dictionary of its statistics."""
    text = get_book_text(book_path)
    num_words = count_words(text)
    chars = count_characters(text)
    char_report = get_sorted_character_report(chars)
    most_common_words = count_word_frequency(text)
    avg_word_length = calculate_average_word_length(text)

    return {
        "book_path": book_path,
        "word_count": num_words,
        "character_count": char_report,
        "most_common_words": most_common_words,
        "average_word_length": avg_word_length
    }

class BookbotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Bookbot Analyzer")

        self.book_paths = []

        # File Selection
        self.file_frame = tk.LabelFrame(master, text="Select Books")
        self.file_frame.pack(pady=10, padx=10, fill="x")

        self.select_button = tk.Button(self.file_frame, text="Add Book(s)", command=self.add_books)
        self.select_button.pack(side="left", padx=5, pady=5)

        self.clear_button = tk.Button(self.file_frame, text="Clear List", command=self.clear_books)
        self.clear_button.pack(side="left", padx=5, pady=5)

        self.book_list_label = tk.Label(self.file_frame, text="No books selected.")
        self.book_list_label.pack(side="left", padx=5, pady=5)

        # Analysis Options
        self.options_frame = tk.LabelFrame(master, text="Analysis Options")
        self.options_frame.pack(pady=10, padx=10, fill="x")

        self.common_words_var = tk.BooleanVar(value=True)
        self.avg_word_len_var = tk.BooleanVar(value=True)
        self.char_count_var = tk.BooleanVar(value=True)

        tk.Checkbutton(self.options_frame, text="Most Common Words", variable=self.common_words_var).pack(anchor="w")
        tk.Checkbutton(self.options_frame, text="Average Word Length", variable=self.avg_word_len_var).pack(anchor="w")
        tk.Checkbutton(self.options_frame, text="Character Count", variable=self.char_count_var).pack(anchor="w")

        # Output
        self.output_frame = tk.LabelFrame(master, text="Output")
        self.output_frame.pack(pady=10, padx=10, fill="x")

        self.output_label = tk.Label(self.output_frame, text="Output JSON File:")
        self.output_label.pack(side="left", padx=5, pady=5)

        self.output_entry = tk.Entry(self.output_frame, width=40)
        self.output_entry.insert(0, "book_analysis_report.json")
        self.output_entry.pack(side="left", padx=5, pady=5)

        self.browse_output_button = tk.Button(self.output_frame, text="Browse", command=self.browse_output_file)
        self.browse_output_button.pack(side="left", padx=5, pady=5)

        # Analyze Button
        self.analyze_button = tk.Button(master, text="Analyze Books", command=self.run_analysis)
        self.analyze_button.pack(pady=10)

        self.status_label = tk.Label(master, text="")
        self.status_label.pack(pady=5)

    def add_books(self):
        files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf"), ("All files", "*.*")])
        if files:
            self.book_paths.extend(files)
            self.update_book_list_label()

    def clear_books(self):
        self.book_paths = []
        self.update_book_list_label()

    def update_book_list_label(self):
        if self.book_paths:
            self.book_list_label.config(text=f"{len(self.book_paths)} book(s) selected.")
        else:
            self.book_list_label.config(text="No books selected.")

    def browse_output_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file)

    def run_analysis(self):
        if not self.book_paths:
            messagebox.showwarning("No Books Selected", "Please add at least one book to analyze.")
            return

        output_json_path = self.output_entry.get()
        if not output_json_path:
            messagebox.showwarning("Output File Missing", "Please specify an output JSON file.")
            return

        self.analyze_button.config(state=tk.DISABLED)
        self.status_label.config(text="Analyzing books... Please wait.")

        analysis_thread = threading.Thread(target=self._start_analysis_thread, args=(output_json_path,))
        analysis_thread.start()

    def _start_analysis_thread(self, output_json_path):
        all_book_reports = []
        try:
            for book_path in self.book_paths:
                try:
                    report = analyze_book(book_path)
                    all_book_reports.append(report)
                except Exception as e:
                    self.master.after(0, lambda: messagebox.showerror("Analysis Error", f"Error analyzing {os.path.basename(book_path)}: {e}"))
                    return

            with open(output_json_path, 'w', encoding='utf-8') as f:
                json.dump(all_book_reports, f, indent=4)
            self.master.after(0, lambda: messagebox.showinfo("Analysis Complete", f"Analysis complete. Report saved to {output_json_path}"))
            self.master.after(0, lambda: self.status_label.config(text="Analysis complete."))
        except Exception as e:
            self.master.after(0, lambda: messagebox.showerror("Save Error", f"Error saving report to {output_json_path}: {e}"))
            self.master.after(0, lambda: self.status_label.config(text="Analysis failed."))
        finally:
            self.master.after(0, lambda: self.analyze_button.config(state=tk.NORMAL))

if __name__ == "__main__":
    root = tk.Tk()
    app = BookbotGUI(root)
    root.mainloop()
