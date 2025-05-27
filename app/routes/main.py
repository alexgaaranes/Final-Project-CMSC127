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
    print(members)
    return render_template('org/org_members.html', org=org_deets, members=members)


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

    orgs = member.get_member_org(std_num)

    orgList = []
    resultList = []

    for idx, org in enumerate(orgs):

        orgList.append(org['org_name'])

    for idx, org in enumerate(orgList):
        result = member.get_member_unpaid_fee(std_num, org)
        resultList.append(result[0])

    return render_template('mem/mem_fees.html', member=mem_deets, fees=resultList, orgs = orgs)