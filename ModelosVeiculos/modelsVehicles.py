class Vehicle:
  def __init__(self, id,available, model, plate, year, timestamp):
    self.id = id
    self.available = available
    self.model = model
    self.plate = plate
    self.year = year
    self.timestamp = timestamp

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def serialize(self):
    return {
      'id': self.id,
      'available': self.available,
      'model': self.model,
      'plate': self.plate,
      'year': self.year,
      'timestamp':self.timestamp
    }