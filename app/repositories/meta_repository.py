
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.meta_models import TableInfo, ColumnInfo, MetricInfo, ColumnMetric

class MetaRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_table_by_id(self, table_id: str) -> TableInfo:
        return await self.session.get(TableInfo, table_id)

    async def get_columns_by_table(self, table_id: str) -> list[ColumnInfo]:
        result = await self.session.execute(
            ColumnInfo.__table__.select().where(ColumnInfo.table_id == table_id)
        )
        return result.scalars().all()

    async def get_metric_by_id(self, metric_id: str) -> MetricInfo:
        return await self.session.get(MetricInfo, metric_id)

    async def get_column_metrics(self, column_id: str) -> list[ColumnMetric]:
        result = await self.session.execute(
            ColumnMetric.__table__.select().where(ColumnMetric.column_id == column_id)
        )
        return result.scalars().all()
