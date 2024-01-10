from flask import Flask, render_template, request, redirect, abort
import sqlite3
import random
from collections import Counter

app = Flask(__name__)

DATABASE = 'university.db'


def connect_db():
    return sqlite3.connect(DATABASE)


def query_db(query, args=(), one=False):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    connection.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def index():
    return render_template('index.html')


def paginate_results(results, page, per_page):
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    return results[start_index:end_index]


@app.route('/view_table', methods=['POST'])
def view_table():
    selected_table = request.form['table']
    return redirect(f'/{selected_table}')


def get_teachers_statistics():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM Teachers')
    total_records = cursor.fetchone()[0]

    cursor.execute('SELECT first_name, COUNT(*) as count FROM Teachers GROUP BY first_name ORDER BY count DESC LIMIT 5')
    popular_names = cursor.fetchall()

    connection.close()

    return {'total_records': total_records, 'popular_names': popular_names}


@app.route('/teachers')
def teachers():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Teachers')
    teachers_data = cursor.fetchall()
    connection.close()

    search_term = request.args.get('search_term')
    page = int(request.args.get('page', 1))
    per_page = 30

    if search_term:
        search_terms = search_term.lower().split()
        teachers_data = [teacher for teacher in teachers_data if
                         all(term in f"{teacher[1].lower()} {teacher[2].lower()}" for term in search_terms)]

    total_records = len(teachers_data)
    total_pages = (total_records + per_page - 1) // per_page

    if page < 1 or page > total_pages:
        abort(404)

    teachers_data_paginated = paginate_results(teachers_data, page, per_page)

    teachers_statistics = get_teachers_statistics()

    return render_template('teachers.html', data=teachers_data_paginated, statistics=teachers_statistics,
                           search_term=search_term, current_page=page, total_pages=total_pages)


def get_courses_statistics(courses_data):
    total_records = len(courses_data)
    popular_course_names = Counter(course[1] for course in courses_data).most_common(5)
    return {'total_records': total_records, 'popular_course_names': popular_course_names}


@app.route('/courses')
def courses():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Courses')
    courses_data = cursor.fetchall()
    connection.close()

    search_term = request.args.get('search_term')
    page = int(request.args.get('page', 1))
    per_page = 30

    if search_term:
        search_terms = search_term.lower().split()
        courses_data = [course for course in courses_data if
                        any(term in course[1].lower() for term in search_terms)]

    total_records = len(courses_data)
    total_pages = (total_records + per_page - 1) // per_page

    if page < 1 or page > total_pages:
        abort(404)

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    courses_data_paginated = courses_data[start_index:end_index]

    courses_statistics = get_courses_statistics(courses_data)

    return render_template('courses.html', data=courses_data_paginated, statistics=courses_statistics,
                           search_term=search_term, current_page=page, total_pages=total_pages)


def get_students_statistics(students_data):
    total_records = len(students_data)

    popular_names = Counter(student[1] for student in students_data).most_common(5)

    return {'total_records': total_records, 'popular_names': popular_names}


@app.route('/students')
def students():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Students')
    students_data = cursor.fetchall()
    connection.close()

    search_term = request.args.get('search_term')
    page = int(request.args.get('page', 1))
    per_page = 30

    if search_term:
        search_terms = search_term.lower().split()
        students_data = [student for student in students_data if
                         all(term in f"{student[1].lower()} {student[2].lower()}" for term in search_terms)]

    total_records = len(students_data)
    total_pages = (total_records + per_page - 1) // per_page

    if page < 1 or page > total_pages:
        abort(404)

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    students_data_paginated = students_data[start_index:end_index]

    students_statistics = get_students_statistics(students_data)

    return render_template('students.html', data=students_data_paginated, statistics=students_statistics,
                           search_term=search_term, current_page=page, total_pages=total_pages)


def get_results_statistics(results_data):
    total_records = len(results_data)

    type_of_course_counts = Counter(result[3] for result in results_data)

    return {'total_records': total_records, 'type_of_course_counts': type_of_course_counts}


@app.route('/results')
def results():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Results')
    results_data = cursor.fetchall()
    connection.close()

    search_term = request.args.get('search_term')
    page = int(request.args.get('page', 1))
    per_page = 30

    if search_term:
        search_terms = search_term.lower().split()
        results_data = [result for result in results_data if
                        any(term in str(result) for term in search_terms)]

    total_records = len(results_data)
    total_pages = (total_records + per_page - 1) // per_page

    if page < 1 or page > total_pages:
        abort(404)

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    results_data_paginated = results_data[start_index:end_index]

    results_statistics = get_results_statistics(results_data)

    return render_template('results.html', data=results_data_paginated, statistics=results_statistics,
                           search_term=search_term, current_page=page, total_pages=total_pages)



def get_mark_statistics(mark_data):
    total_records = len(mark_data)

    mark_counts = Counter(mark[3] for mark in mark_data)

    return {'total_records': total_records, 'mark_counts': mark_counts}


@app.route('/mark')
def mark():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Mark')
    mark_data = cursor.fetchall()
    connection.close()

    search_term = request.args.get('search_term')
    page = int(request.args.get('page', 1))
    per_page = 30

    if search_term:
        search_terms = search_term.lower().split()
        mark_data = [mark for mark in mark_data if
                     any(term in str(mark) for term in search_terms)]

    total_records = len(mark_data)
    total_pages = (total_records + per_page - 1) // per_page

    if page < 1 or page > total_pages:
        abort(404)

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    mark_data_paginated = mark_data[start_index:end_index]

    mark_statistics = get_mark_statistics(mark_data)

    return render_template('mark.html', data=mark_data_paginated, statistics=mark_statistics,
                           search_term=search_term, current_page=page, total_pages=total_pages)


@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Teachers (first_name, last_name) VALUES (?, ?)', (first_name, last_name))
        connection.commit()
        connection.close()

        return redirect('/teachers')

    return render_template('add_teacher.html')


@app.route('/delete_teacher/<int:teacher_id>')
def delete_teacher(teacher_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Teachers WHERE teacher_id = ?', (teacher_id,))
    connection.commit()
    connection.close()

    return redirect('/teachers')


@app.route('/delete_mark/<int:mark_id>')
def delete_mark(mark_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Mark WHERE mark_id = ?', (mark_id,))
    connection.commit()
    connection.close()

    return redirect('/mark')


@app.route('/edit_teacher/<int:teacher_id>', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Teachers WHERE teacher_id = ?', (teacher_id,))
    teacher_data = cursor.fetchone()
    connection.close()

    if request.method == 'POST':
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute('UPDATE Teachers SET first_name = ?, last_name = ? WHERE teacher_id = ?',
                       (new_first_name, new_last_name, teacher_id))
        connection.commit()
        connection.close()

        return redirect('/teachers')

    return render_template('edit_teacher.html', teacher=teacher_data)


@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name_of_course = request.form['name_of_course']
        teacher_id = request.form['teacher_id']
        type_of_course = request.form['type_of_course']

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Courses (name_of_course, teacher_id, type_of_course) VALUES (?, ?, ?)',
                       (name_of_course, teacher_id, type_of_course))
        connection.commit()
        connection.close()

        return redirect('/courses')

    return render_template('add_course.html')


@app.route('/delete_course/<int:course_id>')
def delete_course(course_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Courses WHERE course_id = ?', (course_id,))
    connection.commit()
    connection.close()

    return redirect('/courses')


@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Courses WHERE course_id = ?', (course_id,))
    course_data = cursor.fetchone()
    connection.close()

    if request.method == 'POST':
        new_name_of_course = request.form['name_of_course']
        new_teacher_id = request.form['teacher_id']
        new_type_of_course = request.form['type_of_course']

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute('UPDATE Courses SET name_of_course = ?, teacher_id = ?, type_of_course = ? WHERE course_id = ?',
                       (new_name_of_course, new_teacher_id, new_type_of_course, course_id))
        connection.commit()
        connection.close()

        return redirect('/courses')

    return render_template('edit_course.html', course=course_data)


@app.route('/edit_mark/<int:mark_id>', methods=['GET', 'POST'])
def edit_mark(mark_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Mark WHERE mark_id = ?', (mark_id,))
    mark_data = cursor.fetchone()
    connection.close()

    if request.method == 'POST':
        new_mark = request.form['mark']

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute('UPDATE Mark SET mark = ? WHERE mark_id = ?', (new_mark, mark_id))
        connection.commit()
        connection.close()

        return redirect('/mark')

    return render_template('edit_mark.html', mark_id=mark_id, mark_data=mark_data)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthdate = request.form['birthdate']
        city = request.form['city']

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Students (first_name, last_name, birthdate, city) VALUES (?, ?, ?, ?)',
                       (first_name, last_name, birthdate, city))
        connection.commit()
        connection.close()

        return redirect('/students')

    return render_template('add_student.html')


@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Students WHERE student_id = ?', (student_id,))
    connection.commit()
    connection.close()

    return redirect('/students')


@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Students WHERE student_id = ?', (student_id,))
    student_data = cursor.fetchone()
    connection.close()

    if request.method == 'POST':
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']
        new_birthdate = request.form['birthdate']
        new_city = request.form['city']

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute(
            'UPDATE Students SET first_name = ?, last_name = ?, birthdate = ?, city = ? WHERE student_id = ?',
            (new_first_name, new_last_name, new_birthdate, new_city, student_id))
        connection.commit()
        connection.close()

        return redirect('/students')

    return render_template('edit_student.html', student=student_data)


if __name__ == '__main__':
    app.run(debug=True)
