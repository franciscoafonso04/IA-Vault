import csv
from datetime import datetime
import os

def read_guest_preferences(filename):
    guests = {}
    
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Guest'].strip()
            prefers = [row[f'Together{i}'].strip() for i in range(1, 4) if row.get(f'Together{i}') and row[f'Together{i}'].strip()]
            avoids = [row[f'Apart{i}'].strip() for i in range(1, 4) if row.get(f'Apart{i}') and row[f'Apart{i}'].strip()]
            
            guests[name] = {
                'prefers': prefers,
                'avoids': avoids
            }
    
    return guests

def generate_output_folder():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join("results", f"arrangement_{timestamp}")
    os.makedirs(folder, exist_ok=True)
    return folder

def write_seating_arrangement(tables, filename=None, current_score=None, perfect_score=None, optimality=None, algorithm=None):
    if filename is None:
        folder = generate_output_folder()
        filename = os.path.join(folder, "seating.txt")
    else:
        folder = os.path.dirname(filename)
        os.makedirs(folder, exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as txtfile:
        txtfile.write("==================================================\n")
        txtfile.write("SEATING ARRANGEMENT RESULTS\n")
        txtfile.write("==================================================\n\n")
        
        txtfile.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if current_score is not None:
            txtfile.write("-------------------- Metrics --------------------\n")
            if algorithm is not None:
                txtfile.write(f"Algorithm: {algorithm}\n")
            txtfile.write(f"Current Score: {round(current_score,2)}\n")
            if perfect_score is not None:
                txtfile.write(f"Perfect Score: {round(perfect_score,2)}\n")
            if optimality is not None:
                txtfile.write(f"Optimality: {round(optimality,1)}%\n\n")
        
        txtfile.write("-------------------- Tables ---------------------\n\n")
        for i, table in enumerate(tables, 1):
            txtfile.write(f"Table {i}:\n")
            for guest in table:
                txtfile.write(f"  • {guest}\n")
            txtfile.write("\n")
        
        txtfile.write("==================================================\n")
    
    return folder

