import mysql.connector

_conn = None
_cursor = None

def initialize_db(config):
    global _conn, _cursor
    _conn = mysql.connector.connect(
        host=config['HOST'],
        user=config['USER'],
        password=config['PASSWORD'],
        database=config['DB_NAME']
    )
    _cursor = _conn.cursor(dictionary=True)

    # Table Creation
    _cursor.execute("""
    CREATE TABLE IF NOT EXISTS organization(
        org_name VARCHAR(50) UNIQUE NOT NULL,
        org_account VARCHAR(20) UNIQUE NOT NULL,
        org_password VARCHAR(30) NOT NULL, 
        date_formed DATE NOT NULL,
        org_funds INT(10) DEFAULT 0,
        PRIMARY KEY(org_name)
    )
    """)

    _cursor.execute("""
    CREATE TABLE IF NOT EXISTS member(
        std_num CHAR(10),
        mem_password VARCHAR(30),
        degree_program VARCHAR(50) NOT NULL,
        gender VARCHAR(10),
        debt INT(8) DEFAULT 0, 
        f_name VARCHAR(50) NOT NULL,
        l_name VARCHAR(50),
        m_name VARCHAR(50),
        PRIMARY KEY(std_num),
        CONSTRAINT std_num_ck CHECK(std_num LIKE '____-_____'), 
        CONSTRAINT debt_ck CHECK(debt >= 0)
    )
    """)

    _cursor.execute("""
    CREATE TABLE IF NOT EXISTS fee(
        fee_id INT(3) AUTO_INCREMENT,
        fee_name VARCHAR(50),
        amount INT(5) NOT NULL,
        due_date DATE NOT NULL,
        fee_sem VARCHAR(1),
        fee_acad_year CHAR(9),
        org_name VARCHAR(50),
        PRIMARY KEY(fee_id),
        CONSTRAINT fee_org_name_fk FOREIGN KEY(org_name)
            REFERENCES organization(org_name),
        CONSTRAINT fee_acad_year_ck CHECK(fee_acad_year LIKE '____-____'),
        CONSTRAINT fee_sem_ck CHECK(fee_sem IN ('1', '2')),
        CONSTRAINT valid_fee_year_ck CHECK((CAST(SUBSTRING(fee_acad_year, 1, 4) AS SIGNED)+1) = (CAST(SUBSTRING(fee_acad_year, 6) AS SIGNED)))
    )
    """)

    _cursor.execute("""
    CREATE TABLE IF NOT EXISTS organization_has_member(
        std_num CHAR(10),
        org_name VARCHAR(50),
        mem_sem VARCHAR(1),
        mem_acad_year CHAR(9),
        batch INT(4) NOT NULL,
        role VARCHAR(20) DEFAULT "regular member",
        committee_name VARCHAR(50),
        status VARCHAR(15) DEFAULT "active",
        PRIMARY KEY(std_num, org_name, mem_sem, mem_acad_year),
        CONSTRAINT org_has_mem_std_num_fk FOREIGN KEY(std_num)
            REFERENCES member(std_num),
        CONSTRAINT org_has_mem_org_name_fk FOREIGN KEY(org_name)
            REFERENCES organization(org_name),
        CONSTRAINT std_num_ck CHECK(std_num LIKE '____-_____'),
        CONSTRAINT mem_acad_year_ck CHECK(mem_acad_year LIKE '____-____'),
        CONSTRAINT mem_sem_ck CHECK(mem_sem IN ('1', '2')),
        CONSTRAINT mem_year_stdnum_ck CHECK((CAST(SUBSTRING(mem_acad_year, 1, 4) AS SIGNED)+1)  >= (CAST(SUBSTRING(std_num, 1, 4) AS SIGNED))),
        CONSTRAINT valid_acad_year_ck CHECK((CAST(SUBSTRING(mem_acad_year, 1, 4) AS SIGNED)+1) = (CAST(SUBSTRING(mem_acad_year, 6) AS SIGNED))),
        CONSTRAINT member_status_ck CHECK(status IN ('active', 'inactive', 'alumni'))
    )
    """)

    _cursor.execute("""
    CREATE TABLE IF NOT EXISTS member_pays_fee(
        std_num CHAR(10),
        fee_id INT(3),
        status VARCHAR(2) DEFAULT "NP",
        paid_date DATE,
        PRIMARY KEY(std_num, fee_id),
        CONSTRAINT member_pays_fee_fee_id_fk FOREIGN KEY(fee_id)
            REFERENCES fee(fee_id),
        CONSTRAINT member_pays_fee_std_num_fk FOREIGN KEY(std_num)
            REFERENCES member(std_num),
        CONSTRAINT std_num_ck CHECK(std_num LIKE '____-_____'),
        CONSTRAINT status_ck CHECK(status IN ('P', 'NP')),
        CONSTRAINT fee_id_ck CHECK(fee_id > 0)
    )
    """)

    _conn.commit()

def get_conn():
    return _conn

def get_cursor():
    return _cursor
