import csv
from datetime import datetime
import os

# ========================================================================================================================================================
# Função: read_guest_preferences
# Descrição: Lê um ficheiro CSV com os nomes dos convidados e as suas preferências.
#            Retorna um dicionário com os campos 'prefers' e 'avoids' para cada convidado.
# ---------------------------------------------------------------------------------------------------
# Espera um CSV com colunas:
# Guest, Together1, Together2, Together3, Apart1, Apart2, Apart3
# ========================================================================================================================================================

def read_guest_preferences(filename):
    guests = {}
    
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Guest'].strip()

            # Lê os nomes das pessoas com quem o convidado quer ficar
            prefers = [row[f'Together{i}'].strip() for i in range(1, 4) if row.get(f'Together{i}') and row[f'Together{i}'].strip()]

            # Lê os nomes das pessoas que o convidado quer evitar
            avoids = [row[f'Apart{i}'].strip() for i in range(1, 4) if row.get(f'Apart{i}') and row[f'Apart{i}'].strip()]
            
            guests[name] = {
                'prefers': prefers,
                'avoids': avoids
            }
    
    return guests

# ========================================================================================================================================================
# Função: generate_output_folder
# Descrição: Cria uma nova pasta em "results/" com timestamp atual para guardar os resultados.
# ========================================================================================================================================================

def generate_output_folder():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join("results", f"seating_{timestamp}")
    os.makedirs(folder, exist_ok=True)
    return folder

# ========================================================================================================================================================
# Função: write_seating_arrangement
# Descrição: Escreve os resultados da disposição das mesas num ficheiro .txt.
#            Inclui métricas se forem fornecidas (score, optimality, etc).
#
# Parâmetros:
#   - tables: lista de listas com os convidados por mesa
#   - filename: caminho do ficheiro onde guardar (se None, cria novo em pasta com timestamp)
#   - current_score: score da disposição gerada
#   - perfect_score: score teórico máximo possível
#   - optimality: percentagem de quão perto está do score perfeito
#   - algorithm: nome do algoritmo usado
# ========================================================================================================================================================

def write_seating_arrangement(tables, filename=None, current_score=None, perfect_score=None, optimality=None, algorithm=None):

    # Se não for fornecido um nome, cria uma pasta nova com timestamp
    if filename is None:
        folder = generate_output_folder()
        filename = os.path.join(folder, "seating.txt")
    else:
        folder = os.path.dirname(filename)
        os.makedirs(folder, exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as txtfile:
        # Cabeçalho
        txtfile.write("==================================================\n")
        txtfile.write("SEATING ARRANGEMENT RESULTS\n")
        txtfile.write("==================================================\n\n")
        
        txtfile.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Escrita das métricas, se existirem
        if current_score is not None:
            txtfile.write("-------------------- Metrics --------------------\n")
            if algorithm is not None:
                txtfile.write(f"Algorithm: {algorithm}\n")
            txtfile.write(f"Score: {round(current_score,2)}\n")
            if perfect_score is not None:
                txtfile.write(f"Perfect Score: {round(perfect_score,2)}\n")
            if optimality is not None:
                txtfile.write(f"Optimality: {round(optimality,1)}%\n\n")
        
        # Escrita das mesas
        txtfile.write("-------------------- Tables ---------------------\n\n")
        for i, table in enumerate(tables, 1):
            txtfile.write(f"Table {i}:\n")
            for guest in table:
                txtfile.write(f"  • {guest}\n")
            txtfile.write("\n")
        
        txtfile.write("==================================================\n")
    
    return folder