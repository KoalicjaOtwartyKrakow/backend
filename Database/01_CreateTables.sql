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
    guid uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name varchar(20),
    phone_number varchar(20)
);

CREATE TABLE IF NOT EXISTS public.languages (
    name varchar(20) NOT NULL,
    code2 varchar(2) NOT NULL, /*iso_639_1_code*/
    code3 varchar(3) NOT NULL, /*iso_639_2_code*/
    PRIMARY KEY(code2)
);

CREATE TYPE public.verificationstatus AS ENUM ('CREATED', 'VERIFIED', 'REJECTED');

CREATE TABLE IF NOT EXISTS public.hosts (
	guid UUID NOT NULL,
	full_name VARCHAR(256) NOT NULL,
	email VARCHAR(100) NOT NULL,
	phone_number VARCHAR(20) NOT NULL,
	call_after VARCHAR(64),
	call_before VARCHAR(64),
	comments TEXT,
	status verificationstatus DEFAULT 'CREATED' NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	system_comments TEXT,
	PRIMARY KEY (guid)
);

CREATE TRIGGER set_host_timestamp
    BEFORE
        UPDATE ON public.hosts
    FOR EACH ROW
    EXECUTE PROCEDURE public.trigger_set_timestamp();

CREATE TABLE IF NOT EXISTS public.host_teammembers (
    teammember_id uuid,
    host_id uuid,
    PRIMARY KEY(host_id,teammember_id),
    CONSTRAINT fk_teammember
        FOREIGN KEY(teammember_id)
            REFERENCES teammembers(guid),
    CONSTRAINT fk_host
        FOREIGN KEY(host_id)
            REFERENCES hosts(guid)
);

CREATE TABLE IF NOT EXISTS public.host_languages (
	language_code VARCHAR(2),
	host_id UUID,
	guid UUID DEFAULT uuid_generate_v4() NOT NULL,
	PRIMARY KEY (guid),
	CONSTRAINT lang_host_pair_unique UNIQUE (language_code, host_id),
	CONSTRAINT fk_language FOREIGN KEY(language_code) REFERENCES languages (code2),
	CONSTRAINT fk_host FOREIGN KEY(host_id) REFERENCES hosts (guid)
);

CREATE TYPE public.voivodeship AS ENUM (
    'DOLNOSLASKIE',
    'KUJAWSKOPOMORSKIE',
    'LUBELSKIE',
    'LUBUSKIE',
    'LODZKIE',
    'MALOPOLSKIE',
    'MAZOWIECKIE',
    'OPOLSKIE',
    'PODKARPACKIE',
    'PODLASKIE',
    'POMORSKIE',
    'SLASKIE',
    'SWIETOKRZYSKIE',
    'WARMINSKOMAZURSKIE',
    'WIELKOPOLSKIE',
    'ZACHODNIOPOMORSKIE'
);

CREATE TABLE IF NOT EXISTS public.accommodation_units (
	guid UUID NOT NULL,
	host_id UUID NOT NULL,
	city VARCHAR(50),
	zip VARCHAR(10) NOT NULL,
	voivodeship voivodeship,
	address_line VARCHAR(512) NOT NULL,
	vacancies_total INTEGER NOT NULL,
	pets_present BOOLEAN,
	pets_accepted BOOLEAN,
	disabled_people_friendly BOOLEAN,
	lgbt_friendly BOOLEAN,
	parking_place_available BOOLEAN,
	owner_comments TEXT,
	easy_ambulance_access BOOLEAN,
	vacancies_free INTEGER,
	staff_comments TEXT,
	status verificationstatus DEFAULT 'CREATED' NOT NULL,
	system_comments TEXT,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	PRIMARY KEY (guid),
	CONSTRAINT fk_host FOREIGN KEY(host_id) REFERENCES hosts (guid)
);


CREATE TRIGGER set_accommodation_units_timestamp
    BEFORE
        UPDATE ON public.accommodation_units
    FOR EACH ROW
    EXECUTE PROCEDURE public.trigger_set_timestamp();

CREATE TYPE public.guest_status AS ENUM ('CREATED', 'VERIFIED', 'REJECTED');

CREATE TYPE public.guestprioritystatus AS ENUM (
    'DOES_NOT_RESPOND',
    'ACCOMMODATION_NOT_NEEDED',
    'EN_ROUTE_UA',
    'EN_ROUTE_PL',
    'IN_KRK',
    'AT_R3',
    'ACCOMMODATION_FOUND',
    'UPDATED'
);

CREATE TABLE IF NOT EXISTS public.guests (
	guid UUID NOT NULL,
	full_name VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	phone_number VARCHAR(20) NOT NULL,
	is_agent BOOLEAN DEFAULT false NOT NULL,
	document_number VARCHAR(255),
	people_in_group INTEGER DEFAULT 1 NOT NULL,
	adult_male_count INTEGER DEFAULT 0 NOT NULL,
	adult_female_count INTEGER DEFAULT 0 NOT NULL,
	children_ages INTEGER[] NOT NULL,
	have_pets BOOLEAN DEFAULT false NOT NULL,
	pets_description VARCHAR(255),
	special_needs TEXT,
	food_allergies TEXT,
	meat_free_diet BOOLEAN DEFAULT false NOT NULL,
	gluten_free_diet BOOLEAN DEFAULT false NOT NULL,
	lactose_free_diet BOOLEAN DEFAULT false NOT NULL,
	finance_status VARCHAR(255),
	how_long_to_stay VARCHAR(255),
	desired_destination VARCHAR(255),
	priority_status guestprioritystatus,
	priority_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
	staff_comments TEXT,
	verification_status verificationstatus DEFAULT 'CREATED' NOT NULL,
	system_comments TEXT,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	accommodation_unit_id UUID,
	PRIMARY KEY (guid),
	CONSTRAINT fk_accommodation_unit_id FOREIGN KEY(accommodation_unit_id) REFERENCES accommodation_units (guid)
);

CREATE TRIGGER set_guests_timestamp
    BEFORE
        UPDATE ON public.guests
    FOR EACH ROW
    EXECUTE PROCEDURE public.trigger_set_timestamp();
