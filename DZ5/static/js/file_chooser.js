document.getElementById("file-input").addEventListener("change", function () {
    var filePath = this.files[0]?.name || "No file selected";
    document.getElementById("file-path").value = filePath;

    var formData = new FormData();
    formData.append('file', this.files[0]);

    fetch(uploadUrl, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector('[name="csrfmiddlewaretoken"]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const fileUrl = data.file_url;
            document.getElementById("file-path").value = fileUrl;
            document.getElementById("avatar").src = fileUrl;
        } else {
            alert('Image upload failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('AAAAAAAAAAAAAA');
    });
});
