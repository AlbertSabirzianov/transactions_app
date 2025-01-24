from datetime import datetime
from typing import Optional, Type, Sequence

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import delete, select, func, insert

from .exeptions import TransactionAlreadyExists
from .settings import DbSettings
from .models import Base, Transaction, TransactionStatistic
from .schema import TransactionSchema

db_settings = DbSettings()
engine = create_async_engine(db_settings.postgres_url, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_transaction_by_id(transaction_id: int) -> Optional[Transaction]:
    async with async_session() as session:
        stmt = select(Transaction).where(Transaction.transaction_id == transaction_id)
        result = await session.scalars(stmt)
        return result.first()


async def save_transaction_in_db(transaction: TransactionSchema) -> None:
    trans = await get_transaction_by_id(transaction.transaction_id)
    if trans:
        raise TransactionAlreadyExists(
            f"Transaction with {transaction.transaction_id} already exists"
        )
    async with async_session() as session:
        session.add(
            Transaction(
                **transaction.model_dump()
            )
        )
        await session.commit()


async def delete_all_from_table(table: Type[Base]) -> None:
    async with async_session() as session:
        stmt = delete(table)
        await session.execute(stmt)
        await session.commit()


async def get_last_statistic() -> Optional[TransactionStatistic]:
    async with async_session() as session:
        stmt = select(TransactionStatistic).order_by(
            TransactionStatistic.timestamp.desc()
        ).limit(1)
        result = await session.scalars(stmt)
        last_statistic = result.first()
        return last_statistic


async def get_biggest_transactions(top: int) -> Sequence[Transaction]:
    async with async_session() as session:
        stmt = select(Transaction).order_by(Transaction.amount.desc()).limit(top)
        result = await session.scalars(stmt)
        return result.fetchall()


async def save_new_statistic_to_db() -> None:
    async with async_session() as session:
        stmt = insert(TransactionStatistic).values(
            timestamp=int(datetime.now().timestamp() * 1000),
            total_transactions=select(func.count(Transaction.transaction_id)).label('total_count'),
            average_transaction_amount=select(func.avg(Transaction.amount)).label('average_amount')
        ).returning(TransactionStatistic)

        await session.execute(stmt)
        await session.commit()
