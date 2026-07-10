from fastapi import APIRouter
from db.mysql import get_connection


router = APIRouter()

@router.post("/users")
async def create_user(user: dict):
    conn = await get_connection()    
    async with conn.cursor() as cur:
        sql_create_now_user = '''
        INSERT INTO users (email, name) VALUES (%s, %s);'''
        await cur.execute(sql_create_now_user, (user["email"], user["name"]))
        await conn.commit()

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        result = await cur.fetchone()
        return result