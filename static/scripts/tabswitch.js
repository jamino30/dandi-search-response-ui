// show a tab
function showTab(tabIdx) {
    var tabs = document.querySelectorAll('.tab');
    var startTab = document.querySelector('.start-tab');
    
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].style.display = "none";
    }
    
    if (tabIdx != -1) {
        tabs[tabIdx].style.display = "block";
        startTab.style.display = "none";
    } 
};

// show the initial start tab
showTab(-1);