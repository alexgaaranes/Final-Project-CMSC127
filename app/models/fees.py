from app.db import get_cursor

def get_all_fees(org_name, year = None, sem = None):
    cursor = get_cursor()
    
    # array of filters
    filters = []
    
    # by default have this in there 
    filters.append(' WHERE org_name = "'+org_name+'"')
    
    # long ass query
    query = "SELECT fee_id,fee_name, amount, due_date, fee_sem, fee_acad_year FROM fee NATURAL JOIN organization "   
    
    if year is not None:
        filters.append('AND fee_acad_year = '+year)
    
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

    
