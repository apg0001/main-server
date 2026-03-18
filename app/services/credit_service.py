from app.repositories.credit_repository import CreditRepository
from app.schemas.credits import (
    CreditBalanceResponse,
    CreditTransactionItem,
    CreditTransactionListQuery,
    CreditTransactionListResponse,
    PageInfo,
)


class CreditService:
    def __init__(self, repository: CreditRepository):
        self.repository = repository

    async def get_credit_balance(self, user_id: int) -> CreditBalanceResponse:
        exists = await self.repository.user_exists(user_id)
        if not exists:
            raise ValueError("NOT_FOUND")

        result = await self.repository.get_credit_balance(user_id)
        return CreditBalanceResponse(**result)

    async def get_credit_transactions(
        self,
        user_id: int,
        query: CreditTransactionListQuery,
    ) -> CreditTransactionListResponse:
        exists = await self.repository.user_exists(user_id)
        if not exists:
            raise ValueError("NOT_FOUND")

        rows, total = await self.repository.get_credit_transactions(
            user_id=user_id,
            query=query,
        )

        items = [CreditTransactionItem(**row) for row in rows]

        return CreditTransactionListResponse(
            items=items,
            page_info=PageInfo(
                page=query.page,
                size=query.size,
                total=total,
                has_next=query.page * query.size < total,
            ),
        )