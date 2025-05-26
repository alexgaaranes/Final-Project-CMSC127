from app.db import get_cursor, get_conn

def get_member_from_org(org_name, committee = None, status = None, batch = None, gender = None, role = None, start = None, end = None):
    cursor = get_cursor()
    
    # array of filters
    filters = []
    
    # by default have this in there 
    filters.append(' WHERE org_name = "'+org_name+'"')
    
    # long ass query
    query = "SELECT std_num, l_name, f_name, m_name, batch, role, status, gender, degree_program, committee_name FROM member NATURAL JOIN (organization_has_member NATURAL JOIN mem_org_batch) "   
    
    if committee is not None:
        filters.append('AND committee_name = "'+committee+'"')
    
    # active, inactive, alumni
    if status is not None:
        filters.append('AND status = "'+status+'"')

    # year number
    if batch is not None:
        filters.append('AND batch = '+batch)
    
    if role is not None:
        filters.append('AND role = "'+role+'"')
        
    # M or F pero ? ung rn
    if gender is not None:
        filters.append('AND gender = "'+gender+'"')
    
    # should place YEAR  
    if start is not None and end is not None:
        filters.append('AND (CAST(substring(mem_acad_year, 1, 4) AS int)) BETWEEN'+start+' AND '+end)
    
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
        WHERE mem_username = %s
        AND mem_password = %s;
        """, (mem_username, mem_password)
    )
    return cursor.fetchone()


# register a new student member
def register_org(std_num, mem_username, mem_password, degree_program, gender, f_name, l_name, m_name):
    cursor = get_cursor()
    cursor.execute(
        """
        INSERT INTO member(mem_username, mem_password, degree_program, gender, f_name, l_name, m_name)
        VALUES (%s, %s, %s, %s);
        """, (std_num, mem_username, mem_password, degree_program, gender, f_name, l_name, m_name,)
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
    
    cursor.execute("select std_num from organization_has_member where std_num = 2024-01345")
    if len(cursor.fetchall()) == 0:       
        return "no student number found"
    
    
    cursor.execute(
            """
            INSERT INTO 
                organization_has_member 
            VALUES (%s, %s, %s, %s, %s, %s);
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

