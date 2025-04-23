// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            placement: 'right'
        });
    });

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Search functionality
    const searchForm = document.querySelector('.input-group');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const service = this.querySelector('input[placeholder="ما هي الخدمة التي تحتاجها؟"]').value;
            const location = this.querySelector('input[placeholder="الموقع"]').value;
            // Here you would typically make an API call to search for services
            console.log('البحث عن:', service, 'في', location);
        });
    }

    // Service card hover effect
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Mobile menu toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
    }

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            this.classList.add('was-validated');
        });
    });

    // Lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Add animation class on scroll
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.service-card, .feature-icon');
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            if (elementPosition < windowHeight - 100) {
                element.classList.add('animate');
            }
        });
    };

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Initial check

    // Arabic date formatting
    const formatArabicDate = (date) => {
        const options = { 
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };
        return date.toLocaleDateString('ar-SA', options);
    };

    // Update any date elements on the page
    const dateElements = document.querySelectorAll('.date');
    dateElements.forEach(element => {
        const date = new Date(element.textContent);
        element.textContent = formatArabicDate(date);
    });

    // Handle RTL specific interactions
    const handleRTLInteractions = () => {
        // Add any RTL specific event handlers here
        const rtlElements = document.querySelectorAll('[dir="rtl"]');
        rtlElements.forEach(element => {
            // Add any RTL specific event listeners
        });
    };

    handleRTLInteractions();

    // Function to handle craftsman registration
    function handleCraftsmanRegistration(formData) {
        // Get the management data
        fetch('management_data.json')
            .then(response => response.json())
            .then(data => {
                // Create new employee ID
                const newEmployeeId = 'E' + (Object.keys(data.employees).length + 1).toString().padStart(3, '0');
                
                // Create new employee object
                const newEmployee = {
                    employee_id: newEmployeeId,
                    name: formData.get('name'),
                    position: formData.get('profession'),
                    email: formData.get('email'),
                    phone: formData.get('phone'),
                    salary_history: [],
                    performance_reviews: []
                };

                // Add to employees
                data.employees[newEmployeeId] = newEmployee;

                // Save updated data
                return fetch('management_data.json', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
            })
            .then(response => {
                if (response.ok) {
                    alert('تم تسجيل الحرفي بنجاح!');
                    window.location.href = 'management.html';
                } else {
                    throw new Error('Network response was not ok');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('حدث خطأ أثناء التسجيل. يرجى المحاولة مرة أخرى.');
            });
    }

    // Function to handle service requests
    function handleServiceRequest(formData) {
        fetch('management_data.json')
            .then(response => response.json())
            .then(data => {
                // Create new customer ID
                const newCustomerId = 'C' + (Object.keys(data.customers).length + 1).toString().padStart(3, '0');
                
                // Create new customer object
                const newCustomer = {
                    customer_id: newCustomerId,
                    name: formData.get('name'),
                    email: formData.get('email'),
                    phone: formData.get('phone'),
                    address: formData.get('address'),
                    requests: [{
                        type: formData.get('service_type'),
                        description: formData.get('description'),
                        date: new Date().toISOString(),
                        status: 'Pending'
                    }],
                    evaluations: []
                };

                // Add to customers
                data.customers[newCustomerId] = newCustomer;

                // Create new transaction
                const newTransactionId = 'T' + (Object.keys(data.transactions).length + 1).toString().padStart(3, '0');
                const newTransaction = {
                    transaction_id: newTransactionId,
                    customer_id: newCustomerId,
                    amount: parseFloat(formData.get('budget')),
                    transaction_type: 'pending',
                    description: formData.get('service_type'),
                    date: new Date().toISOString()
                };

                // Add to transactions
                data.transactions[newTransactionId] = newTransaction;

                // Save updated data
                return fetch('management_data.json', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
            })
            .then(response => {
                if (response.ok) {
                    alert('تم تقديم طلب الخدمة بنجاح!');
                    window.location.href = 'management.html';
                } else {
                    throw new Error('Network response was not ok');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('حدث خطأ أثناء تقديم الطلب. يرجى المحاولة مرة أخرى.');
            });
    }

    // Function to handle customer evaluation
    function handleCustomerEvaluation(formData) {
        fetch('management_data.json')
            .then(response => response.json())
            .then(data => {
                const customerId = formData.get('customer_id');
                if (data.customers[customerId]) {
                    // Add evaluation
                    data.customers[customerId].evaluations.push({
                        rating: parseInt(formData.get('rating')),
                        comment: formData.get('comment'),
                        date: new Date().toISOString()
                    });

                    // Save updated data
                    return fetch('management_data.json', {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });
                } else {
                    throw new Error('Customer not found');
                }
            })
            .then(response => {
                if (response.ok) {
                    alert('تم تقديم التقييم بنجاح!');
                    window.location.href = 'management.html';
                } else {
                    throw new Error('Network response was not ok');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('حدث خطأ أثناء تقديم التقييم. يرجى المحاولة مرة أخرى.');
            });
    }

    // Craftsman registration form
    const craftsmanForm = document.getElementById('craftsman-registration-form');
    if (craftsmanForm) {
        craftsmanForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(craftsmanForm);
            handleCraftsmanRegistration(formData);
        });
    }

    // Service request form
    const serviceForm = document.getElementById('service-request-form');
    if (serviceForm) {
        serviceForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(serviceForm);
            handleServiceRequest(formData);
        });
    }

    // Evaluation form
    const evaluationForm = document.getElementById('evaluation-form');
    if (evaluationForm) {
        evaluationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(evaluationForm);
            handleCustomerEvaluation(formData);
        });
    }

    // Function to handle contact form submission
    function handleContactForm(formData) {
        // Here you would typically send the data to a server
        // For now, we'll just show a success message
        const contactData = {
            name: formData.get('name'),
            email: formData.get('email'),
            subject: formData.get('subject'),
            message: formData.get('message'),
            date: new Date().toISOString()
        };

        console.log('Contact Form Data:', contactData);
        alert('تم إرسال رسالتك بنجاح! سنتواصل معك قريباً.');
        return true;
    }

    // Contact form
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(contactForm);
            if (handleContactForm(formData)) {
                contactForm.reset();
            }
        });
    }
}); 