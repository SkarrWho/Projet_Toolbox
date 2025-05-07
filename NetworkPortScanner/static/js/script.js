document.addEventListener('DOMContentLoaded', function() {
    const scanTypeSelect = document.getElementById('scanType');
    const customPortsField = document.getElementById('customPortsField');
    const startScanBtn = document.getElementById('startScanBtn');
    const ipInput = document.getElementById('ip');
    const domainInput = document.getElementById('domain');
    const portsInput = document.getElementById('ports');
    const scanForm = document.getElementById('scanForm');
    
    // Toggle custom ports field
    scanTypeSelect.addEventListener('change', function() {
        if (this.value === 'custom') {
            customPortsField.classList.remove('d-none');
        } else {
            customPortsField.classList.add('d-none');
            portsInput.value = '';
        }
        validateForm();
    });
    
    // Validate form on input
    [ipInput, domainInput, portsInput].forEach(input => {
        input.addEventListener('input', validateForm);
    });
    
    // Form validation
    function validateForm() {
        let isValidIP = false;
        let isValidDomain = false;
        let isValidPorts = true;
        
        // IP validation (only if field is not empty)
        const ipValue = ipInput.value.trim();
        if (ipValue) {
            const ipPattern = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;
            isValidIP = ipPattern.test(ipValue);
        } else {
            // Si le champ IP est vide, on le considère comme valide pour permettre
            // l'utilisation du domaine seul
            isValidIP = true;
        }
        
        // Domain validation (only if field is not empty)
        const domainValue = domainInput.value.trim();
        if (domainValue) {
            const domainPattern = /^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+$/;
            isValidDomain = domainPattern.test(domainValue);
        } else {
            // Si le champ domaine est vide, on le considère comme valide pour permettre
            // l'utilisation de l'IP seule
            isValidDomain = true;
        }
        
        // Additional validation for custom ports
        if (scanTypeSelect.value === 'custom') {
            const portsPattern = /^\d+(?:,\d+)*$/;
            isValidPorts = portsPattern.test(portsInput.value.trim());
        }
        
        // Au moins un des deux champs (IP ou domaine) doit être rempli et valide
        const hasValidTarget = (ipValue && isValidIP) || (domainValue && isValidDomain);
        const isValid = hasValidTarget && isValidPorts;
        
        // Enable/disable submit button
        startScanBtn.disabled = !isValid;
    }
    
    // Update form action before submission
    scanForm.addEventListener('submit', function(e) {
        if (scanTypeSelect.value === 'top') {
            portsInput.disabled = true;
        }
    });
    
    // Initial validation
    validateForm();
});
