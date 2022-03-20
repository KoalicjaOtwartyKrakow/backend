import click
import csv
import datetime
import re
import uuid
from pyrnalist import report
from dotenv import load_dotenv

LUDZI_HEADERS = ['ID#', 'GDZIE ZNALEZIONE  (ID z Mieskań  i Imię hosta lub adres)', 'DATA ', 'STATUS',
                 'Przypisane do wolontariusza (imie & nazwisko):', 'Nazwisko', 'Telefon (z kodem kierunkowym)',
                 'Priorytet', 'TOTAL Ilość osób', 'Dorosly', 'Dzieci', 'Wiek Dzieci np 6m; 5 i 8', 'Zwierz',
                 'Uwagi(Czy są kobieta w ciazy, inwalidy (jaka grupa?) Czy sa potrzebny leki, przelewanie krwi dializ etd? Czy są jakies alergie?',
                 'Finanse', 'Na Ile Czasu', 'Uwagi', 'Apartment Status (do NOT edit here)']
RECEPCJA_HEADERS = ['va', 'Notatki', 'Timestamp', "Imię | Ім'я ", 'Nazwisko | Прізвище ',
                    'Numer kontaktowy | Номер телефону', 'Osoba do kontaktu? | Особа до контакту?',
                    'Numer dokumentu | Номер паспорту (ID)',
                    'Ile osób potrzebują zakwaterowania? | Скільки осіб потребують житла? [Mężczyźni | Чоловіки]',
                    'Ile osób potrzebują zakwaterowania? | Скільки осіб потребують житла? [Kobiety | Жінки]',
                    'Ile osób potrzebują zakwaterowania? | Скільки осіб потребують житла? [Dzieci | Діти]',
                    'Wiek dziecka (dzieci) | Вік дитини (дітей)',
                    'Wiek dorosłej osoby (osób) | Вік дорослої особи (осіб)',
                    'Zwierzęta domowe | Домашні тварини [Pies | Собака]',
                    'Zwierzęta domowe | Домашні тварини [Kot | Кіт]',
                    'Zwierzęta domowe | Домашні тварини [Inne (dopisać niżej) | Інше (дописати внизу)]',
                    'Na jaki okres potrzebują zakwaterowania? | На який час потрібне житло?',
                    'Mieszkanie płatne czy za darmo? | Житло платне чи безплатне?',
                    'Jeśli odpłatnie to ile mogą wydać w miesiącu? | Якщо платне то скільки можуть потратити за місяць?',
                    'Czy mają własny transport? | Чи є власний транспорт?', 'Miejscowość | Місцевість',
                    'Od jakiej daty  jest potrzebne zakwaterowanie? | Від якого числа (дати) потрібне житло?',
                    'Notatki i komentarze dotyczące zwierząt domowych, zakwaterowania, stanu zdrowia, edukacji itd (opcjonalnie) | Нотатки і коментарі відносно домашніх тварин, житла, стану здоров"я, освіти та інше', 'Czy osoba zostaje na noc w naszym punkcie pomocy przy ul. Radziwiłłowska 3? | Чи особа залишається в нашому пункті допомоги на Radziwiłłowska 3?', 'Numer telefonu (wolontariusza akceptującego zgłoszenie) | Номер телефону (волонтера, що приймає заявку)', 'Oświadczenie znajomości reguł przebywania | Підтвердження знайомості правил перебування', 'Czy osoba potrzebuje mieszkania? | Чи особа шукає житло?', '', '', '']
MIESZKANIA_HEADERS = ['25151', 'NASZE UWAGI', 'KIM jest juz zajety? (ID czlowieka) / Data kiedy aktualizowane', '', 'Timestamp', 'W jaki sposób chcesz pomóc?', 'Miasto lokalu', 'Adres lokalu', 'Imię i nazwisko:', 'Adres email:', 'Numer telefonu', 'Numer telefonu / adres email', 'Maksymalna ilość ludzi, które możesz przyjąć w swoim lokalu mieszkalnym?', 'Uwagi: Czy posiadasz zwierzęta? Czy akceptujesz gości ze zwierzętami? Godziny w których możemy do Ciebie dzwonić? Masz inne uwagi?', 'Numer telefonu/ adres email', 'Jakie znasz języki?', 'Czy masz doświadczenie w tłumaczeniach?', 'Jeśli tak, czy możesz krótko opisać Twoje doświadczenie?', 'Czy masz doświadczenie w pomocy edukacyjnej?', 'Jeśli tak, czy możesz krótko opisać Twoje doświadczenie?', 'Jeśli masz jakieś pytania, uwagi lub dodatkowe komentarze, na które nie znalazł_ś miejsca w formularzu, napisz je proszę poniżej:', 'Wyrażam zgodę na przetwarzanie moich danych osobowych przez Stowarzyszenie Laboratorium Działań dla Pokoju w celu organizacji pomocy osobom uchodźczym z Ukrainy.']
CHILDREN_AGES_LAT_REGEXP = r"\s?lat"


def try_split(string, separators):
    for s in separators:
        try_arr = string.strip().split(s)
        if isinstance(try_arr, list) and len(try_arr) > 1:
            return list(filter(lambda x: x != '', try_arr))
    return string


def map_how_long(s, vn):
    match s.strip():
        case "1 d.":
            return "1d"
        case "1 dzień | 1 день":
            return "1d"
        case "1-2 d.":
            return "3d"
        case "2-3 dni | 2-3 дні":
            return "3d"
        case "3-7 d.":
            return "1w"
        case "4-7 dni | 4-7 дні":
            return "1w"
        case "1 t.":
            return "1w"
        case "2 t.":
            return "2w"
        case "1-2 tygodnie | 1-2 тижні":
            return "2w"
        case "3 t.":
            return "3w"
        case "3-4 tygodnie | 3-4 тижні":
            return "3w"
        case "1 m.":
            return "1m"
        case "1 miesiąc | 1 місяць":
            return "1m"
        case "1-2 m.":
            return "2m"
        case "1-2 miesięcy | 1-2 місяців":
            return "2m"
        case "3 m.":
            return "3m"
        case ">3 m.":
            return "1y"
        case "3-12m":
            return "1y"
        case "długoterminowo":
            return "1y"
        case "3-12 miesięcy | 3-12 місяців":
            return "1y"
        case "nie ma danych":
            return None
        case _:
            vn.append(f'Could not understand time period: {s}')
            return None

def get_how_long_can_stay(string, vn):
    if string == '':
        return None
    return ", ".join(filter(lambda x: x, [map_how_long(x, vn) for x in string.split(",")]))


def map_location(s, vn):
    match s.strip():
        case "Kraków | Краків":
            return "kraków"
        case "Kraków i okolice | Краків і передмістя":
            return "kraków area"
        case "Inne miasto | Інше місто":
            return "other"
        case _:
            vn.append(f'Could not understand preferred location: {s}')
            return None


def get_preferred_location(string, vn):
    if string == '':
        return None
    return ", ".join(filter(lambda x: x, [map_location(x, vn) for x in string.split(",")]))

def import_ludzi():
    ludzi = []
    with open("[salam] Ludzi (Ukrainska) - Ludzi.tsv", encoding='utf-8', newline='') as cf:
        cr = csv.reader(cf, delimiter="\t")
        headers = next(cr, [0])
        headers_match = all(i for i in [i == j for i, j in zip(headers, LUDZI_HEADERS)])
        if not headers_match:
            report.error("Headers do not match with Ludzi tab format")
            print(LUDZI_HEADERS)
            print(headers)
            return

        for row in cr:
            validation_notes = []
            old_guest_id = row[0]
            old_accommodation_id = row[1]
            created_at = datetime.datetime.now().isoformat()
            try:
                created_at = datetime.datetime.strptime(row[2], "%d/%m/%Y").isoformat()
            except:
                validation_notes.append(f'Could not understand created_at date: {row[2]}')
            status = row[3]
            volunteer_assigned = row[4]
            full_name = row[5]
            email = ""
            phone_number = row[6]
            priority_date_cell = re.sub(r'\s+', '', row[7])
            priority_date = None
            try:
                if priority_date_cell != '':
                    priority_date = datetime.datetime.strptime(priority_date_cell, "%d/%m/%Y").isoformat()
            except:
                validation_notes.append(f'Could not understand priority date: {priority_date_cell}')
            people_in_group_cell = re.sub(r'\s+', '', row[8])
            people_in_group = 0
            if people_in_group_cell == '':
                validation_notes.append("People in group cell I was empty.")
                adults_cell = re.sub(r'\s+', '', row[9])
                if adults_cell == '':
                    validation_notes.append('Both cells I and J were empty.')
                else:
                    try:
                        people_in_group = int(adults_cell)
                    except:
                        validation_notes.append(f'Could not understand adults count cell: {adults_cell}')
            else:
                try:
                    people_in_group = int(people_in_group_cell)
                except:
                    validation_notes.append(f'Could not understand people in group cell: {adults_cell}')

            # we only have total number of adults, no distinction
            # let's flag it to the volunteer
            validation_notes.append('No information on Male/Female')
            adult_male_count = 0
            adult_female_count = 0

            children_count = 0
            try:
                children_count = int(row[10]) if re.sub(r'\s+', '', row[10]) != '' else 0
            except:
                validation_notes.append(f'Could not understand children count: {row[10]}')
            children_ages_str = row[11]
            children_ages_str = re.sub(CHILDREN_AGES_LAT_REGEXP, "", children_ages_str, 0, re.MULTILINE)
            children_ages = []
            if children_ages_str != '' and children_ages_str != '-':
                children_ages = try_split(children_ages_str, [',', ';', 'i', ' '])
                if not isinstance(children_ages, list):
                    validation_notes.append(f'Could not parse children ages: {children_ages}')
                    children_ages = []

            pets_description = row[12]
            have_pets = pets_description != ""
            special_needs = row[13]
            finance_status = row[14]
            how_long_to_stay = get_how_long_can_stay(row[15], validation_notes)
            volunteer_note = row[16]

            data = {
                'full_name': full_name,
                'email': email,
                'phone_number': phone_number,
                'is_agent': False,
                'document_number': None,
                'people_in_group': people_in_group,
                'adult_male_count': adult_male_count,
                'adult_female_count': adult_female_count,
                'children_count': children_count,
                'children_ages': children_ages,
                'have_pets': have_pets,
                'pets_description': pets_description,
                'special_needs': special_needs,
                'priority_date': priority_date,
                'finance_status': finance_status,
                'how_long_to_stay': how_long_to_stay,
                'preferred_location': None,
                'volunteer_note': volunteer_note,
                'created_at': created_at,
                'validation_notes': validation_notes,
                'priority_status': status,
                '__old_guest_id': old_guest_id,
                '__old_accommodation_id': old_accommodation_id,
                '__volunteer_assigned': volunteer_assigned,
            }
            if full_name != ' ' and full_name != '':
                ludzi.append(data)
    return ludzi


def import_recepcja():
    recepcja = []
    with open("[salam] Ludzi (Ukrainska) - UPD Data from Reception.tsv", encoding='utf-8', newline='') as cf:
        cr = csv.reader(cf, delimiter="\t")
        headers = next(cr, [0])
        headers_match = all(i for i in [i == j for i, j in zip(headers, RECEPCJA_HEADERS)])
        if not headers_match:
            report.error("Headers do not match with UPD Data tab format")
            print(RECEPCJA_HEADERS)
            print('---')
            print(headers)
            return

        for row in cr:
            validation_notes = []

            created_at = datetime.datetime.now().isoformat()
            try:
                created_at = datetime.datetime.strptime(row[2], "%d/%m/%Y %H:%M:%S").isoformat()
            except:
                validation_notes.append(f'Could not understand created_at: {row[2]}')

            full_name = ' '.join([row[3], row[4]])
            email = ''
            phone_number = row[5]
            is_agent = True if row[6].startswith("Tak") else False
            document_number = row[7] if re.sub(r'\s+', '', row[7]) != '' else None

            adult_male_count = 0
            adult_male_count_cell = re.sub(r'\s+', '', row[8])
            if adult_male_count_cell != '':
                try:
                    adult_male_count = int(adult_male_count_cell)
                except:
                    validation_notes.append(f'Could not understand total male count: {adult_male_count_cell}')

            adult_female_count = 0
            adult_female_count_cell = re.sub(r'\s+', '', row[9])
            if adult_female_count_cell != '':
                try:
                    adult_female_count = int(adult_female_count_cell)
                except:
                    validation_notes.append(f'Could not understand total female count: {adult_female_count_cell}')

            children_count = 0
            children_count_cell = re.sub(r'\s+', '', row[10])
            if children_count_cell != '':
                try:
                    children_count = int(children_count_cell)
                except:
                    validation_notes.append(f'Could not understand total children count: {children_count_cell}')

            people_in_group = adult_male_count + adult_female_count + children_count

            children_ages_str = row[11]
            children_ages_str = re.sub(CHILDREN_AGES_LAT_REGEXP, "", children_ages_str, 0, re.MULTILINE)
            children_ages = []
            if children_ages_str != '' and children_ages_str != '-':
                children_ages = try_split(children_ages_str, [',', ';', 'i', ' '])
                if not isinstance(children_ages, list):
                    validation_notes.append(f'Could not parse children ages: {children_ages}')
                    children_ages = []

            # row 12 - age of adults, ignore

            have_dogs = row[13] != ''
            have_cats = row[14] != ''
            have_pets = have_dogs or have_cats
            pets_description = "\n".join(filter(lambda x: x, ["dog" if have_dogs else None, "cat" if have_cats else None]))

            # row 15 is hidden

            how_long_to_stay = get_how_long_can_stay(row[16], validation_notes)
            finance_status = "\n".join([row[17], row[18]])

            # row 19 - transport. na razie nie.
            preferred_location = get_preferred_location(row[20], validation_notes)

            priority_date_cell = re.sub(r'\s+', '', row[21])
            priority_date = None
            try:
                if priority_date_cell != '':
                    priority_date = datetime.datetime.strptime(priority_date_cell, "%d/%m/%Y").isoformat()
            except:
                validation_notes.append(f'Could not understand priority date: {priority_date_cell}')

            special_needs = row[22]

            data = {
                'full_name': full_name,
                'email': email,
                'phone_number': phone_number,
                'is_agent': is_agent,
                'document_number': document_number,
                'people_in_group': people_in_group,
                'adult_male_count': adult_male_count,
                'adult_female_count': adult_female_count,
                'children_count': children_count,
                'children_ages': children_ages,
                'have_pets': have_pets,
                'pets_description': pets_description,
                'finance_status': finance_status,
                'how_long_to_stay': how_long_to_stay,
                'preferred_location': preferred_location,
                'priority_date': priority_date,
                'special_needs': special_needs,
                'created_at': created_at,
                'validation_notes': validation_notes,
                'volunteer_note': volunteer_note,
                'priority_status': None,
                '__old_guest_id': None,
                '__old_accommodation_id': None,
                '__volunteer_assigned': None,
            }
            if full_name != ' ' and full_name != '':
                recepcja.append(data)
    return recepcja


def merge_ludzi_recepcja(ludzi, recepcja):
    merged = [x for x in ludzi]
    phone_numbers_dict = {}
    full_name_dict = {}
    for x in recepcja:
        phone_numbers_dict[x['phone_number']] = x
        full_name_dict[x['full_name']] = x

    duplicate_ludzi = {}
    for i, x in enumerate(merged):
        key = x['full_name']
        r = full_name_dict.get(key, None)
        if r:
            x['document_number'] = r['document_number']
            x['is_agent'] = r['is_agent']
            x['adult_male_count'] = r['adult_male_count']
            x['adult_female_count'] = r['adult_female_count']
            finance_status = "\n".join([x['finance_status'], r['finance_status']])
            x['finance_status'] = finance_status
            r['finance_status'] = finance_status
            x['preferred_location'] = r['preferred_location']
            x['priority_status'] = r['priority_status']
            for vn in r['validation_notes']:
                x['validation_notes'].append(vn)
            r['validation_notes'] = x['validation_notes']
            x['created_at'] = r['created_at']
            notes = "\n".join([x['volunteer_note'], r['volunteer_note']])
            x['volunteer_note'] = notes
            r['volunteer_note'] = notes
            special_needs = "\n".join([x['special_needs'], r['special_needs']])
            x['special_needs'] = special_needs
            r['special_needs'] = special_needs
            merge_issues = {i: (x[i], r[i]) for i, j in x.items() if x[i] != r[i]}
            merge_issues_arr = []
            for k in merge_issues.keys():
                if not k.startswith("__"):
                    v = merge_issues[k]
                    row = f'{k} - {v[0]} vs. {v[1]}'
                    merge_issues_arr.append(row)
            merge_issues_str = "\n".join(merge_issues_arr)
            x['validation_notes'].append(f'Could not merge following data:\n{merge_issues_str}')
            merged[i] = x
            full_name_dict.pop(key, None)
    [merged.append(x) for x in full_name_dict.values()]
    return merged


def import_mieszkania():
    hosts = []
    units = []
    languages = []
    with open("[salam] Mieszkania (Polska) - Automated Mieszkania.tsv", encoding='utf-8', newline='') as cf:
        cr = csv.reader(cf, delimiter="\t")
        headers = next(cr, [0])
        headers_match = all(i for i in [i == j for i, j in zip(headers, MIESZKANIA_HEADERS)])
        if not headers_match:
            report.error("Headers do not match with Mieszkania tab format")
            print(MIESZKANIA_HEADERS)
            print(headers)
            return

        for row in cr:
            host_validation_notes = []
            unit_validation_notes = []

            host_guid = str(uuid.uuid4())
            host_fullname = row[8]
            host_email = row[9]
            host_phone_number = row[10]
            host_comments = row[13]

            created_at = datetime.datetime.now().isoformat()
            try:
                created_at = datetime.datetime.strptime(row[2], "%d/%m/%Y %H:%M:%S").isoformat()
            except:
                host_validation_notes.append(f'Could not understand created_at: {row[2]}')
                unit_validation_notes.append(f'Could not understand created_at: {row[2]}')

            host_langs = row[15].lower()
            languages.append({'host_id': host_guid, 'language_code': 'pl'}) if "polski" in host_langs else None
            languages.append({'host_id': host_guid, 'language_code': 'en'}) if "angielski" in host_langs else None
            languages.append({'host_id': host_guid, 'language_code': 'ru'}) if "rosyjski" in host_langs else None
            languages.append({'host_id': host_guid, 'language_code': 'uk'}) if "ukraiński" in host_langs else None

            host_data = {
                'guid': host_guid,
                'full_name': host_fullname,
                'email': host_email,
                'phone_number': host_phone_number,
                'comments': host_comments,
                'created_at': created_at,
                'system_comments': "\n".join(host_validation_notes)
            }
            hosts.append(host_data)

            staff_comments = "\n".join([row[0], row[1]])
            guest_id = row[2]
            city = row[6]
            address_line = row[7]
            additional_comments = row[16]
            vacancies_total = 0
            vtstr = row[12]
            if vtstr == "1-2":
                vacancies_total = 2
            elif vtstr == "3-5":
                vacancies_total = 5
            elif vtstr == "6-10":
                vacancies_total = 10
            elif vtstr == "Więcej niż 10":
                vacancies_total = 12
                unit_validation_notes.append("Vacancies_total upper bound not specified")
            else:
                unit_validation_notes.append('Vacancies total not understood')

            unit_data = {
                'city': city,
                'zip': 'N/A',
                'address_line': address_line,
                'vacancies_total': vacancies_total,
                'owner_comments': additional_comments,
                'staff_comments': staff_comments,
                'system_comments': "\n".join(unit_validation_notes),
                'host_id': host_guid,
                '___guest_id': guest_id
            }
            units.append(unit_data)
            if len(units) > 10:
                break
    return (hosts, units, languages)


def to_pgsql_value(v):
    if isinstance(v, list):
        return "'{" + ", ".join([to_pgsql_value(x) for x in v]) + "}'"
    elif isinstance(v, str):
        return f"'{v}'"
    elif isinstance(v, bool):
        return 'true' if v else 'false'
    else:
        return str(v)


def to_sql(table, values):
    if len(values)>0:
        with open(f'{table}.sql', 'w', encoding='utf-8') as file:
            keys = [x for x in values[0].keys() if not x.startswith("__")]
            keys_quoted = [f'"{x}"' for x in keys]
            keys_str = ", ".join(keys_quoted)
            sql = f'INSERT INTO {table}({keys_str}) VALUES'
            value_inserts = []
            for v in values:
                values_str = ", ".join([to_pgsql_value(v[k]) for k in keys])
                value_inserts.append(f'({values_str})')
            sql += ", ".join(value_inserts)
            file.write(sql)


@click.command()
def import_data():
    ludzi = import_ludzi()
    recepcja = import_recepcja()

    report.info(f'Imported {len(ludzi)} from Ludzi')
    report.info(f'Imported {len(recepcja)} from UPD Data from Reception')

    merged = merge_ludzi_recepcja(ludzi, recepcja)
    report.info(f'Total guests after merge: {len(merged)}')

    (hosts, units, languages) = import_mieszkania()
    report.info(f'Imported {len(hosts)} hosts from Mieszkania (live)')
    report.info(f'Imported {len(units)} units from Mieszkania (live)')
    report.info(f'Imported {len(languages)} languages from Mieszkania (live)')

    to_sql('public.hosts', hosts)
    to_sql('public.host_languages', languages)
    to_sql('public.accommodation_units', units)
    to_sql('public.guests', merged)


# TODO: try to match guest to accommodation by __old_id, __guest_id
# TODO: try to extract zip out of address_line. what to do if failed?
if __name__ == '__main__':
    load_dotenv()
    import_data()
    report.footer()
