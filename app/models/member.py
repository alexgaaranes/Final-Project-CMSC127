from app.db import get_cursor, get_conn


def get_member_from_org(org_name, sem = "all", committee = "all", status = "all", batch = "all", std_num = None, role = "all", start = None, end = None):

    cursor = get_cursor()
    
    # array of filters
    filters = []
    
    # by default have this in there 
    filters.append(' WHERE org_name = "'+org_name+'"')
    

    query = "SELECT std_num, l_name, f_name, m_name, batch, role, status, gender, degree_program, committee_name FROM member NATURAL JOIN organization_has_member "   
    
    
    if sem != "all" and sem is not None:
        filters.append('AND mem_sem = "'+sem+'"')
    
    if committee != "all" and committee is not None:
        filters.append('AND committee_name = "'+committee+'"')
    
    # active, inactive, alumni
    if status != "all" and status is not None:
        filters.append('AND status = "'+status+'"')

    # year number
    if batch != "all" and batch is not None:
        filters.append('AND batch = '+batch)

    
    if role != "all" and role is not None:
        filters.append('AND role = "'+role+'"')


    if std_num is not None:
        filters.append('AND std_num = "'+std_num+'"')
    
    # should place YEAR  
    if start is not None and end is not None:
        filters.append('AND (CAST(substring(mem_acad_year, 1, 4) AS int)) BETWEEN '+start+' AND '+end)
    
    # joining of all filters togther
    query += "".join(filters) 
    query += ";"
    
    print(query)
    cursor.execute(
        query
    )

    return cursor.fetchall()


# Login member
def login_member(mem_username, mem_password):

    cursor = get_cursor()
    cursor.execute(
        """
        SELECT *
        FROM member
        WHERE std_num = %s
        AND mem_password = %s;
        """, (mem_username, mem_password)
    )
    return cursor.fetchone()


# Login member
def delete_member(org_name, std_num):

    cursor = get_cursor()
    cursor.execute(
        """
        DELETE 
        FROM organization_has_member
        WHERE std_num = %s AND
        org_name = %s;
        """, (std_num, org_name)
    )
    get_conn().commit()


# register a new student member
def add_member(std_num, mem_password, degree_program, gender, f_name, l_name, m_name):
    cursor = get_cursor()
    cursor.execute(
        """
        INSERT INTO member(std_num, mem_password, degree_program, gender, f_name, l_name, m_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (std_num, mem_password, degree_program, gender, f_name, l_name, m_name,)
    )
    cursor.execute(
    """
    SELECT *
    FROM member 
    """

    )
    print(cursor.fetchall())
    get_conn().commit()

# assign a member to the organization
def add_org_member(std_num, org_name, mem_sem, mem_acad_year, batch, role, committee_name, status):
    cursor = get_cursor()
    
    print(std_num)
    cursor.execute("SELECT std_num FROM member WHERE std_num = %s", (std_num,))
    if len(cursor.fetchall()) == 0:       
        return "no student number found"
    
    
    cursor.execute(
            """
            INSERT INTO 
                organization_has_member 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (std_num, org_name, mem_sem, mem_acad_year, batch, role, committee_name, status)
        )
        
    cursor.execute(
    """
    SELECT *
    FROM organization_has_member  
    """
    )
    
    print(cursor.fetchall())
    get_conn().commit()


#view member's organizations
def get_member_org(std_num):
    cursor = get_cursor()
    
    cursor.execute("""

        SELECT m.std_num, m.org_name, m.mem_sem, m.mem_acad_year, m.role, m.committee_name, m.status
        FROM organization o join organization_has_member m on o.org_name = m.org_name
        WHERE m.std_num = %s;
    """, (std_num, ))


    return cursor.fetchall()


#view member's fees
def get_member_fee(std_num):
    cursor = get_cursor()
    
    cursor.execute("""

        SELECT std_num, m.fee_id, fee_name, amount, due_date, paid_date, fee_sem, fee_acad_year, org_name, status
        FROM member_pays_fee m join fee f ON m.fee_id = f.fee_id
        WHERE std_num = %s;
                   
    """, (std_num, ))

    return cursor.fetchall()

