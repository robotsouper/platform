document.addEventListener("DOMContentLoaded", () => {
  const userName = localStorage.getItem("userName");
  if (userName) {
    document.getElementById("username").textContent = userName;
  }
  const signoutLink = document.getElementById("signout");
  signoutLink.addEventListener("click", () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userName");
    localStorage.removeItem("userId");
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
      const commentsContainer = document.getElementById(`comments-${postId}`);
      commentsContainer.innerHTML = comments.map(c => `
        <div class="comment">
          <img src="${c.user_photo_url}" class="profilePhoto" />
          <p class="postUser"><strong>${c.username}</strong></p>
          <p>${c.content}</p>
        </div>
      `).join("");
    });
}

function addComment(postId) {
  const input = document.getElementById(`commentInput-${postId}`);
  const content = input.value.trim();
  if (!content) return;

  fetch("/comments", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      post_id: postId,
      user_id: 1,  // static user id for testing, replace with actual user id after auth
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

    if (!isLiked) {
      // like
      fetch("/like_post", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          post_id: postId,
          user_id: 1  // static user id for testing
        })
      }).then(() => {
        e.target.classList.remove("far");
        e.target.classList.add("fas");
      });
    } else {
      // unlike
      fetch(`/like_post?post_id=${postId}&user_id=1`, {
        method: "DELETE"
      }).then(() => {
        e.target.classList.remove("fas");
        e.target.classList.add("far");
      });
    }
  }
});
