document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("submit-button").addEventListener("click", async () => {
        var submit_button = document.getElementById("submit-button");
        var text_area = document.getElementById("user-query");
        const user_query = text_area.value;
        var ds1 = document.getElementById('ds1');
        var ds2 = document.getElementById('ds2');
        var ds3 = document.getElementById('ds3');
        var ds4 = document.getElementById('ds4');
        var ds5 = document.getElementById('ds5');
        var ds6 = document.getElementById('ds6');

        var formData = {
            "query": user_query,
            "responses": {
                [ds1.value]: ds1.checked,
                [ds2.value]: ds2.checked,
                [ds3.value]: ds3.checked,
                [ds4.value]: ds4.checked,
                [ds5.value]: ds5.checked,
                [ds6.value]: ds6.checked,
            }
        };

        const response = await fetch("/upload/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({"data": formData}),
        });
        const result = await response.json();
        
        submit_button.disabled = true;
        submit_button.style.background = "white";
        if ("error" in result) {
            console.log(result["error"]);
            submit_button.textContent = "Error Occurred";
            submit_button.style.border = "1.5px red solid";
            submit_button.style.color = "red";
        }
        else {
            submit_button.textContent = "Submission Complete";
            submit_button.style.border = "1.5px green solid";
            submit_button.style.color = "green";
            
            // reload page below
            setTimeout(function() {
                location.reload();
            }, 2000);

            // show thank you message once submission complete
            var thank_you_response = document.querySelector(".thank-you-response");
            thank_you_response.style.display = "block";
        }
    });
})