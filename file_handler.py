import csv

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
