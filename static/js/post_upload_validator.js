document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('id_avatar');
    fileInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (!file) return;

        const maxSizeMB = 5;
        if (file.size > maxSizeMB * 1024 * 1024) {
            alert(`File is too big! Max size allowed is ${maxSizeMB}MB.`);
            this.value = "";
            return;
        }

        const fileName = file.name;
        const validExtensions = /(\.jpg|\.jpeg|\.png)$/i;
        if (!validExtensions.exec(fileName)) {
            alert(`Invalid file type. Please upload a JPG, JPEG, or PNG file. Current file: ${fileName}`);
            this.value = "";
        }
    });
});