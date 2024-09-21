document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const closeButton = document.createElement('button');

    closeButton.textContent = 'X';
    closeButton.classList.add('close-btn');
    sidebar.appendChild(closeButton);

    // Function to open the sidebar
    function openSidebar() {
        sidebar.classList.add('open-sidebar');
    }

    // Function to close the sidebar
    function closeSidebar() {
        sidebar.classList.remove('open-sidebar');
    }

    // Event listener for opening the sidebar
    menuToggle.addEventListener('click', openSidebar);

    // Event listener for closing the sidebar
    closeButton.addEventListener('click', closeSidebar);
});
