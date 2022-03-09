CREATE USER ApiServiceUser WITH PASSWORD 'aB94cgg4s?FkLzsi';

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT select,insert,update,delete,truncate ON TABLES TO ApiServiceUser;



GRANT select,insert,update,delete,truncate ON ALL TABLES IN schema public TO ApiServiceUser;


REVOKE select,insert,update,delete,truncate ON public.languages from ApiServiceUser;