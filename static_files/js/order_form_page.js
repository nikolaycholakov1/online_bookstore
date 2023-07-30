const ongoingContainer = document.getElementById('ongoing-order')
const completedContainer = document.getElementById('completed-order')
const orderBtn = document.getElementById('btn-order')

orderBtn.addEventListener('click', function () {
    ongoingContainer.innerHTML = ''
    completedContainer.style.display = 'flex';
    completedContainer.style.justifyContent = 'center';
    completedContainer.style.margin = '0px 0px 60px 0px';
})
