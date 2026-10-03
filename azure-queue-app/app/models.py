from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    sku: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: float = Field(ge=0)


class OrderRequest(BaseModel):
    customer: str = Field(min_length=1)
    items: list[OrderItem] = Field(min_length=1)
