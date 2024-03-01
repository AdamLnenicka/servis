#FUNKCE ZMENIT HESLO

def zmenit_heslo(user_id, nove_heslo):
    import sqlite3, hashlib
    conn = sqlite3.connect('servis.db')
    heslo = hashlib.md5(nove_heslo.encode()).hexdigest()  # Použití hexdigest místo digest

    # Aktualizace hesla v tabulce passwords
    conn.execute("""
        UPDATE passwords SET encrypted_password = ? WHERE user_id = ?
    """, (heslo, user_id))

    conn.commit()
    conn.close()

#######################################################

#FUNKCE OVERIT UZIVATELE

def je_uzivatel(email, heslo):
    import sqlite3, hashlib
    # conn = sqlite3.connect('C:\\Users\\lnead\\Desktop\\VWA\\vwa_zs2023_xzilavy\\servis.db')
    conn = sqlite3.connect('servis.db')
    #heslo = hashlib.md5(heslo.encode()).hexdigest()
    
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
    user_id = cursor.fetchall()

    if user_id:
        cursor.execute("SELECT encrypted_password FROM passwords WHERE user_id = ?", (user_id[0][0],))
        password_match = cursor.fetchone()[0]
        if password_match == heslo:
            conn.close()
            return True
        else:
            conn.close()
            return False
    else:
        return False


#######################################################

#FUNKCE PRIDAT UZIVATELE

def add_user(name, surname, email, password, role_id, department_id):
    import sqlite3
    conn = sqlite3.connect('servis.db')
    cursor = conn.cursor()

    query = "SELECT email FROM users WHERE email = ?"
    cursor.execute(query, (email,))
    email_exists = cursor.fetchone()

    if email_exists == None: # email neexistuje, mozeme pokracovat pri vytvarani noveho pouzivatela
        query = "INSERT INTO USERS (name, surname, email, role_id, department_id) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (name, surname, email, role_id, department_id))
        conn.commit()
        query = "SELECT user_id FROM users WHERE email = ?"
        cursor.execute(query, (email,))
        user_id = cursor.fetchone()[0]
        q = "INSERT INTO passwords (user_id, encrypted_password) VALUES (?, ?)"
        cursor.execute(q, (user_id, password))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

###############################################################

#FUNKCE ZISKEJ INFORMACE O UZIVATELI
def get_user_info(email):
    import sqlite3
    # conn = sqlite3.connect('C:\\Users\\lnead\\Desktop\\VWA\\vwa_zs2023_xzilavy\\servis.db')
    conn = sqlite3.connect('servis.db')
    cursor = conn.cursor()

    query = """
        SELECT u.user_id, u.name, u.surname, r.role_name, u.email, u.department_id
        FROM USERS u
        JOIN ROLES r ON u.role_id = r.role_id
        WHERE u.email = ?
    """

    cursor.execute(query, (email,))
    user_info = cursor.fetchone()
    conn.close()

    if user_info:
        return user_info  # Vraci tuple (user_id, name, surname, role_name, email)
    else:
        return None  # Kdyztak handling
###################################################################

#FUNKCE ZISKEJ SEZNAM UZIVATELU
def get_users():
    import sqlite3
    # conn = sqlite3.connect('C:\\Users\\lnead\\Desktop\\VWA\\vwa_zs2023_xzilavy\\servis.db')
    conn = sqlite3.connect('servis.db')
    cursor = conn.cursor()

    query = """
            SELECT u.name, u.surname, r.role_name
            FROM USERS u
            JOIN ROLES r ON u.role_id = r.role_id
        """
    cursor.execute(query)
    users = cursor.fetchall()
    conn.close()

    return users

####################################################################

#FUNKCE SMAZAT UZIVATELE (neřeší heslo)
def remove_user(user_id):
    import sqlite3
    conn = sqlite3.connect('servis.db')
    cursor = conn.cursor()
    query = "DELETE FROM USERS WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    conn.commit()
    conn.close()
    return True

####################################################################

#FUNKCE AKTUALIZUJ UZIVATELE (neřeší heslo)
def update_user(user_id, name, surname, role_id):
    import sqlite3
    conn = sqlite3.connect('servis.db')
    cursor = conn.cursor()
    query = "UPDATE USERS SET name = ?, surname = ?, role_id = ? WHERE user_id = ?"
    cursor.execute(query, (name, surname, role_id, user_id))
    conn.commit()
    conn.close()
    return True

#########################################################################
    
#FUNKCE ZMENA HESLA UZIVATELE (neřeší heslo)

def zmenit_heslo(user_id, nove_heslo):
    import sqlite3, hashlib
    conn = sqlite3.connect('servis.db')
    heslo = hashlib.md5(nove_heslo.encode()).hexdigest()

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE passwords SET encrypted_password = ? WHERE user_id = ?
    """, (heslo, user_id))
    
    conn.commit()
    conn.close()

##########################################################################

#FUNKCIA NA PRIDANIE VOZIDLA DO db

def add_vehicle(customer_id, spz, brnad, model, year):
    import sqlite3
    conn = sqlite3.connect('servis.db')

    cursor = conn.cursor()
    query = "INSERT INTO vehicles (customer_id, vehicle_spz, vehicle_brand, vehicle_model, vehicle_year) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (customer_id, spz, brnad, model, year))
    conn.commit()
    conn.close()

def get_vehicles(user_email):
    import sqlite3
    conn = sqlite3.connect('servis.db')

    cursor = conn.cursor()
    query = "SELECT user_id FROM users WHERE email = ?"
    cursor.execute(query, (user_email,))
    user_id = cursor.fetchone()[0]

    q = "SELECT vehicle_spz, vehicle_brand, vehicle_model, vehicle_year, vehicle_id FROM vehicles WHERE customer_id = ?"
    cursor.execute(q, (user_id,))
    vehicles = cursor.fetchall()
    conn.close()

    return vehicles

def get_vehicle_info(vehicle_id):
    import sqlite3
    conn = sqlite3.connect('servis.db')

    cursor = conn.cursor()
    query = """SELECT r.record_date, s.type, r.results, u.name, u.surname
               FROM technical_records r
               JOIN service s ON r.service_id = s.service_id
               JOIN users u ON r.technician_id = u.user_id
               WHERE vehicle_id = ?"""
    cursor.execute(query, (vehicle_id,))
    records = cursor.fetchall()
    conn.close()

    return records

def get_vehicle_spz(vehicle_id):
    import sqlite3
    conn = sqlite3.connect('servis.db')

    cursor = conn.cursor()
    query = "SELECT vehicle_spz FROM vehicles WHERE vehicle_id = ?"
    cursor.execute(query, (vehicle_id,))
    spz = cursor.fetchone()[0]
    conn.close()

    return spz

def get_vehicles_technician(user_email):
    import sqlite3
    conn = sqlite3.connect('servis.db')

    cursor = conn.cursor()
    query = "SELECT user_id FROM users WHERE email = ?"
    cursor.execute(query, (user_email,))
    user_id = cursor.fetchone()[0]

    q = """SELECT DISTINCT v.vehicle_spz, v.vehicle_brand, v.vehicle_model, v.vehicle_year, u.name, u.surname, t.vehicle_id
           FROM technical_records t
           JOIN vehicles v ON t.vehicle_id = v.vehicle_id
           JOIN users u ON v.customer_id = u.user_id
           WHERE t.technician_id = ?"""
    cursor.execute(q, (user_id,))
    vehicles = cursor.fetchall()
    conn.close()

    return vehicles

def vehicle_details_technician(vehicle_id):
    import sqlite3
    conn = sqlite3.connect('servis.db')

    cursor = conn.cursor()
    query ="""SELECT r.record_date, s.type, r.results, r.record_id
               FROM technical_records r
               JOIN service s ON r.service_id = s.service_id
               WHERE vehicle_id = ?;"""
    cursor.execute(query, (vehicle_id,))
    records = cursor.fetchall()
    conn.close()

    return records

def insert_new_record(vehicle_id, techinician_id, service_id, record_date, results):
    import sqlite3
    conn = sqlite3.connect('servis.db')

    cursor = conn.cursor()
    query = "INSERT INTO technical_records (vehicle_id, technician_id, service_id, record_date, results) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (vehicle_id, techinician_id, service_id, record_date, results))
    conn.commit()
    conn.close()

def servis(type):
    if type == 'technická kontrola':
        service_id = 1
    elif type == 'servis':
        service_id = 2
    else:
        service_id = 3
    return service_id

def get_vehicle_id(spz):
    import sqlite3
    conn = sqlite3.connect('servis.db')

    cursor = conn.cursor()
    query = "SELECT vehicle_id FROM vehicles WHERE vehicle_spz = ?"
    cursor.execute(query, (spz,))
    vehicle_id = cursor.fetchone()[0]

    return vehicle_id

def delete_record_from_db(record_id):
    import sqlite3
    conn = sqlite3.connect('servis.db')

    cursor = conn.cursor()
    query = "DELETE FROM technical_records WHERE record_id=?"
    cursor.execute(query, (record_id,))
    conn.commit()
    conn.close()

def alter_record_form_db(record_id, result):
    import sqlite3
    conn = sqlite3.connect('servis.db')

    cursor = conn.cursor()
    query = "UPDATE technical_records SET results=? WHERE record_id=?"
    cursor.execute(query, (result, record_id))
    conn.commit()
    conn.close()

#FUNKCE PRO ZISKANI SEZNAMU ODDELENI
def get_departments(department_id):
    import sqlite3
    # conn = sqlite3.connect('C:\\Users\\lnead\\Desktop\\VWA\\vwa_zs2023_xzilavy\\servis.db')
    conn = sqlite3.connect('servis.db')
    cursor = conn.cursor()
    cursor.execute("SELECT department_name FROM departments WHERE department_id=?", (department_id,))
    departments = cursor.fetchone()[0]
    conn.close()
    return departments


#FUNKCE PRO ZÍSKÁNÍ TECHNICKÝCH ZÁZNAMŮ Z DATABÁZE


def car_records_manager(record_id):
    import sqlite3
    # conn = sqlite3.connect('C:\\Users\\lnead\\Desktop\\VWA\\vwa_zs2023_xzilavy\\servis.db')
    conn = sqlite3.connect('servis.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT v.vehicle_spz, v.vehicle_brand, v.vehicle_model, v.vehicle_year
                            FROM technical_records t
                            JOIN  vehicles v ON t.vehicle_id=v.vehicle_id
                            where t.record_id = ?""", (record_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def list_technicians(department_id):
    import sqlite3
    # conn = sqlite3.connect('C:\\Users\\lnead\\Desktop\\VWA\\vwa_zs2023_xzilavy\\servis.db')
    conn = sqlite3.connect('servis.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT u.user_id, u.name, u.surname
                                FROM users u 
                                where u.department_id = ? and u.role_id > 4""", (department_id,))
    technicians = cursor.fetchall()
    conn.close()
    return technicians

def assign_technician_to_db(record_id, technician_id):
    import sqlite3
    conn = sqlite3.connect('servis.db')

    cursor = conn.cursor()
    query = "UPDATE technical_records SET technician_id=? WHERE record_id=?"
    cursor.execute(query, (technician_id, record_id))
    conn.commit()
    conn.close()

def get_technical_records(role):
    import sqlite3
    # conn = sqlite3.connect('C:\\Users\\lnead\\Desktop\\VWA\\vwa_zs2023_xzilavy\\servis.db')
    conn = sqlite3.connect('servis.db')
    cursor = conn.cursor()



    if role == "Manažer technické kontroly":
        cursor.execute("""SELECT v.vehicle_spz, t.record_date, t.results, t.technician_id, t.record_id
                          FROM technical_records t
                          JOIN vehicles v ON t.vehicle_id = v.vehicle_id
                          WHERE t.service_id=1""")
    elif role == "Manažer servisu":
        cursor.execute("""SELECT v.vehicle_spz, t.record_date, t.results, t.technician_id, t.record_id
                          FROM technical_records t
                          JOIN vehicles v ON t.vehicle_id = v.vehicle_id
                          WHERE t.service_id=2""")
    elif role == "Manažer likvidace vraků":
        cursor.execute("""SELECT v.vehicle_spz, t.record_date, t.results, t.technician_id, t.record_id
                          FROM technical_records t
                          JOIN vehicles v ON t.vehicle_id = v.vehicle_id
                          WHERE t.service_id=3""")
    elif role == "Administrátor/boss":
        cursor.execute(cursor.execute("""SELECT v.vehicle_spz, t.record_date, t.results, t.technician_id, t.record_id
                                         FROM technical_records t
                                         JOIN vehicles v ON t.vehicle_id = v.vehicle_id"""))
    records = cursor.fetchall()
    conn.close()
    return records
