from flask import Flask, jsonify, request
import psycopg2


# https://spaces-property-service.azurewebsites.net/v1/property/3


DB_CONFIG = {
    'host': "aws-0-ap-south-1.pooler.supabase.com",
    'database': "postgres",
    'user': "postgres.fayafjrwupqupjltsdeg",
    'password': "@Satwikkr055"
}

connection = psycopg2.connect(**DB_CONFIG)
cursor = connection.cursor()
app = Flask(__name__)

property_types = ["WORKSPACE", "LOUNGE"]


@app.route('/v1/property', methods=['GET'])
def get_properties_by_type():
    property_type = request.args.get('type')

    try:
        if property_type not in property_types:
            raise Exception("Invalid property type")

        if not property_type:
            raise Exception("Property type is required")

        cursor.callproc('get_properties_by_type', [property_type])
        response = cursor.fetchone()

        if response is None:
            raise Exception(f"No property available of {property_type} type")

        else:
            columns = [desc[0] for desc in cursor.description]
            response_dict = dict(zip(columns, response))
            return jsonify(response_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/v1/property/<int:property_id>', methods=['GET'])
def get_property_by_id(property_id):
    try:
        cursor.callproc('get_property_by_id', [property_id])

        response = cursor.fetchone()

        if response is None:
            return jsonify({"error": f"No property with id {property_id} found"}), 400
        else:
            columns = [desc[0] for desc in cursor.description]
            response_dict = dict(zip(columns, response))
            return jsonify(response_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World"


if __name__ == '__main__':
    app.run()
