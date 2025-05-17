from flask import Blueprint, render_template
from app.models.member import get_member_from_org

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    member = get_member_from_org('org')
    return render_template('index.html', members=member)