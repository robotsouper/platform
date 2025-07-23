document.addEventListener("DOMContentLoaded", () => {
  const userName = localStorage.getItem("userName");
  if (userName) {
    document.getElementById("username").textContent = userName;
  }

  const signoutLink = document.getElementById("signout");
  signoutLink.addEventListener("click", () => {
    localStorage.clear();
    window.location.href = "/login.html";
  });

  loadPosts();
});

function loadPosts() {
  fetch("/posts")
    .then(res => res.json())
    .then(posts => {
      const cardPanel = document.getElementById("cardPanel");
      cardPanel.innerHTML = "";
      posts.forEach(post => {
        const postCard = buildPostCard(post);
        cardPanel.appendChild(postCard);
        loadComments(post.post_id);
      });
    });
}

function buildPostCard(post) {
  const card = document.createElement("div");
  card.className = "card";
  card.innerHTML = `
    <div class="postHeader">
      <img src="${post.user_photo_url}" alt="profile" class="profilePhoto"/>
      <div class="postUser">${post.username}</div>
    </div>
    ${post.image_url ? `
      <div class="postPic">
        <img src="${post.image_url}" alt="postPic"/>
      </div>
    ` : ''}
    <div class="postContent">
      <div class="realContent">
        <p>${post.content}</p>
      </div>      
      <div class="icons">
        <div class="threeIcons">
          <em class="far fa-heart" data-postid="${post.post_id}"></em>
          <em class="far fa-comment"></em>
          <em class="far fa-paper-plane"></em>
        </div>
        <div><em class="far fa-bookmark"></em></div>
      </div>
      <div class="comments" id="comments-${post.post_id}"></div>
      <div class="addCommentSection">
        <div class="addComment">
          <em class="far fa-smile"></em>
          <input placeholder="Add a comment" id="commentInput-${post.post_id}"/>
        </div>
        <button onclick="addComment(${post.post_id})">Post</button>
      </div>
    </div>
  `;
  return card;
}

function loadComments(postId) {
  fetch(`/comments/${postId}`)
    .then(res => res.json())
    .then(comments => {
      const currentUserId = parseInt(localStorage.getItem("userId"));
      const commentsContainer = document.getElementById(`comments-${postId}`);
      commentsContainer.innerHTML = "";

      comments.forEach(c => {
        const commentEl = document.createElement("div");
        commentEl.className = "comment";
        commentEl.innerHTML = `
          <p class="postUser"><strong>${c.user_id}</strong></p>
          <p>${c.content}</p>
        `;

        if (c.user_id === currentUserId) {
          commentEl.addEventListener("contextmenu", e => {
            e.preventDefault();
            showDeletePopup(e.pageX, e.pageY, c.comment_id, postId);
          });
        }

        commentsContainer.appendChild(commentEl);
      });
    });
}

function showDeletePopup(x, y, commentId, postId) {
  const existing = document.querySelector(".delete-popup");
  if (existing) existing.remove();

  const popup = document.createElement("div");
  popup.textContent = "Delete";
  popup.className = "delete-popup";
  popup.style.position = "absolute";
  popup.style.top = `${y}px`;
  popup.style.left = `${x}px`;
  popup.style.background = "#fff";
  popup.style.border = "1px solid #ccc";
  popup.style.padding = "5px 10px";
  popup.style.cursor = "pointer";
  popup.style.zIndex = 1000;

  popup.onclick = () => {
    const token = localStorage.getItem("token");
    fetch(`/comments/${commentId}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
    .then(res => res.json())
    .then(() => {
      popup.remove();
      loadComments(postId);
    })
    .catch(err => alert(err.message));
  };

  document.body.appendChild(popup);
  document.addEventListener("click", () => popup.remove(), { once: true });
}

function addComment(postId) {
  const input = document.getElementById(`commentInput-${postId}`);
  const content = input.value.trim();
  if (!content) return;

  const userId = parseInt(localStorage.getItem("userId"));
  fetch("/comments", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      post_id: postId,
      user_id: userId,
      content: content
    })
  })
  .then(res => res.json())
  .then(() => {
    loadComments(postId);
    input.value = "";
  });
}

document.addEventListener("click", e => {
  if (e.target.classList.contains("fa-heart")) {
    const postId = e.target.dataset.postid;
    const isLiked = e.target.classList.contains("fas");
    const userId = parseInt(localStorage.getItem("userId"));

    if (!isLiked) {
      fetch("/like_post", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          post_id: postId,
          user_id: userId
        })
      }).then(() => {
        e.target.classList.remove("far");
        e.target.classList.add("fas");
      });
    } else {
      fetch(`/like_post?post_id=${postId}&user_id=${userId}`, {
        method: "DELETE"
      }).then(() => {
        e.target.classList.remove("fas");
        e.target.classList.add("far");
      });
    }
  }
});
