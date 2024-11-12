const textarea = document.querySelector('.main-textarea');
        textarea.style.height = 'auto'; 
        textarea.style.height = textarea.scrollHeight + 'px'; 

textarea.addEventListener('input', () => {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
});