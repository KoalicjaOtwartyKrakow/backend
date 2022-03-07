import random
import csv
import string

from datasets import male_first_names_id, male_middle_names_id, female_first_names_id, female_middle_names_id, \
    female_last_names_id, male_last_names_id
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


email_domains = ["hotmail.com", "gmail.com", "yahoo.com", "protonmail.com", "interia.pl", "poczta.onet.pl", "o2.pl"]


def generate_email_address():
    pieces = [''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 14))) for x in
              range(0, random.randint(1, 3))]
    domain = random.choice(email_domains)
    user = random.choice(['.', '-', '_']).join(pieces)
    return '@'.join([user, domain])


def generate_random_call_time():
    minutes = ['00', '10', '15', '30', '45']
    call_before_h = random.randint(5, 20)
    call_before_m = random.choice(minutes)
    call_after_h = random.randint(call_before_h + 1, 23)
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
    first_name = random.choices(first_name_male,
                                weights=first_name_male_weights) if assigned_sex == 'male' else random.choices(
        first_name_female, weights=first_name_female_weights)
    middle_name = random.choices(middle_name_male,
                                 weights=middle_name_male_weights) if assigned_sex == 'male' else random.choices(
        middle_name_female, weights=middle_name_female_weights)
    return " ".join([first_name[0], middle_name[0]]) if has_middle_name else first_name[0]


def generate_last_name(assigned_sex):
    last_name = random.choices(last_name_male,
                               weights=last_name_male_weights) if assigned_sex == 'male' else random.choices(
        last_name_female, weights=last_name_female_weights)
    return last_name[0]


wojewodztwa = {}
powiaty = {}
gminy_dict = {}
gminy = []
miejscowosci_dict = {}
miejscowosci = []
ulice_dict = {}
ulice = []
ulice_weights = []

def seed_address_generator(datasets):
    teryt = datasets['teryt']
    with open(teryt['terc'], newline='') as cf:
        terc_reader = csv.reader(cf, delimiter=';')
        next(terc_reader, None)
        for row in terc_reader:
            if not row:
                continue
            (woj, pow, gmi, rodz, name, type) = row[:6]
            if type == 'województwo':
                wojewodztwa[woj] = name
            elif type == 'powiat':
                powiaty[pow] = name
            else:
                data = {
                    'woj': woj,
                    'pow': pow,
                    'gmi': gmi,
                    'rodz': rodz,
                    'name': name,
                    'type': type
                }
                gminy.append(data)
                key = f'{woj}{pow}{gmi}{rodz}'
                gminy_dict[key] = data
        report.verbose(f'Read {len(gminy)} counties.')

    with open(teryt['simc'], newline='') as cf:
        simc_reader = csv.reader(cf, delimiter=';')
        next(simc_reader, None)
        for row in simc_reader:
            if not row:
                continue
            (woj, pow, gmi, rodz, rm, mz, name, sym, sympod) = row[:9]
            data = {
                'woj': woj,
                'pow': pow,
                'gmi': gmi,
                'rodz': rodz,
                'rm': rm,
                'name': name,
                'sym': sym,
                'sympod': sympod
            }
            miejscowosci.append(data)
            key = f'{sym}{sympod}'
            miejscowosci_dict[key] = data
        report.verbose(f'Read {len(miejscowosci)} cities.')

    with open(teryt['ulic'], newline='') as cf:
        ulic_reader = csv.reader(cf, delimiter=';')
        next(ulic_reader, None)
        for row in ulic_reader:
            if not row:
                continue
            (woj, pow, gmi, rodz, sym, symul, cecha, nazwa1, nazwa2) = row[:9]
            data = {
                'woj': woj,
                'pow': pow,
                'gmi': gmi,
                'rodz': rodz,
                'sym': sym,
                'symul': symul,
                'cecha': cecha,
                'nazwa1': nazwa1,
                'nazwa2': nazwa2
            }
            ulice.append(data)
            key = f'{sym}{symul}'
            ulice_dict[key] = data
        report.verbose(f'Read {len(ulice)} streets.')

    for ulica in ulice:
        woj = ulica['woj']
        pow = ulica['pow']
        rodz = ulica['rodz']
        weight = 100 if rodz in ['1', '8', '9'] else 1
        weight = 1000 if woj == '12' and pow == '61' else weight
        ulice_weights.append(weight)


def seed_generators(datasets):
    seed_first_name_generator(datasets)
    seed_last_name_generator(datasets)
    seed_address_generator(datasets)


def generate_host():
    assigned_sex = generate_assigned_sex()
    first_name = generate_first_name(assigned_sex)
    last_name = generate_last_name(assigned_sex)
    phone_number = generate_phone_number()
    email_address = generate_email_address()
    call_time = generate_random_call_time()
    return {
        'full_name': ' '.join([first_name, last_name]),
        'phone_number': phone_number,
        'email': email_address,
        'call_after': call_time[0],
        'call_before': call_time[1],
        'comments': ''
    }


languages = ['En', 'Uk', 'Pl', 'Ru']
languages_weights = [8, 2, 10, 2]


def generate_languages():
    l = random.sample(languages, counts=languages_weights, k=random.randint(1, len(languages)))
    return list(set(l))


def generate_teammember():
    assigned_sex = generate_assigned_sex()
    first_name = generate_first_name(assigned_sex)
    last_name = generate_last_name(assigned_sex)
    phone_number = generate_phone_number()
    return {
        'full_name': ' '.join([first_name, last_name]),
        'phone_number': phone_number
    }


def generate_accomodation_unit():
    ulic = random.choices(ulice, weights=ulice_weights, k=1)[0]
    woj = ulic['woj']
    pow = ulic['pow']
    gmi = ulic['gmi']
    rodz = ulic['rodz']
    key = f'{woj}{pow}{gmi}{rodz}'
    simc = gminy_dict[key]

    cecha = ulic['cecha']
    nazwa1 = ulic['nazwa1']
    nazwa2 = ulic['nazwa2']
    nazwa = nazwa1 if not nazwa2 else ' '.join([nazwa2, nazwa1])
    address_line = f'{cecha} {nazwa}' if cecha else nazwa

    building_no = str(random.randint(1, 100))
    has_apartment = random.randint(0, 100) < 50
    has_letter = random.randint(0, 100) < 20
    if has_letter:
        letter = random.choice(string.ascii_uppercase)
        building_no = f'{building_no}{letter}'

    if has_apartment:
        apt = str(random.randint(1, 40))
        glue = random.choice(['m', 'm.', 'M', '/'])
        building_no = glue.join([building_no, apt])

    zip = f'{woj}-{pow}{rodz}'
    city = simc['name']
    voivodeship = wojewodztwa[woj]
    big_apt = random.randint(0, 100) < 20
    vacancies_total = random.randint(10, 40) if big_apt else random.randint(1, 10)
    vacancies_free = random.randint(0, vacancies_total/2) if random.randint(0, 100) < 40 else vacancies_total
    have_pets = random.randint(0, 100) < 30
    accept_pets = random.randint(0, 100) < 20
    return {
        'address_line': f'{address_line} {building_no}',
        'city': city,
        'zip': zip,
        'voivodeship': voivodeship,
        'vacancies_total': vacancies_total,
        'vacancies_free': vacancies_free,
        'have_pets': have_pets,
        'accept_pets': accept_pets,
        'comments': ''
    }


def generate_guest():
    assigned_sex = generate_assigned_sex()
    first_name = generate_first_name(assigned_sex)
    last_name = generate_last_name(assigned_sex)
    phone_number = generate_phone_number()
    people_in_group = random.randint(1, 15)
    does_have_men = random.randint(0, 100) < 30
    adult_men_count = random.randint(1, people_in_group/3) if does_have_men else 0
    adult_woman_count = random.randint(1, people_in_group/3)
    children_count = people_in_group - adult_men_count - adult_woman_count
    children_ages = [random.randint(1, 17) for x in range(1, children_count)]
    have_pets = random.randint(0, 100) < 40
    pets_description = random.choice(['dog', 'cat', 'parrot', 'rat', 'rabbit']) if have_pets else ''
    special_needs = ''
    how_lon_to_stay = f'{random.randint(1, 10)} days' if random.randint(0, 100) < 70 else 'miesiąc'
    return {
        'full_name': ' '.join([first_name, last_name]),
        'phone_number': phone_number,
        'people_in_group': people_in_group,
        'adult_men_'
    }