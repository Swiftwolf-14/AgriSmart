document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("recommendationForm");
    const errorSummary = document.getElementById("formErrorSummary");
    const sendButton = document.getElementById(
        "sendRecommendationButton"
    );

    if (!form || !errorSummary) {
        return;
    }

    let submittedAction = "draft";

    form.querySelectorAll('button[type="submit"]').forEach(function (button) {
        button.addEventListener("click", function () {
            submittedAction = button.value || "draft";
        });
    });

    form.addEventListener("submit", function (event) {
        errorSummary.textContent = "";
        errorSummary.hidden = true;

        if (submittedAction !== "send") {
            return;
        }

        const findings = form.querySelector(
            '[name="findings"]'
        );

        const recommendations = form.querySelector(
            '[name="recommendations"]'
        );

        const missingFields = [];

        if (!findings || !findings.value.trim()) {
            missingFields.push("Assessment Findings");
        }

        if (
            !recommendations ||
            !recommendations.value.trim()
        ) {
            missingFields.push("Recommended Actions");
        }

        if (missingFields.length > 0) {
            event.preventDefault();

            errorSummary.textContent =
                "Please complete the following required fields: " +
                missingFields.join(", ") +
                ".";

            errorSummary.hidden = false;

            errorSummary.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });

            if (findings && !findings.value.trim()) {
                findings.focus();
            } else if (
                recommendations &&
                !recommendations.value.trim()
            ) {
                recommendations.focus();
            }

            return;
        }

        if (sendButton) {
            sendButton.disabled = true;
            sendButton.textContent = "Sending...";
        }
    });
});