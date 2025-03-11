import random
import math

def calculate_cost(tables, guests):
    cost = 0
    for table in tables:
        for guest in table:
            for preferred_guest in guests[guest]['prefers']:
                if preferred_guest in table:
                    cost -= 1  
            for avoided_guest in guests[guest]['avoids']:
                if avoided_guest in table:
                    cost += 1  
    return cost

def calculate_tables_needed(num_guests, seats_per_table=6):
    return math.ceil(num_guests / seats_per_table)

def create_random_seating(guests, min_per_table=4, max_per_table=6):
    guest_list = list(guests.keys())
    total_guests = len(guest_list)
    
    # Calculate optimal number of tables
    # Try to maximize table usage while keeping tables within min-max limits
    num_tables = max(2, total_guests // ((min_per_table + max_per_table) // 2))
    
    # Verify if we can reduce number of tables
    while num_tables > 2:
        guests_per_table = math.ceil(total_guests / (num_tables - 1))
        if guests_per_table <= max_per_table:
            num_tables -= 1
        else:
            break
    
    # Calculate final distribution
    base_guests_per_table = total_guests // num_tables
    extra_guests = total_guests % num_tables
    
    # Create and fill tables
    tables = [[] for _ in range(num_tables)]
    random.shuffle(guest_list)
    guest_index = 0
    
    for table_index in range(num_tables):
        guests_for_this_table = base_guests_per_table + (1 if table_index < extra_guests else 0)
        tables[table_index] = guest_list[guest_index:guest_index + guests_for_this_table]
        guest_index += guests_for_this_table
    
    return tables
