from flask import Blueprint, request, jsonify
from app import db
from app.models import Comment

bp = Blueprint('comment_routes', __name__)

@bp.route('/comments', methods=['POST'])
def add_comment():
    data = request.json

    comment = Comment(
        post_id=data['post_id'],
        parent_comment_id=data.get('parent_comment_id'),  # nullable
        user_id=data['user_id'],
        content=data.get('content')
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added', 'comment_id': comment.comment_id})

@bp.route('/comments/<int:post_id>', methods=['GET'])
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
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comment deleted'})
    return jsonify({'error': 'Comment not found'}), 404
