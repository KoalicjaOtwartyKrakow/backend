DELETE FROM accommodation_units;

DELETE FROM hosts;

INSERT INTO hosts("full_name", "phone_number", "email", "call_after", "call_before", "comments", "guid")
VALUES ('Ewelina Głuszek', '443 143 258', 'wdonx.e@o2.pl', '17:30', '18:00', '',
        'dc6d05bb-9bd6-4e9d-a8e9-8b88d29adee5'),
       ('Edmund Królikowski', '550.343.606', 'dqova@poczta.onet.pl', '7:10', '8:00', '',
        '2078dad6-5dc9-4e5a-8ee0-d69c44f460e2');
