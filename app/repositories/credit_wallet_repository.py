from sqlalchemy.ext.asyncio import AsyncSession

from app.models.credit import CreditWallet


async def create_credit_wallet(
    db: AsyncSession,
    user_id: int,
) -> CreditWallet:
    wallet = CreditWallet(
        user_id=user_id,
        balance=0,
    )
    db.add(wallet)
    await db.flush()
    return wallet