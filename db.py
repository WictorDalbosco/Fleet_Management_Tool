import sqlite3, random
from datetime import datetime
from models import Vehicle

# Gera IDs para novas instâncias
def getNewId():
    return random.getrandbits(28)

# Lista de veículos de exemplo
vehicles = [
    {
        'available': True,
        'model': 'Ônibus Convencional',
        'plate': 'ABC1D23',
        'year': 2022,
        'timestamp': datetime.now()
    },
    {
        'available': False,
        'model': 'Ônibus Articulado',
        'plate': 'XYZ8W9V',
        'year': 2021,
        'timestamp': datetime.now()
    },
    {
        'available': True,
        'model': 'Micro-Ônibus',
        'plate': 'DEF4G56',
        'year': 2020,
        'timestamp': datetime.now()
    },
    {
        'available': True,
        'model': 'BRT',
        'plate': 'GHI7J89',
        'year': 2019,
        'timestamp': datetime.now()
    },
    {
        'available': False,
        'model': 'Ônibus Elétrico',
        'plate': 'JKL0M12',
        'year': 2022,
        'timestamp': datetime.now()
    },
    {
        'available': True,
        'model': 'Ônibus Híbrido',
        'plate': 'MNO3P45',
        'year': 2021,
        'timestamp': datetime.now()
    },
    {
        'available': True,
        'model': 'Double-Decker',
        'plate': 'PQR6S78',
        'year': 2020,
        'timestamp': datetime.now()
    },
    {
        'available': True,
        'model': 'Ônibus Escolar',
        'plate': 'STU9V01',
        'year': 2019,
        'timestamp': datetime.now()
    },
    {
        'available': True,
        'model': 'Ônibus Expresso',
        'plate': 'VWX2Y34',
        'year': 2022,
        'timestamp': datetime.now()
    },
    {
        'available': True,
        'model': 'Ônibus Executivo',
        'plate': 'YZA5B67',
        'year': 2021,
        'timestamp': datetime.now()
    },
]

# Conecta ao banco de dados e cria a tabela se não existir
def connect():
    conn = sqlite3.connect('vehicles.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS vehicles (id INTEGER PRIMARY KEY, available BOOLEAN, model TEXT, plate TEXT, year INTEGER, timestamp TEXT)")
    conn.commit()
    conn.close()
    
    # Insere os veículos na tabela
    for i in vehicles:
        vehicle = Vehicle(getNewId(), i['available'], i['model'],i['plate'],i['year'],i['timestamp'])
        insert(vehicle)

# Insere um veículo na tabela
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

# Retorna uma lista de todos os veículos na tabela
def view():
    conn = sqlite3.connect('vehicles.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles")
    rows = cur.fetchall()
    vehicles = []
    for i in rows:
        vehicle = Vehicle(i[0], i[1], i[2], i[3], i[4], i[5])
        vehicles.append(vehicle)
    conn.close()
    return vehicles

# Atualiza os detalhes de um veículo na tabela
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

# Deleta um veículo da tabela usando o ID
def delete(theId):
    conn = sqlite3.connect('vehicles.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM vehicles WHERE id=?", (theId,))
    conn.commit()
    conn.close()

# Deleta todos os veículos da tabela
def deleteAll():
    conn = sqlite3.connect('vehicles.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM vehicles")
    conn.commit()
    conn.close()

# Retorna um veículo específico com base no ID 
def get_by_id(vehicle_id):
    vehicles = view() 
    for vehicle in vehicles:
        if vehicle.id == vehicle_id:
            return vehicle
    return None  # Retorna None se o veículo não for encontrado
