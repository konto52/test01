drop database vsearchlogDB;
create database vsearchlogDB;
grant all on vsearchlogDB.* to 'vsearch' identified by 'vsearchpasswd';

use vsearchlogDB

DROP TABLE IF EXISTS log;
create table log (id int auto_increment primary key,
ts timestamp default current_timestamp,
pharse varchar(128) not null,
letters varchar(32) not null,
ip varchar(16) not null,
browser_string varchar(256) not null,
results varchar(64) not null);
