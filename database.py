import sqlite3

# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect(
    "onetapresq.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =====================================================
# CREATE TABLE
# =====================================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS mechanic_requests (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        phone TEXT,

        vehicle TEXT,

        issue TEXT,

        help_type TEXT,

        location TEXT
    )
    """
)

conn.commit()
# =====================================================
# CREATE EMERGENCY ALERT TABLE
# =====================================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS emergency_alerts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        location TEXT
    )
    """
)

conn.commit()
# =====================================================
# CREATE FUEL SHARE TABLE
# =====================================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS fuel_requests (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        helper_name TEXT,

        phone TEXT,

        location TEXT
    )
    """
)

conn.commit()
# =====================================================
# CREATE EV REQUEST TABLE
# =====================================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS ev_requests (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        vehicle_type TEXT,

        battery_percentage INTEGER,

        estimated_range REAL
    )
    """
)

conn.commit()
# =====================================================
# CREATE USERS TABLE
# =====================================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        password TEXT,

        phone TEXT,

        role TEXT
    )
    """
)

conn.commit()
# =====================================================
# ADD PHONE COLUMN IF NOT EXISTS
# =====================================================

try:

    cursor.execute(
        """
        ALTER TABLE users
        ADD COLUMN phone TEXT
        """
    )

    conn.commit()

except:

    pass

# =====================================================
# SAVE MECHANIC REQUEST
# =====================================================

def save_mechanic_request(
    name,
    phone,
    vehicle,
    issue,
    help_type,
    location
):

    cursor.execute(
        """
        INSERT INTO mechanic_requests (

            name,
            phone,
            vehicle,
            issue,
            help_type,
            location

        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            phone,
            vehicle,
            issue,
            help_type,
            location
        )
    )
    print("DATA SAVED SUCCESSFULLY")

    conn.commit()
# =====================================================
# GET ALL MECHANIC REQUESTS
# =====================================================

def get_mechanic_requests():

    conn = sqlite3.connect(
        "onetapresq.db",
        check_same_thread=False
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM mechanic_requests
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data
# =====================================================
# SAVE EMERGENCY ALERT
# =====================================================

def save_emergency_alert(location):

    conn = sqlite3.connect(
        "onetapresq.db",
        check_same_thread=False
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO emergency_alerts (
            location
        )

        VALUES (?)
        """,
        (location,)
    )

    conn.commit()

    conn.close()


# =====================================================
# GET EMERGENCY ALERTS
# =====================================================

def get_emergency_alerts():

    conn = sqlite3.connect(
        "onetapresq.db",
        check_same_thread=False
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM emergency_alerts
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data
# =====================================================
# SAVE FUEL REQUEST
# =====================================================

def save_fuel_request(
    helper_name,
    phone,
    location
):

    conn = sqlite3.connect(
        "onetapresq.db",
        check_same_thread=False
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO fuel_requests (

            helper_name,
            phone,
            location

        )

        VALUES (?, ?, ?)
        """,
        (
            helper_name,
            phone,
            location
        )
    )

    conn.commit()

    conn.close()


# =====================================================
# GET FUEL REQUESTS
# =====================================================

def get_fuel_requests():

    conn = sqlite3.connect(
        "onetapresq.db",
        check_same_thread=False
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM fuel_requests
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data
# =====================================================
# SAVE EV REQUEST
# =====================================================

def save_ev_request(
    vehicle_type,
    battery_percentage,
    estimated_range
):

    conn = sqlite3.connect(
        "onetapresq.db",
        check_same_thread=False
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ev_requests (

            vehicle_type,
            battery_percentage,
            estimated_range

        )

        VALUES (?, ?, ?)
        """,
        (
            vehicle_type,
            battery_percentage,
            estimated_range
        )
    )

    conn.commit()

    conn.close()


# =====================================================
# GET EV REQUESTS
# =====================================================

def get_ev_requests():

    conn = sqlite3.connect(
        "onetapresq.db",
        check_same_thread=False
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM ev_requests
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data

# =====================================================
# CREATE USER
# =====================================================

def create_user(
    username,
    password,
    phone,
    role
    
):

    conn = sqlite3.connect(
        "onetapresq.db",
        check_same_thread=False
    )

    cursor = conn.cursor()

    # =================================================
    # CHECK EXISTING USERNAME
    # =================================================

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username = ?
        """,
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        conn.close()

        return False

    # =================================================
    # CREATE NEW USER
    # =================================================

    cursor.execute(
        """
        INSERT INTO users (

            username,
            password,
            phone,
            role

        )

        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            password,
            phone,
            role
        )
    )

    conn.commit()

    conn.close()

    return True


# =====================================================
# LOGIN USER
# =====================================================

def login_user(
    username,
    password
):

    conn = sqlite3.connect(
        "onetapresq.db",
        check_same_thread=False
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users

        WHERE username = ?
        AND password = ?
        """,
        (
            username,
            password,
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user