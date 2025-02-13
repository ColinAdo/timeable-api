import os
import json
import random

from groq import Groq # type: ignore

from django.conf import settings
from datetime import datetime, timedelta

# Double check timetable using groq api 
def double_check_timetable(timetable, prompt):
    try:
        client = Groq(
            api_key=os.environ.get(settings.GROQ_API_KEY),
        )
        
        constrains = f"{prompt}. Return the timetable data in a plain JSON format, like the following: [ {{ unit_name: 'value', unit_code: 'value'... }} ]. Only return the JSON data, without any additional text or quotes."
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{timetable} {constrains}",
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        
        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)
    
    except Exception as e:
        print(f"Error in double_check_timetable: {e}")
        raise

# Helper function
def generate_random_time(start_time, end_time, duration, first_constrain, second_constrain):
    start_datetime = datetime.strptime(start_time, "%H:%M")
    end_datetime = datetime.strptime(end_time, "%H:%M")
    latest_start_time = end_datetime - timedelta(hours=duration)

    # Only parse constraints if they are provided
    constrain_start = datetime.strptime(first_constrain, "%H:%M").time() if first_constrain else None
    constrain_end = datetime.strptime(second_constrain, "%H:%M").time() if second_constrain else None

    valid_times = []

    current_time = start_datetime
    while current_time <= latest_start_time:
        # Ensure class start time does NOT fall inside the constraint range
        if not (constrain_start and constrain_end and constrain_start <= current_time.time() < constrain_end):
            valid_times.append(current_time)
        current_time += timedelta(minutes=30)  # Ensure step is in 30-minute intervals

    if not valid_times:
        raise ValueError(f"No valid start times available outside {first_constrain} - {second_constrain}!")

    # Pick a valid start time at random
    random_start = random.choice(valid_times)
    random_end = random_start + timedelta(hours=duration)

    return random_start.strftime("%H:%M:%S"), random_end.strftime("%H:%M:%S")

# Initialize the Population
def initialize_population(units, population_size, start_time, end_time, duration, first_constrain, second_constrain):
    population = []
    for _ in range(population_size):
        timetable = []
        for unit in units:
            valid = False
            while not valid:
                day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
                start, end = generate_random_time(start_time, end_time, duration, first_constrain, second_constrain)
                if first_constrain and start != datetime.strptime(first_constrain, "%H:%M").time():
                    valid = True
                    timetable.append((unit, day, start, end))
                elif not first_constrain or second_constrain:  # If no constraint, always valid
                    valid = True
                    timetable.append((unit, day, start, end))
        population.append(timetable)
    return population

# Define the Fitness Function
def fitness_function(timetable, start_time, duration, first_constrain, second_constrain):
    score = 0
    daily_units = {}

    # Convert constraints only if provided
    constrain_start = datetime.strptime(first_constrain, "%H:%M").time() if first_constrain else None
    constrain_end = datetime.strptime(second_constrain, "%H:%M").time() if second_constrain else None

    # Generate dynamic restricted start times
    constrain_times = []
    if constrain_start and constrain_end:
        class_start_time = datetime.strptime(start_time, "%H:%M")  # Earliest possible class start
        while class_start_time.time() < constrain_end:  # Until second_constrain
            class_end_time = (class_start_time + timedelta(hours=duration)).time()  # Assume class duration is 3 hours
            if class_end_time > constrain_start:  # If the class overlaps the restricted range
                constrain_times.append(class_start_time.strftime("%H:%M:%S"))
            class_start_time += timedelta(minutes=30)  # Move in 30-minute intervals

    for unit, day, class_start_time, class_end_time in timetable:
        if day not in daily_units:
            daily_units[day] = []
        daily_units[day].append(unit)

        # Check if class starts at a restricted time
        if constrain_times and class_start_time in constrain_times:
            score -= 10  # Apply penalty

    # Check for constraints and calculate the score
    for day, units in daily_units.items():
        year_semester_count = {}
        for unit in units:
            year_semester = unit[2]  # Year and semester format like Y1S1, Y1S2
            if year_semester not in year_semester_count:
                year_semester_count[year_semester] = 0
            year_semester_count[year_semester] += 1
        
        # Penalize if more than 2 units for the same academic year and semester in a day
        for year_semester, count in year_semester_count.items():
            if count > 2:
                score -= 10
        if all(count <= 2 for count in year_semester_count.values()):
            score += 1
    
    if score == 0:
        score = 1 

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

# mutation function
def mutation(individual, mutation_rate, start_time, end_time, duration, first_constrain, second_constrain):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
            start, end = generate_random_time(start_time, end_time, duration, first_constrain, second_constrain)
            individual[i] = (individual[i][0], day, start, end)
    return individual

# Generate timetable function
def generate_timetable(units, population_size, generations, mutation_rate, start_time, end_time, duration, first_constrain, second_constrain):
    population = initialize_population(units, population_size, start_time, end_time, duration, first_constrain, second_constrain)
    
    for generation in range(generations):
        fitness_values = [fitness_function(timetable, start_time, duration, first_constrain, second_constrain) for timetable in population]
        
        if sum(fitness_values) == 0:
            fitness_values = [1 for _ in fitness_values]

        try:
            population = selection(population, fitness_values)
        except ValueError:
            population = random.choices(population, k=len(population))

        next_generation = []
        for i in range(0, len(population), 2):
            parent1 = population[i]
            parent2 = population[i + 1] if i + 1 < len(population) else population[0]
            offspring1, offspring2 = crossover(parent1, parent2)
            next_generation.append(mutation(offspring1, mutation_rate, start_time, end_time, duration, first_constrain, second_constrain))
            next_generation.append(mutation(offspring2, mutation_rate, start_time, end_time, duration, first_constrain, second_constrain))
        
        population = next_generation

    best_timetable = max(population, key=lambda timetable: fitness_function(timetable, start_time, duration, first_constrain, second_constrain))
    return best_timetable