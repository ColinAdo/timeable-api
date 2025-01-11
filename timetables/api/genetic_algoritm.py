import random
from datetime import datetime, timedelta

# helper function
def generate_random_time():
    start_hour = random.randint(8, 15)
    start_minute = random.choice([0, 30])
    if start_hour == 11 and start_minute == 30:
        start_minute = 0  # Avoid 11:30 start time
    start_time = datetime.strptime(f"{start_hour}:{start_minute:02d}", "%H:%M").time()
    end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=3)).time()
    return start_time, end_time

# Initialize the Population
def initialize_population(units, population_size):
    population = []
    for _ in range(population_size):
        timetable = []
        for unit in units:
            valid = False
            while not valid:
                day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
                start_time, end_time = generate_random_time()
                if start_time != datetime.strptime("11:30", "%H:%M").time():
                    valid = True
                    timetable.append((unit, day, start_time, end_time))
        population.append(timetable)
    return population

# Define the Fitness Function
def fitness_function(timetable):
    score = 0
    daily_units = {}
    
    for unit, day, start_time, end_time in timetable:
        if day not in daily_units:
            daily_units[day] = []
        daily_units[day].append(unit)
        
        # Penalize if a class starts at 11:30
        if start_time == datetime.strptime("11:30", "%H:%M").time():
            score -= 10
    
    # Check for constraints and calculate the score
    for day, units in daily_units.items():
        year_semester_count = {}
        for unit in units:
            year_semester = unit[2]  # Year and semester format like Y1S1, Y1S2
            if year_semester not in year_semester_count:
                year_semester_count[year_semester] = 0
            year_semester_count[year_semester] += 1
        
        # Penalize if there are more than 2 units for the same academic year and semester in a day
        for year_semester, count in year_semester_count.items():
            if count > 2:
                score -= 10
        if all(count <= 2 for count in year_semester_count.values()):
            score += 1
    
    if score == 0:
        score = 1 

    print(f"Score: {score}") 
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

# Helper function
def generate_random_time():
    # Generate a random start time between 8 AM and 3 PM (latest start time for a 3-hour class)
    start_hour = random.randint(8, 15)
    start_time = datetime.strptime(f"{start_hour}:00", "%H:%M").time()
    end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=3)).time()
    return start_time, end_time

# Mutation
def mutation(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
            start_time, end_time = generate_random_time()
            individual[i] = (individual[i][0], day, start_time, end_time)
    return individual

def generate_timetable(units, population_size, generations, mutation_rate):
    population = initialize_population(units, population_size)
    for generation in range(generations):
        fitness_values = [fitness_function(timetable) for timetable in population]
        print(f"Generation {generation}, Fitness Values: {fitness_values}")  # Debugging print

        if sum(fitness_values) == 0:
            print("All fitness values are zero, adjusting fitness values to avoid stagnation.")
            fitness_values = [1 for _ in fitness_values]  # Adjust fitness values to avoid zero weights

        try:
            population = selection(population, fitness_values)
        except ValueError as e:
            print(f"Selection error: {e}")
            print(f"Fitness values: {fitness_values}")
            # Fallback to a random selection to avoid the error
            population = random.choices(population, k=len(population))

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
