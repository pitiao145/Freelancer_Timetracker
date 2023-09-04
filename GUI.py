import tkinter as tk

root = tk.Tk()

root.geometry("800x500")
root.title("Freelance time tracker")

label = tk.Label(root, text="Input a new task:", font=("Roboto", 18))
label.pack(padx=10, pady=10)

task_entry = tk.Entry(root)
task_entry.pack(padx=10, pady=10)

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)

start_button = tk.Button(buttonframe, text="Start", font=("Roboto", 16))
stop_button = tk.Button(buttonframe, text="Stop", font=("Roboto", 16))

start_button.grid(row=0, column=0, sticky=tk.W+tk.E)
stop_button.grid(row=0, column=1, sticky=tk.W+tk.E)

buttonframe.pack()

root.mainloop()