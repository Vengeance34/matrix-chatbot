async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  addMessage("You", message, "user");
  input.value = "";

  const response = await fetch("https://matrix-chatbot-jsq6.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  const data = await response.json();
  addMessage("Bot", data.reply, "bot");
}

function addMessage(sender, text, cls) {
  const box = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = "message " + cls;
  div.innerHTML = `<strong>${sender}:</strong> ${text}`;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}
