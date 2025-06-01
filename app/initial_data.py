from app.database import check_db_exists, Base, engine
from app.users.auth import get_password_hash
from app.users.service import UsersService

async def init_db():
    existing_tables = await check_db_exists()

    if not existing_tables:
        print("Создание таблиц базы данных...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Таблицы созданы.")
    else:
        print("Таблицы уже существуют.")

    admin_exists = await UsersService.find_one_or_none(username="admin")
    if not admin_exists:
        print("Создаём администратора...")
        hashed_password = get_password_hash("admin")
        await UsersService.add(
            email="admin@admin.ru",
            hash_password=hashed_password,
            name="admin",
            surname="admin",
            patronymic="admin",
            username="admin",
            is_admin=True
        )
        print("Администратор создан.")
    else:
        print("Администратор уже существует.")