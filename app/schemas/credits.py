from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class CreditTransactionType(str, Enum):
    ALLOCATE = "ALLOCATE"
    USAGE = "USAGE"
    REFUND = "REFUND"
    ADJUST = "ADJUST"


class CreditBalanceResponse(BaseModel):
    user_id: int
    balance: int
    updated_at: datetime


class CreditTransactionListQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    type: Optional[CreditTransactionType] = None


class CreditTransactionItem(BaseModel):
    id: int
    type: str
    amount: int
    balance_after: int
    description: Optional[str]
    created_at: datetime


class PageInfo(BaseModel):
    page: int
    size: int
    total: int
    has_next: bool


class CreditTransactionListResponse(BaseModel):
    items: List[CreditTransactionItem]
    page_info: PageInfo