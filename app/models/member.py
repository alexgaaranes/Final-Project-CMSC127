from app.db import get_cursor

def get_member_from_org(org_name):
    cursor = get_cursor()
    cursor.execute(
        """
        SELECT
            std_num,
            role, 
            status, 
            gender, 
            degree_program, 
            committee_name 
        FROM member 
        NATURAL JOIN organization_has_member 
        WHERE org_name = %s
        AND status = "active";
        """, (org_name, )
    )
    return cursor.fetchall()