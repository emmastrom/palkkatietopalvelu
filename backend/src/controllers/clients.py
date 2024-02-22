from flask import request, jsonify
from app import app
from utilities import client_methods as clients
from utilities import client_user
from utilities.require_login import require_login
from utilities.require_admin import require_admin

@app.route("/api/clients")
@require_login
def get_clients():
    try:
        all_clients = clients.get_clients()
        return jsonify(all_clients)
    # tähän pitäisi ideaalisti antaa tarkemmat tiedot exceptionista
    except Exception as error: # pylint: disable=broad-except
        return str(error), 400

@app.route("/api/client/<int:client_id>", methods=["GET"])
@require_login
def get_client(client_id):
    try:
        client_data = clients.get_client_data(client_id)
        if client_data:
            return jsonify(client_data), 200
        return jsonify({'message': 'Asiakasta ei löytynyt'}), 404
    # tähän pitäisi ideaalisti antaa tarkemmat tiedot exceptionista
    except Exception as error: # pylint: disable=broad-except
        return str(error), 400

@app.route("/api/client", methods=["POST"])
@require_login
@require_admin
def add_client():
    try:
        client_data = request.json
        clients.validate_client_data(client_data)
        clients.validate_email(client_data)
        clients.add_client(client_data)
        client_user.create_client_user(client_data.get("email"))
        return "Client added successfully", 201
    # tähän pitäisi ideaalisti antaa tarkemmat tiedot exceptionista
    except Exception as error: # pylint: disable=broad-except
        return str(error), 400

@app.route("/api/client/<int:client_id>", methods=["POST"])
@require_login
@require_admin
def update_client(client_id):
    try:
        client_data = request.json
        updated_client = clients.update_client(client_id, client_data)
        return jsonify(updated_client), 200
    except Exception as error:  # pylint: disable=broad-except
        return str(error), 400

@app.route("/api/client/<int:client_id>", methods=["DELETE"])
@require_login
@require_admin
def delete_client(client_id):
    try:
        clients.delete_client(client_id)
        return "Asiakas poistettu", 200
    except Exception as error:  # pylint: disable=broad-except
        return str(error), 400
