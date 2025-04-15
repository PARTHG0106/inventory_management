document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    var addFormField = document.querySelector('.add-form-field');
    if (addFormField) {
        addFormField.addEventListener('click', function(e) {
            e.preventDefault();
            var formRow = this.closest('.form-row');
            var newRow = formRow.cloneNode(true);
            formRow.parentNode.insertBefore(newRow, formRow.nextSibling);
        });
    }

    var fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            var fileName = e.target.files[0].name;
            var label = input.nextElementSibling;
            if (label && label.classList.contains('custom-file-label')) {
                label.textContent = fileName;
            }
        });
    });

    var searchInput = document.querySelector('.search-input');
    if (searchInput) {
        var searchTimeout;
        searchInput.addEventListener('input', function(e) {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                performSearch(e.target.value);
            }, 500);
        });
    }

    var bulkActionCheckboxes = document.querySelectorAll('.bulk-action-checkbox');
    var bulkActionSelect = document.querySelector('.bulk-action-select');
    if (bulkActionSelect) {
        bulkActionSelect.addEventListener('change', function(e) {
            var selectedAction = e.target.value;
            var selectedItems = Array.from(bulkActionCheckboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.value);
            
            if (selectedItems.length > 0 && selectedAction) {
                handleBulkAction(selectedAction, selectedItems);
            }
        });
    }

    var barcodeInput = document.querySelector('.barcode-input');
    if (barcodeInput) {
        barcodeInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                handleBarcodeScan(this.value);
            }
        });
    }
});

function performSearch(query) {
    fetch(`/api/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            updateSearchResults(data);
        })
        .catch(error => console.error('Error:', error));
}

function updateSearchResults(data) {
    var resultsContainer = document.querySelector('.search-results');
    if (resultsContainer) {
        resultsContainer.innerHTML = '';
        data.forEach(item => {
            resultsContainer.innerHTML += `
                <div class="search-result-item">
                    <h5>${item.name}</h5>
                    <p>${item.description}</p>
                </div>
            `;
        });
    }
}

function handleBulkAction(action, items) {
    fetch('/api/bulk-action/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            action: action,
            items: items
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Error performing bulk action');
        }
    })
    .catch(error => console.error('Error:', error));
}

function handleBarcodeScan(barcode) {
    fetch(`/api/barcode/${encodeURIComponent(barcode)}/`)
        .then(response => response.json())
        .then(data => {
            if (data.product) {
                updateProductInfo(data.product);
            } else {
                alert('Product not found');
            }
        })
        .catch(error => console.error('Error:', error));
}

function updateProductInfo(product) {
    var form = document.querySelector('.product-form');
    if (form) {
        form.querySelector('[name="name"]').value = product.name;
        form.querySelector('[name="price"]').value = product.price;
        form.querySelector('[name="quantity"]').value = product.quantity;
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function validateForm(form) {
    var isValid = true;
    form.querySelectorAll('[required]').forEach(function(input) {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });
    return isValid;
}

function showLoading() {
    var spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    spinner.innerHTML = `
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    `;
    document.body.appendChild(spinner);
}

function hideLoading() {
    var spinner = document.querySelector('.loading-spinner');
    if (spinner) {
        spinner.remove();
    }
} 