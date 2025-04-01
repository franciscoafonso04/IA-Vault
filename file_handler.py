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

def generate_arrangement_filename(extension='.txt'):
    """Generate a unique filename for each arrangement"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"arrangement_{timestamp}{extension}"
    return os.path.join("results", filename)

def write_seating_arrangement(tables, filename=None, current_score=None, perfect_score=None, optimality=None, algorithm=None):
    if filename is None:
        # Create results directory if it doesn't exist
        os.makedirs("results", exist_ok=True)
        
        # Write both TXT and CSV versions
        txt_filename = generate_arrangement_filename('.txt')
        csv_filename = generate_arrangement_filename('.csv')
        
        # Write TXT format
        with open(txt_filename, 'w', encoding='utf-8') as txtfile:
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
        
        # Write CSV format
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            if current_score is not None:
                writer.writerow(['Metrics'])
                if algorithm is not None:
                    writer.writerow(['Algorithm', algorithm])
                writer.writerow(['Current Score', round(current_score, 2)])
                if perfect_score is not None:
                    writer.writerow(['Perfect Score', round(perfect_score, 2)])
                if optimality is not None:
                    writer.writerow(['Optimality', f"{round(optimality, 1)}%"])
                writer.writerow([])
                
            writer.writerow(['Table', 'Guests'])
            for i, table in enumerate(tables, 1):
                writer.writerow([f'Table {i}', ', '.join(table)])
                
        return txt_filename  # Return the txt filename for compatibility
    else:
        # If filename is provided, use the old CSV-only format
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            if current_score is not None:
                writer.writerow(['Metrics'])
                if algorithm is not None:
                    writer.writerow(['Algorithm', algorithm])
                writer.writerow(['Current Score', round(current_score, 2)])
                if perfect_score is not None:
                    writer.writerow(['Perfect Score', round(perfect_score, 2)])
                if optimality is not None:
                    writer.writerow(['Optimality', f"{round(optimality, 1)}%"])
                writer.writerow([])  # Empty row for separation
                
            writer.writerow(['Table', 'Guests'])  # Header row
            for i, table in enumerate(tables, 1):
                writer.writerow([f'Table {i}', ', '.join(table)])
