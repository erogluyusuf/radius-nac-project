from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from datetime import datetime
from app.database import connect_db, disconnect_db, connect_redis, disconnect_redis, get_db, get_redis
from app.models import AuthRequest, AcctRequest

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    await connect_redis()
    yield
    await disconnect_db()
    await disconnect_redis()

app = FastAPI(lifespan=lifespan)

@app.post("/auth")
async def auth(req: AuthRequest):
    db = get_db()
    redis_client = get_redis()

    identifier = req.username or req.calling_station_id
    if not identifier:
        raise HTTPException(status_code=401, detail="Reject")

    attempts = await redis_client.get(f"auth_fails:{identifier}")
    if attempts and int(attempts) >= 5:
        raise HTTPException(status_code=401, detail="Rate limit exceeded")

    async with db.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT value FROM radcheck WHERE username = $1 AND attribute = 'Cleartext-Password'",
            identifier
        )

        if user and req.password and user['value'] == req.password:
            await redis_client.delete(f"auth_fails:{identifier}")
            return {"status": "Accept"}

        mac_user = await conn.fetchrow(
            "SELECT value FROM radcheck WHERE username = $1 AND attribute = 'Calling-Station-Id'",
            identifier
        )
        if mac_user and req.password == identifier:
            await redis_client.delete(f"auth_fails:{identifier}")
            return {"status": "Accept"}

    await redis_client.incr(f"auth_fails:{identifier}")
    await redis_client.expire(f"auth_fails:{identifier}", 300)
    raise HTTPException(status_code=401, detail="Reject")
@app.post("/authorize")
async def authorize(req: AuthRequest):
    db = get_db()
    identifier = req.username or req.calling_station_id
    reply_dict = {"control:Auth-Type": "rest"}

    async with db.acquire() as conn:
        reply_attrs = await conn.fetch(
            "SELECT attribute, value FROM radreply WHERE username = $1",
            identifier
        )
        for row in reply_attrs:
            reply_dict[row['attribute']] = row['value']

        group_rows = await conn.fetch(
            "SELECT groupname FROM radusergroup WHERE username = $1 ORDER BY priority DESC",
            identifier
        )
        for group_row in group_rows:
            group_attrs = await conn.fetch(
                "SELECT attribute, value FROM radgroupreply WHERE groupname = $1",
                group_row['groupname']
            )
            for g_attr in group_attrs:
                if g_attr['attribute'] not in reply_dict:
                    reply_dict[g_attr['attribute']] = g_attr['value']

    return reply_dict

@app.post("/accounting")
async def accounting(req: AcctRequest):
    db = get_db()
    redis_client = get_redis()

    async with db.acquire() as conn:
        if req.acct_status_type == "Start":
            await conn.execute(
                ,
                req.acct_session_id, req.username, req.nas_ip_address, req.calling_station_id, req.called_station_id
            )
            session_data = {"username": str(req.username), "ip": str(req.nas_ip_address), "start": datetime.now().isoformat()}
            await redis_client.hset(f"session:{req.acct_session_id}", mapping=session_data)

        elif req.acct_status_type == "Interim-Update":
            await conn.execute(
                ,
                req.acct_input_octets, req.acct_output_octets, req.acct_session_id
            )

        elif req.acct_status_type == "Stop":
            await conn.execute(
                ,
                req.acct_session_time, req.acct_input_octets, req.acct_output_octets, req.acct_terminate_cause, req.acct_session_id
            )
            await redis_client.delete(f"session:{req.acct_session_id}")

    return {"status": "ok"}

@app.get("/users")
async def get_users():
    db = get_db()
    async with db.acquire() as conn:
        users = await conn.fetch("SELECT username, attribute, value FROM radcheck")
        return [dict(u) for u in users]

@app.get("/sessions/active")
async def get_active_sessions():
    redis_client = get_redis()
    keys = await redis_client.keys("session:*")
    sessions = []
    for key in keys:
        data = await redis_client.hgetall(key)
        sessions.append({"session_id": key.split(":")[1], **data})
    return sessions
