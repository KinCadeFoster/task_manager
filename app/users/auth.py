from app.users.hashing import verify_password


async def authenticate_user(username: str, password: str):
    from app.users.service import UsersService  # импорт ВНУТРИ функции
    user = await UsersService.find_one_or_none(username=username)
    if not user or not verify_password(password, user.hash_password):
        return None
    return user
