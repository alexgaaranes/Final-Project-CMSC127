from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import org, member

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
    return render_template('orglogin.html')

@main_bp.route('/memlogin', methods=['GET'])
def mem_login():
    if 'member' in session:
        return redirect(url_for('main.mem_home'))
    return render_template('memlogin.html')

@main_bp.route('/registerorg', methods=['GET'])
def org_register():
    return render_template('orgregister.html')

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
        return render_template('orglogin.html', error=str(e))
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
        return render_template('memlogin.html', error=str(e))
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
        return render_template('orgregister.html', error=err_msg)
    return render_template('orglogin.html', success="Organization registered successfully!")

# OTHER routes
@main_bp.route('/org_home', methods=['GET'])
def org_home():
    if 'org' not in session:
        return redirect(url_for('main.orglogin'))
    org_deets = session['org']
    return render_template('org_dashboard.html', org=org_deets)

@main_bp.route('/mem_home', methods=['GET'])
def mem_home():
    if 'member' not in session:
        return redirect(url_for('main.mem_login'))
    mem_deets = session['member']
    return render_template('mem_dashboard.html', member=mem_deets)