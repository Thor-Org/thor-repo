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

-- permutations
CREATE TABLE IF NOT EXISTS permutations(
    permutation char(256) NOT NULL,
    meta_data   char(256) NOT NULL,
    PRIMARY KEY (permutation)
    );

-- bug_report
CREATE TABLE IF NOT EXISTS bug_report(
    user    char,
    date    datetime,
    comment char,
    );
