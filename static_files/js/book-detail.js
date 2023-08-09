document.addEventListener('DOMContentLoaded', () => {
            // Book Description Show More/Less
            const bookDescriptionShowMoreBtn = document.querySelector('.book-description .show-more-btn');
            const bookDescriptionShowLessBtn = document.querySelector('.book-description .show-less-btn');
            const bookDescriptionTruncate = document.querySelector('.book-description .description-truncate');
            const bookDescriptionFull = document.querySelector('.book-description .description-full');

            bookDescriptionShowMoreBtn.addEventListener('click', () => {
                bookDescriptionTruncate.style.display = 'none';
                bookDescriptionFull.style.display = 'block';
            });

            bookDescriptionShowLessBtn.addEventListener('click', () => {
                bookDescriptionFull.style.display = 'none';
                bookDescriptionTruncate.style.display = 'block';
            });

            // Reader Reviews Show More/Less
            const showMoreBtns = document.querySelectorAll('.description-truncate .show-more-btn');
            const showLessBtns = document.querySelectorAll('.description-full .show-less-btn');

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

            const editReviewBtns = document.querySelectorAll('.edit-review-btn');

            editReviewBtns.forEach((btn) => {
                btn.addEventListener('click', (event) => {
                    event.preventDefault();
                    const reviewId = btn.dataset.reviewId;

                    // Redirect to the edit page with the reviewId
                    window.location.href = `/edit-review/${reviewId}/`; // Update URL pattern as needed
                });
            });

            $(function () {
                $('[data-toggle="tooltip"]').tooltip();
            });

        });