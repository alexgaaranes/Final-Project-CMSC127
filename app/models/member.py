from app.db import get_cursor

def get_member_from_org(org_name):
    cursor = get_cursor()
    cursor.execute(
        """
        SELECT
            std_num,
            l_name,
            f_name,
            m_name,
            batch,
            role, 
            status, 
            gender, 
            degree_program, 
            committee_name 
        FROM member 
        NATURAL JOIN organization_has_member 
        WHERE org_name = %s;
        """, (org_name, )
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