FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir \
    --timeout 120 \
    -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    -r requirements.txt
COPY . .
EXPOSE 80

# Запуск с подробным логированием
CMD python manage.py makemigrations && \
    python manage.py migrate && \
    python -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" && \
    python manage.py runserver 0.0.0.0:80 --verbosity 2