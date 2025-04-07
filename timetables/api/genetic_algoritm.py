import os
import json
import random

from groq import Groq  # type: ignore

from django.conf import settings
from datetime import datetime, timedelta

# Groq ai function
def double_check_timetable(timetable, prompt):
    try:
        client = Groq(
            api_key=os.environ.get(settings.GROQ_API_KEY),
        )
        
        constraints = f"'{prompt}.' Return the timetable data in a plain JSON format, like the following: [ {{ unit_name: 'value', unit_code: 'value'... }} ]. Only return the JSON data, without any additional text or quotes."
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{timetable} {constraints}",
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        
        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)
    
    except Exception as e:
        print(f"Error in double_check_timetable: {e}")
        raise

# Generate random time helper function
def generate_random_time(start_time, end_time, duration, first_constrain=None, second_constrain=None):
    start_datetime = datetime.strptime(start_time, "%H:%M" if len(start_time) == 5 else "%H:%M:%S")

    # Only parse constraints if they are provided
    end_datetime = datetime.strptime(end_time, "%H:%M" if len(end_time) == 5 else "%H:%M:%S")
    latest_start_time = end_datetime - timedelta(hours=duration)

    constrain_start = datetime.strptime(first_constrain, "%H:%M" if first_constrain and len(first_constrain) == 5 else "%H:%M:%S").time() if first_constrain else None
    constrain_end = datetime.strptime(second_constrain, "%H:%M" if second_constrain and len(second_constrain) == 5 else "%H:%M:%S").time() if second_constrain else None

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

# Initialize population
def initialize_population(units, population_size, start_time, end_time, duration, first_constrain=None, second_constrain=None):
    population = []
    for _ in range(population_size):
        timetable = []
        day_count = {day: {} for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}
        for unit in units:
            valid = False
            attempts = 0
            while not valid and attempts < 100:  # Prevent infinite loop
                day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
                start, end = generate_random_time(start_time, end_time, duration, first_constrain, second_constrain)
                year_semester = unit[2]

                if day not in day_count or year_semester not in day_count[day]:
                    day_count[day][year_semester] = 0

                if day_count[day][year_semester] < 2:
                    valid = True
                    timetable.append((unit, day, start, end))
                    day_count[day][year_semester] += 1

                attempts += 1

            if not valid:  # Force addition if attempts threshold is reached
                day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
                start, end = generate_random_time(start_time, end_time, duration, first_constrain, second_constrain)
                timetable.append((unit, day, start, end))

        population.append(timetable)
    return population


def fitness_function(timetable):
    score = 1

    daily_units = {}

    for unit, day in timetable:
        if day not in daily_units:
            daily_units[day] = []
        daily_units[day].append(unit)

    for day, units in daily_units.items():
        year_semester_count = {}

        for unit in units:
            year_semester = unit[2]
            if year_semester not in year_semester_count:
                year_semester_count[year_semester] = 0
            year_semester_count[year_semester] += 1
        
        # Penalize if more than 2 units for the same academic year and semester in a day
        for year_semester, count in year_semester_count.items():
            if count > 2:
                score -= 10 * (count - 2)  # Heavy penalty for each extra unit beyond 2
            elif count == 2:
                score += 5  # Reward valid timetables

    return max(score, 1)


# Selection function
def selection(population, fitness_values):
    if sum(fitness_values) == 0:  
        fitness_values = [1] * len(fitness_values)

    return random.choices(population, weights=fitness_values, k=len(population))


# Crossover
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    return offspring1, offspring2

# mutation function
def mutation(individual, mutation_rate, start_time, end_time, duration, first_constrain=None, second_constrain=None):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            day_count = {day: {} for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}
            for unit, day, start_time, end_time in individual:
                year_semester = unit[2]
                if day not in day_count or year_semester not in day_count[day]:
                    day_count[day][year_semester] = 0
                day_count[day][year_semester] += 1

            retries = 10
            valid = False
            while not valid and retries > 0:
                day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
                start, end = generate_random_time(start_time, end_time, duration, first_constrain, second_constrain)
                year_semester = individual[i][0][2]

                if day not in day_count or year_semester not in day_count[day]:
                    day_count[day][year_semester] = 0

                if day_count[day][year_semester] < 2:
                    individual[i] = (individual[i][0], day, start, end)
                    valid = True
                    day_count[day][year_semester] += 1

                retries -= 1
    return individual

# Main function to generate timetable
def generate_timetable(units, population_size, generations, mutation_rate, start_time, end_time, duration, first_constrain=None, second_constrain=None):
    population = initialize_population(units, population_size, start_time, end_time, duration, first_constrain, second_constrain)
    
    for generation in range(generations):
        fitness_values = [fitness_function(timetable) for timetable in population]
        
        if sum(fitness_values) == 0:
            fitness_values = [1 for _ in fitness_values]

        selected = selection(population, fitness_values)
        
        next_generation = []
        for i in range(0, len(selected), 2):
            parent1 = selected[i]
            parent2 = selected[i + 1] if i + 1 < len(selected) else selected[0]
            offspring1, offspring2 = crossover(parent1, parent2)
            next_generation.append(mutation(offspring1, mutation_rate, start_time, end_time, duration, first_constrain, second_constrain))
            next_generation.append(mutation(offspring2, mutation_rate, start_time, end_time, duration, first_constrain, second_constrain))
        
        population = next_generation

    best_timetable = max(population, key=lambda timetable: fitness_function(timetable))
    return best_timetable
