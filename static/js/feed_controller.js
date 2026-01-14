// Toggle specific menu of post
function togglePostMenu(postId) {
    const menu = document.getElementById(`post-menu-${postId}`);
    // Close all other open menus
    document.querySelectorAll('[id^="post-menu-"]').forEach(el => {
        if (el !== menu) el.classList.add('hidden');
    });
    menu.classList.toggle('hidden');
}

// Close when clicking outside
document.addEventListener('click', function (event) {
    const isButton = event.target.closest('button');
    const isMenu = event.target.closest('[id^="post-menu-"]');

    if (!isButton && !isMenu) {
        document.querySelectorAll('[id^="post-menu-"]').forEach(menu => {
            menu.classList.add('hidden');
        });
    }
});

// LIKE BUTTON (AJAX)
function toggleLike(event, postId) {
    event.preventDefault();

    const url = `/post/like/${postId}/`;
    const iconContainer = document.getElementById(`like-icon-${postId}`);
    const countSpan = document.getElementById(`like-count-${postId}`);

    // Fetching the likes data from backend in background (from Django)
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.status === 403 || response.status === 401) {
            window.location.href = "{% url 'login' %}";
            return;
        }
        return response.json();
    }).then(data => {
        countSpan.innerText = data.count;
        if (data.liked) {
            // turning the like RED
            countSpan.classList.remove('text-gray-400');
            countSpan.classList.add('text-red-500');
            iconContainer.innerHTML = `
                    <svg class="w-6 h-6 text-red-500 group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                    </svg>`;
        } else {
            // turning the like GRAY
            countSpan.classList.remove('text-red-500');
            countSpan.classList.add('text-gray-400');
            iconContainer.innerHTML = `
                    <svg class="w-6 h-6 text-gray-400 group-hover:text-red-500 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>`;
        }
    }).catch(error => console.error('Error:', error));
}