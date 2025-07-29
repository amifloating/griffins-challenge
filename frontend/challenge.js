let current = 1;

// Typing animation for Matrix-style effect
async function typeText(element, text, speed = 40) {
  element.innerText = "";
  for (let i = 0; i < text.length; i++) {
    element.innerText += text.charAt(i);
    await new Promise(resolve => setTimeout(resolve, speed));
  }
}

async function login() {
  const username = document.getElementById("username").value;
  await fetch("http://localhost:5000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ username })
  });
  document.getElementById("login").classList.add("hidden");
  document.getElementById("challenge").classList.remove("hidden");
  loadChallenge();
}

async function loadChallenge() {
  const res = await fetch("http://localhost:5000/challenge", {
    credentials: "include"
  });
  const data = await res.json();
  const questionEl = document.getElementById("question");
  if (data.question) {
    await typeText(questionEl, data.question);
    updateProgress();
  } else {
    await typeText(questionEl, "All challenges complete!");
  }
}

async function submit() {
  const flag = document.getElementById("answer").value;
  const res = await fetch("http://localhost:5000/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ flag })
  });
  const data = await res.json();
  const feedback = document.getElementById("feedback");
  feedback.innerText = data.correct ? "✅ Correct!" : "❌ Try again!";
  if (data.correct) {
    loadChallenge();
  }
}

async function updateProgress() {
  const res = await fetch("http://localhost:5000/progress", {
    credentials: "include"
  });
  const data = await res.json();
  const total = 3;
  const percent = ((data.current - 1) / total) * 100;
  document.getElementById("progress").innerText = `Progress: ${percent}%`;
}
