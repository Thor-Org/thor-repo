CREATE DATABASE IF NOT EXISTS Lightning_Data;
USE Lightning_Data;

-- lightning_record
CREATE TABLE IF NOT EXISTS lightning_record(
    strike_time  datetime,
    nano_seconds int,
    lat          double,
    lon          double,
    rise_time    double,
    fall         double,
    peakcurrent  int,
    PRIMARY KEY (strike_time, nano_seconds)
    );

-- crypt
CREATE TABLE IF NOT EXISTS crypt(
    strike_time   datetime,
    nano_seconds  int,
    generated_key int,
    PRIMARY KEY (strike_time, nano_seconds)
    );

-- bug_report
CREATE TABLE IF NOT EXISTS bug_report(
    user    char,
    date    datetime,
    comment char,
    );
