document.addEventListener("DOMContentLoaded", function () {
    // change size
    document.getElementById("left-larger").addEventListener("click", async () => {
        var left_frame = document.querySelector('.leftFrame');
        var right_frame = document.querySelectorAll(".rightFrame");
        var left_larger = document.querySelector(".left-larger");
        var right_larger = document.querySelector(".right-larger");
        var styles = window.getComputedStyle(left_larger);
        var current_posn_from_left = parseInt(styles.getPropertyValue("left"));
        var container_width = parseInt(left_frame.parentElement.clientWidth);
        var width_percent = Math.round((current_posn_from_left / container_width) * 100);
        
        if (width_percent < 75) {
            var new_width_percent = width_percent + 10;

            // update widths
            left_frame.style.width = new_width_percent + "%";
            for (var i = 0; i < right_frame.length; i++) {
                right_frame[i].style.width = (100 - new_width_percent) + "%";
            }
            left_larger.style.left = new_width_percent + "%";
            right_larger.style.right = (100 - new_width_percent) + "%";
        }
    });

    document.getElementById("right-larger").addEventListener("click", async () => {
        var left_frame = document.querySelector('.leftFrame');
        var right_frame = document.querySelectorAll(".rightFrame");
        var left_larger = document.querySelector(".left-larger");
        var right_larger = document.querySelector(".right-larger");
        var styles = window.getComputedStyle(right_larger);
        var current_posn_from_right = parseInt(styles.getPropertyValue("right"));
        var container_width = parseInt(right_frame[0].parentElement.clientWidth);
        var width_percent = Math.round((current_posn_from_right / container_width) * 100);
        
        if (width_percent < 75) {
            var new_width_percent = width_percent + 10;

            // update widths
            left_frame.style.width = (100 - new_width_percent) + "%";
            for (var i = 0; i < right_frame.length; i++) {
                right_frame[i].style.width = new_width_percent + "%";
            }
            left_larger.style.left = (100 - new_width_percent) + "%";
            right_larger.style.right = new_width_percent + "%";
        }
    });

    // reset page button
    document.getElementById("reset-page").addEventListener("click", async () => {
        var iframes = document.querySelectorAll(".tab");
        for (var i = 0; i < iframes.length; i++) {
            if (iframes[i].style.display == "block") {
                var src = iframes[i].src;
                iframes[i].src = src;
                break;
            }
        }   
    })

    // open in new tab button
    document.getElementById("open-in-new-tab").addEventListener("click", async () => {
        var iframes = document.querySelectorAll(".tab");
        var activeFrameSrc;
        for (var i = 0; i < iframes.length; i++) {
            if (iframes[i].style.display == "block") {
                activeFrameSrc = iframes[i].src;
                break;
            }
        }
        window.open(activeFrameSrc, "_blank");
    })
});