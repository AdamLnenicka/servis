from flask import Flask, render_template, url_for, redirect, request, session
from funkce import je_uzivatel, get_user_info, get_users, add_user, add_vehicle, get_vehicle_info, get_departments, get_vehicles,get_vehicle_spz, get_technical_records, get_vehicles_technician, vehicle_details_technician, servis, insert_new_record, delete_record_from_db, alter_record_form_db, remove_user, update_user, get_vehicle_id, car_records_manager, list_technicians, assign_technician_to_db
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'key'

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))
    return decorated

@app.route('/')
def index():
    return render_template('index.html', log='Přihlášení')

@app.route('/registrace', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        if password != confirm_password:
            return render_template('registration.html')
        else:
            if add_user(name, surname, email, password, 4): # zatial to je 4 ale zmeni sa to na 8
                return redirect(url_for('login'))
            else:
                return render_template('registration.html', log='Přihlášení')
    else:
        return render_template('registration.html', log='Přihlášení')

@app.route('/prihlaseni/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['email']
        password = request.form['password']

        if je_uzivatel(user, password):
            session['user'] = user
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', log='Přihlášení')
    else:
        return render_template('login.html', log='Přihlášení')

@app.route('/profil/')
@auth_required
def profile():
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        if user_info:
            user_id, name, surname, role, email, department_id = user_info
            if role == "Administrátor/boss":
                return render_template('my_profile_admin.html', name=name, surname=surname, role=role, email=email)
            elif role == "Manažer technické kontroly" or role == "Manažer servisu" or role == "Manažer likvidace vraků":
                return render_template('my_profile_manager.html', name=name, surname=surname, role=role, email=email)
            elif role == "Technik technické kontroly" or role == "Technik servisu" or role == 'Technik likvidace':
                return render_template('my_profile_technician.html', name=name, surname=surname, role=role, email=email)
            elif role == "Zákazník":
                return render_template('my_profile_customer.html', name=name, surname=surname, role=role, email=email)

@app.route('/uzivatele/')
@auth_required
def user_management():
    if 'user' in session:
        users = get_users()  # Získání seznamu uživatelů z funkce get_users
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        return render_template('admin_users.html', users=users, name=name, surname=surname, role=role)

@app.route('/novy_pouzivatel', methods=['POST', 'GET'])
@auth_required
def new_user_admin():
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        if request.method == 'POST':
            new_name = request.form['new-name']
            new_surname = request.form['new-surname']
            new_email = request.form['new-email']
            new_password = request.form['new-password']
            new_role = request.form['user-role']
            new_department = request.form['user-department']
            if add_user(new_name, new_surname, new_email, new_password, new_role, new_department):
                return redirect(url_for('user_management'))
            else:
                return render_template('new_user.html', name=name, surname=surname, role=role)
        else:
            return render_template('new_user.html', name=name, surname=surname, role=role)


@app.route('/odhlaseni', methods=['POST'])
@auth_required
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/sluzby')
def services():
    return render_template('services.html')

@app.route('/kontakty')
def contacts():
    return render_template('contacts.html')

@app.route('/nova_objednavka', methods=['POST', 'GET'])
@auth_required
def new_order():
    years = range(1900, 2025)
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        if request.method == 'POST':
            car_spz = request.form['spz']
            car_brand = request.form['brand']
            car_year = request.form['year']
            car_model = request.form['model']
            service = request.form['service-type']
            date = request.form['date']
            time = request.form['time']
            record_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result = f'objednávka na {date} {time}'
            add_vehicle(user_id, car_spz, car_brand, car_model, car_year)
            vehicle_id = get_vehicle_id(car_spz)
            insert_new_record(vehicle_id, None, service, record_date, result)
            return redirect(url_for('profile'))
        else:
            return render_template('new_order.html', years=years, log="Konto", name=name, surname=surname, role=role)

@app.route('/stav_vozidla', methods=['POST', 'GET'])
@auth_required
def car_status_customer():
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        vehicles = get_vehicles(user_email)
        return render_template('stav_vozidla.html',vehicles=vehicles, name=name, surname=surname, role=role)

@app.route('/stav_vozidla_detail/<int:vehicle_id>', methods=['POST', 'GET'])
@auth_required
def car_status_customer_detail(vehicle_id):
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        records = get_vehicle_info(vehicle_id)
        spz = get_vehicle_spz(vehicle_id)
        return render_template('stav_vozidla_po.html', name=name, surname=surname, role=role, records=records, spz=spz)

@app.route('/moje_prace')
@auth_required
def my_work():
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        vehicles = get_vehicles_technician(user_email)
        return render_template('my_work.html', name=name, surname=surname, role=role, vehicles=vehicles)
@app.route('/moje_prace_detail/<int:vehicle_id>')
@auth_required
def my_work_detail(vehicle_id):
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        records = vehicle_details_technician(vehicle_id)
        spz = get_vehicle_spz(vehicle_id)
        return render_template('my_work_detail.html', name=name, surname=surname, role=role, records=records, spz=spz, vehicle_id=vehicle_id)
@app.route('/novy_zaznam/<int:vehicle_id>', methods=['POST', 'GET'])
@auth_required
def new_record(vehicle_id):
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        spz = get_vehicle_spz(vehicle_id)
        records = vehicle_details_technician(vehicle_id)
        if request.method == 'POST':
            vehicle_id = vehicle_id
            techinician_id = user_id
            service_id = servis(records[0][1])
            record_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            results = request.form['poznamka']
            insert_new_record(vehicle_id, techinician_id, service_id, record_date, results)
            return redirect(url_for('my_work_detail', vehicle_id=vehicle_id))
        else:
            return render_template('new_record_technician.html', name=name, surname=surname, records=records, role=role, spz=spz, vehicle_id=vehicle_id)
@app.route('/moje_prace_detail/<int:vehicle_id>/odstranit_zaznam/<int:record_id>', methods=['POST'])
@auth_required
def delete_record(vehicle_id, record_id):
    if 'user' in session:
        delete_record_from_db(record_id)
        return redirect(url_for('my_work_detail', vehicle_id=vehicle_id))

@app.route('/moje_prace_detail/<int:vehicle_id>/upravit_zaznam/<int:record_id>', methods=['POST', 'GET'])
@auth_required
def edit_record_page(vehicle_id, record_id):
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        records = vehicle_details_technician(vehicle_id)
        spz = get_vehicle_spz(vehicle_id)
        return render_template('edit_record_technician.html', name=name, surname=surname, role=role, records=records, spz=spz, vehicle_id=vehicle_id, record_id=record_id)

@app.route('/moje_prace_detail/<int:vehicle_id>/upravit_zaznam/<int:record_id>/#', methods=['POST', 'GET'])
@auth_required
def edit_record(vehicle_id, record_id):
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        records = vehicle_details_technician(vehicle_id)
        spz = get_vehicle_spz(vehicle_id)
        if request.method == 'POST':
            result = request.form['poznamka']
            alter_record_form_db(record_id, result)
            return redirect(url_for('my_work_detail', vehicle_id=vehicle_id))
        else:
            return redirect(url_for('edit_record_page', name=name, surname=surname, role=role, records=records, spz=spz, vehicle_id=vehicle_id, record_id=record_id))

@app.route('/departments')
@auth_required
def departments():
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        department = get_departments(department_id)
        records = get_technical_records(role)
        return render_template('manager_departments.html', department=department, name=name, surname=surname, role=role, records=records)

@app.route('/departments/<int:record_id>/pridelit_technikovi', methods=['GET', 'POST'])
@auth_required
def assign_technician(record_id):
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        car_records = car_records_manager(record_id)
        technicians = list_technicians(department_id)
        return render_template('assign_technician.html', name=name, surname=surname, role=role, records=car_records, record_id=record_id, technicians=technicians)

@app.route('/departments/<int:record_id>/pridelit_technikovi/#', methods=['GET', 'POST'])
@auth_required
def assign(record_id):
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        car_records = car_records_manager(record_id)
        technicians = list_technicians(department_id)
        department = get_departments(department_id)
        records = get_technical_records(role)
        if request.method == 'POST':
            technik = request.form['technik']
            assign_technician_to_db(record_id, technik)
            return redirect(url_for('departments', department=department, name=name, surname=surname, role=role, records=records))
        else:
            return render_template('assign_technician.html', name=name, surname=surname, role=role, records=car_records,record_id=record_id, technicians=technicians)

@app.route('/departments/<int:record_id>/vymazat', methods=['POST'])
@auth_required
def delete_record_manager(record_id):
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        department = get_departments(department_id)
        records = get_technical_records(role)
        delete_record_from_db(record_id)
        return redirect(url_for('departments', department=department, name=name, surname=surname, role=role, records=records))


@app.route('/enter_department', methods=['GET', 'POST'])
@auth_required
def enter_department():
    if 'user' in session:
        user_email = session['user']
        user_info = get_user_info(user_email)
        user_id, name, surname, role, email, department_id = user_info
        print(1)

        if role == "Manažer technické kontroly":
            print(2)
            technical_records = get_technical_records(role)
            return render_template('admin_departments_technic.html', technical_records=technical_records, name=name,
                                   surname=surname, role=role)
        if role == "Manažer servisu":
            print(3)
            technical_records = get_technical_records(role)
            return render_template('admin_departments_servis.html', technical_records=technical_records, name=name,
                                   surname=surname, role=role)
        if role == "Manažer likvidace vraků":
            print(4)
            technical_records = get_technical_records(role)
            return render_template('admin_departments_liqui.html', technical_records=technical_records, name=name,
                                   surname=surname, role=role)
        if role == "Administrátor/boss":
            print(5)
            technical_records = get_technical_records(role)
            return render_template('admin_departments.html', technical_records=technical_records, name=name,
                                   surname=surname, role=role)


if __name__ == '__main__':
    app.run(debug=True)


