import tkinter as tk
from tkinter import messagebox
import os
import win32api
import win32print

itens_pedido = {}

def adicionar_item(nome_item):
    if nome_item in itens_pedido:
        itens_pedido[nome_item] += 1
    else:
        itens_pedido[nome_item] = 1
    atualizar_bloco_de_notas()

def atualizar_bloco_de_notas():
    bloco_de_notas.delete('1.0', tk.END)
    for item, qtd in itens_pedido.items():
        bloco_de_notas.insert(tk.END, f"{item}: {qtd}\n")

def gerar_pedido():
    pedido = entrada_pedido.get()
    cliente = entrada_cliente.get()
    telefone = entrada_telefone.get()
    horario = entrada_horario.get()
    endereco = entrada_endereco.get()
    valor = entrada_valor.get()
        
    if not cliente or not endereco or not valor or not pedido:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return
    
    with open("pedido.txt", "w") as f:
        f.write(f"Pedido Nº: {pedido}\n")
        f.write(f"Cliente: {cliente}\n")
        f.write(f"Telefone: {telefone}\n")
        f.write(f"Horario entrega: {horario}\n")
        f.write("\nItens:\n")
        for item, qtd in itens_pedido.items():
            f.write(f"{item}: {qtd}\n")
        f.write(f"Endereço: {endereco}\n")
        f.write(f"Valor Cobrança: {valor}\n")
    
    messagebox.showinfo("Sucesso", "Pedido gerado com sucesso!")
    
    imprimir_pedido("pedido.txt")
    
    reset_fields()

def imprimir_pedido(arquivo):
    try:
        win32api.ShellExecute(0, "print", arquivo, None, ".", 0)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao imprimir: {str(e)}")

def reset_fields():
    entrada_pedido.delete(0, tk.END)
    entrada_cliente.delete(0, tk.END)
    entrada_telefone.delete(0, tk.END)
    entrada_horario.delete(0, tk.END)
    entrada_endereco.delete(0, tk.END)
    entrada_valor.delete(0, tk.END)
    itens_pedido.clear()
    atualizar_bloco_de_notas()

janela = tk.Tk()
janela.title("Gerador de Pedidos")

tk.Label(janela, text="Pedido Nº:").pack()
entrada_pedido = tk.Entry(janela)
entrada_pedido.pack()

tk.Label(janela, text="Cliente:").pack()
entrada_cliente = tk.Entry(janela)
entrada_cliente.pack()

tk.Label(janela, text="Telefone:").pack()
entrada_telefone = tk.Entry(janela)
entrada_telefone.pack()

tk.Label(janela, text="Horario entrega:").pack()
entrada_horario = tk.Entry(janela)
entrada_horario.pack()

tk.Label(janela, text="Endereço:").pack()
entrada_endereco = tk.Entry(janela)
entrada_endereco.pack()

tk.Label(janela, text="Valor cobrança:").pack()
entrada_valor = tk.Entry(janela)
entrada_valor.pack()

tk.Button(janela, text="Item 1", command=lambda: adicionar_item("Item 1")).pack()
tk.Button(janela, text="Item 2", command=lambda: adicionar_item("Item 2")).pack()
tk.Button(janela, text="Item 3", command=lambda: adicionar_item("Item 3")).pack()

bloco_de_notas = tk.Text(janela, height=10, width=40)
bloco_de_notas.pack()

tk.Button(janela, text="Gerar Pedido", command=gerar_pedido).pack()

janela.mainloop()