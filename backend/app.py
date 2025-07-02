from flask import Flask, request, jsonify
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

# Open the json file holding all the data
with open("permits.json", "r") as file:
    permit_data = json.load(file)


# Method to retrive permits
@app.route("/permits/<zipcode>")
def get_permits(zipcode):
    permits = permit_data.get(zipcode)

    if permits is None:
        return jsonify({"error": "Zipcode not found"}), 404

    for permit in permits:
        if permit["type"] == "Electrical Upgrade":
            return jsonify(permit)

    return jsonify({"error": "no: match found"}), 404


# Method to retrive all permits
@app.route("/permits/<zipcode>/all")
def get_all_permits(zipcode):
    if not zipcode or len(zipcode) < 5:
        return jsonify({"error": "Invalid zipcode"}), 404

    permits = permit_data.get(zipcode)

    if permits is None:
        return jsonify({"error": "Zip not found"}), 404

    return jsonify(permits)


# Method to retrieve all zipcodes
@app.route("/zipcodes/", methods=["GET"])
def get_all_zipcodes():
    zip_store = []

    for key in permit_data.keys():
        zip_store.append(key)

    return jsonify(zip_store)


# Method to group permit types
@app.route("/permits/<zipcode>/grouped")
def grouped_types(zipcode):
    type_collection = {}

    permits = permit_data.get(zipcode)

    for permit in permits:
        permit_type = permit["type"]
        if permit_type not in type_collection:
            type_collection[permit_type] = []

        type_collection[permit_type].append(permit)

    return jsonify(type_collection)


# Method to retrieve all permit types
@app.route("/permits/<zipcode>/types")
def get_all_types(zipcode):
    existing = set()

    permits = permit_data.get(zipcode)

    for permit in permits:
        if permit["type"] in existing:
            continue
        else:
            existing.add(permit["type"])

    return jsonify(list(existing))


# Method to search and look up permits
@app.route("/permits/search")
def search_permits():
    keyword = request.args.get("keyword")
    results = []

    for zipcode in permit_data:
        for permit in permit_data[zipcode]:
            if keyword.lower() in permit["type"].lower():
                results.append(permit)

    return jsonify(results)


@app.route("/permits/filter")
def filter_pricing():
    filtered_fee = []

    if (request.args.get("min_fee") is None) or (request.args.get("max_fee") is None):
        return jsonify({"error": "Missing or invalid fee parameters"})

    try:
        min_fee = int(request.args.get("min_fee"))
        max_fee = int(request.args.get("max_fee"))
    except ValueError:
        return jsonify({"error": "conversion error, from string literal to int object"}), 400

    for zipcode in permit_data:
        for permit in permit_data[zipcode]:
            if min_fee <= permit["fee"] <= max_fee:
                filtered_fee.append(permit)

    return jsonify(filtered_fee)


@app.route("/permits", methods=["POST"])
def requested_permit_type():
    data = request.get_json()
    get_zipcode = data.get("zipcode")
    get_project_type = data.get("project_type")
    permits = permit_data.get(get_zipcode)

    for permit in permits:
        if permit["type"] == get_project_type:
            return jsonify(permit)

    return jsonify({"error": "no match found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
