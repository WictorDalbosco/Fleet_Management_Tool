# Definição da classe Vehicle
class Vehicle:
  # Construtor da classe, inicializando as propriedades do veículo
  def __init__(self, id,available, model, plate, year, timestamp):
    self.id = id  # ID único do veículo
    self.available = available  # Indica se o veículo está disponível
    self.model = model  # Modelo do veículo
    self.plate = plate  # Placa do veículo
    self.year = year  # Ano de fabricação do veículo
    self.timestamp = timestamp  # Timestamp (data e hora) do registro do veículo

  # Método especial para representação textual do objeto (usado para debug)
  def __repr__(self):
    return '<id {}>'.format(self.id)

  # Método para serializar o objeto em um formato JSON-like
  def serialize(self):
    return {
      'id': self.id,
      'available': self.available,
      'model': self.model,
      'plate': self.plate,
      'year': self.year,
      'timestamp':self.timestamp
    }