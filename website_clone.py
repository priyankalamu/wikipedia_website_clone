import tkinter as tk
from tkinter import ttk, messagebox
import wikipedia

# Initialize the main window
root = tk.Tk()
root.title("Wikipedia Search")
root.geometry("800x600")
root.configure(bg="#f4f4f4")

# Function to handle search
def search_wikipedia():
    query = search_entry.get()
    if not query:
        messagebox.showerror("Error", "Search query cannot be empty!")
        return

    try:
        wikipedia.set_lang("en")
        results = wikipedia.search(query, results=10)
        if not results:
            results_text.set("No results found. Try another query!")
            return

        results_text.set("\n".join(results))
        display_result(results[0])  # Show the first result by default
    except Exception as e:
        results_text.set(f"Error: {str(e)}")

# Function to display detailed information
def display_result(title):
    try:
        summary = wikipedia.summary(title, sentences=5)
        result_textbox.delete(1.0, tk.END)
        result_textbox.insert(tk.END, f"Title: {title}\n\n{summary}")
    except Exception as e:
        result_textbox.delete(1.0, tk.END)
        result_textbox.insert(tk.END, f"Error: {str(e)}")

# Header label
header = tk.Label(
    root, text="Wikipedia Search", font=("Raleway", 24, "bold"), bg="#f4f4f4"
)
header.pack(pady=10)

# Search bar frame
search_frame = tk.Frame(root, bg="#f4f4f4")
search_frame.pack(pady=20)

search_entry = tk.Entry(
    search_frame, font=("Arial", 16), width=40, borderwidth=2, relief="solid"
)
search_entry.pack(side=tk.LEFT, padx=10)

search_button = tk.Button(
    search_frame, text="Search", font=("Arial", 14), command=search_wikipedia
)
search_button.pack(side=tk.LEFT)

# Results frame
results_frame = tk.Frame(root, bg="#f4f4f4")
results_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Results label
results_label = tk.Label(
    results_frame, text="Search Results:", font=("Arial", 16), bg="#f4f4f4"
)
results_label.pack(anchor="w")

# Scrollable results list
results_text = tk.StringVar()
results_list = tk.Listbox(results_frame, font=("Arial", 14), height=10, width=50)
results_list.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

scrollbar = tk.Scrollbar(results_frame, orient="vertical")
scrollbar.config(command=results_list.yview)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)

results_list.config(yscrollcommand=scrollbar.set)

# Bind list item selection to display details
def on_list_select(event):
    try:
        selected_index = results_list.curselection()
        if selected_index:
            selected_title = results_list.get(selected_index)
            display_result(selected_title)
    except Exception as e:
        messagebox.showerror("Error", str(e))

results_list.bind("<<ListboxSelect>>", on_list_select)

# Detailed result display
result_textbox = tk.Text(root, font=("Arial", 14), wrap=tk.WORD, height=10)
result_textbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Populate results list dynamically
def update_results():
    results_list.delete(0, tk.END)
    for result in results_text.get().split("\n"):
        results_list.insert(tk.END, result)

results_text.trace("w", lambda *args: update_results())

# Run the app
root.mainloop()
