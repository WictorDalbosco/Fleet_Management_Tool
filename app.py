from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import Vehicle
import os, datetime, db

#  CORS está sendo utilizada para permitir solicitações de origens diferentes (Cross-Origin Resource Sharing)
app = Flask(__name__)
CORS(app)

# Verificar se o banco de dados já existe e, se não, criá-lo e inserir dados de teste
if not os.path.isfile('vehicles.db'):
    db.connect()

# Rota para a página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Rota para criar um novo veículo
@app.route("/request", methods=['POST'])
def postRequest():
    req_data = request.get_json()

    model = req_data['model']
    if not model:
        return jsonify({
            'status': '400',
            'res': 'failure',
            'error': 'Model is required in the request body.'
        })

    vcs = [v.serialize() for v in db.view()]

    for v in vcs:
        if v['model'] == model:
            return jsonify({
                'res': f'Error! Vehicle with model {model} is already in the fleet!',
                'status': '404'
            })

    vc = Vehicle(db.getNewId(), True, model, req_data['plate'], req_data['year'], datetime.datetime.now())
    db.insert(vc)

    return jsonify({
        'res': vc.serialize(),
        'status': '200',
        'msg': 'Success creating a new vehicle!'
    })
            
# Rota para obter todos os veículos
@app.route('/request_all', methods=['GET'])
def getRequest():
    
    content_type = request.headers.get('Content-Type')
    vcs = [v.serialize() for v in db.view()]
    
    if content_type == 'application/json':
        json_data = request.json
        print("JSON Data:", json_data)
        
    if content_type == 'application/json':
        json = request.json
        for v in vcs:
            if v['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': v,
                    'status': '200',
                    'msg': 'Success getting all vehicles in the fleet!'
                })
        return jsonify({
            'error': f"Error! Vehicle with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            # 'error': '',
            'res': vcs,
            'status': '200',
            'msg': 'Success getting all vehicles in the fleet!',
            'no_of_vehicles': len(vcs)
        })

# Rota para obter um veículo por ID
@app.route('/request/<id>', methods=['GET'])
def getRequestId(id):
    req_args = request.view_args
    vehicles = [v.serialize() for v in db.view()]

    if req_args:
        for v in vehicles:
            if v['id'] == int(req_args['id']):
                return jsonify({
                    # 'error': '',
                    'res': v,
                    'status': '200',
                    'msg': 'Success getting vehicle by ID!'
                })
        return jsonify({
            'error': f"Error! Vehicle with id '{req_args['id']}' was not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            # 'error': '',
            'res': vehicles,
            'status': '200',
            'msg': 'Success getting all vehicles!',
            'no_of_vehicles': len(vehicles)
        })

# Rota para atualizar um veículo por ID     
@app.route("/request/<id>", methods=['PUT'])
def putRequest(id):
    req_data = request.get_json()

    the_id = int(id)
    model = req_data.get('model')
    availability = req_data.get('available')
    plate = req_data.get('plate')
    year = req_data.get('year')

    # Verificar a existência do veículo pelo ID
    existing_vehicle = db.get_by_id(the_id)
    if existing_vehicle is None:
        return jsonify({
            'res': f"Error! Vehicle with ID {the_id} not found.",
            'status': '404'
        })

    # Atualizar os campos do veículo
    existing_vehicle.model = model
    existing_vehicle.available = availability
    existing_vehicle.plate = plate
    existing_vehicle.year = year
    existing_vehicle.timestamp = datetime.datetime.now()

    # Atualizar no banco de dados
    db.update(existing_vehicle)

    return jsonify({
        'res': existing_vehicle.serialize(),
        'status': '200',
        'msg': f'Success updating the vehicle with ID {the_id}!'
    })
    
# Rota para excluir um veículo por ID  
@app.route('/request/<id>', methods=['DELETE'])
def deleteRequest(id):
    req_args = request.view_args
    vcs = [v.serialize() for v in db.view()]

    if req_args:
        for v in vcs:
            if v['id'] == int(req_args['id']):
                db.delete(v['id'])
                updated_vehicles = [v.serialize() for v in db.view()]
                print('Updated vehicles: ', updated_vehicles)
                
                return jsonify({
                    'res': updated_vehicles,
                    'status': '200',
                    'msg': 'Success deleting vehicle by ID!',
                    'no_of_vehicles': len(updated_vehicles)
                })

    else:
        return jsonify({
            'error': f"Error! No Vehicle ID sent!",
            'res': '',
            'status': '404'
        })
        
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

if __name__ == '__main__':
    app.run()