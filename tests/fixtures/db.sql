TRUNCATE hosts RESTART IDENTITY CASCADE;

INSERT INTO hosts("full_name", "phone_number", "email", "call_after", "call_before", "comments", "guid")
VALUES ('Ewelina Głuszek', '443 143 258', 'wdonx.e@o2.pl', '17:30', '18:00', '',
        'dc6d05bb-9bd6-4e9d-a8e9-8b88d29adee5'),
       ('Edmund Królikowski', '550.343.606', 'dqova@poczta.onet.pl', '7:10', '8:00', '',
        '2078dad6-5dc9-4e5a-8ee0-d69c44f460e2');

TRUNCATE accommodation_units_version RESTART IDENTITY;
TRUNCATE accommodation_units RESTART IDENTITY CASCADE;

INSERT INTO accommodation_units("guid", "address_line", "city", "zip", "voivodeship", "vacancies_total",
                                "vacancies_free", "host_id")
VALUES('008c0243-0060-4d11-9775-0258ddac7620', 'ul. Zimna 19m.28', 'Lublin', '06-631',
       'LUBELSKIE', 5, 5, '2078dad6-5dc9-4e5a-8ee0-d69c44f460e2');

TRUNCATE users RESTART IDENTITY CASCADE;

INSERT INTO users (guid, given_name, family_name, email, google_sub, google_picture)
VALUES ('782962fc-dc11-4a33-8f08-b7da532dd40d', 'John', 'Doe',
        'john.doe@example.com', '10769150350006150715113082367', 'https://img.google.com/1.jpg'),
       ('46389922-28b5-430f-a2e1-04fcddd70117', 'Jane', 'Doe',
        'jane.doe@example.com', '10769150350006150715113082000', 'https://img.google.com/2.jpg');

TRUNCATE guests_version RESTART IDENTITY;
TRUNCATE guests RESTART IDENTITY CASCADE;

INSERT INTO guests(guid, full_name, email, phone_number, children_ages, updated_by_id, accommodation_unit_id)
VALUES ('744418aa-e1d9-45f8-ae6f-356ea146ac20', 'Adam Majcher',
        'gsssltitzwwg@gmail.com', '+48 388-808-644', '{13,12,17}', '782962fc-dc11-4a33-8f08-b7da532dd40d',
        '008c0243-0060-4d11-9775-0258ddac7620');

TRUNCATE transaction RESTART IDENTITY;
