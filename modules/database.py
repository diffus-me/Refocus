import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from sqlalchemy import String, Integer, DateTime, Text, func, select
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from dotenv import dotenv_values
config = dotenv_values(".env")

SQLALCHEMY_DATABASE_URL = config.get('SQL_DATABASE_URL')

if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = os.environ['SQL_DATABASE_URL']

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
    },
    pool_pre_ping=True,
    pool_recycle=3600
)
Session = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_db():
    async with Session() as session:
        yield session


class FocusTaskRecord(Base):
    __tablename__ = "focus_task_records"

    id = mapped_column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id = mapped_column(String(64), index=True, nullable=False)
    task_id = mapped_column(String(64), index=True, nullable=False)
    hostname = mapped_column(String(64), index=True, nullable=False)
    server_ip = mapped_column(String(32), index=True, nullable=False)
    status = mapped_column(String(16), index=True, nullable=False)
    params = mapped_column(Text, nullable=False)
    result = mapped_column(Text, nullable=True)
    created_at = mapped_column(DateTime(), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(), server_default=func.now(), nullable=False)
    started_at = mapped_column(DateTime(), nullable=True)
    finished_at = mapped_column(DateTime(), nullable=True)


async def insert_focus_task_record(
        session: AsyncSession, user_id: str, task_id: str, status: str, params: str, hostname: str, ip: str) -> FocusTaskRecord:
    record = FocusTaskRecord(user_id=user_id, task_id=task_id, status=status, params=params, hostname=hostname, server_ip=ip)
    session.add(record)
    await session.commit()
    return record


async def update_focus_task_record(
        session: AsyncSession,
        task_id: str,
        status: str,
        result: str | None = None,
        started_at: datetime | None = None,
        finished_at: datetime | None = None) -> FocusTaskRecord | None:
    statement = select(FocusTaskRecord).where(FocusTaskRecord.task_id == task_id).limit(1)
    query_result = await session.execute(statement)
    record = query_result.scalar_one_or_none()
    if record:
        record.status = status
        if result:
            record.result = result
        if started_at:
            record.started_at = started_at
        if finished_at:
            record.finished_at = finished_at
        record.updated_at = datetime.now(timezone.utc)
        await session.commit()
        return record
    return None


async def query_focus_task_record_with_status(
        session: AsyncSession, user_id: str, status: str) -> list[FocusTaskRecord]:
    statement = select(FocusTaskRecord).where(
        FocusTaskRecord.user_id == user_id, FocusTaskRecord.status == status).order_by(FocusTaskRecord.created_at.desc())
    query_result = await session.execute(statement)
    records = query_result.scalars().all()
    return list(records)
