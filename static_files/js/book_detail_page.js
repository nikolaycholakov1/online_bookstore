const readMoreBtns = document.querySelectorAll('.read-more-btn');
readMoreBtns.forEach((btn) => {
    btn.addEventListener('click', (event) => {
        const reviewContent = event.target.parentElement.querySelector('.review-content');
        const fullText = reviewContent.dataset.fullText;
        reviewContent.textContent = fullText;
        event.target.style.display = 'none';
    });
}); // <-- Missing closing parenthesis

document.addEventListener('DOMContentLoaded', () => {
    // Add event listener to "Show More" button
    const showMoreBtn = document.querySelector('.show-more-btn');
    const descriptionTruncate = document.querySelector('.description-truncate');
    const descriptionFull = document.querySelector('.description-full');

    if (showMoreBtn && descriptionTruncate && descriptionFull) {
        showMoreBtn.addEventListener('click', () => {
            descriptionTruncate.style.display = 'none';
            descriptionFull.style.display = 'block';
        });
    }

    // Add event listener to "Show Less" button
    const showLessBtn = document.querySelector('.show-less-btn');

    if (showLessBtn && descriptionTruncate && descriptionFull) {
        showLessBtn.addEventListener('click', () => {
            descriptionTruncate.style.display = 'block';
            descriptionFull.style.display = 'none';
        });
    }
});
