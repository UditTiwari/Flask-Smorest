import uuid
from flask import Flask,jsonify , request
from flask_smorest import abort
from db import items,stores

app = Flask(__name__)


#400 -BAD   REQUEST
#404 -PAGE NOT FOUND/tHE REQUESTED url WAS NOT FOUND
#201 - Created success status



@app.route('/store',methods=['GET'])
def get_stores():
    return {'stores':list(stores.values())}

@app.route('/store/<string:store_id>',methods=['GET'])
def get_store(store_id):
    try:  
        return stores[store_id]
    except KeyError:
        abort(404,message="Store not found.")


@app.route('/store',methods=['POST'])
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload.",
        )
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")

    store_id = uuid.uuid4().hex
    store = {**store_data,"id":store_id}
    stores[store_id] = store
    return store , 201


@app.route("/store/<string:store_id>",methods=['DELETE'])
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")



# @app.route('/item',methods=['POST'])
# def create_item():
#     item_data = request.get_json()
#     if (
#         "price" not in item_data
#         or "store_id" not in item_data
#         or "name" not in item_data
#     ):
#         abort(
#             400,
#             message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
#         )
#     #check that we dont add item same already exist
#     for item in items.values():
#         if (
#             item_data["name"] == item["name"]
#             and item_data["store_id"] == item["store_id"]
#         ):
#             abort(400, message=f"Item already exists.")

#     if item_data["store_id"] not in stores:
#          abort(404,message="Store not found.")
    
#     item_id = uuid.uuid4().hex
#     item = {**item_data,"id":item_id}
#     item[item_id] = item
    
#     return item , 201

#get all items
@app.route('/item',methods=['GET'])
def get_all_items():
    return jsonify({'stores':list(items.values())})


@app.route('/item/<string:item_id>',methods=['GET'])
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404,message="Item not found.")


@app.post("/item")
def create_item():
    item_data = request.get_json()
    # Here not only we need to validate data exists,
    # But also what type of data. Price should be a float,
    # for example.
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
        )
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item



@app.route('/item/<string:item_id>',methods=['DELETE'])
def delete_item(item_id):
    try:
        del items[item_id]
        return {"messgae":"Item deleted"}
    except KeyError:
        abort(404,message="Item not found.")

@app.route("/item/<string:item_id>",methods=['PUT'])
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(
            400,
            message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
        )
    try:
        item = items[item_id]
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found.")









if __name__=='__main__':
    app.run(debug=True)