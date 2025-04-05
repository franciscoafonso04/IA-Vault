import random
import math
import copy
from datetime import datetime
import plotting
import file_handler

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


def validate_parameters(params, num_guests):
    """
    Validate the parameters to ensure they are logical and within acceptable ranges.
    
    Args:
        params (dict): Dictionary containing the parameters.
        num_guests (int): Total number of guests.
    
    Raises:
        ValueError: If any parameter is invalid.
    """
    # Verifica min_per_table e max_per_table
    if not (isinstance(params["min_per_table"], int) and params["min_per_table"] > 0):
        raise ValueError("min_per_table must be a positive integer.")
    if not (isinstance(params["max_per_table"], int) and params["max_per_table"] > 0):
        raise ValueError("max_per_table must be a positive integer.")
    if params["max_per_table"] < params["min_per_table"]:
        raise ValueError("max_per_table must be greater than or equal to min_per_table.")
    
    # Verifica se o número de mesas é viável
    min_tables_needed = math.ceil(num_guests / params["max_per_table"])
    max_tables_needed = math.ceil(num_guests / params["min_per_table"])
    if min_tables_needed > max_tables_needed:
        raise ValueError("Invalid table sizes: Not possible to seat all guests with the given min_per_table and max_per_table.")
    
    # Verifica initial_temperature
    if not (isinstance(params["initial_temperature"], (int, float)) and params["initial_temperature"] > 0):
        raise ValueError("initial_temperature must be a positive number.")
    
    # Verifica cooling_rate
    if not (isinstance(params["cooling_rate"], (int, float)) and 0 < params["cooling_rate"] < 1):
        raise ValueError("cooling_rate must be between 0 and 1.")
    
    # Verifica iterations
    if not (isinstance(params["iterations"], int) and params["iterations"] > 0):
        raise ValueError("iterations must be a positive integer.")
    
    # Verifica cooling_type
    if params["cooling_type"] not in ["exponential", "linear", "logarithmic"]:
        raise ValueError("cooling_type must be 'exponential', 'linear', or 'logarithmic'.")
    
def simulated_annealing(guests, initial_temperature, cooling_rate, iterations, min_per_table, max_per_table, cooling_type, output_folder=None):
    """Apply simulated annealing to find an optimal seating arrangement."""
    
    # Initialize metrics collection
    metrics = {
        'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
        'iterations': [],
        'costs': [],
        'best_costs': [],
        'temperatures': []
    }
    
    # Create initial solution
    tables = create_balanced_seating(guests, min_per_table, max_per_table)
    current_cost = calculate_cost(tables, guests)
    
    best_tables = copy.deepcopy(tables)
    best_cost = current_cost
    temperature = initial_temperature
    
    for i in range(iterations):
        # Record metrics
        metrics['iterations'].append(i)
        metrics['costs'].append(current_cost)
        metrics['best_costs'].append(best_cost)
        metrics['temperatures'].append(temperature)
        
        # Generate neighbor solution
        neighbor_tables = create_neighbor(tables, min_per_table, max_per_table)
        neighbor_cost = calculate_cost(neighbor_tables, guests)
        
        # Calculate delta cost
        delta_cost = neighbor_cost - current_cost
        
        # Decide whether to accept the new solution
        if delta_cost < 0 or random.random() < math.exp(-delta_cost / temperature):
            tables = neighbor_tables
            current_cost = neighbor_cost
            
            # Update best solution if this is better
            if current_cost < best_cost:
                best_tables = copy.deepcopy(tables)
                best_cost = current_cost
        
        # Cool down temperature
        if cooling_type == "exponential":
            temperature *= cooling_rate
        elif cooling_type == "linear":
            temperature -= initial_temperature / iterations
        elif cooling_type == "logarithmic":
            temperature = initial_temperature / (1 + math.log(1 + i))

        if temperature < 0.01:
            break
    
    if output_folder:
        plotting.plot_performance_metrics(metrics, save_dir=output_folder)
    else:
        plotting.plot_performance_metrics(metrics)
    
    # Print final results
    final_sizes = [len(table) for table in best_tables]
    print(f"Simulated annealing completed. Best cost: {round(float(best_cost),2)}, Table sizes: {final_sizes}")
    
    return best_tables

def create_balanced_seating(guests, min_per_table, max_per_table):
    """
    Create a perfectly balanced initial seating arrangement
    """
    guest_list = list(guests.keys())
    total_guests = len(guest_list)
    
    # Calculate number of tables needed
    num_tables = math.ceil(total_guests / max_per_table)

    if num_tables * min_per_table > len(guest_list):
        raise ValueError("Not possible to create a disposition with those arguments.")
    
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

def genetic_algorithm(guests, min_per_table, max_per_table, population_size=10, generations=1000, mutation_rate=0.01):
    """
    Implements a Genetic Algorithm to optimize guest seating arrangements.
    """
    import random
    
    def create_initial_population():
        """Creates an initial population of balanced table arrangements."""
        population = []
        for _ in range(population_size):
            tables = create_balanced_seating(guests, min_per_table, max_per_table)
            all_guests = [guest for table in tables for guest in table]
            if len(all_guests) != len(set(all_guests)):
                raise ValueError("Duplicate guests detected in initial population!")
            population.append(tables)
        return population
    
    def select_parents(population):
        """Selects two parents using tournament selection."""
        tournament_size = min(10, len(population))  # Ensure tournament size is not larger than the population
        tournament = random.sample(population, tournament_size)
        tournament.sort(key=lambda x: calculate_cost(x, guests))  # Sort by cost
        return tournament[0], tournament[1]  # Pick best two

    
    def crossover(parent1, parent2):
        """Performs crossover between two parents to generate a child."""
        child = []
        used_guests = set()

        # Combine tables from both parents while avoiding duplicates
        for table1, table2 in zip(parent1, parent2):
            combined_table = []
            for guest in table1 + table2:
                if guest not in used_guests:
                    combined_table.append(guest)
                    used_guests.add(guest)
            child.append(combined_table)

        # Redistribute guests to balance tables
        all_guests = set(guest for table in parent1 + parent2 for guest in table)
        missing_guests = all_guests - used_guests

        # Flatten child tables and redistribute guests
        flattened_child = [guest for table in child for guest in table]
        flattened_child.extend(missing_guests)

        # Calculate the number of tables needed
        num_tables = len(parent1)  # Assume the number of tables is the same as the parents
        avg_table_size = len(flattened_child) // num_tables
        extra_guests = len(flattened_child) % num_tables

        # Create balanced tables
        child = []
        start_idx = 0
        for i in range(num_tables):
            table_size = avg_table_size + (1 if i < extra_guests else 0)
            table = flattened_child[start_idx:start_idx + table_size]
            child.append(table)
            start_idx += table_size

        # Validate the child
        all_guests_in_child = [guest for table in child for guest in table]
        if len(all_guests_in_child) != len(all_guests) or len(all_guests_in_child) != len(set(all_guests_in_child)):
            print("Debug: Parent 1:", parent1)
            print("Debug: Parent 2:", parent2)
            print("Debug: Child:", child)
            print("Debug: Missing Guests:", missing_guests)
            raise ValueError("Crossover produced an invalid child: Missing or duplicate guests!")

        return child

    
    def mutate(individual):
        """Applies mutation to an individual to introduce diversity."""
        max_retries = 10  # Limit the number of retries to avoid infinite loops
        for _ in range(max_retries):
            # Select two random tables
            table1, table2 = random.sample(individual, 2)

            # Swap two random guests between the tables
            if table1 and table2:
                guest1 = random.choice(table1)
                guest2 = random.choice(table2)
                table1[table1.index(guest1)], table2[table2.index(guest2)] = guest2, guest1

            # Ensure no duplicates across all tables
            all_guests = [guest for table in individual for guest in table]
            if len(all_guests) == len(set(all_guests)):
                return individual  # Return the valid individual if no duplicates are found

        # If retries are exhausted, return the original individual without mutation
        print("Warning: Mutation failed to produce a valid individual after retries.")
        return individual
    
    def validate_population(population, guests):
        """Ensures that all individuals in the population are valid."""
        for individual in population:
            all_guests = [guest for table in individual for guest in table]
            if len(all_guests) != len(guests):
                raise ValueError("Population contains an invalid individual: Missing guests!")
            if len(all_guests) != len(set(all_guests)):
                raise ValueError("Population contains an invalid individual: Duplicate guests!")

 
    population = create_initial_population()
    validate_population(population, guests)

    for generation in range(generations):
        new_population = []

        # Generate children through crossover and mutation
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2), crossover(parent2, parent1)
            new_population.extend([mutate(child1), mutate(child2)])

        # Keep the best individuals (elitism)
        elite_size = 5  # Number of best individuals to carry over
        elites = sorted(population, key=lambda x: calculate_cost(x, guests))[:elite_size]

        # Combine elites with the new population
        combined_population = elites + new_population

        # Select the top individuals to form the next generation
        population = sorted(combined_population, key=lambda x: calculate_cost(x, guests))[:population_size]

        # Validate the population
        validate_population(population, guests)

        # Debugging information
        if generation % 100 == 0:
            print(f"Generation {generation}: Best cost = {calculate_cost(population[0], guests)}")
            print(f"Population diversity: {len(set(tuple(tuple(table) for table in individual) for individual in population))} unique individuals")

    # Return the best solution
    best_tables = min(population, key=lambda x: calculate_cost(x, guests))
    print(f"Best tables found: Cost = {calculate_cost(best_tables, guests)}")
    return best_tables

def hill_climbing(guests, min_per_table, max_per_table, iterations=500):
    """
    Algoritmo ganancioso (greedy): aceita apenas vizinhos com melhor custo.
    Útil como baseline simples para comparação com metaheurísticas.
    """

    current = create_balanced_seating(guests, min_per_table, max_per_table)
    current_cost = calculate_cost(current, guests)
    best = copy.deepcopy(current)
    best_cost = current_cost

    for _ in range(iterations):
        neighbor = create_neighbor(current, min_per_table, max_per_table)
        neighbor_cost = calculate_cost(neighbor, guests)

        if neighbor_cost < current_cost:
            current = neighbor
            current_cost = neighbor_cost

            if neighbor_cost < best_cost:
                best = copy.deepcopy(neighbor)
                best_cost = neighbor_cost

    return best
