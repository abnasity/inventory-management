// Barcode Scanner functionality
let isScanning = false;
let scannerModal;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize scanner modal
    scannerModal = new bootstrap.Modal(document.getElementById('scannerModal'));
});

function initializeScanner(targetInputId) {
    // Show the scanner modal
    scannerModal.show();
    
    Quagga.init({
        inputStream: {
            name: "Live",
            type: "LiveStream",
            target: document.querySelector("#interactive"),
            constraints: {
                facingMode: "environment" // use back camera on mobile devices
            },
        },
        decoder: {
            readers: ["ean_reader", "ean_8_reader"] // IMEI is typically EAN format
        }
    }, function(err) {
        if (err) {
            console.error("Failed to initialize scanner:", err);
            return;
        }
        isScanning = true;
        Quagga.start();
    });

    // When barcode is detected
    Quagga.onDetected(function(result) {
        if (result.codeResult.code) {
            let code = result.codeResult.code;
            document.getElementById(targetInputId).value = code;
            stopScanner();
            // Close the modal
            let modal = bootstrap.Modal.getInstance(document.getElementById('scannerModal'));
            modal.hide();
        }
    });
}

function startScanner(targetInputId) {
    if (!isScanning) {
        initializeScanner(targetInputId);
    }
}

function stopScanner() {
    if (isScanning) {
        Quagga.stop();
        isScanning = false;
    }
}

// Clean up when modal is closed
document.addEventListener('hidden.bs.modal', function (event) {
    if (event.target.id === 'scannerModal') {
        stopScanner();
    }
});
