const createPostBtn = document.getElementById("create-post-btn");
const loadPostsBtn = document.getElementById("load-posts-btn");
const signupBtn = document.getElementById("signup-btn");
const loginBtn = document.getElementById("login-btn");
const logoutBtn = document.getElementById("logout-btn");
const postList = document.getElementById("post-list");

async function checkLoginStatus() {
  const res = await fetch("/me");
  const data = await res.json()

  if (data.loggedIn) {
    loginBtn.classList.add("hidden");
    logoutBtn.classList.remove("hidden");
  } else {
    loginBtn.classList.remove("hidden");
    logoutBtn.classList.add("hidden");
  }
}

async function renderPost(post) {
  const li = document.createElement("li");

  const text = document.createElement("span");
  text.textContent = `${post.content} / ${post.user_id}`;

  const editBtn = document.createElement("button");
  editBtn.textContent = "수정";

  editBtn.addEventListener("click", async () => {
    const newContent = prompt("수정할 내용");

    if (!newContent?.trim()) {
      return;
    }

    const res = await fetch(`/posts/${post.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        content: newContent
      })
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.message);
      return;
    }

    text.textContent = `${newContent} / ${post.user_id}`;
  });

  const deleteBtn = document.createElement("button");
  deleteBtn.textContent = "삭제";

  deleteBtn.addEventListener("click", async () => {
    const res = await fetch(`/posts/${post.id}`, {
      method: "DELETE"
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.message);
      return;
    }

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

  const res = await fetch("/posts", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ content })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.message);
    return;
  }

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

loginBtn.addEventListener("click", async () => {
  const loginUsername = document.getElementById("login-username").value;
  const loginPassword = document.getElementById("login-password").value;

  const res = await fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username: loginUsername,
      password: loginPassword
    })
  });

  if (res.ok) {
    loginBtn.classList.add("hidden");
    logoutBtn.classList.remove("hidden");
  } else {
    const data = await res.json();
    alert(data.message);
  }
});

logoutBtn.addEventListener("click", async () => {
  const res = await fetch("/logout", {
    method: "POST"
  });

  if (res.ok) {
    loginBtn.classList.remove("hidden");
    logoutBtn.classList.add("hidden");
  } else {
    const data = await res.json();
    alert(data.message);
  }
});

checkLoginStatus();
loadPosts();