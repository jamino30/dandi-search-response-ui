document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("scan-button").addEventListener("click", async () => {
        var scan_button = document.getElementById("scan-button");
        scan_button.disabled = true;
        scan_button.textContent = "Scanning...";
        scan_button.style.cursor = "default";
        scan_button.style.border = "1.5px green solid";
        scan_button.style.color = "green";
        scan_button.style.background = "white";

        var text_area = document.getElementById("user-query");
        const user_query = text_area.value;

        var dropdown_select = document.getElementById("model-selection-dropdown");
        const model_selection = dropdown_select.value;
        
        const response = await fetch("/scan/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query: user_query , model: model_selection}),
        });
        const result = await response.json();
        
        var iframes = document.querySelectorAll(".tab");

        for (var i = 0; i < iframes.length; i++) {
            iframes[i].src = `https://dandiarchive.org/dandiset/${result.ids[i]}`;
        }

        var left_frame = document.querySelector(".leftFrame");
        var right_frame = document.querySelector(".rightFrame");
        
        left_frame.style.width = "var(--leftFrameWidth)";
        left_frame.style.borderRight = "1px black solid";
        right_frame.style.display = "block";

        text_area.disabled = true;

        scan_button.style.display = "none";

        var choose_relevant_form = document.getElementById("choose-relevant-form");
        choose_relevant_form.style.display = "block";

        var ds_labels = document.querySelectorAll(".ds-label");
        var ds_checkboxes = document.querySelectorAll(".ds-checkbox-icon");
        var ds_names = document.querySelectorAll(".ds-name");
        var ds_version = document.querySelectorAll(".ds-version");
        for (var i = 0; i < ds_labels.length; i++) {
            var split_result = result.ids[i].split("/");
            ds_labels[i].innerHTML = "<b>ID</b> | " + split_result[0];
            ds_version[i].innerHTML = "<b>Version</b> | " + split_result[1];
            ds_checkboxes[i].value = result.ids[i];
            ds_names[i].innerHTML = "<b>Title:</b> " + result.names[i];
        }

        var left_larger_button = document.getElementById("left-larger");
        var right_larger_button = document.getElementById("right-larger");
        left_larger_button.style.display = "block";
        right_larger_button.style.display = "block";

        var thank_you_response = document.querySelector(".thank-you-response");
        thank_you_response.style.display = "none";

        // handle click to edit query function
        var query_label = document.getElementById("click-to-edit-query");
        var cte_style = "margin-left: 8px; font-size: 12px; text-decoration: none; color: blue;";
        localStorage.setItem("query", user_query);
        query_label.innerHTML += `<a href='' id='click-to-edit-button' onclick='location.reload()' style='${cte_style}'>(click to edit)</a>`;
    });
})