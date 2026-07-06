document.addEventListener("DOMContentLoaded", () => {
  const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
  if (!csrfTokenMeta) return;
  const csrfToken = csrfTokenMeta.getAttribute("content");

  // ==========================================
  // UI UTILITIES
  // ==========================================

  window.triggerToast = function (icon, message, actor = "System") {
    const container = document.getElementById("toast-container");
    if (!container) return;
    const toast = document.createElement("div");
    toast.className =
      "bg-gray-800 border border-blue-500/50 shadow-2xl shadow-blue-900/20 p-2 rounded-lg flex items-center gap-3 transform transition-all translate-y-10 opacity-0 z-50";
    toast.innerHTML = `
            <div class="w-10 h-10 bg-blue-900/30 rounded-full flex items-center justify-center text-xl shrink-0">${icon}</div>
            <div>
                <p class="text-sm text-gray-200">Alert from <span class="font-bold text-blue-400">${actor}</span></p>
                <p class="text-xs text-gray-500 mt-0.5">${message}</p>
            </div>
        `;
    container.appendChild(toast);
    setTimeout(
      () => toast.classList.remove("translate-y-10", "opacity-0"),
      100,
    );
    setTimeout(() => {
      toast.classList.add("translate-y-10", "opacity-0");
      setTimeout(() => toast.remove(), 300);
    }, 5000);
  };

  // ==========================================
  // ASYNC API CALLS (LIKES, SAVES, REPORTS)
  // ==========================================

  window.toggleLike = async function (postId) {
    try {
      const res = await fetch(`/post/like/${postId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "X-Requested-With": "XMLHttpRequest",
        },
      });
      const data = await res.json();
      document.getElementById(`like-count-${postId}`).innerText =
        data.like_count;
      document.getElementById(`like-icon-${postId}`).innerText = data.liked
        ? "❤️"
        : "🤍";
    } catch (e) {
      console.error("Network Error", e);
    }
  };

  window.toggleBookmark = async function (postId) {
    try {
      const res = await fetch(`/post/${postId}/bookmark/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "X-Requested-With": "XMLHttpRequest",
        },
      });
      const data = await res.json();
      const btn = document.getElementById(`bookmark-btn-${postId}`);
      if (btn) {
        // Visual feedback
        if (data.saved) {
          btn.classList.replace("text-gray-400", "text-blue-500");
        } else {
          btn.classList.replace("text-blue-500", "text-gray-400");
        }
      }
      triggerToast("🔖", data.message);
    } catch (e) {
      console.error("Network Error", e);
    }
  };

  window.submitReport = async function (postId) {
    try {
      const res = await fetch(`/post/${postId}/report/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "X-Requested-With": "XMLHttpRequest",
        },
      });
      const data = await res.json();
      triggerToast("🚩", data.message);
    } catch (e) {
      console.error("Network Error", e);
    }
  };

  // ==========================================
  // POST EXPANSION ENGINE
  // ==========================================
  document.querySelectorAll(".post-content-wrapper").forEach((wrapper) => {
    const container = wrapper.querySelector(".post-text-container");
    const prose = wrapper.querySelector(".prose");
    const btn = wrapper.querySelector(".toggle-text-btn");
    const overlay = wrapper.querySelector(".fade-overlay");

    if (prose && btn && container && prose.scrollHeight > 72) {
      btn.classList.remove("hidden");
      btn.addEventListener("click", () => {
        if (container.classList.contains("max-h-[4.5rem]")) {
          container.classList.remove("max-h-[4.5rem]");
          container.style.maxHeight = prose.scrollHeight + "px";
          overlay.classList.add("hidden");
          btn.innerText = "Show less";
        } else {
          container.classList.add("max-h-[4.5rem]");
          container.style.maxHeight = null;
          overlay.classList.remove("hidden");
          btn.innerText = "Show all";
        }
      });
    } else if (overlay) {
      overlay.classList.add("hidden");
    }
  });

  // ==========================================
  // COMMENTS UI CONTROLLER
  // ==========================================
  window.toggleReplyForm = function (commentId) {
    const formDiv = document.getElementById(`reply-form-${commentId}`);
    if (formDiv) {
      formDiv.classList.toggle("hidden");
      if (!formDiv.classList.contains("hidden"))
        formDiv.querySelector('input[name="body"]').focus();
    }
  };
});
