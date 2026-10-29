document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("soilUploadForm");
    const fileInput = document.getElementById("soilFile");
    const uploadArea = document.getElementById("uploadArea");
    const browseButton = document.getElementById("browseButton");
    const selectedFile = document.getElementById("selectedFile");
    const fileName = document.getElementById("fileName");
    const fileSize = document.getElementById("fileSize");
    const removeFileButton = document.getElementById("removeFile");
    const formMessage = document.getElementById("formMessage");
    const startUploadButton = document.getElementById("startUploadButton");

    const MAX_FILE_SIZE = 10 * 1024 * 1024;
    const ALLOWED_EXTENSIONS = ["pdf", "jpg", "jpeg", "png"];

    function showMessage(message, type) {
        formMessage.textContent = message;
        formMessage.className = "form-message " + type;
    }

    function clearMessage() {
        formMessage.textContent = "";
        formMessage.className = "form-message";
    }

    function formatFileSize(bytes) {
        if (bytes < 1024) {
            return bytes + " bytes";
        }

        if (bytes < 1024 * 1024) {
            return (bytes / 1024).toFixed(1) + " KB";
        }

        return (bytes / (1024 * 1024)).toFixed(2) + " MB";
    }

    function validateFile(file) {
        if (!file) {
            showMessage(
                "Please select a soil assessment file.",
                "error"
            );
            return false;
        }

        const extension = file.name.split(".").pop().toLowerCase();

        if (!ALLOWED_EXTENSIONS.includes(extension)) {
            showMessage(
                "Invalid file format. Please choose a PDF, JPG, JPEG, or PNG file.",
                "error"
            );
            return false;
        }

        if (file.size > MAX_FILE_SIZE) {
            showMessage(
                "The selected file exceeds 10 MB. Please choose a smaller file.",
                "error"
            );
            return false;
        }

        return true;
    }

    function displayFile(file) {
        if (!validateFile(file)) {
            fileInput.value = "";
            selectedFile.hidden = true;
            return false;
        }

        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        selectedFile.hidden = false;

        clearMessage();
        return true;
    }

    function clearSelectedFile() {
        fileInput.value = "";
        selectedFile.hidden = true;
        fileName.textContent = "";
        fileSize.textContent = "";

        clearMessage();
    }

    // Open the file picker.
    browseButton.addEventListener("click", function () {
        fileInput.click();
    });

    // Display the selected file.
    fileInput.addEventListener("change", function () {
        const file = fileInput.files[0];

        if (file) {
            displayFile(file);
        } else {
            clearSelectedFile();
        }
    });

    // Remove the selected file.
    removeFileButton.addEventListener("click", function () {
        clearSelectedFile();
    });

    // Drag-and-drop visual feedback.
    ["dragenter", "dragover"].forEach(function (eventName) {
        uploadArea.addEventListener(eventName, function (event) {
            event.preventDefault();
            uploadArea.classList.add("dragging");
        });
    });

    ["dragleave", "drop"].forEach(function (eventName) {
        uploadArea.addEventListener(eventName, function (event) {
            event.preventDefault();
            uploadArea.classList.remove("dragging");
        });
    });

    // Accept a dropped file.
    uploadArea.addEventListener("drop", function (event) {
        const files = event.dataTransfer.files;

        if (!files || files.length === 0) {
            return;
        }

        const file = files[0];

        if (!validateFile(file)) {
            return;
        }

        const transfer = new DataTransfer();
        transfer.items.add(file);
        fileInput.files = transfer.files;

        displayFile(file);
    });

    // Clear the form.
    form.addEventListener("reset", function () {
        window.setTimeout(function () {
            clearSelectedFile();
        }, 0);
    });

    // Scroll to the upload form.
    if (startUploadButton) {
        startUploadButton.addEventListener("click", function () {
            document.getElementById("upload-section").scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        });
    }

    // Validate the file before submitting to Django.
    form.addEventListener("submit", function (event) {
        clearMessage();

        const file = fileInput.files[0];

        if (!validateFile(file)) {
            event.preventDefault();
        }
    });
});