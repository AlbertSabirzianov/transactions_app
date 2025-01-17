from pydantic import BaseModel


class TransactionSchema(BaseModel):

    transaction_id: int
    user_id: str
    amount: float
    currency: str
    timestamp: str


class TransactionMiniSchema(BaseModel):
    transaction_id: int
    amount: float


class StatisticSchema(BaseModel):
    total_transactions: int
    average_transaction_amount: float
    top_transactions: list[TransactionMiniSchema]


class SussesResponseSchema(BaseModel):
    message: str
    task_id: str


class ErrorResponse(BaseModel):
    detail: str
