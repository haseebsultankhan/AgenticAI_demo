// --- Chat UI Controls ---
function toggleChat() {
  const chat = document.getElementById("chat-wrapper");
  const input = document.getElementById("chat-input");
  const chatBody = document.getElementById("chat-body");

  const isOpening = chat.style.display === "none" || chat.style.display === "";
  chat.style.display = isOpening ? "flex" : "none";

  if (isOpening) {
    setTimeout(() => input && input.focus(), 300);

    // Show a one-time welcome message when chat opens and no messages yet
    if (chatBody && chatBody.childElementCount === 0) {
      appendMessage("Hello! I’m Nadra Agent. How can I assist you today?", "bot");
    }
  }
}

function appendMessage(text, sender = "bot") {
  const chatBody = document.getElementById("chat-body");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.style.backgroundImage =
    sender === "bot"
      ? "url('static/images/NADRA-Logo-removebg-preview.png')"
      : "url('static/images/user-286.png')";

  const textDiv = document.createElement("div");
  textDiv.className = "text";
  textDiv.textContent = text;

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(textDiv);
  chatBody.appendChild(messageDiv);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function handleKeyPress(event) {
  if (event.key === "Enter") sendMessage();
}

// --- Typing Indicator Helpers ---
function startTypingAnimation(textDiv, label = "Nadra Agent is typing") {
  let dots = 0;
  textDiv.textContent = label;
  const intervalId = setInterval(() => {
    dots = (dots + 1) % 4; // 0..3
    textDiv.textContent = label + ".".repeat(dots);
  }, 500);
  return intervalId;
}

function stopTypingAnimation(intervalId, textDiv) {
  if (intervalId) clearInterval(intervalId);
  if (textDiv) textDiv.textContent = "";
}

// --- Streaming Sender (/stream) ---
async function sendMessage() {
  const input = document.getElementById("chat-input");
  const question = (input.value || "").trim();
  if (!question) return;

  appendMessage(question, "user");
  input.value = "";
  input.focus();

  const chatBody = document.getElementById("chat-body");
  const messageDiv = document.createElement("div");
  messageDiv.className = "message bot";

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.style.backgroundImage = "url('static/images/NADRA-Logo-removebg-preview.png')";

  const textDiv = document.createElement("div");
  textDiv.className = "text";

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(textDiv);
  chatBody.appendChild(messageDiv);
  chatBody.scrollTop = chatBody.scrollHeight;

  // Start typing animation until real text arrives
  const typingId = startTypingAnimation(textDiv, "Nadra Agent is typing");

  try {
    const response = await fetch("/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    if (!response.ok || !response.body) {
      throw new Error(`Bad response: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let done = false;
    let firstchunk = true;

    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      const chunk = value ? decoder.decode(value, { stream: true }) : "";

      if (firstchunk) {
        stopTypingAnimation(typingId, textDiv); // stop the animation on first real token
        firstchunk = false;
      }
      textDiv.textContent += chunk;
      chatBody.scrollTop = chatBody.scrollHeight;
    }
  } catch (error) {
    stopTypingAnimation(typingId, textDiv);
    textDiv.textContent = "Sorry, something went wrong.";
    console.error(error);
  }
}

// --- Non-streaming Sender (/ask) ---
async function sendAskMessage() {
  const input = document.getElementById("chat-input");
  const question = (input.value || "").trim();
  if (!question) return;

  appendMessage(question, "user");
  input.value = "";
  input.focus();

  const chatBody = document.getElementById("chat-body");
  const messageDiv = document.createElement("div");
  messageDiv.className = "message bot";

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.style.backgroundImage = "url('static/images/NADRA-Logo-removebg-preview.png')";

  const textDiv = document.createElement("div");
  textDiv.className = "text";

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(textDiv);
  chatBody.appendChild(messageDiv);
  chatBody.scrollTop = chatBody.scrollHeight;

  // Typing animation for non-streaming flow
  const typingId = startTypingAnimation(textDiv, "Nadra Agent is typing");

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    if (!response.ok) {
      throw new Error(`Server returned status ${response.status}`);
    }

    const data = await response.json();
    stopTypingAnimation(typingId, textDiv);
    textDiv.textContent = data.answer || "No response received.";
    chatBody.scrollTop = chatBody.scrollHeight;
  } catch (error) {
    stopTypingAnimation(typingId, textDiv);
    textDiv.textContent = "Sorry, something went wrong.";
    console.error(error);
  }
}