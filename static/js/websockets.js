document.addEventListener("DOMContentLoaded", () => {
  const userMeta = document.querySelector('meta[name="current-user"]');
  if (!userMeta) return; // Stop execution if the user is not logged in

  const currentUser = userMeta.getAttribute("content");
  const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
  const wsHost = window.location.host;

  // ==========================================
  // 1. GLOBAL NOTIFICATION ENGINE
  // ==========================================
  const notifSocket = new WebSocket(
    `${wsScheme}://${wsHost}/ws/notifications/`,
  );

  notifSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.is_dm) {
      // Unhide all Purple Inbox Dots globally
      document
        .querySelectorAll(".inbox-dot")
        .forEach((dot) => dot.classList.remove("hidden"));

      // Specialized DM Toast
      createAndShowToast(
        "💬",
        `New message from @${data.actor}`,
        data.message_preview,
        true,
        data.actor,
      );
    } else {
      // Increment the Dropdown Alerts Counters
      document.querySelectorAll(".alerts-counter").forEach((badge) => {
        badge.innerText = parseInt(badge.innerText || "0") + 1;
      });

      // Standard System Toast
      createAndShowToast(
        data.icon || "🔔",
        `Alert from @${data.actor}`,
        data.verb,
        false,
      );
    }
  };

  function createAndShowToast(
    icon,
    title,
    message,
    isClickable = false,
    actor = null,
  ) {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    const baseClasses =
      "bg-gray-800 shadow-2xl p-4 rounded-xl flex items-center gap-3 transform transition-all translate-y-10 opacity-0 z-[100] border";

    if (isClickable) {
      toast.className = `${baseClasses} border-purple-500/50 shadow-purple-900/20 cursor-pointer hover:bg-gray-700/80`;
      toast.onclick = () => (window.location.href = `/inbox/${actor}/`);
    } else {
      toast.className = `${baseClasses} border-blue-500/50 shadow-blue-900/20`;
    }

    toast.innerHTML = `
            <div class="w-10 h-10 ${isClickable ? "bg-purple-900/30 text-purple-400" : "bg-blue-900/30 text-blue-400"} rounded-full flex items-center justify-center text-xl shrink-0">${icon}</div>
            <div class="overflow-hidden">
                <p class="text-sm text-gray-200 truncate">${title}</p>
                <p class="text-xs text-gray-500 mt-0.5 truncate">${message}</p>
            </div>
        `;

    container.appendChild(toast);

    // Animate In & Out
    setTimeout(
      () => toast.classList.remove("translate-y-10", "opacity-0"),
      100,
    );
    setTimeout(() => {
      toast.classList.add("translate-y-10", "opacity-0");
      setTimeout(() => toast.remove(), 300);
    }, 5000);
  }

  // ==========================================
  // 2. LIVE CHAT ENGINE (Only runs on chat_thread.html)
  // ==========================================
  const chatBox = document.getElementById("chat-box");
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");

  if (chatBox && chatForm && chatInput) {
    // Auto-scroll chat to bottom on load
    chatBox.scrollTop = chatBox.scrollHeight;

    const contactUsername = chatBox.getAttribute("data-contact");
    const chatSocket = new WebSocket(
      `${wsScheme}://${wsHost}/ws/chat/${contactUsername}/`,
    );

    // Receive Message
    chatSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      const isMe = data.sender === currentUser;

      const bubble = `
                <div class="flex ${isMe ? "justify-end" : "justify-start"} mb-4">
                    <div class="max-w-[70%] rounded-2xl p-3 shadow-sm ${isMe ? "bg-blue-600 text-white rounded-br-none" : "bg-gray-700 text-gray-100 rounded-bl-none border border-gray-600"}">
                        <p class="text-sm whitespace-pre-wrap">${data.message}</p>
                        <span class="text-[9px] mt-1 block ${isMe ? "text-blue-200 text-right" : "text-gray-400 text-left"}">${data.time}</span>
                    </div>
                </div>
            `;

      chatBox.insertAdjacentHTML("beforeend", bubble);
      chatBox.scrollTop = chatBox.scrollHeight;
    };

    // Handle URL Intents (Pre-filling text)
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get("intent") === "hire") {
      chatInput.value = `Hello @${contactUsername},\n\nI reviewed your profile and projects. I'd like to discuss a potential opportunity with you.`;
    } else if (urlParams.get("intent") === "getHired") {
      chatInput.value = `Hello @${contactUsername},\n\nI just saw your profile and work. I'm available as a skilled professional for hiring. If possible, I would like to avail any opportunities.`;
    }

    // Send Message
    chatForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const message = chatInput.value.trim();
      if (message) {
        chatSocket.send(JSON.stringify({ message: message }));
        chatInput.value = "";
      }
    });
  }
});
