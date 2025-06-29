from flask import Flask, Blueprint, request, jsonify
from app import db
from app.models import LikePost, LikeComment
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('like_routes', __name__)

@bp.route('/like_post', methods=['POST'])
@jwt_required()
def like_post():
    data = request.json
    like = LikePost(post_id=data['post_id'], user_id= get_jwt_identity())
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Post liked'})

@bp.route('/like_comment', methods=['POST'])
@jwt_required()
def like_comment():
    data = request.json
    like = LikeComment(comment_id=data['comment_id'], user_id=get_jwt_identity())
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Comment liked'})

@bp.route('/like_post', methods=['DELETE'])
@jwt_required()
def unlike_post():
    post_id = request.args.get('post_id')
    user_id = get_jwt_identity()
    like = LikePost.query.filter_by(post_id=post_id, user_id=user_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'message': 'Post like removed'})
    return jsonify({'error': 'Like not found'}), 404

@bp.route('/like_comment', methods=['DELETE'])
@jwt_required()
def unlike_comment():
    comment_id = request.args.get('comment_id')
    user_id = get_jwt_identity()
    like = LikeComment.query.filter_by(comment_id=comment_id, user_id=user_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'message': 'Comment like removed'})
    return jsonify({'error': 'Like not found'}), 404

