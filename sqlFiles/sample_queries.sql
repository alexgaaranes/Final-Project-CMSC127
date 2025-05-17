-- Add an organization
INSERT INTO organization (org_name, org_account, org_password, date_formed, org_funds)
VALUES(
    "MyOrg", 
    "myorg@email.org", 
    "secretPW123", 
    str_to_date('16-FEB-1998','%d-%M-%Y'),
    1000
);

-- Add a member and bind to an organization
INSERT INTO member (std_num, mem_username, mem_password, degree_program, batch, gender, debt, f_name, l_name, m_name)
VALUES(
    "1996-74832",
    "myUsername123",
    "myPassword123",
    "BS Computer Science",
    1999,
    "Male",
    0,
    "John",
    "Geronimo",
    "Elundad"
);

INSERT INTO organization_has_member (std_num, org_name, mem_sem, mem_acad_year, committee_name)
VALUES(
    "1996-74832",
    "MyOrg",
    "2",
    "1999-10-24",
    "Finance"
);

-- Add a fee and impose to all org members
INSERT INTO fee (fee_id, fee_name, amount, due_date, fee_sem, fee_acad_year, org_name)
VALUES (
    "Membership Fee",
    500,
    "1999-12-12",
    "1",
    "1999-08-30",
    "MyOrg"
);

INSERT INTO member_pays_fee (std_num, fee_id)
SELECT std_num, fee_id
FROM organization_has_member o, fee f
WHERE o.org_name = "MyOrg" AND f.fee_id = 1;

-- update to inactive
