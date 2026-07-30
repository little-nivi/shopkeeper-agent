
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TableInfo(Base):
    __tablename__ = "table_info"
    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    role = Column(String(16), nullable=False)
    description = Column(Text)

class ColumnInfo(Base):
    __tablename__ = "column_info"
    id = Column(String(128), primary_key=True)
    name = Column(String(128), nullable=False)
    type = Column(String(64), nullable=False)
    role = Column(String(16), nullable=False)
    examples = Column(Text)
    description = Column(Text)
    alias = Column(Text)
    table_id = Column(String(64), ForeignKey("table_info.id"))

class MetricInfo(Base):
    __tablename__ = "metric_info"
    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    relevant_columns = Column(Text)
    alias = Column(Text)

class ColumnMetric(Base):
    __tablename__ = "column_metric"
    column_id = Column(String(128), ForeignKey("column_info.id"), primary_key=True)
    metric_id = Column(String(64), ForeignKey("metric_info.id"), primary_key=True)
