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

-- combinations
CREATE TABLE IF NOT EXISTS combinations(
    combination  varchar(256) NOT NULL,
    strike_time  datetime,
    nano_seconds int,
    lat          double,
    lon          double,
    rise_time    double,
    fall         double,
    peakcurrent  int,
    PRIMARY KEY (combination)
    );

-- keys_used
CREATE TABLE IF NOT EXISTS keys_used(
    used_key  varchar(256) NOT NULL,
    );

-- permutations
CREATE TABLE IF NOT EXISTS permutations(
    permutation varchar(256) NOT NULL,
    );

-- bug_report
CREATE TABLE IF NOT EXISTS bug_report(
    user    char,
    date    datetime,
    comment varchar(200),
    );
