// show a tab
function showTab(tabIdx) {
    var tabs = document.querySelectorAll('.tab');
    var startTab = document.querySelector('.start-tab');
    var reset_page = document.querySelector(".reset-page");
    var open_in_new_tab = document.querySelector(".open-in-new-tab");
    
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].style.display = "none";
    }
    reset_page.style.display = "none";
    open_in_new_tab.style.display = "none";
    
    if (tabIdx != -1) {
        tabs[tabIdx].style.display = "block";
        startTab.style.display = "none";
        reset_page.style.display = "block";
        open_in_new_tab.style.display = "block";
    }
};

// show the initial start tab
showTab(-1);