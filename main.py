from flask import Flask, render_template, request, redirect
import sqlite3

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


@app.route('/teachers')
def teachers():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Teachers')
    teachers_data = cursor.fetchall()
    connection.close()

    print(teachers_data)  # Добавьте эту строку для отладки

    return render_template('teachers.html', data=teachers_data)


@app.route('/courses')
def courses():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Courses')
    courses_data = cursor.fetchall()
    connection.close()

    print(courses_data)  # Добавьте эту строку для отладки

    return render_template('courses.html', data=courses_data)


@app.route('/students')
def students():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Students')
    students_data = cursor.fetchall()
    connection.close()

    print(students_data)  # Добавьте эту строку для отладки

    return render_template('students.html', data=students_data)


@app.route('/results')
def results():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Results')
    results_data = cursor.fetchall()
    connection.close()

    print(results_data)  # Добавьте эту строку для отладки

    return render_template('results.html', data=results_data)

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
        cursor.execute('UPDATE Teachers SET first_name = ?, last_name = ? WHERE teacher_id = ?', (new_first_name, new_last_name, teacher_id))
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
        cursor.execute('INSERT INTO Courses (name_of_course, teacher_id, type_of_course) VALUES (?, ?, ?)', (name_of_course, teacher_id, type_of_course))
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
        cursor.execute('UPDATE Courses SET name_of_course = ?, teacher_id = ?, type_of_course = ? WHERE course_id = ?', (new_name_of_course, new_teacher_id, new_type_of_course, course_id))
        connection.commit()
        connection.close()

        return redirect('/courses')

    return render_template('edit_course.html', course=course_data)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthdate = request.form['birthdate']
        city = request.form['city']

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Students (first_name, last_name, birthdate, city) VALUES (?, ?, ?, ?)', (first_name, last_name, birthdate, city))
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
        cursor.execute('UPDATE Students SET first_name = ?, last_name = ?, birthdate = ?, city = ? WHERE student_id = ?', (new_first_name, new_last_name, new_birthdate, new_city, student_id))
        connection.commit()
        connection.close()

        return redirect('/students')

    return render_template('edit_student.html', student=student_data)


if __name__ == '__main__':
    app.run(debug=True)
