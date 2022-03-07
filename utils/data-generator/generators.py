
import random
import csv
import string

from datasets import male_first_names_id, male_middle_names_id, female_first_names_id, female_middle_names_id, female_last_names_id, male_last_names_id
from pyrnalist import report

def generate_assigned_sex():
    # https://dane.gov.pl/pl/dataset/718,rocznik-demograficzny-2020
    # in 2021, there is 1.13 f/m ratio
    if random.randint(0, 213) <= 100:
        return 'male'
    else:
        return 'female'


def generate_phone_number():
    glue = random.choice(['', ' ', '.', '-'])
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 888)).zfill(3)
    last = (str(random.randint(1, 999)).zfill(3))
    number = glue.join([first, second, last])
    return f'+48 {number}' if random.randint(0, 100) < 20 else number


email_domains = [ "hotmail.com", "gmail.com", "yahoo.com", "protonmail.com", "interia.pl", "poczta.onet.pl", "o2.pl"]


def generate_email_address():
    pieces = [''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 14))) for x in range(0, random.randint(1, 3))]
    domain = random.choice(email_domains)
    user = random.choice(['.', '-', '_']).join(pieces)
    return '@'.join([user, domain])


def generate_random_call_time():
    minutes = ['00', '10', '15', '30', '45']
    call_before_h = random.randint(5,20)
    call_before_m = random.choice(minutes)
    call_after_h = random.randint(call_before_h+1, 23)
    call_after_m = random.choice(minutes)
    return [':'.join([str(call_before_h), call_before_m]), ':'.join([str(call_after_h), call_after_m])]


first_name_female = []
first_name_female_weights = []
middle_name_female = []
middle_name_female_weights = []
first_name_male = []
first_name_male_weights = []
middle_name_male = []
middle_name_male_weights = []


def seed_first_name_generator(datasets):
    first_names = datasets['first_names']
    with open(first_names[male_first_names_id], newline='') as cf:
        male_first_names = csv.reader(cf)
        next(male_first_names, None)
        for row in male_first_names:
            first_name_male.append(row[0].lower().capitalize())
            first_name_male_weights.append(int(row[2]))
        report.verbose(f'Imported {len(first_name_male_weights)} male first names.')

    with open(first_names[male_middle_names_id], newline='') as cf:
        male_middle_names = csv.reader(cf)
        next(male_middle_names)
        for row in male_middle_names:
            middle_name_male.append(row[0].lower().capitalize())
            middle_name_male_weights.append(int(row[2]))
        report.verbose(f'Imported {len(middle_name_male_weights)} male middle names.')

    with open(first_names[female_first_names_id], newline='') as cf:
        female_first_names = csv.reader(cf)
        next(female_first_names, None)
        for row in female_first_names:
            first_name_female.append(row[0].lower().capitalize())
            first_name_female_weights.append(int(row[2]))
        report.verbose(f'Imported {len(first_name_female_weights)} female first names.')

    with open(first_names[female_middle_names_id], newline='') as cf:
        female_middle_names = csv.reader(cf)
        next(female_middle_names)
        for row in female_middle_names:
            middle_name_female.append(row[0].lower().capitalize())
            middle_name_female_weights.append(int(row[2]))
        report.verbose(f'Imported {len(middle_name_female_weights)} female middle names.')


last_name_female = []
last_name_female_weights = []
last_name_male = []
last_name_male_weights = []


def seed_last_name_generator(datasets):
    last_names = datasets['last_names']
    with open(last_names[male_last_names_id], newline='') as cf:
        male_last_names = csv.reader(cf)
        next(male_last_names, None)
        for row in male_last_names:
            last_name_male.append(row[0].lower().capitalize())
            last_name_male_weights.append(int(row[1]))
        report.verbose(f'Imported {len(last_name_male_weights)} male last names.')
        
    with open(last_names[female_last_names_id], newline='') as cf:
        female_last_names = csv.reader(cf)
        next(female_last_names, None)
        for row in female_last_names:
            last_name_female.append(row[0].lower().capitalize())
            last_name_female_weights.append(int(row[1]))
        report.verbose(f'Imported {len(last_name_female_weights)} female last names.')
   

def generate_first_name(assigned_sex):
    has_middle_name = True if random.randint(0, 100) < 20 else False
    first_name = random.choices(first_name_male, weights=first_name_male_weights) if assigned_sex == 'male' else random.choices(first_name_female, weights=first_name_female_weights)
    middle_name = random.choices(middle_name_male, weights=middle_name_male_weights) if assigned_sex == 'male' else random.choices(middle_name_female, weights=middle_name_female_weights)
    return " ".join([first_name[0], middle_name[0]]) if has_middle_name else first_name[0]


def generate_last_name(assigned_sex):
    last_name = random.choices(last_name_male, weights=last_name_male_weights) if assigned_sex == 'male' else random.choices(last_name_female, weights=last_name_female_weights)
    return last_name[0]


def seed_generators(datasets):
    seed_first_name_generator(datasets)
    seed_last_name_generator(datasets)


def generate_host():
    assigned_sex = generate_assigned_sex()
    first_name = generate_first_name(assigned_sex)
    last_name = generate_last_name(assigned_sex)
    phone_number = generate_phone_number()
    email_address = generate_email_address()
    call_time = generate_random_call_time()
    print(assigned_sex, first_name, last_name, phone_number, email_address, call_time[0], call_time[1])