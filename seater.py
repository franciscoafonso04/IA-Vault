import random
import math
import copy
from datetime import datetime
import plotting

# ============================================================================================================================================================
# Função: calculate_cost
# Descrição: Calcula o custo total de uma disposição de convidados.
# Penaliza estar com quem se quer evitar e recompensa estar com quem se prefere.
# Penaliza também mesas desequilibradas.
# ============================================================================================================================================================

def calculate_cost(tables, guests):
    
    cost = 0
    # Itera sobre cada mesa
    for table in tables:
        for guest in table:
            preferences = guests[guest]
            
            # Penaliza por estar com quem se quer evitar.
            cost += sum(20 for avoided in preferences['avoids'] if avoided in table)

            # Recompensa por estar com quem se prefere.
            cost -= sum(10 for preferred in preferences['prefers'] if preferred in table)
                    
    # Penaliza mesas desequilibradas
    table_sizes = [len(table) for table in tables]
    if not table_sizes:
        return cost
    
    avg_size = sum(table_sizes) / len(tables) if tables else 0
    max_size = max(table_sizes)
    min_size = min(table_sizes)
    
    # Penaliza mesas com mais de 1 convidado de diferença
    if max_size - min_size > 1:
        cost += (max_size - min_size) * 200 # Penalidade alta para mesas muito desequilibradas
    
    # Adiciona penalidade para mesas com tamanhos muito diferentes da média
    for size in table_sizes:
        cost += abs(size - avg_size) * 20  # Penalidade proporcional à diferença do tamanho médio
                    
    return cost

# ========================================================================================================================================================
# Função: calculate_tables_needed
# Descrição: Calcula o número de mesas necessárias dado o número de convidados.
# ========================================================================================================================================================

def calculate_tables_needed(num_guests, seats_per_table=6):
    return math.ceil(num_guests / seats_per_table)

# ========================================================================================================================================================
# Função: evaluate_seating
# Descrição: Avalia uma disposição de mesas atribuindo uma pontuação positiva
# por estar com preferidos e negativa por estar com evitados.
# ========================================================================================================================================================

def evaluate_seating(tables, guests):
    
    score = 0
    
    # Para cada mesa
    for table in tables:
        # Para cada convidado na mesa
        for guest in table:
            preferences = guests[guest]
            
            # Checka se pessoas preferidas estão na mesma mesa (bonus)
            for preferred in preferences.get('prefers',[]):
                if preferred in table:
                    score += 10  # Aumenta a pontuação se preferidos estão juntos
            
            # Checka se pessoas evitadas estão na mesma mesa (penalidade)
            for avoided in preferences.get('avoids',[]):
                if avoided in table:
                    score -= 20  # Diminui a pontuação se evitados estão juntos
    
    return score

# ========================================================================================================================================================
# Função: calculate_theoretical_perfect_score
# Descrição: Calcula o score perfeito se todos os convidados estivessem com os
# seus preferidos.
# ========================================================================================================================================================

def calculate_theoretical_perfect_score(guests):
    
    perfect_score = 0
    
    # Para cada convidado
    for guest, preferences in guests.items():
        # Contar quantas pessoas preferidas quer que fiquem na mesma mesa que ele
        preferred_count = len(preferences['prefers'])
        # Adiciona 10 pontos por cada preferido
        perfect_score += preferred_count * 10
    
    return perfect_score

# ========================================================================================================================================================
# Função: create_neighbor
# Descrição: Gera uma nova solução válida a partir da atual mudando convidados
# entre mesas de forma a manter os limites.
# ========================================================================================================================================================

def create_neighbor(tables, min_per_table, max_per_table):
    
    new_tables = copy.deepcopy(tables)                      # Cria uma cópia da disposição atual
    
    table_sizes = [len(table) for table in new_tables]      # Obtém o número de mesas
    min_size = min(table_sizes)                             # Obtém o tamanho mínimo   
    max_size = max(table_sizes)                             # Obtém o tamanho máximo    
    
    # Se a diferença entre o tamanho máximo e mínimo for maior que 1, força a mudança
    if max_size - min_size > 1:

        # Identifica as mesas maiores e menores
        largest_tables = [i for i, size in enumerate(table_sizes) if size == max_size]
        smallest_tables = [i for i, size in enumerate(table_sizes) if size == min_size]
        
        # Escolhe aleatoriamente uma mesa maior e uma menor
        from_table = random.choice(largest_tables)
        to_table = random.choice(smallest_tables)
        
        if new_tables[from_table]:  # Verifica se a mesa não está vazia
            guest_index = random.randint(0, len(new_tables[from_table]) - 1)
            guest = new_tables[from_table].pop(guest_index)
            new_tables[to_table].append(guest)      # Adiciona o convidado à mesa menor

        return new_tables
    
    # Mantém os limites de capacidade em todas as operações
    def is_valid_move(from_table, to_table):
        return (
            len(new_tables[from_table]) > min_per_table and
            len(new_tables[to_table]) < max_per_table
        )
    
    # Se não houver mesas desequilibradas, escolhe aleatoriamente entre swap e move
    operation = random.choice(['swap', 'move'])
    
    if operation == 'swap' and len(new_tables) >= 2:
        # Swap: Troca dois convidados entre mesas diferentes
        table1_index = random.randint(0, len(new_tables) - 1)
        table2_index = random.randint(0, len(new_tables) - 1)
        
        # Mantém a condição de que as mesas não sejam iguais
        while table1_index == table2_index:
            table2_index = random.randint(0, len(new_tables) - 1)
            
        # Verifica se as mesas não estão vazias
        if new_tables[table1_index] and new_tables[table2_index]:
            guest1_index = random.randint(0, len(new_tables[table1_index]) - 1)
            guest2_index = random.randint(0, len(new_tables[table2_index]) - 1)
            
            # Troca os convidados entre as mesas
            new_tables[table1_index][guest1_index], new_tables[table2_index][guest2_index] = \
                new_tables[table2_index][guest2_index], new_tables[table1_index][guest1_index]
    
    elif operation == 'move' and len(new_tables) >= 2:
        from_table = random.randint(0, len(new_tables) - 1)     
        to_table = random.randint(0, len(new_tables) - 1)
        if from_table != to_table and new_tables[from_table]:
        
        # Move: Move um convidado de uma mesa para outra
            if is_valid_move(from_table, to_table):
                guest_index = random.randint(0, len(new_tables[from_table]) - 1)
                guest = new_tables[from_table].pop(guest_index)
                new_tables[to_table].append(guest)

    # Verifica se as mesas resultantes ainda estão dentro dos limites
    if any(len(table) < min_per_table or len(table) > max_per_table for table in new_tables):
        return tables 
    
    return new_tables

# ========================================================================================================================================================
# Função: validate_parameters
# Descrição: Valida os parâmetros fornecidos para garantir que fazem sentido.
# Lança exceções se houver algo inválido.
# ========================================================================================================================================================

def validate_parameters(params, num_guests):
    
    # Verifica min_per_table e max_per_table
    if not (isinstance(params["min_per_table"], int) and params["min_per_table"] > 0):
        raise ValueError("min_per_table deve ser um inteiro positivo.")
    if not (isinstance(params["max_per_table"], int) and params["max_per_table"] > 0):
        raise ValueError("max_per_table deve ser um inteiro positivo.")
    if params["max_per_table"] < params["min_per_table"]:
        raise ValueError("max_per_table deve ser maior ou igual a min_per_table.")
    
    # Verifica se o número de mesas é viável
    min_tables_needed = math.ceil(num_guests / params["max_per_table"])
    max_tables_needed = math.ceil(num_guests / params["min_per_table"])
    if min_tables_needed > max_tables_needed:
        raise ValueError("Tamanho inviável para as mesas. min_per_table e max_per_table não permitem acomodar todos os convidados.")
    
    # Verifica initial_temperature
    if not (isinstance(params["initial_temperature"], (int, float)) and params["initial_temperature"] > 0):
        raise ValueError("initial_temperature deve ser um número positivo.")
    
    # Verifica cooling_rate
    if not (isinstance(params["cooling_rate"], (int, float)) and 0 < params["cooling_rate"] < 1):
        raise ValueError("cooling_rate deve ser um número entre 0 e 1.")
    
    # Verifica iterations
    if not (isinstance(params["iterations"], int) and params["iterations"] > 0):
        raise ValueError("iterations deve ser um inteiro positivo.")
    
    # Verifica cooling_type
    if params["cooling_type"] not in ["exponential", "linear", "logarithmic"]:
        raise ValueError("cooling_type deve ser 'exponential', 'linear' ou 'logarithmic'.")

# ========================================================================================================================================================
# Função: create_balanced_seating
# Descrição: Cria uma disposição inicial equilibrada entre mesas. Tenta maximizar
# preferências já de início.
# ========================================================================================================================================================

def create_balanced_seating(guests, min_per_table, max_per_table):
    
    # Cria uma lista de convidados e calcula o seu número total de convidados
    guest_list = list(guests.keys())    
    total_guests = len(guest_list)  
    
    # Calcula o número de mesas necessárias
    num_tables = math.ceil(total_guests / max_per_table)

    if num_tables * min_per_table > len(guest_list):
        raise ValueError("Número de mesas insuficiente para acomodar todos os convidados.")
    
    # Calcula o tamanho ideal de cada mesa
    ideal_size = total_guests / num_tables
    base_size = math.floor(ideal_size)
    extra = total_guests - (base_size * num_tables)
    
    # Assegura que o número de mesas não excede o máximo permitido
    if base_size + 1 > max_per_table:
        num_tables += 1
        # Recalcula o tamanho ideal
        ideal_size = total_guests / num_tables
        base_size = math.floor(ideal_size)
        extra = total_guests - (base_size * num_tables)
    
    # Checka se o número de mesas é viável
    if base_size < min_per_table and extra < num_tables:
        
        # Se adicionar uma mesa extra não violar o limite mínimo por mesa
        test_num_tables = num_tables - 1
        test_base_size = total_guests // test_num_tables
        test_extra = total_guests % test_num_tables
        
        if test_base_size >= min_per_table:
            num_tables = test_num_tables
            base_size = test_base_size
            extra = test_extra
    
    # Inicializa a lista de mesas
    random.shuffle(guest_list)
    tables = []
    guest_index = 0
    
    # Cria as mesas com o número ideal de convidados
    for i in range(num_tables):
        table_size = base_size + (1 if i < extra else 0)
        table = guest_list[guest_index:guest_index + table_size]
        tables.append(table)
        guest_index += table_size
    
    # Verifica se o número de mesas não excede o máximo permitido
    sizes = [len(table) for table in tables]
    
    best_tables = tables.copy()
    best_score = evaluate_seating(tables, guests)
    
    # Experimenta várias disposições para encontrar uma boa
    for attempt in range(1000):  
        # Cria uma nova disposição aleatória
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

# ========================================================================================================================================================
# Função: simulated_annealing
# Descrição: Implementa o algoritmo de Simulated Annealing para encontrar uma
# disposição de convidados com custo mínimo. Guarda métricas e gráficos.
# ========================================================================================================================================================

def simulated_annealing(guests, initial_temperature, cooling_rate, iterations, min_per_table, max_per_table, cooling_type, output_folder=None):
    
    # Inicializa parâmetros
    metrics = {
        'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
        'iterations': [],
        'costs': [],
        'best_costs': [],
        'temperatures': []
    }
    
    tables = create_balanced_seating(guests, min_per_table, max_per_table)      # Cria uma disposição inicial
    current_cost = calculate_cost(tables, guests)                               # Calcula o custo inicial
    best_tables = copy.deepcopy(tables)                                         # Guarda a melhor disposição        
    best_cost = current_cost                                                    # Guarda o melhor custo 
    temperature = initial_temperature                                           # Inicializa a temperatura
    
    for i in range(iterations):
        # Guarda métricas
        metrics['iterations'].append(i)
        metrics['costs'].append(current_cost)
        metrics['best_costs'].append(best_cost)
        metrics['temperatures'].append(temperature)
        
        # Gera um vizinho
        neighbor_tables = create_neighbor(tables, min_per_table, max_per_table)
        neighbor_cost = calculate_cost(neighbor_tables, guests)
        
        # Calcula a diferença de custo
        delta_cost = neighbor_cost - current_cost
        
        # Decide se aceita o vizinho
        if delta_cost < 0 or random.random() < math.exp(-delta_cost / temperature):
            tables = neighbor_tables
            current_cost = neighbor_cost
            
            # Atualiza a melhor disposição se o custo for melhor
            if current_cost < best_cost:
                best_tables = copy.deepcopy(tables)
                best_cost = current_cost
        
        # Atualiza a temperatura
        if cooling_type == "exponential":
            temperature *= cooling_rate
        elif cooling_type == "linear":
            temperature -= initial_temperature / iterations
        elif cooling_type == "logarithmic":
            temperature = initial_temperature / (1 + math.log(1 + i))

        if temperature < 0.01:  # Limite mínimo para a temperatura
            break
    
    # Cria a pasta de resultados
    if output_folder:
        plotting.plot_performance_metrics(metrics, save_dir=output_folder)
    else:
        plotting.plot_performance_metrics(metrics)
    
    return best_tables

# ========================================================================================================================================================
# Função: genetic_algorithm
# Descrição: Algoritmo genético com seleção, crossover, mutação e elitismo.
# Requer tuning para resultados mais estáveis.
# ========================================================================================================================================================

def genetic_algorithm(guests, min_per_table, max_per_table, population_size, generations, mutation_rate, output_folder=None):
    
    # -----------------------------------------------------
    # Criação da população inicial com disposições válidas
    # -----------------------------------------------------
    def create_initial_population():
        population = []
        for _ in range(population_size):
            tables = create_balanced_seating(guests, min_per_table, max_per_table)
            all_guests = [guest for table in tables for guest in table]

            # Validação: garantir que não há convidados repetidos
            if len(all_guests) != len(set(all_guests)):
                raise ValueError("Convidados duplicados!")
            population.append(tables)
        return population
    
    # -----------------------------------------------------
    # Seleção dos pais via torneio (Tournament Selection)
    # Escolhe os dois melhores de um subconjunto aleatório
    # -----------------------------------------------------
    def select_parents(population):
        tournament_size = min(10, len(population))                  # Assegura que o tamanho do torneio não exceda a população
        tournament = random.sample(population, tournament_size)     # Seleciona aleatoriamente um subconjunto
        tournament.sort(key=lambda x: calculate_cost(x, guests))    # Ordena pelo custo
        return tournament[0], tournament[1]                         # Seleciona os dois melhores
    
    # -----------------------------------------------------
    # Crossover: gera um filho combinando duas soluções
    # Combina mesas dos pais evitando convidados repetidos
    # -----------------------------------------------------
    def crossover(parent1, parent2):
        child = []
        used_guests = set()

        # Combina mesas de ambos os pais (sem repetições)
        for table1, table2 in zip(parent1, parent2):
            combined_table = []
            for guest in table1 + table2:
                if guest not in used_guests:
                    combined_table.append(guest)    # Adiciona o convidado se não estiver repetido
                    used_guests.add(guest)          # Marca como usado
            child.append(combined_table)

        # Verifica se há convidados por atribuir e adiciona
        all_guests = set(guest for table in parent1 + parent2 for guest in table)
        missing_guests = all_guests - used_guests

        # Flatten da solução e redistribuição balanceada
        flattened_child = [guest for table in child for guest in table]
        flattened_child.extend(missing_guests)

        # Calcula o tamanho necessário para cada mesa
        num_tables = len(parent1)                               # Assume o mesmo número de mesas que os pais
        avg_table_size = len(flattened_child) // num_tables     
        extra_guests = len(flattened_child) % num_tables

        # Cria mesas balanceadas
        child = []
        start_idx = 0
        for i in range(num_tables):
            table_size = avg_table_size + (1 if i < extra_guests else 0)
            table = flattened_child[start_idx:start_idx + table_size]
            child.append(table)
            start_idx += table_size

        # Validação do filho: todos os convidados presentes, sem duplicados
        all_guests_in_child = [guest for table in child for guest in table]
        if len(all_guests_in_child) != len(all_guests) or len(all_guests_in_child) != len(set(all_guests_in_child)):
            raise ValueError("Crossover produziu um filho inválido!")

        return child

    # -----------------------------------------------------
    # Mutação: troca dois convidados aleatórios entre mesas
    # Ajuda a diversificar a população e escapar de mínimos
    # -----------------------------------------------------
    def mutate(individual):
        
        max_retries = 10  # Limita o número de tentativas para evitar loops infinitos
        for _ in range(max_retries):
            # Seleciona duas mesas aleatórias
            table1, table2 = random.sample(individual, 2)

            # Troca dois convidados entre as mesas
            if table1 and table2:
                guest1 = random.choice(table1)
                guest2 = random.choice(table2)
                table1[table1.index(guest1)], table2[table2.index(guest2)] = guest2, guest1

            # Assegura que a mutação não cria duplicatas
            all_guests = [guest for table in individual for guest in table]
            if len(all_guests) == len(set(all_guests)):
                return individual  # Retorna o indivíduo mutado se válido

        # Se tentativas falharem, retorna o indivíduo original
        print("Warning: Mutation failed to produce a valid individual after retries.")
        return individual
    
    # -----------------------------------------------------
    # Validação da população: todos os convidados e únicos
    # -----------------------------------------------------
    def validate_population(population, guests):
        
        for individual in population:
            all_guests = [guest for table in individual for guest in table]
            if len(all_guests) != len(guests):
                raise ValueError("Population contains an invalid individual: Missing guests!")
            if len(all_guests) != len(set(all_guests)):
                raise ValueError("Population contains an invalid individual: Duplicate guests!")

    # -------------------------
    # Etapa 1: inicialização
    # -------------------------
    population = create_initial_population()
    validate_population(population, guests)
    best_costs = []  # Guarda os melhores custos para plotar depois
    # -------------------------
    # Etapa 2: evolução
    # -------------------------
    for generation in range(generations):
        new_population = []

        # Geração de filhos
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2), crossover(parent2, parent1)
            new_population.extend([mutate(child1), mutate(child2)])

        # Elitismo: preserva os melhores da geração atual
        elite_size = 5  # Number of best individuals to carry over
        elites = sorted(population, key=lambda x: calculate_cost(x, guests))[:elite_size]

        # Combina elites e novos filhos
        combined_population = elites + new_population

        # Seleciona os melhores para a próxima geração
        population = sorted(combined_population, key=lambda x: calculate_cost(x, guests))[:population_size]
        validate_population(population, guests)

        # Print debug ocasionalmente
        if generation % 100 == 0:
            best_cost = calculate_cost(population[0], guests)
            best_costs.append(calculate_cost(population[0], guests))
            print(f"Geracão {generation}: Melhor custo = {best_cost}")
            print(f"Diversidade da Populacão: {len(set(tuple(tuple(table) for table in individual) for individual in population))} indivíduos únicos")

    # -------------------------
    # Etapa 3: resultado final
    # -------------------------
    best_tables = min(population, key=lambda x: calculate_cost(x, guests))
    plotting.plot_genetic_progress(best_costs, save_dir=output_folder)
    print(f"Best tables found: Cost = {calculate_cost(best_tables, guests)}")
    return best_tables

# ========================================================================================================================================================
# Função: hill_climbing
# Descrição: Algoritmo ganancioso. Aceita apenas vizinhos que melhoram o custo.
# Útil como baseline para comparação com heurísticas mais avançadas.
# ========================================================================================================================================================
def hill_climbing(guests, min_per_table, max_per_table, iterations=500, output_folder=None):
    
    current = create_balanced_seating(guests, min_per_table, max_per_table)     # Cria uma disposição inicial
    current_cost = calculate_cost(current, guests)                              # Calcula o custo inicial   
    best = copy.deepcopy(current)                                               # Guarda a melhor disposição
    best_cost = current_cost                                                    # Guarda o melhor custo 

    costs = []                                                                 # Guarda os custos para plotar depois
    for _ in range(iterations):
        neighbor = create_neighbor(current, min_per_table, max_per_table)       # Gera um vizinho
        neighbor_cost = calculate_cost(neighbor, guests)                        # Calcula o custo do vizinho
        costs.append(neighbor_cost)                                             # Guarda o custo do vizinho
        if neighbor_cost < current_cost:                                        # Aceita o vizinho se o custo for melhor
            current = neighbor
            current_cost = neighbor_cost

            if neighbor_cost < best_cost:                                       # Atualiza a melhor disposição se o custo for melhor
                best = copy.deepcopy(neighbor)                                  
                best_cost = neighbor_cost 

    plotting.plot_hill_climbing_progress(costs, save_dir=output_folder)
    return best              
