from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from database import db
from models.meal import Meal

meal_bp = Blueprint('meal', __name__, url_prefix='/api/meals')

@meal_bp.route('', methods=['POST'])
@login_required
def create_meal():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    date_time_str = data.get('date_time')
    is_in_diet = data.get('is_in_diet')

    if not name or is_in_diet is None:
        return jsonify({"message": "Campos 'name' e 'is_in_diet' são obrigatórios"}), 400

    date_time = datetime.fromisoformat(date_time_str) if date_time_str else datetime.utcnow()

    meal = Meal(
        name=name,
        description=description,
        date_time=date_time,
        is_in_diet=bool(is_in_diet),
        user_id=current_user.id
    )

    db.session.add(meal)
    db.session.commit()

    return jsonify({"message": "Refeição registrada com sucesso!", "meal": meal.to_dict()}), 201

@meal_bp.route('', methods=['GET'])
@login_required
def list_meals():
    # Lista APENAS as refeições do usuário autenticado
    meals = Meal.query.filter_by(user_id=current_user.id).all()
    return jsonify([meal.to_dict() for meal in meals]), 200

@meal_bp.route('/<int:meal_id>', methods=['GET'])
@login_required
def get_meal(meal_id):
    meal = Meal.query.filter_by(id=meal_id, user_id=current_user.id).first()
    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404
    
    return jsonify(meal.to_dict()), 200

@meal_bp.route('/<int:meal_id>', methods=['PUT'])
@login_required
def update_meal(meal_id):
    meal = Meal.query.filter_by(id=meal_id, user_id=current_user.id).first()
    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404

    data = request.get_json()
    meal.name = data.get('name', meal.name)
    meal.description = data.get('description', meal.description)
    meal.is_in_diet = data.get('is_in_diet', meal.is_in_diet)
    
    if data.get('date_time'):
        meal.date_time = datetime.fromisoformat(data.get('date_time'))

    db.session.commit()
    return jsonify({"message": "Refeição atualizada com sucesso!", "meal": meal.to_dict()}), 200

@meal_bp.route('/<int:meal_id>', methods=['DELETE'])
@login_required
def delete_meal(meal_id):
    meal = Meal.query.filter_by(id=meal_id, user_id=current_user.id).first()
    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404

    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": "Refeição deletada com sucesso!"}), 200