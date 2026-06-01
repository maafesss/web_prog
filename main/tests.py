from django.contrib.auth import get_user_model
User = get_user_model()

for user in User.objects.all():
    print(f"Пользователь: {user.username}")
    print(f"Пароль: {user.password}")
    print(f"Алгоритм хэширования: {user.password.split('$')[0]}")
    print("---")