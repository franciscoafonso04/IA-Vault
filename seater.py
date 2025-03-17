import random
import math
import copy

def calculate_cost(tables, guests):
    """
    Calculate the cost (energy) of a seating arrangement.
    Lower cost means better arrangement.

    The cost is calculated based on:
      - Rewarding seating guests with those they prefer.
      - Penalizing seating guests with those they want to avoid.
      - Adding penalties for unbalanced table sizes.
    """

    cost = 0
    
    # Check each table
    for table in tables:
        for guest in table:
            preferences = guests[guest]
            
            # Penalty for being seated with someone the guest wants to avoid.
            cost += sum(20 for avoided in preferences['avoids'] if avoided in table)

            # Reward for being seated with a preferred guest.
            cost -= sum(10 for preferred in preferences['prefers'] if preferred in table)
                    
    # Add much stronger penalty for unbalanced tables.
    table_sizes = [len(table) for table in tables]
    if not table_sizes:
        return cost
    
    avg_size = sum(table_sizes) / len(tables) if tables else 0
    max_size = max(table_sizes)
    min_size = min(table_sizes)
    
    # Extreme penalty if max and min differ by more than 1
    if max_size - min_size > 1:
        cost += (max_size - min_size) * 200 # Scalable Penalty
    
    # Normal balance penalty proportional to deviation from the average table size.
    for size in table_sizes:
        cost += abs(size - avg_size) * 20  # Higher penalty for unbalanced tables
                    
    return cost

def calculate_tables_needed(num_guests, seats_per_table=6):
    return math.ceil(num_guests / seats_per_table)

def evaluate_seating(tables, guests):
    """
    Evaluate how good a seating arrangement is based on guest preferences.
    Higher score means better arrangement.
    """
    score = 0
    
    # Check each table
    for table in tables:
        # For each guest at this table
        for guest in table:
            preferences = guests[guest]
            
            # Check if preferred people are at same table
            for preferred in preferences.get('prefers',[]):
                if preferred in table:
                    score += 10  # High positive score for respecting "together" preferences
            
            # Check if avoided people are at same table (penalty)
            for avoided in preferences.get('avoids',[]):
                if avoided in table:
                    score -= 20  # High penalty for putting people who should be apart together
    
    return score



def create_neighbor(tables, min_per_table, max_per_table):
    """
    Create a neighbor solution by making a small change to the current solution
    while maintaining balanced tables.
    Returns a new tables arrangement without modifying the original.
    """
    new_tables = copy.deepcopy(tables)
    
    # Get current table sizes
    table_sizes = [len(table) for table in new_tables]
    min_size = min(table_sizes)
    max_size = max(table_sizes)
    
    # If tables are severely unbalanced, force balancing
    if max_size - min_size > 1:
        # Find the largest and smallest tables
        largest_tables = [i for i, size in enumerate(table_sizes) if size == max_size]
        smallest_tables = [i for i, size in enumerate(table_sizes) if size == min_size]
        
        # Force move from largest to smallest
        from_table = random.choice(largest_tables)
        to_table = random.choice(smallest_tables)
        
        if new_tables[from_table]:  # Make sure source table is not empty
            guest_index = random.randint(0, len(new_tables[from_table]) - 1)
            guest = new_tables[from_table].pop(guest_index)
            new_tables[to_table].append(guest)

        return new_tables
    
    # Mantém os limites de capacidade em todas as operações
    def is_valid_move(from_table, to_table):
        return (
            len(new_tables[from_table]) > min_per_table and
            len(new_tables[to_table]) < max_per_table
        )
    # If tables are balanced (diff ≤ 1), use normal operations
    operation = random.choice(['swap', 'move'])
    
    if operation == 'swap' and len(new_tables) >= 2:
        # Swap: Choose two random guests on different tables and swap them
        table1_index = random.randint(0, len(new_tables) - 1)
        table2_index = random.randint(0, len(new_tables) - 1)
        
        # Ensure different tables
        while table1_index == table2_index:
            table2_index = random.randint(0, len(new_tables) - 1)
            
        # Ensure neither table is empty
        if new_tables[table1_index] and new_tables[table2_index]:
            guest1_index = random.randint(0, len(new_tables[table1_index]) - 1)
            guest2_index = random.randint(0, len(new_tables[table2_index]) - 1)
            
            # Swap guests - this preserves table sizes
            new_tables[table1_index][guest1_index], new_tables[table2_index][guest2_index] = \
                new_tables[table2_index][guest2_index], new_tables[table1_index][guest1_index]
    
    elif operation == 'move' and len(new_tables) >= 2:
        from_table = random.randint(0, len(new_tables) - 1)     
        to_table = random.randint(0, len(new_tables) - 1)
        if from_table != to_table and new_tables[from_table]:
           
           # Check capacity constraints before moving:
            if is_valid_move(from_table, to_table):
              guest_index = random.randint(0, len(new_tables[from_table]) - 1)
              guest = new_tables[from_table].pop(guest_index)
              new_tables[to_table].append(guest)

    # Reassures that every table respects the mins and maxs.
    if any(len(table) < min_per_table or len(table) > max_per_table for table in new_tables):
        return tables 
    
    return new_tables

def simulated_annealing(guests, initial_temperature=100, cooling_rate=0.97, iterations=2000, min_per_table=4, max_per_table=6, cooling_type="exponential"):
    """
    Apply simulated annealing to find an optimal seating arrangement.
    """
    # Create initial solution
    tables = create_balanced_seating(guests, min_per_table, max_per_table)
    current_cost = calculate_cost(tables, guests)
    
    best_tables = copy.deepcopy(tables)
    best_cost = current_cost
    temperature = initial_temperature
    
    for i in range(iterations):
        # Generate a neighbor solution
        neighbor_tables = create_neighbor(tables, min_per_table, max_per_table)
        neighbor_cost = calculate_cost(neighbor_tables, guests)
        
        # Calculate delta cost (change in cost)
        delta_cost = neighbor_cost - current_cost
        
        # Decide whether to accept the new solution
        if delta_cost < 0:  # Better solution, always accept
            tables = neighbor_tables
            current_cost = neighbor_cost
            
            # Update best solution if this is better
            if current_cost < best_cost:
                best_tables = copy.deepcopy(tables)
                best_cost = current_cost
        else:
            # Worse solution, accept with a probability
            acceptance_probability = math.exp(-delta_cost / temperature)
            if random.random() < acceptance_probability:
                tables = neighbor_tables
                current_cost = neighbor_cost
        
        # Cool down the temperature
        if cooling_type == "exponential":
            temperature *= cooling_rate
        elif cooling_type == "linear":
            temperature -= initial_temperature / iterations
        elif cooling_type == "logarithmic":
            temperature = initial_temperature / (1 + math.log(1 + i))

        if temperature < 0.01:
            break
        
        # Optionally print progress
        if i % 100 == 0:
            # Check table sizes to monitor balance
            sizes = [len(table) for table in tables]
            print(f"Iteration {i}, Cost: {current_cost}, Temperature: {temperature:.2f}, Table sizes: {sizes}")
    
    # Verify final solution is balanced
    final_sizes = [len(table) for table in best_tables]
    print(f"Simulated annealing completed. Best cost found: {best_cost}, Table sizes: {final_sizes}")
    return best_tables

def create_balanced_seating(guests, min_per_table=4, max_per_table=6):
    """
    Create a perfectly balanced initial seating arrangement
    """
    guest_list = list(guests.keys())
    total_guests = len(guest_list)
    
    # Calculate number of tables needed
    num_tables = math.ceil(total_guests / max_per_table)
    
    # Calculate optimal size distribution
    ideal_size = total_guests / num_tables
    base_size = math.floor(ideal_size)
    extra = total_guests - (base_size * num_tables)
    
    # Ensure we're not exceeding max_per_table
    if base_size + 1 > max_per_table:
        num_tables += 1
        # Recalculate
        ideal_size = total_guests / num_tables
        base_size = math.floor(ideal_size)
        extra = total_guests - (base_size * num_tables)
    
    # Check if we need more tables to meet the minimum size constraint
    if base_size < min_per_table and extra < num_tables:
        # If adding one more table would allow us to meet minimum constraints
        test_num_tables = num_tables - 1
        test_base_size = total_guests // test_num_tables
        test_extra = total_guests % test_num_tables
        
        if test_base_size >= min_per_table:
            num_tables = test_num_tables
            base_size = test_base_size
            extra = test_extra
    
    # Initialize tables with balanced distribution
    random.shuffle(guest_list)
    tables = []
    guest_index = 0
    
    # Create tables with base_size people
    # Add one extra person to the first 'extra' tables
    for i in range(num_tables):
        table_size = base_size + (1 if i < extra else 0)
        table = guest_list[guest_index:guest_index + table_size]
        tables.append(table)
        guest_index += table_size
    
    # Verify the created tables meet our constraints
    sizes = [len(table) for table in tables]
    print(f"Created {num_tables} balanced tables with sizes: {sizes}")
    
    # Ensure no tables differ by more than one person
    max_size = max(sizes)
    min_size = min(sizes)
    if max_size - min_size > 1:
        print("WARNING: Tables are not properly balanced!")
    
    # Try multiple random arrangements while maintaining size balance
    best_tables = tables.copy()
    best_score = evaluate_seating(tables, guests)
    
    # Try several arrangements to find a good one
    for attempt in range(1000):  # Increased from 50 to 1000
        # Create new arrangement by shuffling guests while keeping table sizes fixed
        all_guests = []
        for table in tables:
            all_guests.extend(table)
        
        random.shuffle(all_guests)
        
        new_tables = []
        start_idx = 0
        
        for size in sizes:
            table = all_guests[start_idx:start_idx + size]
            new_tables.append(table)
            start_idx += size
            
        new_score = evaluate_seating(new_tables, guests)
        
        if new_score > best_score:
            best_score = new_score
            best_tables = [table.copy() for table in new_tables]
                    
    return best_tables

# Replace create_random_seating calls with create_balanced_seating
def create_random_seating(guests, min_per_table=4, max_per_table=6):
    """
    Legacy function - now delegates to create_balanced_seating
    """
    return create_balanced_seating(guests, min_per_table, max_per_table)

def calculate_theoretical_perfect_score(guests):
    """
    Calculate the theoretical perfect score if all seating preferences were satisfied.
    
    Args:
        guests: Dictionary of guest preferences
        
    Returns:
        A theoretical perfect score
    """
    perfect_score = 0
    
    # For each guest
    for guest, preferences in guests.items():
        # Count how many preferred people they have
        preferred_count = len(preferences['prefers'])
        # Each preferred match contributes +10 to score (higher is better)
        perfect_score += preferred_count * 10
    
    return perfect_score
