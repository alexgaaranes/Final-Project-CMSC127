-- 1
select role, status, gender, degree_program, batch, committee_name from member natural join organization_has_member;

-- 3
select fee_name, amount, org_name, due_date from 
fee natural join (member natural join member_pays_fee) 
where std_num = "2024-0143" and status = "NP" order by due_date desc;

-- 5
select f_name as "First Name", committee_name, year(mem_acad_year) as "Academic Year" 
from  member natural join organization_has_member Where role = "head" && committee_name = "executive"  Order by `Academic Year` desc;

-- 7 Assumed that 1st and 2nd semester are each equal to 6 months
select status, Concat(count(status)/(select count(status) from organization_has_member where org_name = "org") * 100, "%") 
as percentage from organization_has_member where org_name = "org" && mem_acad_year between (select adddate(curdate(), interval -6*10 month)) and curdate()  
group by status;