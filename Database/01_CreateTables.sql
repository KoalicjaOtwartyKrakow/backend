CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE FUNCTION public.trigger_set_timestamp()
    RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

/* those who work with spreadsheet  */
CREATE TABLE IF NOT EXISTS public.teammembers (
    id integer GENERATED ALWAYS AS IDENTITY,
    guid uuid DEFAULT uuid_generate_v4(),
    full_name varchar(20),
    phone_number varchar(20) ,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS public.languages (
    name varchar(20) NOT NULL,
    code2 varchar(2) NOT NULL, /*iso_639_1_code*/
    code3 varchar(3) NOT NULL, /*iso_639_2_code*/
    PRIMARY KEY(code2)
);

CREATE TYPE public.host_status AS ENUM ('created', 'verified', 'banned');

CREATE TABLE IF NOT EXISTS public.hosts (
    id integer  GENERATED ALWAYS AS IDENTITY,
    guid uuid DEFAULT uuid_generate_v4(),
    full_name varchar(256) NOT NULL,
    email varchar(100) NOT NULL,
    phone_number varchar(20) NOT NULL,
    call_after varchar(20),
    call_before varchar(20),
    comments  text,
    status host_status NOT NULL DEFAULT 'created',
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now(),
    PRIMARY KEY(id)
);

CREATE TRIGGER set_host_timestamp
    BEFORE
        UPDATE ON public.hosts
    FOR EACH ROW
    EXECUTE PROCEDURE public.trigger_set_timestamp();

CREATE TABLE IF NOT EXISTS public.host_teammembers (
    teammember_id integer,
    host_id integer,
    PRIMARY KEY(host_id,teammember_id),
    CONSTRAINT fk_teammember
        FOREIGN KEY(teammember_id)
            REFERENCES teammembers(id),
    CONSTRAINT fk_host
        FOREIGN KEY(host_id)
            REFERENCES hosts(id)
);

CREATE TABLE IF NOT EXISTS public.host_languages (
    id integer GENERATED ALWAYS AS IDENTITY,
    language_code varchar(2),
    host_id integer,
    PRIMARY KEY(id),
    CONSTRAINT fk_language
        FOREIGN KEY(language_code)
        REFERENCES languages(code2),
    CONSTRAINT fk_hosts
        FOREIGN KEY(host_id)
            REFERENCES hosts(id)
);

CREATE TYPE public.voivodeship_enum AS ENUM (
    'DOLNOŚLĄSKIE',
    'KUJAWSKO-POMORSKIE',
    'LUBELSKIE',
    'LUBUSKIE',
    'ŁÓDZKIE',
    'MAŁOPOLSKIE',
    'MAZOWIECKIE',
    'OPOLSKIE',
    'PODKARPACKIE',
    'PODLASKIE',
    'POMORSKIE',
    'ŚLĄSKIE',
    'ŚWIĘTOKRZYSKIE',
    'WARMIŃSKO-MAZURSKIE',
    'WIELKOPOLSKIE',
    'ZACHODNIOPOMORSKIE'
);

CREATE TYPE public.apartment_status AS ENUM ('created', 'verified', 'banned');

CREATE TABLE IF NOT EXISTS public.accommodation_units (
    id integer GENERATED ALWAYS AS IDENTITY,
    guid uuid DEFAULT uuid_generate_v4(),
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now(),
    city varchar(50), /* this should ideally be NOT NULL, but spreadsheet has very unstructured data */
    zip varchar(10) NOT NULL,
    voivodeship voivodeship_enum  NULL,
    address_line varchar(512) NOT NULL,
    vacancies_total smallint NOT NULL,
    vacancies_free	smallint NOT NULL,
    have_pets boolean,
    accept_pets boolean,
    comments varchar(255),
    status apartment_status NOT NULL DEFAULT 'created',
    PRIMARY KEY(id)
);


CREATE TRIGGER set_accommodation_units_timestamp
    BEFORE
        UPDATE ON public.accommodation_units
    FOR EACH ROW
    EXECUTE PROCEDURE public.trigger_set_timestamp();

CREATE TYPE public.guest_status AS ENUM ('created', 'verified', 'banned');

CREATE TABLE IF NOT EXISTS public.guests  (
    id integer GENERATED ALWAYS AS IDENTITY,
    guid uuid DEFAULT uuid_generate_v4(),
    full_name varchar(255) NOT NULL,
    phone_number varchar(20) NULL,
    people_in_group smallint not null DEFAULT 1,
    adult_male_count smallint not null,
    adult_female_count smallint not null,
    children_count smallint not null,
    children_ages smallint array null,
    have_pets boolean,
    pets_description varchar(255),
    special_needs text,
    priority_date  timestamp DEFAULT now(),
    status guest_status NOT NULL DEFAULT 'created',
    finance_status varchar(255), /*could be enum ,bool , or text*/
    how_long_to_stay  varchar(255),
    volunteer_note text,
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now(),
    PRIMARY KEY(id)
);

CREATE TRIGGER set_guests_timestamp
    BEFORE
        UPDATE ON public.guests
    FOR EACH ROW
    EXECUTE PROCEDURE public.trigger_set_timestamp();