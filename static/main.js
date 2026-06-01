const createPostBtn = document.getElementById("create-post-btn");
const loadPostsBtn = document.getElementById("load-posts-btn");
const signupBtn = document.getElementById("signup-btn");
const postList = document.getElementById("post-list");


async function renderPost(post) {
  const li = document.createElement("li");

  const text = document.createElement("span");
  text.textContent = post.content;

  const editBtn = document.createElement("button");
  editBtn.textContent = "수정";

  editBtn.addEventListener("click", async () => {
    const newContent = prompt("수정할 내용");

    if (!newContent?.trim()) {
      return;
    }

    await fetch(`/posts/${post.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        content: newContent
      })
    });

    text.textContent = newContent;
  });

  const deleteBtn = document.createElement("button");
  deleteBtn.textContent = "삭제";

  deleteBtn.addEventListener("click", async () => {
    await fetch(`/posts/${post.id}`, {
      method: "DELETE"
    });

    li.remove();
  });

  li.append(text, editBtn, deleteBtn);
  postList.appendChild(li);
}

async function loadPosts() {
  const res = await fetch("/posts");
  const data = await res.json();

  postList.innerHTML = "";

  data.forEach((post) => {
    renderPost(post);
  });
}

createPostBtn.addEventListener("click", async () => {
  const content = document.getElementById("post-content").value;

  if (!content?.trim()) {
      return;
    }

  await fetch("/posts", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ content })
  });

  await loadPosts();
});

signupBtn.addEventListener("click", async () => {
  const signupUsername = document.getElementById("signup-username").value;
  const signupPassword = document.getElementById("signup-password").value;

  const res = await fetch("/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username: signupUsername,
      password: signupPassword
    })
  });

  const data = await res.json();
  alert(data.message);
});

loadPosts();