import tkinter as tk
from tkinter import messagebox
import win32api
from tkinter import PhotoImage
from PIL import Image, ImageTk

itens_pedido = {}
add_ordem = []

def add_item(nome_item):
    if nome_item in itens_pedido:
        itens_pedido[nome_item] += 1
    else:
        itens_pedido[nome_item] = 1
    add_ordem.append(nome_item)
    atualizar_note()

def atualizar_note():
    note.delete('1.0', tk.END)
    for item, qtd in itens_pedido.items():
        note.insert(tk.END, f"{item}: {qtd}\n")
        
def remover_ultimo_item():
    if add_ordem:
        ultimo_item = add_ordem.pop()
        if itens_pedido[ultimo_item] > 1:
            itens_pedido[ultimo_item] -= 1
        else:
            del itens_pedido[ultimo_item]
        atualizar_note()

def gerar_pedido():
    pedido = entrada_pedido.get()
    cliente = entrada_cliente.get()
    telefone = entrada_telefone.get()
    horario = entrada_horario.get()
    endereco = entrada_endereco.get()
    valor = entrada_valor.get()
    carne = entrada_carne.get()
        
    if not endereco or not pedido:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return
    
    with open("pedido.txt", "w") as f:
        f.write(f"ASSADOS TASCA\n")
        f.write(f"\nPedido Nº: {pedido}\n")
        f.write(f"\nCliente: {cliente}\n")
        f.write(f"\nTelefone: {telefone}\n")
        f.write(f"\nHorário: {horario}\n")
        f.write("\nItens:\n")
        for item, qtd in itens_pedido.items():
            f.write(f"\n{qtd}x {item}\n")
        f.write(f"\nCarne:\n{carne}\n")
        f.write(f"\nEndereço:\n{endereco}\n")
        f.write(f"\nValor: R$ {valor}\n")
    
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
    entrada_carne.delete(0, tk.END)
    itens_pedido.clear()
    add_ordem.clear()
    atualizar_note()

janela = tk.Tk()
janela.title("Gerador de Pedidos")
janela.configure(bg='#f0f0f0')

imagem = Image.open("icon.jpeg")
imagem = imagem.resize((32, 32))
icone = ImageTk.PhotoImage(imagem)
janela.iconphoto(True, icone)
# "scheib"
janela.grid_columnconfigure((0, 1, 2), weight=1)

tk.Label(janela, text="Pedido Nº:", font=("Helvetica", 12, "bold"), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=5, sticky="w")
entrada_pedido = tk.Entry(janela, font=("Arial", 10))
entrada_pedido.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

tk.Label(janela, text="Cliente:", font=("Helvetica", 12, "bold"), bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=5, sticky="w")
entrada_cliente = tk.Entry(janela, font=("Arial", 10))
entrada_cliente.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

tk.Label(janela, text="Telefone:", font=("Helvetica", 12, "bold"), bg='#f0f0f0').grid(row=2, column=0, padx=10, pady=5, sticky="w")
entrada_telefone = tk.Entry(janela, font=("Arial", 10))
entrada_telefone.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

tk.Label(janela, text="Horário:", font=("Helvetica", 12, "bold"), bg='#f0f0f0').grid(row=3, column=0, padx=10, pady=5, sticky="w")
entrada_horario = tk.Entry(janela, font=("Arial", 10))
entrada_horario.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

tk.Label(janela, text="Endereço:", font=("Helvetica", 12, "bold"), bg='#f0f0f0').grid(row=4, column=0, padx=10, pady=5, sticky="w")
entrada_endereco = tk.Entry(janela, font=("Arial", 10))
entrada_endereco.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

tk.Label(janela, text="Valor cobrança:", font=("Helvetica", 12, "bold"), bg='#f0f0f0').grid(row=5, column=0, padx=10, pady=5, sticky="w")
entrada_valor = tk.Entry(janela, font=("Arial", 10))
entrada_valor.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

tk.Label(janela, text="Carne:", font=("Helvetica", 12, "bold"), bg='#f0f0f0').grid(row=6, column=0, padx=10, pady=5, sticky="w")
entrada_carne = tk.Entry(janela, font=("Arial", 10))
entrada_carne.grid(row=6, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

itens = [
    "Frango de aipim", "Frango tradicional", "Frango sem recheio",
    "Salpicão P", "Salpicão G", "Arroz P", "Maionese P",
    "Maionese G", "Arroz G", "Polenta frita P", "Polenta frita G",
    "Farofa", "Batata frita P", "Batata frita G"
]

for idx, item in enumerate(itens):
    coluna = idx % 3
    linha = (idx // 3) + 7
    tk.Button(janela, text=item, command=lambda i=item: add_item(i), 
              bg='white', fg='black', font=("Arial", 12, "bold")).grid(row=linha, column=coluna, padx=10, pady=10, sticky="nsew")

note = tk.Text(janela, height=10, width=40)
note.grid(row=linha+1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

tk.Button(janela, text="Remover Item", command=remover_ultimo_item, 
          bg='red', fg='black', font=("Arial", 12, "bold")).grid(row=linha+2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

tk.Button(janela, text="Gerar Pedido", command=gerar_pedido, 
          bg='#2196F3', fg='black', font=("Arial", 12, "bold")).grid(row=linha+3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

janela.mainloop()
