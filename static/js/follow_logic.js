function toggleFollow(username) {
    const url = `/users/follow/${username}/`;
    const btn = document.getElementById('follow-btn');
    const followersCount = document.getElementById('followers-count');

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            // Update Counter
            followersCount.innerText = data.followers_count;

            // Update Button Style
            if (data.is_following) {
                btn.innerText = "Unfollow";
            } else {
                btn.innerText = "Follow";
            }
        })
        .catch(error => console.error('Error:', error));
}