FROM python:3.11-slim 
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir \
    --timeout 120 \
    -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]