from app.db import get_conn, get_cursor
from datetime import date

# register a new org
def register_org(org_name, org_account, org_password, date_formed):
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

# login org based on account and password
def login_org(org_account, org_password):
    cursor = get_cursor()
    cursor.execute(
        """
        SELECT org_name, org_account, org_password, date_formed, org_funds
        FROM organization 
        WHERE org_account = %s 
        AND org_password = %s;
        """, (org_account, org_password)
    )
    return cursor.fetchone()
