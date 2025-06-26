from flask import Blueprint, request, jsonify
from app import db
from app.models import Post, Image

bp = Blueprint('post_routes', __name__)
@bp.route('/posts', methods=['POST'])
def create_post():
    data = request.json

    # Step 1: Create the post
    post = Post(
        user_id=data['user_id'],
        content=data.get('content'),
    )
    db.session.add(post)
    db.session.flush()  # Get post.post_id

    image_urls = data.get('image_urls', [])
    for url in image_urls:
        image = Image(post_id=post.post_id, image_url=url)
        db.session.add(image)

    # Step 3: Commit everything
    db.session.commit()

    return jsonify({'message': 'Post created', 'post_id': post.post_id})


@bp.route('/posts', methods=['GET'])
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


# Get a specific post by ID
@bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return jsonify({
            'post_id': post.post_id,
            'user_id': post.user_id,
            'content': post.content,
            'date': post.date.isoformat()
        })
    return jsonify({'error': 'Post not found'}), 404


# Delete a post by ID       
@bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted'})
    return jsonify({'error': 'Post not found'}), 404
