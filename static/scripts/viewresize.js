var left_frame = document.querySelector(".leftFrame");
var right_frame = document.querySelector(".rightFrame");
var buttons = document.querySelector(".button-container");
var left_button = document.getElementById('increase-left-size');
var right_button = document.getElementById("increase-right-size");

// increase left frame
document.getElementById("increase-left-size").addEventListener("click", function() {
    var computedStyle = window.getComputedStyle(left_frame);
    var currentWidth = parseInt(computedStyle.getPropertyValue('width'));
    var containerWidth = parseInt(left_frame.parentElement.clientWidth);
    var widthInPercentage = (currentWidth / containerWidth) * 100;

    if (widthInPercentage < 75) {
        let newWidth = Math.round(widthInPercentage + 10);
        left_frame.style.width = `${newWidth}%`;
        let newRightWidth = 100 - newWidth;
        right_frame.style.width = `${newRightWidth}%`;
        buttons.style.width = `${newRightWidth}%`;
        left_button.style.left = `${newWidth}%`;
        right_button.style.right = `${100 - newWidth}%`;
    }
});

// increase right frame
document.getElementById("increase-right-size").addEventListener("click", function() {
    var computedStyle = window.getComputedStyle(right_frame);
    var currentWidth = parseInt(computedStyle.getPropertyValue('width'));
    var containerWidth = parseInt(right_frame.parentElement.clientWidth);
    var widthInPercentage = (currentWidth / containerWidth) * 100;
    
    if (widthInPercentage < 75) {
        let newWidth = Math.round(widthInPercentage + 10);
        left_frame.style.width = `${100 - newWidth}%`;
        right_frame.style.width = `${newWidth}%`;
        buttons.style.width = `${newWidth}%`;
        left_button.style.left = `${100 - newWidth}%`;
        right_button.style.right = `${newWidth}%`;
    }
});