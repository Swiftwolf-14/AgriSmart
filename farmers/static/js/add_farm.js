const farmingType = document.getElementById("id_farming_type");

const cropSection = document.getElementById("cropSection");
const livestockSection =
    document.getElementById("livestockSection");
const otherSection = document.getElementById("otherSection");

const fertilizerCheckbox =
    document.getElementById("id_uses_fertilizer");
const fertilizerSection =
    document.getElementById("fertilizerSection");

const pestCheckbox =
    document.getElementById("id_has_pests_or_diseases");
const pestSection = document.getElementById("pestSection");


function updateFarmSections() {
    const type = farmingType.value;

    // Crop questions
    cropSection.hidden = !["crop", "mixed"].includes(type);

    // Livestock questions
    livestockSection.hidden =
        !["livestock", "mixed"].includes(type);

    // Additional questions for other farming types
    otherSection.hidden =
        !["other", "poultry", "fish", "beekeeping"].includes(type);

    updateOptionalQuestions();
}


function updateOptionalQuestions() {
    fertilizerSection.hidden =
        !fertilizerCheckbox.checked;

    pestSection.hidden =
        !pestCheckbox.checked;
}


farmingType.addEventListener("change", updateFarmSections);

fertilizerCheckbox.addEventListener(
    "change", updateOptionalQuestions
);

pestCheckbox.addEventListener(
    "change", updateOptionalQuestions
);

// Set the correct sections on initial page load
updateFarmSections();
const getLocationBtn = document.getElementById("getLocationBtn");
const locationStatus = document.getElementById("locationStatus");
const latitudeInput = document.getElementById("id_latitude");
const longitudeInput = document.getElementById("id_longitude");

if (getLocationBtn) {
    getLocationBtn.addEventListener("click", function () {
        if (!navigator.geolocation) {
            locationStatus.textContent =
                "GPS is not supported by this browser.";
            return;
        }

        getLocationBtn.disabled = true;
        locationStatus.textContent =
            "Requesting location permission...";

        navigator.geolocation.getCurrentPosition(
            function (position) {
                latitudeInput.value = position.coords.latitude;
                longitudeInput.value = position.coords.longitude;

                locationStatus.textContent =
                    "Farm coordinates captured successfully.";

                getLocationBtn.disabled = false;
            },
            function (error) {
                const messages = {
                    1: "Location permission denied.",
                    2: "Location unavailable. Please try again.",
                    3: "Location request timed out. Please try again."
                };

                locationStatus.textContent =
                    messages[error.code] ||
                    "Unable to get your location.";

                getLocationBtn.disabled = false;
            },
            {
                enableHighAccuracy: true,
                timeout: 15000,
                maximumAge: 60000
            }
        );
    });
}