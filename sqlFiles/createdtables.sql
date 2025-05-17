DROP DATABASE IF EXISTS orgsys;

CREATE OR REPLACE USER 'orgsys'@'localhost' IDENTIFIED BY 'useruser';
CREATE DATABASE orgsys;
GRANT ALL ON orgsys.* TO 'orgsys'@'localhost';

USE orgsys;

create or replace table organization(
org_name varchar(50),
org_account varchar(20),
-- may pake pa ba tayo sa auth?
org_password varchar(30), 
date_formed DATE not null,
org_funds int(10) default 0,
primary key(org_name)
);

create or replace table member(
std_num char(10),
mem_username varchar(20),
mem_password varchar(30),
degree_program varchar(50) not null,
gender varchar(10),
debt int(8) default 0, 
f_name varchar(50) not null,
l_name varchar(50),
m_name varchar(50),
primary key(std_num),
constraint std_num_ck CHECK(std_num like '____-_____'), 
constraint debt_ck CHECK(debt >= 0)
);

create or replace table fee(
fee_id int(3) auto_increment,
fee_name varchar(50),
amount int(5) not null,
due_date DATE not null,
fee_sem varchar(1),
fee_acad_year DATE,
org_name varchar(50),
primary key(fee_id),
constraint fee_org_name_fk foreign key(org_name)
references organization(org_name),
-- ONLY TAKES INTO ACCOUNT 1st and 2nd Sem
constraint fee_sem_ck CHECK(fee_sem in ('1', '2'))
);


create or replace table organization_has_member(
std_num char(10),
org_name varchar(50),
mem_sem varchar(1),
mem_acad_year DATE,
role varchar(20) default "regular member",
committee_name varchar(50),
status varchar(15) default "active",
primary key(std_num, org_name, mem_sem, mem_acad_year),
constraint org_has_mem_std_num_fk foreign key(std_num)
references member(std_num),
constraint org_has_mem_org_name_fk foreign key(org_name)
references organization(org_name),
constraint std_num_ck CHECK(std_num like '____-_____'),
constraint mem_sem_ck CHECK(mem_sem in ('1', '2'))
);


create or replace table mem_org_batch(
std_num char(10),
org_name varchar(50),
batch int(4) not null,
primary key(std_num, org_name, batch),
constraint org_has_batch_std_num_fk foreign key(std_num)
references member(std_num),
constraint org_has_batch_org_name_fk foreign key(org_name)
references organization(org_name),
constraint batch_ck CHECK(batch >= (CAST(substring(std_num, 1, 4) AS int)))
);

create or replace table member_pays_fee(
std_num char(10),
fee_id int(3),
status varchar(2) default "NP",
paid_date DATE,
primary key(std_num, fee_id),
constraint member_pays_fee_fee_id_fk foreign key(fee_id)
references fee(fee_id),
constraint member_pays_fee_std_num_fk foreign key(std_num)
references member(std_num),
constraint std_num_ck CHECK(std_num like '____-_____'),
-- P-PAID NP-NOT PAID
constraint status_ck CHECK(status in ('P', 'NP')),
constraint fee_id_ck CHECK(fee_id > 0)
);

