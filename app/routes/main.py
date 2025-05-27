from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import org, member, fees

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

@main_bp.route('/org/members', methods=['GET'])
def org_members():
    if 'org' not in session:
        return redirect(url_for('main.org_login'))
    org_deets = session['org']
    org_name = org_deets['org_name']
    members = member.get_member_from_org(org_name)
    return render_template('org/org_members.html', org=org_deets, members=members)

@main_bp.route('/org/funds', methods=['GET'])
def org_funds():
    if 'org' not in session:
        return redirect(url_for('main.org_login'))
    org_deets = session['org']
    org_name = org_deets['org_name']
    return render_template('org/org_funds.html', org=org_deets)



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
    org_name = org_deets['org_name']
    std_num = member_data['std-num'] 
    role = member_data['role']
    sem = member_data['sem']
    ay = member_data['ay_start'] + '-' + member_data['ay_end']
    status = member_data['status']
    batch = member_data['batch']
    committee = member_data['committee']

    result = member.add_org_member(std_num, org_name, sem, ay, batch, role, committee, status)    
    print(result)

    return redirect(url_for('main.org_members'))

# Org add fee post req
@main_bp.route('/org/add_fee', methods=['POST'])
def org_add_fee():
    # Insert Query
    org_deets = session['org']
    fee_data = request.form

    org_name = org_deets['org_name']
    fee_name = fee_data['fee_name']
    amount = fee_data['fee_amount']
    due_date = fee_data['fee_due_date']
    sem = fee_data['fee_semester']
    ay = fee_data['fee_year_start'] + '-' + fee_data['fee_year_end']

    result = fees.add_org_fee(fee_name, amount, due_date, sem, ay, org_name)

    return redirect(url_for('main.org_funds'))

# Org total unpaid and paid as of date
@main_bp.route('/org/total_as_of', methods=['GET'])
def org_total_as_of():
    if 'org' not in session:
        return redirect(url_for('main.org_login'))
    org_deets = session['org']
    org_name = org_deets['org_name']
    as_of_date = request.args.get('as_of_date')
    total_unpaid = fees.get_total_unpaid(org_name, as_of_date)['total_unpaid']
    total_paid = fees.get_total_paid(org_name, as_of_date)['total_paid']

    return render_template('org/org_funds.html', org=org_deets, total_unpaid=total_unpaid, total_paid=total_paid)

# ORg unpaid members
@main_bp.route('/org/unpaid_mems', methods=['GET'])
def org_unpaid_mems():
    if 'org' not in session:
        return redirect(url_for('main.org_login'))
    org_deets = session['org']
    org_name = org_deets['org_name']
    sem = request.args.get('unpaid_semester')
    ay = request.args.get('unpaid_year_start') + '-' + request.args.get('unpaid_year_end')

    unpaid_members = fees.get_unpaid_members(org_name, sem, ay)
    return render_template('org/org_funds.html', org=org_deets, unpaid_members=unpaid_members)

# org late payments
@main_bp.route('/org/late_payments', methods=['GET'])
def org_late_payments():
    if 'org' not in session:
        return redirect(url_for('main.org_login'))
    org_deets = session['org']
    org_name = org_deets['org_name']
    sem = request.args.get('late_semester')
    ay = request.args.get('late_year_start') + '-' + request.args.get('late_year_end')
    late_payments = fees.get_late_payers(org_name, sem, ay)

    return render_template('org/org_funds.html', org=org_deets, late_payments=late_payments)

# org mem with highest debt
@main_bp.route('/org/highest_debt_mems', methods=['GET'])
def org_highest_debt_mems():
    if 'org' not in session:
        return redirect(url_for('main.org_login'))
    org_deets = session['org']
    org_name = org_deets['org_name']
    sem = request.args.get('debt_semester')
    ay = request.args.get('debt_year_start') + '-' + request.args.get('debt_year_end')
    highest_debt_mems = fees.get_highest_debt_members(org_name, sem, ay)

    return render_template('org/org_funds.html', org=org_deets, debt_members=highest_debt_mems)

# Edit member in org
@main_bp.route('/org/edit_member', methods=['POST'])
def org_edit_member():
    if 'org' not in session:
        return redirect(url_for('main.org_login'))
    org_deets = session['org']
    org_name = org_deets['org_name']
    member_id = request.form.get('member_id')
    role = request.form.get('edit_role')
    status = request.form.get('edit_status')
    committee = request.form.get('committee')
    sem = request.form.get('edit_sem')
    year_start = request.form.get('edit_ay_start')
    year_end = request.form.get('edit_ay_end')
    ay = f"{year_start}-{year_end}" # format 

    print(member_id, org_name, sem, ay, role, committee, status)

    member.edit_org_member(member_id, org_name, sem, ay, role, committee, status)
    return redirect(url_for('main.org_members'))