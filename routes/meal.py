from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from database import db
from models.meal import Meal

meal_bp = Blueprint('meal', __name__, url_prefix='/api/meals')

@meal_bp.route('', methods=['POST'])
@login_required
def create_meal():
    """
    Registar uma nova refeição
    ---
    tags:
      - Refeições
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - is_in_diet
          properties:
            name:
              type: string
              example: Almoço Balanceado
            description:
              type: string
              example: Arroz integral, frango grelhado e salada
            date_time:
              type: string
              example: 2026-04-12T12:30:00
            is_in_diet:
              type: boolean
              example: true
    responses:
      201:
        description: Refeição registada com sucesso
      400:
        description: Campos obrigatórios em falta ou dados inválidos
    """
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
    """
    Listar todas as refeições do utilizador autenticado
    ---
    tags:
      - Refeições
    responses:
      200:
        description: Lista de refeições retornada com sucesso
    """
    meals = Meal.query.filter_by(user_id=current_user.id).all()
    return jsonify([meal.to_dict() for meal in meals]), 200

@meal_bp.route('/metrics', methods=['GET'])
@login_required
def get_metrics():
    """
    Obter estatísticas e métricas de dieta do utilizador
    ---
    tags:
      - Refeições
    responses:
      200:
        description: Métricas calculadas com sucesso (total, dentro da dieta, fora da dieta e percentagem de adesão)
    """
    user_meals = Meal.query.filter_by(user_id=current_user.id).all()
    
    total_meals = len(user_meals)
    in_diet_count = sum(1 for meal in user_meals if meal.is_in_diet)
    out_diet_count = total_meals - in_diet_count
    
    metrics = {
        "total_meals": total_meals,
        "in_diet_count": in_diet_count,
        "out_diet_count": out_diet_count,
        "adherence_percentage": (in_diet_count / total_meals * 100) if total_meals > 0 else 0
    }
    
    return jsonify(metrics), 200

@meal_bp.route('/<int:meal_id>', methods=['GET'])
@login_required
def get_meal(meal_id):
    """
    Obter os detalhes de uma refeição específica
    ---
    tags:
      - Refeições
    parameters:
      - name: meal_id
        in: path
        type: integer
        required: true
        description: ID da refeição
    responses:
      200:
        description: Detalhes da refeição encontrados
      404:
        description: Refeição não encontrada ou não pertence ao utilizador
    """
    meal = Meal.query.filter_by(id=meal_id, user_id=current_user.id).first()
    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404
    
    return jsonify(meal.to_dict()), 200

@meal_bp.route('/<int:meal_id>', methods=['PUT'])
@login_required
def update_meal(meal_id):
    """
    Atualizar uma refeição existente
    ---
    tags:
      - Refeições
    parameters:
      - name: meal_id
        in: path
        type: integer
        required: true
        description: ID da refeição
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            date_time:
              type: string
            is_in_diet:
              type: boolean
    responses:
      200:
        description: Refeição atualizada com sucesso
      404:
        description: Refeição não encontrada
    """
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
    """
    Eliminar uma refeição
    ---
    tags:
      - Refeições
    parameters:
      - name: meal_id
        in: path
        type: integer
        required: true
        description: ID da refeição
    responses:
      200:
        description: Refeição deletada com sucesso
      404:
        description: Refeição não encontrada
    """
    meal = Meal.query.filter_by(id=meal_id, user_id=current_user.id).first()
    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404

    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": "Refeição deletada com sucesso!"}), 200