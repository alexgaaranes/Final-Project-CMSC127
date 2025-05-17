-- CMSC 127 ST1-6L
-- Aranes, Marfa, Prudencio

-- CREATE DATABASE
DROP DATABASE IF EXISTS orgsys;

CREATE OR REPLACE USER 'orgsys'@'localhost' IDENTIFIED BY 'useruser';
CREATE DATABASE orgsys;
GRANT ALL ON orgsys.* TO 'orgsys'@'localhost';

USE orgsys;


-- TABLE DEFINITION
create or replace table organization(
	org_name varchar(50),
	org_account varchar(20),
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
	fee_acad_year char(9),
	org_name varchar(50),
	primary key(fee_id),
	constraint fee_org_name_fk foreign key(org_name)
	references organization(org_name),
	constraint fee_acad_year_ck CHECK(fee_acad_year like '____-____'),
	-- ONLY TAKES INTO ACCOUNT 1st and 2nd Sem
	constraint fee_sem_ck CHECK(fee_sem in ('1', '2')),
	constraint valid_fee_year_ck CHECK((CAST(substring(fee_acad_year, 1, 4) AS int)+1) = (CAST(substring(fee_acad_year, 6) AS int)))

);


create or replace table organization_has_member(
	std_num char(10),
	org_name varchar(50),
	mem_sem varchar(1),
	mem_acad_year char(9),
	batch int(4) not null,
	role varchar(20) default "regular member",
	committee_name varchar(50),
	status varchar(15) default "active",
	primary key(std_num, org_name, mem_sem, mem_acad_year),
	constraint org_has_mem_std_num_fk foreign key(std_num)
	references member(std_num),
	constraint org_has_mem_org_name_fk foreign key(org_name)
	references organization(org_name),
	constraint std_num_ck CHECK(std_num like '____-_____'),
	constraint mem_acad_year_ck CHECK(mem_acad_year like '____-____'),
	constraint mem_sem_ck CHECK(mem_sem in ('1', '2')),
	constraint mem_year_stdnum_ck CHECK((CAST(substring(mem_acad_year, 1, 4) AS int)+1)  >= (CAST(substring(std_num, 1, 4) AS int))),
	constraint valid_acad_year_ck CHECK((CAST(substring(mem_acad_year, 1, 4) AS int)+1) = (CAST(substring(mem_acad_year, 6) AS int))),
	constraint member_status_ck CHECK(status in ('active', 'inactive', 'alumni'))
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


-- DUMMY DATA (FOR SAMPLE QUERY)
insert into organization (org_name, date_formed, org_funds)
values("org", str_to_date('17-APR-2016','%d-%M-%Y'), 500),
("gets", str_to_date('17-APR-2016','%d-%M-%Y'), 500);


insert into member (std_num, degree_program, gender, debt, f_name, l_name, m_name)
	values
	("2023-04240", "BSCS", "?", 100,"Hello", "World", "Gonzales"),
	("2017-04147", "BSCS", "?", 100,"Yuu", "Mi", "Everyone"),
	("2018-04341", "BSCS", "?", 0,"Jhemmerlyn", "Jackie", "Albert"),
	("2021-19142", "BSCS", "?", 0,"John", "Filipino", "Phil"),
	("2023-09947", "BSCS", "?", 0,"Maria", "DataBase", "Sql"),
	("2020-03349", "BSCS", "?", 0,"John", "Flutter", "Android"),
	("2020-01149", "BSCS", "?", 0,"Umay", "Gets", "Gonzales"),
	("2024-01430", "BSPSYCH", "?", 100,"Gelly", "Fish", "Swims"),
	("2024-01420", "BSPSYCH", "?", 0,"Gold", "Fish", "Swam");

insert into organization_has_member values
	("2023-04240", "org", "1", "2023-2024", 2024, default, "scholastics", default),
	("2017-04147", "org", "2", "2018-2019", 2018, "head", "executive", default),
	("2018-04341", "org", "2", "2018-2019", 2020, "head", "scholastics", default),
	("2021-19142", "org", "2", "2021-2022", 2022, default, "scholastics", "inactive"),
	("2023-09947", "org", "1", "2023-2024", 2023, default, "scholastics", "inactive"),
	("2020-03349", "org", "1", "2022-2023", 2022, default, "secretariat", "inactive"),
	("2020-01149", "org", "1", "2022-2023", 2021, "head", "secretariat", default),
	("2024-01420", "org", "2", "2024-2025", 2024, default, "scholastics", default),
	("2024-01430", "gets", "1", "2024-2025", 2024, default, "secretariat", default),
	("2024-01420", "gets", "1", "2024-2025", 2024, default, "secretariat", default);


insert into fee(fee_name, amount, due_date, fee_sem, fee_acad_year, org_name) values
	("Membership Fee", 100, str_to_date('17-FEB-2021','%d-%M-%Y'), "1", "2022-2023", "org"),
	("Membership Fee", 150, str_to_date('12-FEB-2021','%d-%M-%Y'), "1", "2024-2025", "gets");


insert into member_pays_fee values
	("2023-04240", 1, default,null ),
	("2017-04147", 1, default,null ),
	("2018-04341", 1, "P",str_to_date('17-JAN-2022','%d-%M-%Y') ),
	("2021-19142", 1, "P",str_to_date('12-JAN-2022','%d-%M-%Y') ),
	("2023-09947", 1, "P",str_to_date('13-JAN-2022','%d-%M-%Y') ),
	("2020-03349", 1, "P",str_to_date('17-FEB-2022','%d-%M-%Y') ),
	("2020-01149", 1, "P",str_to_date('17-FEB-2022','%d-%M-%Y') ),
	("2024-01430", 1, default,null ),
	("2024-01430", 2, default,null ),
	("2024-01420", 2, default,null );


-- SAMPLE QUERIES
-- 1 working
select role, status, gender, degree_program, batch, committee_name from member natural join organization_has_member where org_name = "org";


-- 2 members for a given organization with unpaid membership fees or dues for a given semester and acad year
SELECT
    m.std_num,
    CONCAT(m.f_name, ' ', COALESCE(m.m_name, ''), ' ', m.l_name) AS full_name,
    m.degree_program,
    m.debt AS unpaid_fees,
    o.org_name,
    o.mem_sem AS semester,
    o.mem_acad_year AS academic_year,
    o.role,
    o.committee_name
FROM 
    member m
JOIN 
    organization_has_member o ON m.std_num = o.std_num
WHERE 
    o.org_name = 'org'                  -- which org
    AND o.mem_sem = 2                   -- which sem
    AND o.mem_acad_year = '2023-2024'   -- specify which year
    AND m.debt > 0


-- 3 working
select fee_name, amount, org_name, due_date from 
fee natural join (member natural join member_pays_fee) 
where std_num = "2024-01430" and status = "NP" order by due_date desc;


-- 4 View all executive members of a given organization for a given academic year.
select
    o.org_name,
	m.f_name, 
	m.l_name,
	o.std_num,
    o.role,
	o.mem_acad_year
from 
	member m
join 
	organization_has_member o on m.std_num = o.std_num
where 
	committee_name = "executive"
	AND o.mem_acad_year = "2018-2019"
    AND o.org_name = "org";


-- 5 working
select f_name as "First Name", committee_name, mem_acad_year as "Academic Year" 
from  member natural join organization_has_member Where role = "head" && committee_name = "executive" && org_name = "org"  
Order by CAST(substring(mem_acad_year, 1, 4) AS int) desc;


-- 6 View all late payments made by all members of a given organization for a given semester and academic year.
SELECT 
    m.std_num,
    CONCAT(m.f_name, ' ', m.l_name) AS member_name,
    f.fee_name,
    f.fee_acad_year,
    f.amount AS fee_amount,
    f.due_date,
    mpf.paid_date,
    DATEDIFF(f.due_date, mpf.paid_date) AS days_late
FROM 
    member_pays_fee mpf
JOIN 
    fee f ON mpf.fee_id = f.fee_id
JOIN 
    member m ON mpf.std_num = m.std_num
WHERE 
    f.org_name = 'org'
    AND f.fee_sem = 1                  
    AND f.fee_acad_year = '2022-2023'  
    AND mpf.status = 'P'               
    AND mpf.paid_date > f.due_date     
ORDER BY 
    days_late DESC;


-- 7
select status, Concat(count(status)/(select count(*) from organization_has_member where org_name = "org"  && status not in ("alumni") && mem_sem = (select case 
when 5%2=0 then "1" when 5%2=1 then "2" end as "semester") && 
CAST(substring(mem_acad_year, 1, 4) AS int) between (select round(max(CAST(substring(mem_acad_year, 1, 4) AS int)) - 5/2) 
from organization_has_member) and (select max(CAST(substring(mem_acad_year, 1, 4) AS int)) from organization_has_member)), "%") 
as percentage from organization_has_member where org_name = "org" && status not in ("alumni") &&
mem_sem = (select case when 5%2=0 then "1" when 5%2=1 then "2" end as "semester") && CAST(substring(mem_acad_year, 1, 4) AS int) between 
(select round(max(CAST(substring(mem_acad_year, 1, 4) AS int))- 5/2) from organization_has_member)  and (select max(CAST(substring(mem_acad_year, 1, 4) AS int)) from organization_has_member) 
group by status;


-- 8 View all alumni members of a given organization as of a given date.
SELECT 
    m.std_num,
    CONCAT(m.f_name, ' ', m.l_name) AS alumni_name,
    m.degree_program,
    o.org_name,
    o.mem_acad_year AS last_active_year,
    o.mem_sem AS last_active_semester,
    o.role AS last_role,
    o.committee_name AS last_committee
FROM 
    member m
JOIN 
    organization_has_member o ON m.std_num = o.std_num
WHERE 
    o.org_name = 'org'  
    AND o.status = 'alumni'
    AND DATE(CONCAT(SUBSTRING(o.mem_acad_year, 1, 4), '-08-01')) <= '2024-12-31' -- parameter date;
ORDER BY 
    o.mem_acad_year DESC,
    o.mem_sem DESC;


-- 9 View total amount of unpaid and paid fees or dues of an organization as of a given date.
SELECT 
    f.org_name,
    SUM(CASE WHEN mpf.status = 'P' AND mpf.paid_date <= '2024-12-31' THEN f.amount ELSE 0 END) AS total_paid,
    SUM(CASE WHEN (mpf.status = 'NP' OR mpf.paid_date > '2024-12-31') THEN f.amount ELSE 0 END) AS total_unpaid,
    COUNT(CASE WHEN mpf.status = 'P' AND mpf.paid_date <= '2024-12-31' THEN 1 END) AS paid_count,
    COUNT(CASE WHEN (mpf.status = 'NP' OR mpf.paid_date > '2024-12-31') THEN 1 END) AS unpaid_count
FROM 
    fee f
LEFT JOIN 
    member_pays_fee mpf ON f.fee_id = mpf.fee_id
WHERE 
    f.org_name = 'org' OR f.org_name = 'gets'  
GROUP BY 
    f.org_name;


-- 10 View the member/s with the highest debt of a given organization for a given semester.
SELECT 
    m.std_num,
    CONCAT(m.f_name, ' ', m.l_name) AS member_name,
    m.debt AS highest_debt,
    o.org_name,
    o.mem_sem AS semester,
    o.mem_acad_year AS academic_year,
    o.status
FROM 
    member m
JOIN 
    organization_has_member o ON m.std_num = o.std_num
WHERE 
    o.org_name = 'org'              
    AND o.mem_sem = 1
    AND o.mem_acad_year = '2023-2024' 
    AND m.debt = (
        SELECT MAX(m2.debt)
        FROM member m2
        JOIN organization_has_member o2 ON m2.std_num = o2.std_num
        WHERE o2.org_name = o.org_name
          AND o2.mem_sem = o.mem_sem
          AND o2.mem_acad_year = o.mem_acad_year
    )
ORDER BY 
    m.l_name, m.f_name;