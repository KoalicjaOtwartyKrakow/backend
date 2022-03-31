import csv
import datetime
import re
import uuid

from pyrnalist import report


LUDZI_HEADERS = (
    "",
    "Miejsce zamieszkania gdzie wysłaliśmy ludzi",
    "DATA ",
    "STATUS",
    "imie i nazwisko wolontariusza",
    "Imie i Nazwisko",
    "Telefon (z kodem kierunkowym)",
    "Priorytet",
    "TOTAL Ilość osób",
    "Dorosly",
    "Dzieci",
    "Wiek Dzieci np 6m; 5 i 8",
    "Zwierzę",
    "Uwagi(Czy są kobieta w ciazy, inwalidy (jaka grupa?) Czy sa potrzebny leki, przelewanie krwi dializ etd? Czy są jakies alergie?",
    "Finanse",
    "Na Ile Czasu",
    "Uwagi",
    "Apartment Status (do NOT edit here)",
)

RECEPCJA_HEADERS = (
    "",
    "Notatki",
    "Timestamp",
    "Imię | Ім'я ",
    "Nazwisko | Прізвище ",
    "Numer kontaktowy | Номер телефону",
    "Osoba do kontaktu? | Особа до контакту?",
    "Numer dokumentu | Номер паспорту (ID)",
    "Ile osób potrzebują zakwaterowania? | Скільки осіб потребують житла? [Mężczyźni | Чоловіки]",
    "Ile osób potrzebują zakwaterowania? | Скільки осіб потребують житла? [Kobiety | Жінки]",
    "Ile osób potrzebują zakwaterowania? | Скільки осіб потребують житла? [Dzieci | Діти]",
    "Wiek dziecka (dzieci) | Вік дитини (дітей)",
    "Wiek dorosłej osoby (osób) | Вік дорослої особи (осіб)",
    "Zwierzęta domowe | Домашні тварини [Pies | Собака]",
    "Zwierzęta domowe | Домашні тварини [Kot | Кіт]",
    "Zwierzęta domowe | Домашні тварини [Inne (dopisać niżej) | Інше (дописати внизу)]",
    "Na jaki okres potrzebują zakwaterowania? | На який час потрібне житло?",
    "Mieszkanie płatne czy za darmo? | Житло платне чи безплатне?",
    "Jeśli z dopłatą to ile mogą wydać w miesiącu? | Якщо з доплатою то скільки можуть потратити за місяць?",
    "Czy mają własny transport? | Чи є власний транспорт?",
    "Miejscowość | Місцевість",
    "Od jakiej daty  jest potrzebne zakwaterowanie? | Від якого числа (дати) потрібне житло?",
    'Notatki i komentarze dotyczące zwierząt domowych, zakwaterowania, stanu zdrowia, edukacji itd (opcjonalnie) | Нотатки і коментарі відносно домашніх тварин, житла, стану здоров"я, освіти та інше',
    "Czy osoba zostaje na noc w naszym punkcie pomocy przy ul. Radziwiłłowska 3? | Чи особа залишається в нашому пункті допомоги на Radziwiłłowska 3?",
    "Numer telefonu (wolontariusza akceptującego zgłoszenie) | Номер телефону (волонтера, що приймає заявку)",
    "Oświadczenie znajomości reguł przebywania | Підтвердження знайомості правил перебування",
    "Czy osoba potrzebuje mieszkania? | Чи особа шукає житло?",
    "",
    "Czy grupa chciałaby pojechać za granicę? | Чи хотіла би група поїхати за кордон?",
    "",
)
MIESZKANIA_HEADERS = (
    "",
    "NASZE UWAGI",
    "Na jak długo?",
    "KIM jest juz zajety? (ID czlowieka) ",
    "WOLONTARIUSZ (kto się kontaktował)",
    "STATUS",
    "Timestamp",
    "W jaki sposób chcesz pomóc?",
    "Miasto lokalu",
    "Adres lokalu",
    "Imię i nazwisko:",
    "Adres email:",
    "Numer telefonu",
    "Numer telefonu / adres email",
    "Maksymalna ilość ludzi, które możesz przyjąć w swoim lokalu mieszkalnym?",
    "Uwagi: Czy posiadasz zwierzęta? Czy akceptujesz gości ze zwierzętami? Godziny w których możemy do Ciebie dzwonić? Masz inne uwagi?",
    "Numer telefonu/ adres email",
    "Jakie znasz języki?",
    "Czy masz doświadczenie w tłumaczeniach?",
    "Jeśli tak, czy możesz krótko opisać Twoje doświadczenie?",
    "Czy masz doświadczenie w pomocy edukacyjnej?",
    "Jeśli tak, czy możesz krótko opisać Twoje doświadczenie?",
    "Jeśli masz jakieś pytania, uwagi lub dodatkowe komentarze, na które nie znalazł_ś miejsca w formularzu, napisz je proszę poniżej:",
    "Wyrażam zgodę na przetwarzanie moich danych osobowych przez Stowarzyszenie Laboratorium Działań dla Pokoju w celu organizacji pomocy osobom uchodźczym z Ukrainy.",
    "",
    "",
    "Last modified: Sun Mar 27 2022 13:17:41 GMT+0200 (czas środkowoeuropejski letni)",
)
CHILDREN_AGES_LAT_REGEXP = r"\s?lat"


def try_int(value):
    try:
        return int(float(value))
    except:
        return 0


def try_split(string, separators):
    for s in separators:
        try_arr = string.strip().split(s)
        if isinstance(try_arr, list) and len(try_arr) > 1:
            return [try_int(x) for x in list(filter(lambda x: x != "", try_arr))]
    return string


def map_how_long(s, vn):
    s_ = s.strip()

    if s_ == "1 d.":
        return "1d"
    elif s_ == "1 dzień | 1 день":
        return "1d"
    elif s_ == "1-2 d.":
        return "3d"
    elif s_ == "2-3 dni | 2-3 дні":
        return "3d"
    elif s_ == "3-7 d.":
        return "1w"
    elif s_ == "4-7 dni | 4-7 дні":
        return "1w"
    elif s_ == "1 t.":
        return "1w"
    elif s_ == "2 t.":
        return "2w"
    elif s_ == "1-2 tygodnie | 1-2 тижні":
        return "2w"
    elif s_ == "3 t.":
        return "3w"
    elif s_ == "3-4 tygodnie | 3-4 тижні":
        return "3w"
    elif s_ == "1 m.":
        return "1m"
    elif s_ == "1 miesiąc | 1 місяць":
        return "1m"
    elif s_ == "1-2 m.":
        return "2m"
    elif s_ == "1-2 miesięcy | 1-2 місяців":
        return "2m"
    elif s_ == "3 m.":
        return "3m"
    elif s_ == ">3 m.":
        return "1y"
    elif s_ == "3-12m":
        return "1y"
    elif s_ == "długoterminowo":
        return "1y"
    elif s_ == "3-12 miesięcy | 3-12 місяців":
        return "1y"
    elif s_ == "nie ma danych":
        return None
    else:
        vn.append(f"Could not understand time period: {s}")
        return None


def get_how_long_can_stay(string, vn):
    if string == "":
        return None
    return ", ".join(
        filter(lambda x: x, [map_how_long(x, vn) for x in string.split(",")])
    )


def map_location(s, vn):
    s_ = s.strip()

    if s_ == "Kraków | Краків":
        return "kraków"
    elif s_ == "Kraków i okolice | Краків і передмістя":
        return "kraków area"
    elif s_ == "Inne miasto | Інше місто":
        return "other"
    else:
        vn.append(f"Could not understand preferred location: {s}")
        return None


def get_preferred_location(string, vn):
    if string == "":
        return None
    return ", ".join(
        filter(lambda x: x, [map_location(x, vn) for x in string.split(",")])
    )


def row_as_dict(row, headers):
    d = {}
    for h in headers:
        d[h] = row[headers.index(h)]
    return d


def get_priority_status(value):
    if value == "Znalezione":
        return "ACCOMMODATION_FOUND"
    elif value == "Nie odbiera":
        return "DOES_NOT_RESPOND"
    elif value == "Nie potrzebuje":
        return "ACCOMMODATION_NOT_NEEDED"
    elif value == "W drodze na Ukrainie":
        return "EN_ROUTE_UA"
    elif value == "W drodze w Polsce":
        return "EN_ROUTE_PL"
    elif value == "W Krakowie":
        return "IN_KRK"
    elif value == "Na Radziwilowskiej 3":
        return "AT_R3"
    elif value == "Zaktualizowane/Szukają":
        return "UPDATED"
    else:
        return None


def import_ludzi():
    ludzi = []
    with open(
        "[salam] Ludzi (Ukrainska) - Ludzi.tsv", encoding="utf-8", newline=""
    ) as cf:
        cr = csv.reader(cf, delimiter="\t")
        headers = next(cr, [0])
        headers_match = all(i for i in [i == j for i, j in zip(headers, LUDZI_HEADERS)])
        if not headers_match:
            report.error("Headers do not match with Ludzi tab format")
            for (expected, actual) in zip(LUDZI_HEADERS, headers):
                if expected != actual:
                    report.error(f"  - expected={expected}; actual={actual}")
            return []

        for row in cr:
            validation_notes = []

            # Column A contents SHALL be noted, and used to match current Guest with appropriate entry in Column "KIM jest juz zajety? (ID czlowieka)" of AccommodationUnits.
            column_a = row[0]
            __old_guest_id = column_a

            # Column C DATA contents SHALL be converted into UNIX timestamp and placed into guests.created_at
            column_c = row[2]
            created_at = datetime.datetime.now().isoformat()
            try:
                created_at = datetime.datetime.strptime(
                    column_c, "%d/%m/%Y"
                ).isoformat()
            except Exception:
                validation_notes.append(f"DATA: {column_c}")

            # Column D STATUS contents SHALL be converted to guests.priority_status
            column_d = row[3]
            status = get_priority_status(column_d)

            # Column E imie i nazwisko wolontariusza contents SHALL be appended to guests.system_comments
            column_e = row[4]
            validation_notes.append(f"imie i nazwisko wolontariusza: {column_e}")

            # Column F Imie i Nazwisko contents SHALL be placed in guests.full_name
            column_f = row[5]
            full_name = column_f

            # Column G Telefon (z kodem kierunkowym) contents SHALL be placed in guests.phone_number, such that:
            # - whitespaces SHALL be trimed
            # - digits SHALL be grouped in threes.
            # - if phone number consist of more than 9 digits, prefix SHALL be extracted and formatted with +.
            column_g = row[6]
            phone_number = column_g

            # Column H Priorytet contents SHALL be converted into UNIX timestamp and placed in guests.priority_date
            column_h = re.sub(r"\s+", "", row[7])
            priority_date = None
            try:
                if column_h != "":
                    priority_date = datetime.datetime.strptime(
                        column_h, "%d/%m/%Y"
                    ).isoformat()
            except Exception:
                validation_notes.append(f"Priorytet: {column_h}")

            # Column I TOTAL Ilość osób contents SHALL be placed in guests.people_in_group
            column_i = re.sub(r"\s+", "", row[8])
            people_in_group = 0
            try:
                people_in_group = int(column_i)
            except Exception:
                validation_notes.append(f"TOTAL Ilość osób cell: {column_i}")

            # Column J Dorosly contents SHALL be ignored, as there is no reliable way to decide how many women and men are there.
            adult_male_count = 0
            adult_female_count = 0

            # Column K Dzieci contents SHALL be converted into an array with the number of elements specified by the value in the cell.
            # The array SHALL have all 0s, as there is no realiable way to extract the age of the children.
            column_k = re.sub(r"\s+", "", row[10])
            children_count = 0
            try:
                children_count = int(row[10]) if column_k != "" else 0
            except:
                validation_notes.append(f"Dzieci: {column_k}")
            children_ages = [0 for x in range(0, children_count)]

            # Column L Wiek Dzieci np 6m; 5 i 8 contents SHALL be placed in guests.system_comments
            column_l = row[11]
            validation_notes.append(f"Wiek Dzieci np 6m; 5 i 8: {column_l}")

            # Column M Zwierzę:
            # Value Nie SHALL set guests.have_pets to False
            # Other values SHALL set guests.have_pets to True, and append the contents of the cell to guests.pets_description
            column_m = row[12]
            have_pets = column_m != ""
            pets_description = column_m

            # Column N Uwagi(Czy są kobieta w ciazy, inwalidy (jaka grupa?) Czy sa potrzebny leki, przelewanie krwi dializ etd?
            # Czy są jakies alergie? contents SHALL be placed in guests.special_needs
            column_n = row[13]
            special_needs = column_n

            # Column O Finanse contents SHALL be placed in guests.finance_status
            column_o = row[14]
            finance_status = column_o

            # Column P Na ile Czasu:
            # Values matching a pattern \d+\s?(d|w|m|y) SHALL be placed in guests.how_long_to_stay
            # Other values SHALL be appended to guests.system_comments
            column_p = row[15]
            how_long_to_stay = get_how_long_can_stay(column_p, validation_notes)

            # Column Q Uwagi contents SHALL be placed in guests.staff_comments
            staff_comments = row[16]

            data = {
                "full_name": full_name,
                "phone_number": phone_number,
                "is_agent": False,
                "document_number": None,
                "people_in_group": people_in_group,
                "adult_male_count": adult_male_count,
                "adult_female_count": adult_female_count,
                "children_ages": children_ages,
                "have_pets": have_pets,
                "pets_description": pets_description,
                "special_needs": special_needs,
                "priority_date": priority_date,
                "finance_status": finance_status,
                "how_long_to_stay": how_long_to_stay,
                "desired_destination": None,
                "staff_comments": staff_comments,
                "created_at": created_at,
                "system_comments": validation_notes,
                "priority_status": status,
                "updated_by_id": "28ab1bf2-f735-4603-b7f0-7938ba2ab059",  # default system user
                "__old_guest_id": __old_guest_id,
            }
            if full_name != " " and full_name != "":
                ludzi.append(data)
    return ludzi


def import_recepcja():
    recepcja = []
    with open(
        "[salam] Ludzi (Ukrainska) - UPD Data from Reception.tsv",
        encoding="utf-8",
        newline="",
    ) as cf:
        cr = csv.reader(cf, delimiter="\t")
        headers = next(cr, [0])
        headers_match = all(
            i for i in [i == j for i, j in zip(headers, RECEPCJA_HEADERS)]
        )
        if not headers_match:
            report.error("Headers do not match with UPD Data tab format")
            for (expected, actual) in zip(RECEPCJA_HEADERS, headers):
                if expected != actual:
                    report.error(f"  - expected={expected}; actual={actual}")
            return []

        for row in cr:
            validation_notes = []

            # Column C Timestamp contents SHALL be converted into UNIX timestamp and placed in guests.created_at
            column_c = row[2]
            created_at = datetime.datetime.now().isoformat()
            try:
                created_at = datetime.datetime.strptime(
                    column_c, "%d/%m/%Y %H:%M:%S"
                ).isoformat()
            except:
                validation_notes.append(f"Timestamp: {column_c}")

            # Column D Imię | Ім'я contents SHALL be appended to guests.full_name
            # Column E Nazwisko | Прізвище contents SHALL be appended to guests.full_name
            parts = []
            column_d = row[3]
            if column_d:
                parts.append(column_d)
            column_e = row[4]
            if column_e:
                parts.append(column_e)
            full_name = " ".join(parts)

            # Column F Numer kontaktowy | Номер телефону contents SHALL be placed in guests.phone_number
            column_f = row[5]
            phone_number = column_f

            # Column G Osoba do kontaktu? | Особа до контакту? SHALL set guests.is_agent to True
            # if equal to Tak | Так and to False otherwise.
            column_g = row[6]
            is_agent = True if column_g.startswith("Tak") else False

            # Column H Numer dokumentu | Номер паспорту (ID) contents SHALL be placed in guests.document_number
            column_h = row[7]
            document_number = column_h if re.sub(r"\s+", "", column_h) != "" else None

            # Column I Ile osób potrzebują zakwaterowania? | Скільки осіб потребують житла? [Mężczyźni | Чоловіки]
            # contents SHALL be placed in guests.adult_male_count
            column_i = row[8]
            adult_male_count = 0
            adult_male_count_cell = re.sub(r"\s+", "", column_i)
            if adult_male_count_cell != "":
                try:
                    adult_male_count = int(adult_male_count_cell)
                except:
                    validation_notes.append(
                        f"Ile osób potrzebują zakwaterowania? | Скільки осіб потребують житла? [Mężczyźni | Чоловіки]: {column_i}"
                    )

            # Column J Ile osób potrzebują zakwaterowania? | Скільки осіб потребують житла? [Kobiety | Жінки]
            # contents SHALL be placed in guests.adult_female_count
            column_j = row[9]
            adult_female_count = 0
            adult_female_count_cell = re.sub(r"\s+", "", column_j)
            if adult_female_count_cell != "":
                try:
                    adult_female_count = int(adult_female_count_cell)
                except:
                    validation_notes.append(
                        f"Ile osób potrzebują zakwaterowania? | Скільки осіб потребують житла? [Kobiety | Жінки]: {adult_female_count_cell}"
                    )

            # Column K Ile osób potrzebują zakwaterowania? | Скільки осіб потребують житла? [Dzieci | Діти] contents SHALL be converted
            # into an array with the number of elements specified by the value in the cell. The array SHALL have all 0s, as the process
            # of extraction children ages is not reliable
            column_k = row[10]
            children_count = 0
            children_count_cell = re.sub(r"\s+", "", column_k)
            if children_count_cell != "":
                try:
                    children_count = int(children_count_cell)
                except:
                    validation_notes.append(
                        f"Ile osób potrzebują zakwaterowania? | Скільки осіб потребують житла? [Dzieci | Діти]: {children_count_cell}"
                    )
            children_ages = [0 for x in range(0, children_count)]

            # Sum of values in Column I, Column J and Column K SHALL be placed in guests.people_in_group
            people_in_group = adult_male_count + adult_female_count + children_count

            # Column L Wiek dziecka (dzieci) | Вік дитини (дітей) contents SHALL be appended to guests.system_comments

            column_l = row[11]
            # children_ages_str = column_l
            # children_ages_str = re.sub(CHILDREN_AGES_LAT_REGEXP, "", children_ages_str, 0, re.MULTILINE)
            # children_ages = []
            # if children_ages_str != '' and children_ages_str != '-':
            #    children_ages = try_split(children_ages_str, [',', ';', 'i', ' '])
            #    if not isinstance(children_ages, list):
            validation_notes.append(
                f"Wiek dziecka (dzieci) | Вік дитини (дітей): {column_l}"
            )

            # Column M Wiek dorosłej osoby (osób) | Вік дорослої особи (осіб) contents SHALL be appended to guests.system_comments
            column_m = row[12]
            validation_notes.append(
                f"Wiek dorosłej osoby (osób) | Вік дорослої особи (осіб): {column_m}"
            )

            # Column N Zwierzęta domowe | Домашні тварини [Pies | Собака] contents if non-empty SHALL
            # set guests.have_pets value to True and SHALL append Pies to guests.pets_description
            column_m = row[13]
            pets = []
            if column_m:
                have_pets = True
                pets.append("Pies")

            # Column O Zwierzęta domowe | Домашні тварини [Kot | Кіт] contents if non-empty SHALL set guests.have_pets value
            # to True and SHALL append Kot to guests.system_comments
            column_o = row[14]
            if column_o:
                have_pets = True
                pets.append("Kot")

            pets_description = " i ".join(pets)

            # Column Q Na jaki okres potrzebują zakwaterowania? | На який час потрібне житло? contents SHALL take the upper
            # limit value and convert it to \d(d|w|m|y) format and placed in guests.how_long_to_stay
            column_q = row[16]
            how_long_to_stay = get_how_long_can_stay(column_q, validation_notes)

            # Column R Mieszkanie płatne czy za darmo? | Житло платне чи безплатне? contents SHALL be appended to guests.finance_status
            column_r = row[17]

            # Column S Jeśli z dopłatą to ile mogą wydać w miesiącu? | Якщо з доплатою то скільки можуть потратити за місяць?
            # contents SHALL be appended to guests.finance_status
            column_s = row[18]
            finance_status = "\\n".join([column_r, column_s])

            # Column T Czy mają własny transport? | Чи є власний транспорт? contents SHALL be appended to guests.system_comments
            column_t = row[19]
            validation_notes.append(
                f"Czy mają własny transport? | Чи є власний транспорт?: {column_t}"
            )

            # Column U Miejscowość | Місцевість contents SHALL be placed into guests.desired_desitnation
            column_u = row[20]
            preferred_location = column_u

            # Column V Od jakiej daty jest potrzebne zakwaterowanie? | Від якого числа (дати) потрібне житло? contents SHALL be converted
            # to UNIX timestamp and placed in guests.priority_date
            column_v = row[21]
            priority_date_cell = re.sub(r"\s+", "", column_v if column_v else "")
            priority_date = None
            try:
                if priority_date_cell != "":
                    priority_date = datetime.datetime.strptime(
                        priority_date_cell, "%d/%m/%Y"
                    ).isoformat()
            except:
                validation_notes.append(
                    f"Od jakiej daty jest potrzebne zakwaterowanie? | Від якого числа (дати) потрібне житло?: {column_v}"
                )

            # Column W Notatki i komentarze dotyczące zwierząt domowych, zakwaterowania, stanu zdrowia, edukacji itd (opcjonalnie) | Нотатки і коментарі відносно
            # домашніх тварин, житла, стану здоров"я, освіти та інше contents SHALL be appended to guests.staff_comments
            column_w = row[22]
            staff_comments = column_w

            data = {
                "full_name": full_name,
                "phone_number": phone_number,
                "is_agent": is_agent,
                "document_number": document_number,
                "people_in_group": people_in_group,
                "adult_male_count": adult_male_count,
                "adult_female_count": adult_female_count,
                "children_ages": children_ages,
                "have_pets": have_pets,
                "pets_description": pets_description,
                "finance_status": finance_status,
                "how_long_to_stay": how_long_to_stay,
                "desired_destination": preferred_location,
                "priority_date": priority_date,
                "special_needs": None,
                "created_at": created_at,
                "system_comments": validation_notes,
                "staff_comments": staff_comments,
                "priority_status": None,
                "__old_guest_id": None,
            }
            if full_name != " " and full_name != "":
                recepcja.append(data)
    return recepcja


def merge_ludzi_recepcja(ludzi, recepcja):
    merged = [x for x in ludzi]
    phone_numbers_dict = {}
    full_name_dict = {}
    for x in recepcja:
        phone_numbers_dict[x["phone_number"]] = x
        full_name_dict[x["full_name"]] = x

    for i, x in enumerate(merged):
        key = x["full_name"]
        r = full_name_dict.get(key, None)
        if r:
            x["document_number"] = r["document_number"]
            x["is_agent"] = r["is_agent"]
            x["adult_male_count"] = r["adult_male_count"]
            x["adult_female_count"] = r["adult_female_count"]
            finance_status = "\\n".join([x["finance_status"], r["finance_status"]])
            x["finance_status"] = finance_status
            r["finance_status"] = finance_status
            x["desired_destination"] = r["desired_destination"]
            x["priority_status"] = r["priority_status"]
            for vn in r["system_comments"]:
                x["system_comments"].append(vn)
            r["system_comments"] = x["system_comments"]
            x["created_at"] = r["created_at"]
            notes = "\\n".join([x["staff_comments"], r["staff_comments"]])
            x["staff_comments"] = notes
            r["staff_comments"] = notes
            r["special_needs"] = x["special_needs"]
            r["children_ages"] = x["children_ages"]
            merge_issues = {i: (x[i], r[i]) for i, j in x.items() if x[i] != r[i]}
            merge_issues_arr = []
            for k in merge_issues.keys():
                if not k.startswith("__"):
                    v = merge_issues[k]
                    row = f"{k} - {v[0]} vs. {v[1]}"
                    merge_issues_arr.append(row)
            merge_issues_str = "\\n".join(merge_issues_arr)
            x["system_comments"].append(
                f"Could not merge following data:\\n{merge_issues_str}"
            )
            x["system_comments"] = "\\n".join(x["system_comments"])
            merged[i] = x
            full_name_dict.pop(key, None)
    [merged.append(x) for x in full_name_dict.values()]
    return merged


STAY_REGEX = r"(\d+)\s*(d|w|m|y)"


def get_how_long_to_stay(value):
    match = re.match(STAY_REGEX, value) if value else None
    return f"{match.group(1)}{match.group(2)}" if match else None


def get_workflow_status(value, workflow_status):
    if value == "OUT":
        return "WITHDRAWN"
    elif value == "DONE":
        return "DONE"
    elif value == "AVAILABLE" or value == "":
        return "AVAILABLE"
    elif value == "HOLD" or value == "CHANGED":
        return "NEEDS_VERIFICATION"
    elif value == "Przyjęcie krótkoterminowe":
        return "AVAILABLE" if workflow_status else "NEEDS_VERIFICATION"
    else:
        return workflow_status


def import_mieszkania(all_guests):
    hosts = []
    units = []
    languages = []
    with open(
        "[salam] Mieszkania (Polska) - Automated Mieszkania.tsv",
        encoding="utf-8",
        newline="",
    ) as cf:
        cr = csv.reader(cf, delimiter="\t")
        headers = next(cr, [0])
        headers_match = all(
            i for i in [i == j for i, j in zip(headers, MIESZKANIA_HEADERS)]
        )
        if not headers_match:
            report.error("Headers do not match with Mieszkania tab format")
            for (expected, actual) in zip(MIESZKANIA_HEADERS, headers):
                if expected != actual:
                    report.error(f"  - expected={expected}; actual={actual}")
            return []

        for row in cr:
            host_validation_notes = []
            unit_validation_notes = []

            host_guid = str(uuid.uuid4())
            accommodation_unit_guid = str(uuid.uuid4())

            # Column A contents SHALL be appended to acommodation_units.system_comments
            column_a = row[0]
            unit_validation_notes.append(f"column A: {column_a}")

            # Column B NASZE UWAGI contents SHALL be appended to acommodation_units.system_comments
            column_b = row[1]
            unit_validation_notes.append(f"NASZE UWAGI: {column_b}")

            # Column C Na jak długo?:
            # - Values matching a pattern \d+\s?(d|w|m|y) SHALL be placed in acommodation_units.for_how_long
            # - Other values SHALL be appended to accommodation_units.system_comments
            column_c = row[2]
            how_long_to_stay = get_how_long_to_stay(column_c)
            if not how_long_to_stay:
                unit_validation_notes.append(f"Na jak długo?: {column_c}")

            # Column D KIM jest juz zajety? (ID czlowieka) contents SHALL be used to match appropriate Guest.
            # Generated UUIDv4 GUID for current AccommodationUnit SHALL be placed in guest.accommodation_unit_id
            # of a Guest with matching Column A value.
            column_d = row[3]
            try:
                old_guest_id = int(column_d)
                if old_guest_id:
                    for g in all_guests:
                        old_id = g.get("__old_guest_id", None)
                        if old_id == old_guest_id:
                            g["accommodation_unit_id"] = accommodation_unit_guid
            except Exception:
                unit_validation_notes.append(
                    f"KIM jest juz zajety? (ID czlowieka): {column_d}"
                )

            # Column E WOLONTARIUSZ (kto się kontaktował) contents will be used to set workflow_status to
            # either Available if not empty, and Needs verification otherwise.
            column_e = row[4]
            workflow_status = "AVAILABLE" if column_e else "NEEDS_VERIFICATION"

            # Column F STATUS contents SHALL be converted to workflow_status
            column_f = row[5]
            workflow_status = get_workflow_status(column_f, workflow_status)

            # Column G Timestamp shall be converted to UNIX timestamp and placed in acommodation_units.created_at and hosts.created_at
            column_g = row[6]
            created_at = datetime.datetime.now().isoformat()
            try:
                created_at = datetime.datetime.strptime(
                    row[2], "%d/%m/%Y %H:%M:%S"
                ).isoformat()
            except Exception:
                host_validation_notes.append(f"Timestamp: {column_g}")
                unit_validation_notes.append(f"Timestamp: {column_g}")

            # Column I Miasto lokalu contents SHALL be placed in acommodation_units.city
            column_i = row[8]
            if len(column_i) > 50:
                unit_validation_notes.append(f"Miasto lokalu: {column_i}")
                column_i = column_i[:49]
            city = column_i

            # Column J Adres lokalu contents SHALL be placed in accommodation_units.address_line
            column_j = row[9]
            address_line = column_j

            # Column K Imię i nazwisko contents SHALL be placed in hosts.full_name
            column_k = row[10]
            host_fullname = column_k

            # Column L Adres email: contents SHALL be placed in hosts.email
            column_l = row[11]
            host_email = column_l

            # Column M Numer telefonu contents SHALL be placed in hosts.phone_number
            column_m = row[12]
            host_phone_number = column_m

            # Column O Maksymalna ilość ludzi, które możesz przyjąć w swoim lokalu mieszkalnym?:
            # - Values matching a pattern \d-\d SHALL take an upper value and be placed in
            #   accommodation_units.vacancies_total
            # - Other values SHALL be appended to accommodation_units.system_comments
            column_o = row[14]
            vacancies_total = 0
            try:
                parts = column_o.split("-")
                upper = int(parts[1])
                vacancies_total = upper
            except Exception:
                unit_validation_notes.append(
                    f"Maksymalna ilość ludzi, które możesz przyjąć w swoim lokalu mieszkalnym?: {column_o}"
                )

            # Column P Uwagi: Czy posiadasz zwierzęta? Czy akceptujesz gości ze zwierzętami? Godziny w których możemy do
            # Ciebie dzwonić? Masz inne uwagi? contents SHALL be appended to accommodation_unit.owner_comments
            column_p = row[15]
            host_comments = column_p

            # Column R Jakie znasz języki? SHALL be matched against languages Polski, Ukraiński, Rosyjski, Angielski
            # and appropriate entries SHALL be added to host_languages table. Regardless of the matching, contents
            # of the column SHALL be appended to host.system_comments
            column_r = row[17]
            host_langs = column_r.lower()
            languages.append(
                {"host_id": host_guid, "language_code": "pl"}
            ) if "polski" in host_langs else None
            languages.append(
                {"host_id": host_guid, "language_code": "en"}
            ) if "angielski" in host_langs else None
            languages.append(
                {"host_id": host_guid, "language_code": "ru"}
            ) if "rosyjski" in host_langs else None
            languages.append(
                {"host_id": host_guid, "language_code": "uk"}
            ) if "ukraiński" in host_langs else None
            host_validation_notes.append(f"Jakie znasz języki? {column_r}")

            # Column W Jeśli masz jakieś pytania, uwagi lub dodatkowe komentarze, na które nie znalazł_ś miejsca
            # w formularzu, napisz je proszę poniżej: contents SHALL be appended to accommodation_unit.owner_comments.
            column_w = row[22]
            owner_comments = column_w

            host_data = {
                "guid": host_guid,
                "full_name": host_fullname,
                "email": host_email,
                "phone_number": host_phone_number,
                "comments": host_comments,
                "created_at": created_at,
                "system_comments": "\\n".join(host_validation_notes),
            }
            hosts.append(host_data)

            unit_data = {
                "guid": accommodation_unit_guid,
                "city": city,
                "zip": "00-000",
                "address_line": address_line,
                "vacancies_total": vacancies_total,
                "owner_comments": owner_comments,
                "system_comments": "\\n".join(unit_validation_notes),
                "host_id": host_guid,
            }
            units.append(unit_data)
    return hosts, units, languages
