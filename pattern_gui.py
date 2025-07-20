import tkinter as tk

def generate_pattern():
    num = 1
    output = ""
    for i in range(1, 5):
        for j in range(i):
            output += str(num) + " "
            num += 2
        output += "\n"
    text_box.config(state="normal")
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, output)
    text_box.config(state="disabled")

# Create the GUI window
window = tk.Tk()
window.title("Pattern Printer")
window.geometry("300x200")

# Create a button
btn = tk.Button(window, text="Print Pattern", command=generate_pattern)
btn.pack(pady=10)

# Create a text box to display output
text_box = tk.Text(window, height=6, width=30, font=("Courier", 12))
text_box.pack()

# Disable editing
text_box.config(state="disabled")

# Start the GUI loop
window.mainloop()