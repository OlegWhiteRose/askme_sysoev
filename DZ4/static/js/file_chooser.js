document.getElementById('choose-btn').onclick = function() {
    document.getElementById('file-input').click();
};

document.getElementById('file-input').addEventListener('change', function() {
    var filePath = this.files[0].name;
    document.getElementById('file-path').value = filePath;

    var file = this.files[0];
    if (file && document.getElementById('avatar')) {
        var validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
        if (validTypes.includes(file.type)) {
            document.getElementById('file-path').value = file.name;
            var reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('avatar').src = e.target.result;
            };
            reader.readAsDataURL(file);
        } 
    }
});