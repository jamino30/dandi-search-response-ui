// show a tab
function showTab(tabIdx) {
    var tabs = document.querySelectorAll('.tab');
    var startTab = document.querySelector('.start-tab');
    var tabButtons = document.querySelectorAll('.tabButton');
    
    var activeTab;
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].style.display = "none";
        if (tabButtons[i].classList.contains('active')) {
            activeTab = tabs[i]
        }
        tabButtons[i].classList.remove('active');
    }

    if (activeTab == tabs[tabIdx] && tabIdx != -1) {
        startTab.style.display = "block";
    }
    else {
        if (tabIdx != -1) {
            tabs[tabIdx].style.display = "block";
            tabButtons[tabIdx].classList.add('active');
            startTab.style.display = "none";
        } 
    }
};

// show the initial start tab
showTab(-1);