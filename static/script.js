function sendMessage() {
  const userInput = document.getElementById("user-input");
  const message = userInput.value;
  if (!message) return;

  appendMessage(message, 'user-msg');
  userInput.value = '';

  fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message})
  })
  .then(res => res.json())
  .then(data => {
    appendMessage(data.reply, 'bot-msg');
  });
}

function appendMessage(msg, className) {
  const chat = document.getElementById("chat-window");
  const div = document.createElement("div");
  div.className = className;
  div.innerText = msg;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}
