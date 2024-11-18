const mainCard = document.getElementById('main_card');
const bottomLine = document.getElementById('bottom_line');
const textareaComment = document.getElementById('comment');

if (mainCard) {
    const resizeObserver = new ResizeObserver(() => {
        bottomLine.style.width = `${mainCard.offsetWidth}px`;
        textareaComment.style.width = `${mainCard.offsetWidth}px`;
        textareaComment.style.height = `200px`;
    });

    resizeObserver.observe(mainCard);
    
    bottomLine.style.width = `${mainCard.offsetWidth}px`;
    textareaComment.style.width = `${mainCard.offsetWidth}px`;
    textareaComment.style.height = `200px`;
} 