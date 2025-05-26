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


# register a new org
def add_member(org_name, org_account, org_password, date_formed):
    cursor = get_cursor()
    cursor.execute(
        """
        INSERT INTO 
            organization (org_name, org_account, org_password, date_formed)
        VALUES (%s, %s, %s, %s);
        """, (org_name, org_account, org_password, date_formed)
    )
    cursor.execute(
    """
    SELECT *
    FROM organization 
    """
    )
    print(cursor.fetchall())
    get_conn().commit()
