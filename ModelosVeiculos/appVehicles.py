from flask import Flask, render_template, request, jsonify
import os, re, datetime
import db
from modelsVehicles import Vehicle

app = Flask(__name__)

# create the database and table. Insert 10 test books into db
# Do this only once to avoid inserting the test books into 
# the db multiple times
if not os.path.isfile('vehicles.db'):
    db.connect()

# route for landing page
# check out the template folder for the index.html file
# check out the static folder for css and js files
@app.route("/")
def index():
    return render_template("index.html")

def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False


@app.route("/request", methods=['POST'])
def postRequest():
    req_data = request.get_json()
    email = req_data['email']
    if not isValid(email):
        return jsonify({
            'status': '422',
            'res': 'failure',
            'error': 'Invalid email format. Please enter a valid email address'
        })
    
    model = req_data['model']
    vcs = [v.serialize() for v in db.view()]
    
    for v in vcs:
        if v['model'] == model:
            return jsonify({
                # 'error': '',
                'res': f'Error ⛔❌! Vehicle with model {model} is already in the fleet!',
                'status': '404'
            })
            
    vc = Vehicle(db.getNewId(), True, model, req_data['plate'], req_data['year'], datetime.datetime.now())
    print('New vehicle: ', v.serialize())
    db.insert(vc)
    
    updated_vehicles = [v.serialize() for v in db.view()]
    print('Vehicles in fleet: ', updated_vehicles)
    
    return jsonify({
        # 'error': '',
        'res': vc.serialize(),
        'status': '200',
        'msg': 'Success creating a new vehicle!👍😀'
    })
            

@app.route('/request', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    vcs = [v.serialize() for v in db.view()]
    
    if content_type == 'application/json':
        json = request.json
        for v in vcs:
            if v['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': v,
                    'status': '200',
                    'msg': 'Success getting all vehicles in the fleet!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Vehicle with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            # 'error': '',
            'res': vcs,
            'status': '200',
            'msg': 'Success getting all vehicles in the fleet!👍😀',
            'no_of_vehicles': len(vcs)
        })


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
                    'msg': 'Success getting vehicle by ID!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Vehicle with id '{req_args['id']}' was not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            # 'error': '',
            'res': vehicles,
            'status': '200',
            'msg': 'Success getting all vehicles!👍😀',
            'no_of_vehicles': len(vehicles)
        })
        
@app.route("/request", methods=['PUT'])
def putRequest():
    req_data = request.get_json()
    availability = req_data['available']
    model = req_data['model']
    the_id = req_data['id']
    plate = req_data['plate']
    year = req_data['year']
    
    vcs = [v.serialize() for v in db.view()]

    for v in vcs:
        if v['id'] == the_id:
            vc = Vehicle(
                the_id,
                availability,
                model,
                plate,
                year,
                datetime.datetime.now()
            )
            print('new vechicle: ', vc.serialize())
            db.update(vc)
            updated_vehicles = [v.serialize() for v in db.view()]

            print('Vehicles in fleet: ', updated_vehicles)
            
            return jsonify({
                # 'error': '',
                'res': vc.serialize(),
                'status': '200',
                'msg': f'Success updating the vehicle with model {model}!👍😀'
            })

    return jsonify({
        'res': f'Error ⛔❌! Failed to update vehicle with model: {model}!',
        'status': '404'
    })
    
    
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
                    'msg': 'Success deleting vehicle by ID!👍😀',
                    'no_of_vehicles': len(updated_vehicles)
                })

    else:
        return jsonify({
            'error': f"Error ⛔❌! No Vehicle ID sent!",
            'res': '',
            'status': '404'
        })

if __name__ == '__main__':
    app.run()