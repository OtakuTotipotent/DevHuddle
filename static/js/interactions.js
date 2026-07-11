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
  // POST EXPANSION ENGINE (ENTERPRISE GRADED)
  // ==========================================
  function setupPostTruncationEngine() {
    document.querySelectorAll(".post-content-wrapper").forEach((wrapper) => {
      const container = wrapper.querySelector(".post-text-container");
      const prose = wrapper.querySelector(".prose");
      const btn = wrapper.querySelector(".toggle-text-btn");
      const overlay = wrapper.querySelector(".fade-overlay");

      if (!container || !prose || !btn) return;

      const evalTruncationState = () => {
        // 72px corresponds precisely to a 3-line crop limit
        if (prose.scrollHeight > 75) {
          if (container.classList.contains("max-h-[4.5rem]")) {
            btn.classList.remove("hidden");
            if (overlay) overlay.classList.remove("hidden");
          }
        } else {
          btn.classList.add("hidden");
          if (overlay) overlay.classList.add("hidden");
        }
      };

      // Evaluate states across various rendering lifecycles
      evalTruncationState();
      window.addEventListener("load", evalTruncationState);
      setTimeout(evalTruncationState, 400);

      btn.addEventListener("click", (e) => {
        e.preventDefault();
        if (container.classList.contains("max-h-[4.5rem]")) {
          // Expand sequence
          container.classList.remove("max-h-[4.5rem]");
          container.style.maxHeight = prose.scrollHeight + "px";
          if (overlay) overlay.classList.add("hidden");
          btn.innerText = "Show less";

          // Allow fluid rendering after the CSS transition completes
          setTimeout(() => {
            if (!container.classList.contains("max-h-[4.5rem]"))
              container.style.maxHeight = "none";
          }, 300);
        } else {
          // Collapse sequence
          container.style.maxHeight = prose.scrollHeight + "px";
          void container.offsetHeight; // Force a browser repaint event

          container.classList.add("max-h-[4.5rem]");
          container.style.maxHeight = "4.5rem";
          if (overlay) overlay.classList.remove("hidden");
          btn.innerText = "Show all";
        }
      });
    });
  }

  setupPostTruncationEngine();

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

  // ==========================================
  // GLOBAL FORM LOADERS & SPINNERS
  // ==========================================
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", function () {
      const submitBtn = form.querySelector('button[type="submit"]');

      // Only trigger if the button isn't already disabled (prevents double-clicks)
      if (submitBtn && !submitBtn.disabled) {
        submitBtn.disabled = true;
        submitBtn.classList.add("opacity-70", "cursor-not-allowed");

        // Inject SVG Spinner while keeping button dimensions stable
        submitBtn.innerHTML = `
          <div class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-5 w-5 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Processing...</span>
          </div>
        `;
      }
    });
  });
});
