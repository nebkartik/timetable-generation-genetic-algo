from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
from src.utils.decorators import login_required
from src.database.database import connect_db, fetch_data
from src.services.timetable_generation_service import perform_timetable_generation


generation_bp = Blueprint('generation', __name__)

@generation_bp.route('/credits')
@login_required
def credits_page():
    return render_template('credits_page_timeslot.html')

@generation_bp.route('/subjects', methods=['GET'])
@login_required
def subjects():
    class_name = request.args.get('class')
    semester = request.args.get('semester')
    subjects,_ = fetch_data(class_name, semester, session['school_id'])
    return jsonify(subjects)

@generation_bp.route('/save_priorities', methods=['POST'])
@login_required
def save_priorities():
    return jsonify({"success": True})


@generation_bp.route('/generate_setup', methods=['POST'])
@login_required
def generate_setup():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM class WHERE school_id = %s", (session['school_id'],))
    classes = cursor.fetchall()
    db.close()
    return render_template('generate.html', classes=classes)


@generation_bp.route('/generate_timetable', methods=['POST'])
@login_required
def generate_timetable():
    try:
        data = request.get_json()
        class_name = data.get('class')
        semester = data.get('semester')
        priorities = data.get('priorities', {})
        
        timetable, error =  perform_timetable_generation(class_name, semester, priorities,session['school_id'])

        session['timetable'] = timetable  # Store in session for later retrieval
        session['generation_context'] =
        {
            'class_name': class_name,
            'semester': semester,
            'priorities': priorities
        }      
        if error:
            return jsonify({"success": False, "error": error})
    except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"message": "Timetable generated successfully", "redirect": url_for('timetable.view_timetable')})