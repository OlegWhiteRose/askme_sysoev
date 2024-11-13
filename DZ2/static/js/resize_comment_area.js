const cardAnswer = document.querySelector('.card-answer'); 
const bottomLine = document.querySelector('.bottom-line'); 
const textareaComment = document.querySelector('.comment');

const produceWidth = () => {
    const cardAnswerWidth = cardAnswer.offsetWidth;
    bottomLine.style.width = cardAnswerWidth + 'px'; 
    textareaComment.style.width = cardAnswerWidth + 'px';
};

produceWidth();
window.addEventListener('resize', produceWidth);