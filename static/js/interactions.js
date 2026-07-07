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
  // POST EXPANSION ENGINE (BULLETPROOF)
  // ==========================================
  function initExpansions() {
    document.querySelectorAll(".post-content-wrapper").forEach((wrapper) => {
      const container = wrapper.querySelector(".post-text-container");
      const prose = wrapper.querySelector(".prose");
      const btn = wrapper.querySelector(".toggle-text-btn");
      const overlay = wrapper.querySelector(".fade-overlay");

      if (!container || !prose || !btn) return;

      // Strip old event listeners by cloning the button (prevents double-firing)
      const newBtn = btn.cloneNode(true);
      btn.parentNode.replaceChild(newBtn, btn);

      const checkHeight = () => {
        if (!container.classList.contains("max-h-[4.5rem]")) return; // Already expanded
        // 75px threshold ensures a safe buffer for line-heights
        if (prose.scrollHeight > 75) {
          newBtn.classList.remove("hidden");
          overlay.classList.remove("hidden");
        } else {
          newBtn.classList.add("hidden");
          overlay.classList.add("hidden");
        }
      };

      // Check immediately, and check again after fonts/images render
      checkHeight();
      window.addEventListener("load", checkHeight);
      setTimeout(checkHeight, 500);

      newBtn.addEventListener("click", () => {
        if (container.classList.contains("max-h-[4.5rem]")) {
          // EXPAND: Animate from 4.5rem to actual pixel height
          container.classList.remove("max-h-[4.5rem]");
          container.style.maxHeight = prose.scrollHeight + "px";
          overlay.classList.add("hidden");
          newBtn.innerText = "Show less";

          // Remove explicit height after animation so window resizing doesn't crop text
          setTimeout(() => {
            container.style.maxHeight = "none";
          }, 300);
        } else {
          // COLLAPSE: Lock current height, force reflow, then animate to 4.5rem
          container.style.maxHeight = prose.scrollHeight + "px";
          void container.offsetHeight; // Force browser to register the height

          container.classList.add("max-h-[4.5rem]");
          container.style.maxHeight = "4.5rem"; // Animate down smoothly
          overlay.classList.remove("hidden");
          newBtn.innerText = "Show all";
        }
      });
    });
  }

  initExpansions();

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
