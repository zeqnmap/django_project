# Практическая работа

## Цель практической работы
Научиться создавать интерактивную Swagger-документацию для своего проекта на Django REST framework.

### Что нужно сделать
Воспользуйтесь кодовой базой из пройденных модулей или файлами из репозитория с практической работой.

1. Установите библиотеку drf-spectacular, заморозьте зависимости.
2. Обновите настройки в mysite/settings.py:
   - Установите drf_spectacular в INSTALLED_APPS; 
   - REST_FRAMEWORK — добавьте DEFAULT_SCHEMA_CLASS, указывающий на AutoSchema из drf_spectacular; 
   - SPECTACULAR_SETTINGS — укажите TITLE, DESCRIPTION, VERSION, SERVE_INCLUDE_SCHEMA.
3. Обновите mysite/urls.py. Укажите SpectacularAPIView и SpectacularSwaggerView для интерактивной документации.\


### Что оценивается
- Установлена библиотека drf_spectacular.
- В настройках проекта settings.py: 
   - установлено приложение drf_spectacular:
   - указаны дополнительные настройки:
      - DEFAULT_SCHEMA_CLASS в REST_FRAMEWORK;
      - параметры в SPECTACULAR_SETTINGS.
   - Указаны адреса в urls для SpectacularAPIView и SpectacularSwaggerView.

### Как отправить работу на проверку
Сдайте практическую работу через Skillbox GitLab. В поле для сдачи практической работы напишите «Сделано» и прикрепите ссылку на репозиторий.