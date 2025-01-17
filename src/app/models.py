from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import BigInteger


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = 'transaction'

    transaction_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str]
    amount: Mapped[float]
    currency: Mapped[str]
    timestamp: Mapped[str]


class TransactionStatistic(Base):
    __tablename__ = 'transaction_statistic'

    timestamp: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    total_transactions: Mapped[int]
    average_transaction_amount: Mapped[float]





