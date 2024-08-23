import azure.functions as func
from flask import Flask, jsonify, request
from supabase import create_client, Client

app = Flask(__name__)

property_types = ["workspace", "lounge"]

url = "https://fayafjrwupqupjltsdeg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZheWFmanJ3dXBxdXBqbHRzZGVnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQxMjEyODUsImV4cCI6MjAyOTY5NzI4NX0.br5wyl7npqttRCn88rTckdeMR7i8VNsTgPSO0f_aQOo"
supabase: Client = create_client(url, key)

@app.route('/v1/property', methods=['GET'])
def get_properties_by_type():
    property_type = request.args.get('type')

    if property_type not in property_types:
        return jsonify({"error": "Invalid property type"}), 400

    if not property_type:
        return jsonify({"error": "Property type is required."}), 400

    try:
        params = {"type_input": property_type}
        response = supabase.rpc("get_properties_by_type", params).execute()
        
        if len(response.data)== 0:
            return jsonify({"error": f"No property available of {property_type} type"}), 400
    
        else:
            return jsonify(response.data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/v1/property/<int:property_id>', methods=['GET'])
def get_property_by_id(property_id):
    try:
        params = {"id_input": property_id}
        response = supabase.rpc("get_property_by_id", params).execute()

        if len(response.data) == 0:
            return jsonify({"error": f"No property with id {property_id} found"}), 500
        else:
            return jsonify(response.data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()

