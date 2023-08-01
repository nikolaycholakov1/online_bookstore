document.addEventListener('DOMContentLoaded', () => {
    // Show More buttons in the "Reader Reviews" section
    const showMoreBtns = document.querySelectorAll('.description-truncate .show-more-btn');
    // Show Less buttons in the "Reader Reviews" section
    const showLessBtns = document.querySelectorAll('.description-full .show-less-btn');

    // Add event listeners to Show More buttons
    showMoreBtns.forEach((btn) => {
        btn.addEventListener('click', (event) => {
            const showMoreBtn = event.target;
            const reviewContainer = showMoreBtn.closest('.card-body');
            const descriptionTruncate = reviewContainer.querySelector('.description-truncate');
            const descriptionFull = reviewContainer.querySelector('.description-full');

            descriptionTruncate.style.display = 'none';
            descriptionFull.style.display = 'block';
        });
    });

    // Add event listeners to Show Less buttons
    showLessBtns.forEach((btn) => {
        btn.addEventListener('click', (event) => {
            const showLessBtn = event.target;
            const reviewContainer = showLessBtn.closest('.card-body');
            const descriptionTruncate = reviewContainer.querySelector('.description-truncate');
            const descriptionFull = reviewContainer.querySelector('.description-full');

            descriptionFull.style.display = 'none';
            descriptionTruncate.style.display = 'block';
        });
    });
});
