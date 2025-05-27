from app.db import get_cursor, get_conn

def get_all_fees(org_name, sem = "all", start= None, end = None):
    cursor = get_cursor()
    
    # array of filters
    filters = []
    
    # by default have this in there 
    filters.append(' WHERE org_name = "'+org_name+'"')
    
    # long ass query
    query = "SELECT fee_id, fee_name, amount, due_date, fee_sem, fee_acad_year FROM fee "   
    
    if sem != "all" and sem is not None:
        filters.append('AND fee_sem = "'+sem+'"')
    
    
    if start is not None and end is not None:
        filters.append('AND (CAST(substring(fee_acad_year, 1, 4) AS int)) BETWEEN '+start+' AND '+end)
    

    
    # adding the filters together
    query += "".join(filters) 
    query += ";"
    
    print(query)
    cursor.execute(
        query
    )
    return cursor.fetchall()

# get total unpaid
def get_total_unpaid(org_name, as_of_date):
    cursor = get_cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(f.amount), 0) AS total_unpaid
        FROM member_pays_fee m
        JOIN fee f ON m.fee_id = f.fee_id
        WHERE f.org_name = %s
            AND m.status = 'NP'
            AND f.due_date <= %s
        """,
        (org_name, as_of_date)
    )
    result = cursor.fetchone()
    return result if result else 0

# get total paid
def get_total_paid(org_name, as_of_date):
    cursor = get_cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(f.amount), 0) AS total_paid
        FROM member_pays_fee m
        JOIN fee f ON m.fee_id = f.fee_id
        WHERE f.org_name = %s
            AND m.status = 'P'
            AND m.paid_date <= %s
        """,
        (org_name, as_of_date)
    )
    result = cursor.fetchone()
    return result if result else 0

# get unpaid members on given sem adn acad year
def get_unpaid_members(org_name, sem, acad_year):
    cursor = get_cursor()
    
    cursor.execute(
        """
        SELECT m.std_num, m.fee_id, CONCAT(mem.f_name, ' ', mem.l_name) name, f.amount, f.due_date
        FROM member_pays_fee m
        JOIN fee f ON m.fee_id = f.fee_id
        JOIN member mem ON m.std_num = mem.std_num
        WHERE f.org_name = %s
            AND f.fee_sem = %s
            AND f.fee_acad_year = %s
            AND m.status = 'NP';
        """,
        (org_name, sem, acad_year)
    )
    
    return cursor.fetchall()

# get late payers on given sem and acad year
def get_late_payers(org_name, sem, acad_year):
    cursor = get_cursor()
    
    cursor.execute(
        """
        SELECT m.std_num, m.fee_id, CONCAT(mem.f_name, ' ', mem.l_name) name, f.amount, m.paid_date
        FROM member_pays_fee m
        JOIN fee f ON m.fee_id = f.fee_id
        JOIN member mem ON m.std_num = mem.std_num
        WHERE f.org_name = %s
            AND f.fee_sem = %s
            AND f.fee_acad_year = %s
            AND m.status = 'P'
            AND m.paid_date > f.due_date;
        """,
        (org_name, sem, acad_year)
    )
    
    return cursor.fetchall()

# get highest debt members on given sem and acad year
def get_highest_debt_members(org_name, sem, acad_year):
    cursor = get_cursor()
    
    cursor.execute(
        """
        SELECT m.std_num, m.fee_id, CONCAT(mem.f_name, ' ', mem.l_name) name, SUM(f.amount) AS total_debt
        FROM member_pays_fee m
        JOIN fee f ON m.fee_id = f.fee_id
        JOIN member mem ON m.std_num = mem.std_num
        WHERE f.org_name = %s
            AND f.fee_sem = %s
            AND f.fee_acad_year = %s
            AND m.status = 'NP'
        GROUP BY m.std_num
        """,
        (org_name, sem, acad_year)
    )
    
    return cursor.fetchall()

# add a new fee
def add_org_fee(fee_name, amount, due_date, fee_sem, fee_acad_year, org_name):
    cursor = get_cursor()
    
    cursor.execute(
        """
        INSERT INTO 
            fee (fee_name, amount, due_date, fee_sem, fee_acad_year, org_name)
        VALUES (%s, %s, %s, %s, %s, %s);
        """, (fee_name, amount, due_date, fee_sem, fee_acad_year, org_name)
    )
    
    cursor.execute(
    """
    SELECT *
    FROM fee  
    """
    )
    
    print(cursor.fetchall())
    get_conn().commit()
