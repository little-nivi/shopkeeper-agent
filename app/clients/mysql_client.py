
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.conf.config import DatabaseConfig

class MySQLClient:
    def __init__(self, config: DatabaseConfig):
        self.engine = create_async_engine(
            f"mysql+asyncmy://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"
        )
        self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def get_session(self):
        async with self.session_factory() as session:
            yield session
