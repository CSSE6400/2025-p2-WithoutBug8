from flask import Blueprint, jsonify, request
from todo.models import db
from todo.models.todo import Todo
from datetime import datetime, timedelta
 
api = Blueprint('api', __name__, url_prefix='/api/v1') 

TEST_ITEM = {
    "id": 1,
    "title": "Watch CSSE6400 Lecture",
    "description": "Watch the CSSE6400 lecture on ECHO360 for week 1",
    "completed": True,
    "deadline_at": "2023-02-27T00:00:00",
    "created_at": "2023-02-20T00:00:00",
    "updated_at": "2023-02-20T00:00:00"
}
 
@api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})


@api.route('/todos', methods=['GET'])
def get_todos():
    """Return the list of todo items"""
    result = []
    # 添加completed 过滤逻辑
    # 获取HTTP请求参数中的completed参数，返回值为True或False或者空
    completed = request.args.get('completed')
    # 获取HTTP请求参数中的window参数，该值用于查询截止日期window天内的任务
    window = request.args.get('window')
    # 这里处理completed参数
    if completed is not None:
        if completed.lower() == 'true':
            todos = Todo.query.filter_by(completed=True).all()
        elif completed.lower() == 'false':
            todos = Todo.query.filter_by(completed=False).all()
        else:
            todos = Todo.query.all() # 返回所有值              
    else:
        todos = Todo.query.all() # 返回所有值
    # 这里处理window参数
    if window is not None:
        window = int(window)
        cutoff = datetime.now() + timedelta(days=window)
        todos = Todo.query.filter(Todo.deadline_at <= cutoff).all()

    for todo in todos:
        result.append(todo.to_dict())
    return jsonify(result),200

@api.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Return the details of a todo item"""
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error':'Todo not found'}),404
    return jsonify(todo.to_dict())

@api.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo item and return the created item"""
    data = request.json
    # 添加允许添加的字段，避免恶意添加
    allowed_fields = {'title','description','completed','deadline_at'}
    # 检查是否包含额外字段
    if set(data.keys()) - allowed_fields:
        return jsonify({'error': 'Extra fields not allowed'}), 400
    
    # 添加 title 不能空的检查
    if "title" not in data:
        return jsonify({'error':'Title is required'}),400

    todo = Todo(
        title = data.get('title'),
        description = data.get('description'),
        completed = data.get('completed',False),
    )
    if 'deadline_at' in data:
        todo.deadline_at = datetime.fromisoformat(data.get('deadline_at'))
    
    # adds a new record to the database or will update an existing record
    db.session.add(todo)
    # Commits the change to the database
    # This must be called for the changes to be saved
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@api.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo item and return the updated item"""
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo not found'}),404
    # 一般来说id是主键，主键一般不会被修改
    if 'id' in request.json and request.json['id'] != todo_id:
        return jsonify({'error': 'You motherfucker! Cannot change the id'}),400
    
    # 添加允许添加的字段，避免恶意添加
    allowed_fields = {'title','description','completed','deadline_at'}
    # 检查是否包含额外字段
    if set(request.json.keys()) - allowed_fields:
        return jsonify({'error': 'Extra fields not allowed'}), 400
    
    todo.title = request.json.get('title',todo.title)
    todo.description = request.json.get('description',todo.description)
    todo.completed = request.json.get('completed',todo.completed)
    todo.deadline_at = request.json.get('deadline_at',todo.deadline_at)
    db.session.commit()

    return jsonify(todo.to_dict())

@api.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo item and return the deleted item"""
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({}),200
    db.session.delete(todo)
    db.session.commit()
    return jsonify(todo.to_dict()),200
    
 
