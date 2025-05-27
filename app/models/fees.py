from app.db import get_cursor, get_conn

def get_all_fees(org_name, sem = None, start= None, end = None):
    cursor = get_cursor()
    
    # array of filters
    filters = []
    
    # by default have this in there 
    filters.append(' WHERE org_name = "'+org_name+'"')
    
    # long ass query
    query = "SELECT fee_id, fee_name, amount, due_date, fee_sem, fee_acad_year FROM fee "   
    
    if start is not None and end is not None:
        filters.append('AND (CAST(substring(fee_acad_year, 1, 4) AS int)) BETWEEN '+start+' AND '+end)
    
    if sem is not None:
        filters.append('AND fee_sem = '+sem)
    
    # adding the filters together
    query += "".join(filters) 
    query += ";"
    
    print(query)
    cursor.execute(
        query
    )
    return cursor.fetchall()

# add a new fee
def add_org_fee(fee_name, amount, due_date, fee_sem, fee_acad_year, org_name):
    cursor = get_cursor()
    
    cursor.execute(
        """
        INSERT INTO 
            member (fee_name, amount, due_date, fee_sem, fee_acad_year, org_name)
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
