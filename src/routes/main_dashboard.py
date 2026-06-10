from flask import Blueprint, render_template, session
from src.utils.decorators import login_required
from mysql import connector
from src.database.database import connect_db
main_bp = Blueprint('main', __name__)

@main_bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@main_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    school_id = session['school_id']
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("Select count(*) from class where school_id = %s", (school_id,))
    class_count = cursor.fetchone()[0]

    # Count Staff (Teachers)
    cursor.execute("SELECT COUNT(*) FROM teacher WHERE school_id = %s", (school_id,))
    staff_count = cursor.fetchone()[0]

    # Count Saved Timetables (Distinct classes that have schedule entries)
    cursor.execute("SELECT COUNT(DISTINCT class_id) FROM timetable WHERE school_id = %s", (school_id,))
    timetable_count = cursor.fetchone()[0]

    db.close()

    return render_template('dashboard.html', 
                           class_count=class_count, 
                           staff_count=staff_count,
                           timetable_count=timetable_count)