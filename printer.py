import tkinter as tk
import time
from tkinter import messagebox
import win32api
import os
from PIL import Image, ImageTk

itens_pedido = {}
add_ordem = []
carne_separada = []

def obter_proximo_numero_pedido():
    if os.path.exists("pedido_num.txt"):
        with open("pedido_num.txt", "r") as f:
            numero = int(f.read())
    else:
        numero = 1
    with open("pedido_num.txt", "w") as f:
        f.write(str(numero + 1))
    return numero

def add_item(nome_item):
    if not nome_item.strip():
        return
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
    pedido = obter_proximo_numero_pedido()
    cliente = entrada_cliente.get()
    telefone = entrada_telefone.get()
    horario = entrada_horario.get()
    endereco = entrada_endereco.get()
    taxa = entrada_entrega.get()
    valor = entrada_valor.get()
        
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
        f.write(f"\nEndereço:\n{endereco}\n")
        f.write(f"\nValor: R$ {valor}\n")
        f.write(f"\nTaxa entrega: R$ {taxa}\n")
        f.write(f"\nPago: {pago_var.get()}\n")
        f.write(f"\n")
    
    imprimir_pedido("pedido.txt")

    if carne_separada:
        # time.sleep(20)
        with open("carne_pedido.txt", "w") as f:
            f.write(f"\nASSADOS TASCA\n")
            f.write(f"Pedido Nº: {pedido}\n")
            f.write(f"Cliente: {cliente}\n")
            f.write(f"Horário: {horario}\n\n")
            f.write("Carnes:\n")
            for carne in carne_separada:
                f.write(f"- {carne}\n")
            f.write(f"\n")
        imprimir_pedido("carne_pedido.txt")

    reset_fields()

def imprimir_pedido(arquivo):
    try:
        win32api.ShellExecute(0, "print", arquivo, None, ".", 0)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao imprimir: {str(e)}")

def reset_fields():
    for entrada in entradas.values():
        entrada.delete(0, tk.END)
    itens_pedido.clear()
    add_ordem.clear()
    carne_separada.clear()
    atualizar_note()

janela = tk.Tk()
janela.title("Gerador de Pedidos")
janela.configure(bg='#f0f0f0')

try:
    imagem = Image.open("icon.jpeg")
    imagem = imagem.resize((32, 32))
    icone = ImageTk.PhotoImage(imagem)
    janela.iconphoto(True, icone)
except:
    pass

janela.grid_columnconfigure((0, 1, 2), weight=1)

campos = [
    ("Cliente:", "entrada_cliente"),
    ("Telefone:", "entrada_telefone"),
    ("Horário:", "entrada_horario"),
    ("Endereço:", "entrada_endereco"),
    ("Valor cobrança:", "entrada_valor"),
    ("Carne:", "entrada_carne"),
    ("Bebida:", "entrada_bebida"),
    ("Taxa de entrega", "entrada_entrega")
]

entradas = {}
for i, (texto, var) in enumerate(campos, start=1):
    tk.Label(janela, text=texto, font=("Helvetica", 12, "bold"), bg='#f0f0f0').grid(row=i, column=0, sticky="w", padx=10, pady=5)

    frame_input = tk.Frame(janela, bg='#f0f0f0')
    frame_input.grid(row=i, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
    frame_input.grid_columnconfigure(0, weight=1)

    entrada = tk.Entry(frame_input, font=("Arial", 10))
    entrada.grid(row=0, column=0, sticky="ew")
    entradas[var] = entrada

    if var == "entrada_carne":
        def add_carne():
            nome = entrada_carne.get().strip()
            if nome:
                add_item(nome)
                carne_separada.append(nome)
            entrada_carne.delete(0, tk.END)
        btn = tk.Button(frame_input, text="+", font=("Arial", 10, "bold"), width=3, command=add_carne)
        btn.grid(row=0, column=1, padx=(5, 0))
    elif var == "entrada_bebida":
        def add_bebida():
            nome = entrada_bebida.get().strip()
            add_item(nome)
            entrada_bebida.delete(0, tk.END)
        btn = tk.Button(frame_input, text="+", font=("Arial", 10, "bold"), width=3, command=add_bebida)
        btn.grid(row=0, column=1, padx=(5, 0))

entrada_cliente = entradas["entrada_cliente"]
entrada_telefone = entradas["entrada_telefone"]
entrada_horario = entradas["entrada_horario"]
entrada_endereco = entradas["entrada_endereco"]
entrada_valor = entradas["entrada_valor"]
entrada_carne = entradas["entrada_carne"]
entrada_bebida = entradas["entrada_bebida"]
entrada_entrega = entradas["entrada_entrega"]

pago_var = tk.StringVar(value="Não")

linha_pago = len(campos) + 1

tk.Label(janela, text="Pago:", font=("Helvetica", 12, "bold"), bg='#f0f0f0').grid(
    row=linha_pago, column=0, sticky="w", padx=10, pady=5)
tk.Radiobutton(janela, text="Sim", variable=pago_var, value="Sim", bg='#f0f0f0').grid(
    row=linha_pago, column=1, sticky="w")
tk.Radiobutton(janela, text="Não", variable=pago_var, value="Não", bg='#f0f0f0').grid(
    row=linha_pago, column=2, sticky="w")

itens = [
    "Frango de aipim", "Maionese G", "Maionese P",
    "Frango Tradicional", "Salpicão G", "Salpicão P",
    "Frango S/Recheio", "Batata G", "Batata P",
    "Farofa", "Polenta G", "Polenta P",
    "Arroz G", "Arroz P"
]

linha_itens = linha_pago + 1
for i, item in enumerate(itens):
    linha = linha_itens + (i // 3)
    coluna = i % 3
    tk.Button(janela, text=item, command=lambda i=item: add_item(i),
              bg='white', fg='black', font=("Arial", 12, "bold")).grid(
        row=linha, column=coluna, padx=10, pady=5, sticky="nsew")

linha_fim_itens = linha_itens + (len(itens) // 3) + 1

note = tk.Text(janela, height=10, width=40)
note.grid(row=linha_fim_itens, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

tk.Button(janela, text="Remover Item", command=remover_ultimo_item,
          bg='red', fg='black', font=("Arial", 12, "bold")).grid(
    row=linha_fim_itens + 1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

tk.Button(janela, text="Gerar Pedido", command=gerar_pedido,
          bg='#2196F3', fg='black', font=("Arial", 12, "bold")).grid(
    row=linha_fim_itens + 2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

for col in range(3):
    janela.grid_columnconfigure(col, weight=1)
for row in range(linha_fim_itens + 3):
    janela.grid_rowconfigure(row, weight=1)

janela.mainloop()