import pandas as pd
import os
from datetime import datetime
import logging

# Configurando o loggin
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Dir para salvar os dados
DATA_DIR = "Dados_dos_pedidos"
os.makedirs(DATA_DIR, exist_ok=True)

# Simula um banco de dados como uma lista de estoque
ESTOQUE = {
    "Produto_1": 10,
    "Produto_2": 20,
    "Produto_3": 15
}

# Function para validação do pedido
def validar_pedido(pedido):
    if not pedido.get("nome_do_cliente") or not pedido.get("Produtos"):
        logging.warning("Pedido esta incompleto. Necessário: nome_do_cliente e Produtos.")
        return False
    return True

# Function para o processamento do pedido
def processar_pedido(pedido):
    total = 0
    produtos_invalidos = []
    
    for produto, qtd in pedido["Produtos"].items():
        if produto in ESTOQUE and ESTOQUE[produto] >= qtd:
            total += qtd * 10  # Preço fixo por produto (ex: 10 unidades monetárias)
            ESTOQUE[produto] -= qtd  # Atualizar estoque
        else:
            produtos_invalidos.append(produto)
    
    return total, produtos_invalidos

# Funtion para registrar o pedido que foi processado
def registrar_pedido(pedido, total):
    arquivo_pedidos = os.path.join(DATA_DIR, "pedidos_processados.csv")
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    dados_pedido = {
        "Data": data_atual,
        "Nome Cliente": pedido["nome_do_cliente"],
        "Produtos": str(pedido["Produtos"]),
        "Total": total
    }
    
    if not os.path.exists(arquivo_pedidos):
        df = pd.DataFrame([dados_pedido])
    else:
        df = pd.read_csv(arquivo_pedidos)
        df = pd.concat([df, pd.DataFrame([dados_pedido])], ignore_index=True)
    
    df.to_csv(arquivo_pedidos, index=False)
    logging.info(f"Pedido de {pedido['nome_do_cliente']} registrado com sucesso.")

# Funtion main do bot pego o pedido e faz um for com os avisos
def bot_pedidos():
    pedidos = [
        {"nome_do_cliente": "João", "Produtos": {"Produto_1": 2, "Produto_2": 1}},
        {"nome_do_cliente": "Maria", "Produtos": {"Produto_3": 5, "Produto_1": 8}},
        {"nome_do_cliente": "Carlos", "Produtos": {"Produto_2": 50}},  # Não há estoque insuficiente
        {"nome_do_cliente": "", "Produtos": {"Produto_1": 2}},  # Pedido é inválido
    ]
    
    for pedido in pedidos:
        logging.info(f"Recebendo pedido: {pedido}")
        if not validar_pedido(pedido):
            logging.warning("Pedido inválido. Ignorando...")
            continue
        
        total, produtos_invalidos = processar_pedido(pedido)
        if produtos_invalidos:
            logging.warning(f"Produtos indisponíveis: {produtos_invalidos}")
        
        logging.info(f"Total do pedido: {total}")
        registrar_pedido(pedido, total)
    
    logging.info("Processamento foi concluído. Relatório de pedidos foi gerado.")

if __name__ == "__main__":
    bot_pedidos()
