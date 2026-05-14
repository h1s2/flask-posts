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
    li.textContent = `${post.id} / ${post.content}`
    postList.appendChild(li);
  });
});