import aiomysql


async def get_connection():
    conn = await aiomysql.connect(
        host='localhost',
        port=3307,
        user='user',
        password='password',
        db='shop'
    )
    return conn
    
async def create_tables():
    conn = await get_connection()    
    async with conn.cursor() as cur:
        sql_create_users_table = '''
        CREATE TABLE IF NOT EXISTS users(
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT NOW());'''

        sql_create_orders_table = '''
        CREATE TABLE IF NOT EXISTS orders(
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        status CHAR(1),
        total DECIMAL(10,2) NOT NULL,
        created_at TIMESTAMP DEFAULT NOW(),
        FOREIGN KEY (user_id) REFERENCES users(id));'''

        sql_create_order_items_table = '''
        CREATE TABLE IF NOT EXISTS order_items(
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        product_id VARCHAR(50) NOT NULL,
        product_name VARCHAR(255),
        price DECIMAL(10,2),
        quantity INT NOT NULL DEFAULT 1)'''

        await cur.execute(sql_create_users_table)
        await cur.execute(sql_create_orders_table)
        await cur.execute(sql_create_order_items_table)
        await conn.commit()
    
    await conn.ensure_closed()