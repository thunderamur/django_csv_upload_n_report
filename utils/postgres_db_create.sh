#!/usr/bin/env bash

PASSWORD='password'

sudo -u postgres psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    CREATE DATABASE worktime_db;
    CREATE USER worktime_user WITH PASSWORD '${PASSWORD}';
    ALTER ROLE worktime_user SET client_encoding TO 'utf8';
    ALTER ROLE worktime_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE worktime_user SET timezone TO 'Asia/Yakutsk';
    GRANT ALL PRIVILEGES ON DATABASE worktime_db TO worktime_user;
    ALTER USER worktime_user CREATEDB;
EOSQL
