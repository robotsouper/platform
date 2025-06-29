from flask import Blueprint, request, jsonify
from app import db
from app.models import Post, Image
from flask_jwt_extended import jwt_required, get_jwt_identity


bp = Blueprint('post_routes', __name__)
@jwt_required()
@bp.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    user_id = get_jwt_identity()

    post = Post (
        user_id= user_id,
        content=data.get('content'),
    )
    db.session.add(post)
    db.session.flush()  

    image_urls = data.get('image_urls', [])
    for url in image_urls:
        image = Image(post_id=post.post_id, image_url=url)
        db.session.add(image)

    db.session.commit()

    return jsonify({'message': 'Post created', 'post_id': post.post_id})


@bp.route('/posts', methods=['GET'])
@jwt_required()
def get_all_posts():
    posts = Post.query.order_by(Post.date.desc()).all()
    return jsonify([
        {
            'post_id': p.post_id,
            'user_id': p.user_id,
            'content': p.content,
            'date': p.date.isoformat()
        }
        for p in posts
    ])

@bp.route('/my_posts', methods=['GET'])
@jwt_required()
def get_my_posts():
    user_id = get_jwt_identity()
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.date.desc()).all()
    return jsonify([
        {
            'post_id': p.post_id,
            'content': p.content,
            'date': p.date.isoformat()
        }
        for p in posts
    ])

@bp.route('/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    post = Post.query.get(post_id)
    user_id = get_jwt_identity()
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    if post.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'})

  
@bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted'})
    return jsonify({'error': 'Post not found'}), 404
