document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.input-group input');
    inputs.forEach(input => {
        if (!input.placeholder) input.placeholder = ' ';

        if (input.value) {
            input.nextElementSibling.classList.add('active');
        }

        input.addEventListener('focus', function() {
            this.nextElementSibling.classList.add('active');
        });

        input.addEventListener('blur', function() {
            if (!this.value) {
                this.nextElementSibling.classList.remove('active');
            }
        });
    });

    // Анимация кнопки
    const authBtn = document.querySelector('.auth-btn');
    if (authBtn) {
        authBtn.addEventListener('mouseenter', function() {
            this.querySelector('i').style.transform = 'translateX(3px)';
        });

        authBtn.addEventListener('mouseleave', function() {
            this.querySelector('i').style.transform = 'translateX(0)';
        });
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const firstInput = document.querySelector('.input-group input');
    if (firstInput) firstInput.focus();
    const loginForm = document.querySelector('.auth-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = this.querySelectorAll('input[required]');

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('error');
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                this.classList.add('shake');
                setTimeout(() => {
                    this.classList.remove('shake');
                }, 500);
            }
        });
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = this.querySelectorAll('input:required');

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                this.classList.add('was-validated');
            }
        });

        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    });

    const authCards = document.querySelectorAll('.card');
    authCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});