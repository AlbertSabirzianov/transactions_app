import asyncio

from fastapi import APIRouter, Depends, HTTPException

from .schema import SussesResponseSchema, TransactionSchema, ErrorResponse, StatisticSchema, TransactionMiniSchema
from .dependencies import verify_api_key
from .models import Transaction, TransactionStatistic
from .services import save_transaction_in_db, delete_all_from_table, get_last_transactions, get_last_statistic
from .tasks import statistic_task


api_router = APIRouter(dependencies=[Depends(verify_api_key)])


@api_router.post(
    "/transactions",
    responses={
        400: {'model': ErrorResponse},
        200: {'model': SussesResponseSchema}
    }
)
async def create_transaction(transaction_schema: TransactionSchema):
    try:
        await save_transaction_in_db(transaction_schema)
        task = statistic_task.delay()
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
    return SussesResponseSchema(**{
        "message": "Transaction received",
        "task_id": str(task.id)
    })


@api_router.get(
    "/statistics",
    responses={
        200: {'model': StatisticSchema},
        400: {'model': ErrorResponse}
    }
)
async def get_statistic(top_transaction_number: int = 3):
    last_statistic, last_transactions = await asyncio.gather(
        get_last_statistic(),
        get_last_transactions(top_transaction_number)
    )
    if not last_statistic or not last_transactions:
        raise HTTPException(status_code=400, detail="There are no transactions yet")
    return StatisticSchema(
        total_transactions=last_statistic.total_transactions,
        average_transaction_amount=last_statistic.average_transaction_amount,
        top_transactions=[
            TransactionMiniSchema(
                transaction_id=transaction.transaction_id,
                amount=transaction.amount
            ) for transaction in last_transactions
        ]
    )


@api_router.delete("/transactions")
async def delete_all_data():
    await asyncio.gather(
        delete_all_from_table(Transaction),
        delete_all_from_table(TransactionStatistic)
    )
    return {"message": "Deleted"}
