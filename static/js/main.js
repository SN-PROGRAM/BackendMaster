// Данные для курсов
const coursesData = [
    {
        icon: 'fab fa-python',
        title: 'Django с нуля до PRO',
        description: 'Полный курс по созданию веб-приложений на Django. Изучите ORM, шаблоны, формы, аутентификацию и REST API.',
        duration: '8 недель'
    },
    {
        icon: 'fas fa-database',
        title: 'Базы данных и SQL',
        description: 'Глубокое погружение в работу с базами данных. PostgreSQL, оптимизация запросов, индексы и транзакции.',
        duration: '6 недель'
    },
    {
        icon: 'fas fa-plug',
        title: 'REST API разработка',
        description: 'Создание современных API с использованием Django REST Framework. Документирование, авторизация, пагинация.',
        duration: '5 недель'
    },
    {
        icon: 'fas fa-shield-alt',
        title: 'Безопасность веб-приложений',
        description: 'Защита от распространенных уязвимостей: SQL-инъекции, XSS, CSRF и другие методы защиты.',
        duration: '4 недели'
    }
];

// Данные структуры проекта
const projectStructure = [
    {
        name: 'BackendMaster/',
        files: ['settings.py', 'urls.py', 'wsgi.py']
    },
    {
        name: 'courses/',
        files: ['models.py', 'views.py', 'urls.py']
    },
    {
        name: 'tasks/',
        files: ['models.py', 'views.py', 'urls.py']
    },
    {
        name: 'users/',
        files: ['models.py', 'views.py', 'urls.py']
    },
    {
        name: 'static/',
        files: ['css/', 'js/', 'images/']
    },
    {
        name: '',
        files: ['manage.py', 'requirements.txt', 'README.md', '.gitignore']
    }
];

// Данные команд
const commandsData = [
    {
        title: 'Разработка',
        commands: [
            {
                command: 'python manage.py runserver',
                description: 'Запуск сервера разработки'
            },
            {
                command: 'python manage.py migrate',
                description: 'Применение миграций'
            },
            {
                command: 'python manage.py makemigrations',
                description: 'Создание миграций'
            },
            {
                command: 'python manage.py createsuperuser',
                description: 'Создание администратора'
            }
        ]
    },
    {
        title: 'Git',
        commands: [
            {
                command: 'git checkout -b имя-ветки',
                description: 'Создание новой ветки'
            },
            {
                command: 'git push origin имя-ветки',
                description: 'Отправка ветки на GitHub'
            },
            {
                command: 'git checkout main',
                description: 'Переход на основную ветку'
            },
            {
                command: 'git pull origin main',
                description: 'Получение актуальной версии'
            }
        ]
    },
    {
        title: 'Рекомендации',
        commands: [
            {
                command: 'git commit -m "Описание"',
                description: 'Осмысленные описания коммитов'
            },
            {
                command: 'pip freeze > requirements.txt',
                description: 'Обновление зависимостей'
            },
            {
                command: 'git merge --no-ff имя-ветки',
                description: 'Слияние с сохранением истории'
            },
            {
                command: 'python -m venv .venv',
                description: 'Создание виртуального окружения'
            }
        ]
    }
];

// Функция для отображения курсов
function renderCourses() {
    const coursesContainer = document.querySelector('.course-cards');

    coursesData.forEach((course, index) => {
        const courseCard = document.createElement('div');
        courseCard.className = 'course-card';
        courseCard.style.transitionDelay = `${index * 0.1}s`;

        courseCard.innerHTML = `
            <div class="course-img">
                <i class="${course.icon}"></i>
            </div>
            <div class="course-content">
                <h3>${course.title}</h3>
                <p>${course.description}</p>
                <div class="course-duration">
                    <i class="far fa-clock"></i>
                    <span>${course.duration}</span>
                </div>
                <a href="#" class="btn">Подробнее</a>
            </div>
        `;

        coursesContainer.appendChild(courseCard);
    });
}

// Функция для отображения структуры проекта
function renderProjectStructure() {
    const structureContainer = document.querySelector('.structure-container');

    projectStructure.forEach(item => {
        if (item.name) {
            const folder = document.createElement('div');
            folder.className = 'folder';

            const folderName = document.createElement('div');
            folderName.className = 'folder-name';
            folderName.innerHTML = `<i class="far fa-folder"></i>${item.name}`;

            folder.appendChild(folderName);

            item.files.forEach(file => {
                const fileElement = document.createElement('div');
                fileElement.className = 'file';
                fileElement.innerHTML = `<i class="far fa-file"></i>${file}`;
                folder.appendChild(fileElement);
            });

            structureContainer.appendChild(folder);
        } else {
            item.files.forEach(file => {
                const fileElement = document.createElement('div');
                fileElement.className = 'file';
                fileElement.innerHTML = `<i class="far fa-file"></i>${file}`;
                structureContainer.appendChild(fileElement);
            });
        }
    });
}

// Функция для отображения команд
function renderCommands() {
    const commandsContainer = document.querySelector('.command-categories');

    commandsData.forEach((category, index) => {
        const categoryElement = document.createElement('div');
        categoryElement.className = 'command-category';
        categoryElement.style.transitionDelay = `${index * 0.1}s`;

        let commandsHTML = `<h3>${category.title}</h3>`;

        category.commands.forEach(cmd => {
            commandsHTML += `
                <div class="command-item">
                    <div class="command">${cmd.command}</div>
                    <div class="command-desc">${cmd.description}</div>
                </div>
            `;
        });

        categoryElement.innerHTML = commandsHTML;
        commandsContainer.appendChild(categoryElement);
    });
}

// Функция для проверки видимости элементов
function checkVisibility() {
    const elements = document.querySelectorAll('.course-card, .command-category');

    elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        const isVisible = (rect.top <= window.innerHeight * 0.8);

        if (isVisible) {
            el.classList.add('visible');
        }
    });
}

// Функция для обработки формы
function handleFormSubmit(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    // Здесь можно добавить отправку данных на сервер
    alert(`Спасибо, ${name}! Ваш вопрос получен. Мы ответим вам на email ${email} в ближайшее время.`);

    // Очистка формы
    event.target.reset();
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    // Установка текущего года в футере
    document.getElementById('current-year').textContent = new Date().getFullYear();

    // Рендеринг данных
    renderCourses();
    renderProjectStructure();
    renderCommands();

    // Обработчик формы
    document.getElementById('contact-form').addEventListener('submit', handleFormSubmit);

    // Обработчик плавной прокрутки
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Проверка видимости элементов при загрузке и скролле
    window.addEventListener('load', checkVisibility);
    window.addEventListener('scroll', checkVisibility);

    // Первоначальная проверка видимости
    checkVisibility();
});