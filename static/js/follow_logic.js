function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggleFollow(username) {
    const url = `/users/follow/${username}/`;
    const btn = document.getElementById('follow-btn');
    const followersCount = document.getElementById('followers-count');
    const csrftoken = getCookie('csrftoken'); // GET TOKEN FROM COOKIE

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            followersCount.innerText = data.followers_count;
            if (data.is_following) {
                btn.innerText = "Unfollow";
            } else {
                btn.innerText = "Follow";
            }
        })
        .catch(error => console.error('Error:', error));
}