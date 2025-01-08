import random
from datetime import datetime, timedelta

# Initialize the Population
def initialize_population(units, population_size):
    population = []
    for _ in range(population_size):
        timetable = []
        for unit in units:
            # Randomly assign day and time (ensure constraints are met)
            day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
            start_time = '08:00'  # Start at 8 AM
            end_time = '11:00'  # 3 credit hours later
            timetable.append((unit, day, start_time, end_time))
        population.append(timetable)
    return population

# Define the Fitness Function
# def fitness_function(timetable):
#     score = 0
#     # Check for constraint violations and calculate the score
#     # Example: No more than 3 units per day for the same year and semester
#     daily_units = {}
#     for unit, day, start_time, end_time in timetable:
#         if day not in daily_units:
#             daily_units[day] = []
#         daily_units[day].append(unit)
#     for day, units in daily_units.items():
#         if len(units) <= 3:
#             score += 1
#     return score

def fitness_function(timetable):
    score = 0
    daily_units = {}
    for unit, day, start_time, end_time in timetable:
        if day not in daily_units:
            daily_units[day] = []
        daily_units[day].append(unit)

    # Check for constraints and calculate the score
    for day, units in daily_units.items():
        if len(units) <= 3:
            score += 1
    print(f"Timetable: {timetable}, Score: {score}")  # Debugging print
    return score


# Selection
def selection(population, fitness_values):
    selected = random.choices(population, weights=fitness_values, k=len(population))
    return selected

# Crossover
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    return offspring1, offspring2

# Mutation
# def mutation(individual, mutation_rate):
#     for i in range(len(individual)):
#         if random.random() < mutation_rate:
#             day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
#             start_time = '08:00'  # Start at 8 AM
#             end_time = '11:00'  # 3 credit hours later
#             individual[i] = (individual[i][0], day, start_time, end_time)
#     return individual


def generate_random_time():
    # Generate a random start time between 8 AM and 3 PM (latest start time for a 3-hour class)
    start_hour = random.randint(8, 15)
    start_time = datetime.strptime(f"{start_hour}:00", "%H:%M").time()
    end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=3)).time()
    return start_time, end_time

def mutation(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
            start_time, end_time = generate_random_time()
            individual[i] = (individual[i][0], day, start_time, end_time)
    return individual


# Main Genetic Algorithm Loop
# def generate_timetable(units, population_size, generations, mutation_rate):
#     population = initialize_population(units, population_size)
#     for _ in range(generations):
#         fitness_values = [fitness_function(timetable) for timetable in population]
#         population = selection(population, fitness_values)
#         next_generation = []
#         for i in range(0, len(population), 2):
#             parent1 = population[i]
#             parent2 = population[i + 1] if i + 1 < len(population) else population[0]
#             offspring1, offspring2 = crossover(parent1, parent2)
#             next_generation.append(mutation(offspring1, mutation_rate))
#             next_generation.append(mutation(offspring2, mutation_rate))
#         population = next_generation
#     best_timetable = max(population, key=fitness_function)
#     return best_timetable


def generate_timetable(units, population_size, generations, mutation_rate):
    population = initialize_population(units, population_size)
    for generation in range(generations):
        fitness_values = [fitness_function(timetable) for timetable in population]
        print(f"Generation {generation}, Fitness Values: {fitness_values}")  # Debugging print

        # Ensure total fitness value is greater than zero
        if sum(fitness_values) == 0:
            print("All fitness values are zero, adding random noise to avoid stagnation.")
            fitness_values = [1 for _ in fitness_values]  # Temporary fix to avoid zero weights

        population = selection(population, fitness_values)
        next_generation = []
        for i in range(0, len(population), 2):
            parent1 = population[i]
            parent2 = population[i + 1] if i + 1 < len(population) else population[0]
            offspring1, offspring2 = crossover(parent1, parent2)
            next_generation.append(mutation(offspring1, mutation_rate))
            next_generation.append(mutation(offspring2, mutation_rate))
        population = next_generation
    
    best_timetable = max(population, key=fitness_function)
    return best_timetable

