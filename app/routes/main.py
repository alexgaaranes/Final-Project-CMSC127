from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import org, member
from datetime import date

main_bp = Blueprint('main', __name__)

# Logout route
@main_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('org', None)
    session.pop('member', None)
    return redirect(url_for('main.index'))

# Login GET Routes
@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/orglogin', methods=['GET'])
def org_login():
    if 'org' in session:
        return redirect(url_for('main.org_home'))
    return render_template('org_login.html')

@main_bp.route('/memlogin', methods=['GET'])
def mem_login():
    if 'member' in session:
        return redirect(url_for('main.mem_home'))
    return render_template('mem_login.html')


@main_bp.route('/memregister', methods=['GET'])
def mem_register():
    if 'member' in session:
        return redirect(url_for('main.mem_home'))
    return render_template('mem_register.html')

@main_bp.route('/registerorg', methods=['GET'])
def org_register():
    if 'org' in session:
        return redirect(url_for('main.org_home'))
    return render_template('org_register.html')

# Login POST Routes
@main_bp.route('/orglogin', methods=['POST'])
def org_login_post():
    org_account = request.form.get('email')
    password = request.form.get('password')
    # Validate org credentials
    try:
        org_deets =  org.login_org(org_account, password)
        print(org_deets)
        if (org_deets is None):
            raise ValueError("Invalid Credentials")
        session['org'] = org_deets
    except Exception as e:
        return render_template('org_login.html', error=str(e))
    return redirect(url_for('main.org_home'))

@main_bp.route('/memlogin', methods=['POST'])
def mem_login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    # Validate member credentials
    try:
        mem_deets = member.login_member(username, password)
        if (mem_deets is None):
            raise ValueError("Invalid Credentials")
        session['member'] = mem_deets
    except Exception as e:
        return render_template('mem_login.html', error=str(e))
    return redirect(url_for('main.mem_home'))

# Register POST Routes
@main_bp.route('/registerorg', methods=['POST'])
def org_register_post():
    org_name = request.form.get('name')
    org_account = request.form.get('email')
    org_password = request.form.get('password')
    date_formed = request.form.get('date_formed')
    # Register new org
    try:
        org.register_org(org_name, org_account, org_password, date_formed)
    except Exception as e:
        err_code = int(str(e).split(' ')[0])
        err_msg = None
        match err_code:
            case 1062:
                err_msg = "Organization name or account already exists."
            case _:
                err_msg = "An error occurred."
        return render_template('org_register.html', error=err_msg)
    return render_template('org_login.html', success="Organization registered successfully!")

@main_bp.route('/registermember', methods=['POST'])
def member_register_post():
    std_num = request.form.get('std_num')
    mem_password = request.form.get('password')
    degree_program = request.form.get('degree_program')
    gender = request.form.get('sex')
    f_name = request.form.get('first')
    l_name = request.form.get('last')
    m_name = request.form.get('middle')

    try:
        member.add_member(std_num, mem_password, degree_program, gender, f_name, l_name, m_name)
    except Exception as e:
        print(e)
        err_code = int(str(e).split(' ')[0])
        err_msg = None
        match err_code:
            case 1062:
                err_msg = "Organization name or account already exists."
            case 4025:
                err_msg = "Please follow the specified format for student number"
            case _:
                err_msg = "An error occurred."
        return render_template('mem_register.html', error=err_msg)
    return render_template('mem_login.html', success="Account registered successfully!")

# Org routes
@main_bp.route('/org/home', methods=['GET'])
def org_home():
    if 'org' not in session:
        return redirect(url_for('main.org_login'))
    org_deets = session['org']
    return render_template('org/org_dashboard.html', org=org_deets)

@main_bp.route('/org/members', methods=['GET', 'POST'])
def org_members():
    if 'org' not in session:
        return redirect(url_for('main.org_login'))
    org_deets = session['org']
    org_name = org_deets['org_name']
    coms = org.get_all_org_committees(org_name)
    
    
    role = request.form.get('role')
    sem = request.form.get('sem')
    # year = request.form.get('year') if request.form.get('year') != "all" else None
    status = request.form.get('status') 
    committee = request.form.get('committee')
    
    print(committee)
    
    if role is None:
        filter = ["all", "all", "all", "all"]
    else:
        filter = [role, sem, status, committee]
        
    members = member.get_member_from_org(org_name, role=role, status=status, sem=sem)
    return render_template('org/org_members.html', org=org_deets, members=members, filter=filter, coms = coms)


# Mem routes
@main_bp.route('/mem/home', methods=['GET'])
def mem_home():
    if 'member' not in session:
        return redirect(url_for('main.mem_login'))
    mem_deets = session['member']

    return render_template('mem/mem_dashboard.html', member=mem_deets)


@main_bp.route('/mem/orgs', methods=['GET'])
def mem_orgs():
    if 'member' not in session:
        return redirect(url_for('main.mem_login'))
    mem_deets = session['member']
    std_num = mem_deets['std_num']
    result = member.get_member_org(std_num)
    return render_template('mem/mem_orgs.html', member=mem_deets, orgs=result)

@main_bp.route('/mem/fees', methods=['GET'])
def mem_fees():
    if 'member' not in session:
        return redirect(url_for('main.mem_login'))
    mem_deets = session['member']
    std_num = mem_deets['std_num']
    result = member.get_member_fee(std_num)
    print(result)
    return render_template('mem/mem_fees.html', member=mem_deets, fees=result)

# Org add member post req
@main_bp.route('/org/add_member', methods=['POST'])
def org_add_mem():
    # Insert Query
    org_deets = session['org']
    member_data = request.form

    print(member_data)
    # Details for organization_has_member tuple
    org_name = org_deets['org_name']
    std_num = member_data['std-num'] 
    role = member_data['role']
    sem = member_data['sem']
    ay = member_data['ay']
    status = member_data['status']
    batch = member_data['batch']
    committee = member_data['committee']

    result = member.add_org_member(std_num, org_name, sem, ay, batch, role, committee, status)    
    print(result)

    return redirect(url_for('main.org_members'))