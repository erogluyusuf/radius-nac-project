import os
import asyncpg
import redis.asyncio as redis

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ["DB_NAME"]

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db_pool = None
redis_client = None

async def connect_db():
    global db_pool
    db_pool = await asyncpg.create_pool(dsn=DATABASE_URL)

async def disconnect_db():
    global db_pool
    if db_pool:
        await db_pool.close()

async def connect_redis():
    global redis_client
    redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True)

async def disconnect_redis():
    global redis_client
    if redis_client:
        await redis_client.close()

def get_db():
    return db_pool

def get_redis():
    return redis_client
