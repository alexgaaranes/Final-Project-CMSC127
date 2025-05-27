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

# gets number of members depending on status
def get_member_count(org_name, status):
    cursor = get_cursor()
    cursor.execute(
        """
        SELECT
           count(*) AS "mem_count"
        FROM member 
        NATURAL JOIN organization_has_member 
        WHERE org_name = %s
        AND status = %s;
        """, (org_name, status)
    )
    return cursor.fetchall()

# will be used for filtering probably???
def get_all_org_committees(org_name, ):
    cursor = get_cursor()
    cursor.execute(
        """
        SELECT DISTINCT
          committee_name
        FROM member 
        NATURAL JOIN organization_has_member 
        WHERE org_name = %s
        """, (org_name, )
    )
    return cursor.fetchall()
