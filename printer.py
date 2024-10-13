import tkinter as tk
from tkinter import messagebox

orderItems = {}

def addItem(item):
    if item in orderItems:
        orderItems[item] += 1
    else:
        orderItems[item] = 1
    notePadUpdate()

def notePadUpdate():
    notePad.delete('1.0', tk.END)
    for item, qtd in orderItems.items():
        notePad.insert(tk.END, f"{item}: {qtd}\n")

def gerar_pedido():
    name = StartName.get()
    address = StartAddress.get()
    price = StartPrice.get()
    change = StartChange.get()
    
    if not name or not address or not price or not change:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return
    
    with open("pedido.txt", "w") as f:
        f.write(f"Nome: {name}\n")
        f.write(f"Endereço: {address}\n")
        f.write(f"Preço: {price}\n")
        f.write(f"Troco: {change}\n")
        f.write("\nItens:\n")
        for item, qtd in orderItems.items():
            f.write(f"{item}: {qtd}\n")
    
    messagebox.showinfo("Sucesso", "Pedido gerado com sucesso!")

janela = tk.Tk()
janela.title("Gerador de Pedidos")

tk.Label(janela, text="name:").pack()
StartName = tk.Entry(janela)
StartName.pack()

tk.Label(janela, text="Endereço:").pack()
StartAddress = tk.Entry(janela)
StartAddress.pack()

tk.Label(janela, text="Preço:").pack()
StartPrice = tk.Entry(janela)
StartPrice.pack()

tk.Label(janela, text="Troco:").pack()
StartChange = tk.Entry(janela)
StartChange.pack()

tk.Button(janela, text="Item 1", command=lambda: addItem("Item 1")).pack()
tk.Button(janela, text="Item 2", command=lambda: addItem("Item 2")).pack()
tk.Button(janela, text="Item 3", command=lambda: addItem("Item 3")).pack()

notePad = tk.Text(janela, height=10, width=40)
notePad.pack()

tk.Button(janela, text="Gerar Pedido", command=gerar_pedido).pack()

janela.mainloop()
