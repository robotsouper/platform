from flask import Blueprint, request, jsonify
from app import db
from app.models import Comment
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('comment_routes', __name__)

@bp.route('/comments', methods=['POST'])
# @jwt_required()
def add_comment():
    data = request.json
    user_id = get_jwt_identity()

    comment = Comment(
        post_id=data['post_id'],
        parent_comment_id=data.get('parent_comment_id'),  # nullable
        user_id=user_id,
        content=data.get('content')
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added', 'comment_id': comment.comment_id})

@bp.route('/comments/<int:post_id>', methods=['GET'])
# @jwt_required()
def get_all_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date.asc()).all()
    return jsonify([
        {
            'comment_id': c.comment_id,
            'user_id': c.user_id,
            'parent_comment_id': c.parent_comment_id,
            'content': c.content,
            'date': c.date.isoformat()
        }
        for c in comments
    ])

@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
# @jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    if comment.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'})
