from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fruits.db'
db = SQLAlchemy(app)


class Fruit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fruit = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)


# Create the database tables
with app.app_context():
    db.create_all()


# Endpoint to return all fruits in JSON format
@app.route('/fruits', methods=['GET'])
def get_all_fruits():
    all_fruits = Fruit.query.all()
    fruits_list = [{"id": fruit.id, "fruit": fruit.fruit, "color": fruit.color} for fruit in
                   all_fruits]  # returning it in a readable format
    return jsonify(fruits_list)


# Endpoint to return a specific fruit in JSON format
@app.route('/fruits/<int:fruit_id>', methods=['GET'])
def get_specific_fruit(fruit_id):
    fruit = Fruit.query.get(fruit_id)
    if fruit:
        return jsonify({"id": fruit.id, "fruit": fruit.fruit, "color": fruit.color})
    else:
        return jsonify({"error": "Fruit not found"}), 404


# Endpoint to add a fruit to the basket by sending a JSON payload
@app.route('/fruits', methods=['POST'])
def add_fruit_to_basket():
    data = request.get_json()
    if 'fruit' in data and 'color' in data:
        new_fruit = Fruit(fruit=data['fruit'], color=data['color'])
        db.session.add(new_fruit)
        db.session.commit()
        return jsonify({"message": "Fruit added successfully"}), 201
    else:
        return jsonify({"error": "Invalid request"}), 400


if __name__ == '__main__':
    app.run(debug=True)
