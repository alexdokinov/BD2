from flask import Flask, render_template, request, redirect
import sqlite3
import random

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

    teachers_statistics = get_teachers_statistics()

    return render_template('teachers.html', data=teachers_data, statistics=teachers_statistics)


def get_courses_statistics():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM Courses')
    total_records = cursor.fetchone()[0]

    cursor.execute(
        'SELECT name_of_course, COUNT(*) as count FROM Courses GROUP BY name_of_course ORDER BY count DESC LIMIT 5')
    popular_courses = cursor.fetchall()

    connection.close()

    return {'total_records': total_records, 'popular_courses': popular_courses}


@app.route('/courses')
def courses():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Courses')
    courses_data = cursor.fetchall()
    connection.close()

    courses_statistics = get_courses_statistics()

    return render_template('courses.html', data=courses_data, statistics=courses_statistics)


def get_students_statistics():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM Students')
    total_records = cursor.fetchone()[0]

    cursor.execute('SELECT city, COUNT(*) as count FROM Students GROUP BY city ORDER BY count DESC LIMIT 5')
    popular_cities = cursor.fetchall()

    connection.close()

    return {'total_records': total_records, 'popular_cities': popular_cities}


@app.route('/students')
def students():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Students')
    students_data = cursor.fetchall()
    connection.close()

    students_statistics = get_students_statistics()

    return render_template('students.html', data=students_data, statistics=students_statistics)


@app.route('/results')
def results():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Results')
    results_data = cursor.fetchall()
    connection.close()

    print(results_data)

    return render_template('results.html', data=results_data)


def get_mark_statistics():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM Mark')
    total_records = cursor.fetchone()[0]

    cursor.execute('SELECT mark, COUNT(*) as count FROM Mark GROUP BY mark ORDER BY count DESC LIMIT 5')
    popular_marks = cursor.fetchall()

    connection.close()

    return {'total_records': total_records, 'popular_marks': popular_marks}


@app.route('/mark')
def mark():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Mark')
    mark_data = cursor.fetchall()
    connection.close()

    mark_statistics = get_mark_statistics()

    return render_template('mark.html', data=mark_data, statistics=mark_statistics)


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
