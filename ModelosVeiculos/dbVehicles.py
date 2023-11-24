import sqlite3, random, datetime
from modelsVehicles import Vehicle


def getNewId():
    return random.getrandbits(28)

vehicles = [
    {
        'available': True,
        'model': 'Sedan',
        'plate': 'ABC123',
        'year': 2022,
        'timestamp': datetime.datetime.now()
    },
    {
        'available': False,
        'model': 'SUV',
        'plate': 'XYZ789',
        'year': 2021,
        'timestamp': datetime.datetime.now()
    },
    {
        'available': True,
        'model': 'Truck',
        'plate': 'DEF456',
        'year': 2020,
        'timestamp': datetime.datetime.now()
    },
    {
        'available': True,
        'model': 'Compact',
        'plate': 'GHI789',
        'year': 2019,
        'timestamp': datetime.datetime.now()
    },
    {
        'available': False,
        'model': 'Motorcycle',
        'plate': 'JKL012',
        'year': 2022,
        'timestamp': datetime.datetime.now()
    },
    {
        'available': True,
        'model': 'Electric',
        'plate': 'MNO345',
        'year': 2021,
        'timestamp': datetime.datetime.now()
    },
    {
        'available': True,
        'model': 'Convertible',
        'plate': 'PQR678',
        'year': 2020,
        'timestamp': datetime.datetime.now()
    },
    {
        'available': True,
        'model': 'Van',
        'plate': 'STU901',
        'year': 2019,
        'timestamp': datetime.datetime.now()
    },
    {
        'available': True,
        'model': 'Hybrid',
        'plate': 'VWX234',
        'year': 2022,
        'timestamp': datetime.datetime.now()
    },
    {
        'available': True,
        'model': 'Luxury',
        'plate': 'YZA567',
        'year': 2021,
        'timestamp': datetime.datetime.now()
    },
]  

def connect():
    conn = sqlite3.connect('vehicles.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS vehicles (id INTEGER PRIMARY KEY, available BOOLEAN, model TEXT, plate TEXT, year INTEGER, timestamp TEXT)")
    conn.commit()
    conn.close()
    for i in vehicles:
        vc = Vehicle(getNewId(), i['available'], i['model'],i['plate'],i['year'],i['timestamp'])
        insert(vc)

def insert(vehicle):
    conn = sqlite3.connect('vehicles.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO vehicles VALUES (?,?,?,?,?,?)", (
        vehicle.id,
        vehicle.available,
        vehicle.model,
        vehicle.plate,
        vehicle.year,
        vehicle.timestamp
    ))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('vehicles.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles")
    rows = cur.fetchall()
    vehicles = []
    for i in rows:
        vehicle = Vehicle(i[0], True if i[1] == 1 else False, i[2], i[3], i[4], i[5])
        vehicles.append(vehicle)
    conn.close()
    return vehicles

def update(vehicle):
    conn = sqlite3.connect('vehicles.db')
    cur = conn.cursor()
    cur.execute("UPDATE vehicles SET available=?, model=?, plate=?, year=?, timestamp=? WHERE id=?", (
        vehicle.available,
        vehicle.model,
        vehicle.plate,
        vehicle.year,
        vehicle.timestamp,
        vehicle.id
    ))
    conn.commit()
    conn.close()

def delete(theId):
    conn = sqlite3.connect('vehicles.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM vehicles WHERE id=?", (theId,))
    conn.commit()
    conn.close()

def deleteAll():
    conn = sqlite3.connect('vehicles.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM vehicles")
    conn.commit()
    conn.close()
