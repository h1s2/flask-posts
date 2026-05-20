const createPostBtn = document.getElementById("create-post-btn");
const loadPostsBtn = document.getElementById("load-posts-btn");
const postList = document.getElementById("post-list");


createPostBtn.addEventListener("click", async () => {
  const content = document.getElementById("post-content").value;

  const res = await fetch("/posts", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ content })
  });

  const data = await res.json();
  alert(data.message);
});

loadPostsBtn.addEventListener("click", async () => {
  const res = await fetch("/posts");
  const data = await res.json();

  postList.innerHTML = "";

  data.forEach((post) => {
    const li = document.createElement("li");

    const text = document.createElement("span");
    text.textContent = post.content;

    const editBtn = document.createElement("button");
    editBtn.textContent = "수정";

    editBtn.addEventListener("click", async () => {
      const newContent = prompt("수정할 내용");

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
  });
});