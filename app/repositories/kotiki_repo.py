from psycopg_pool import AsyncConnectionPool


class KotikiRepository:
    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool

    async def list_kotiki(self, limit: int, offset: int) -> list[dict]:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "select id::text as id, name from kotiki order by id limit %s offset %s",
                    (limit, offset),
                )
                rows = await cur.fetchall()
        return [{"id": row[0], "name": row[1]} for row in rows]

    async def create_kotik(self, kotik_id: str, name: str) -> dict:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "insert into kotiki (id, name) values (%s, %s) returning id::text as id, name",
                    (kotik_id, name),
                )
                row = await cur.fetchone()
            await conn.commit()
        return {"id": row[0], "name": row[1]}
