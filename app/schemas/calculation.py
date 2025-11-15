from __future__ import annotations

from pydantic import BaseModel, Field, model_validator, ConfigDict, ValidationError
from typing import Optional
from uuid import UUID


class CalculationBase(BaseModel):
    a: float = Field(..., description="Left operand")
    b: float = Field(..., description="Right operand")
    type: str = Field(..., description="Operation type: Add, Sub, Multiply, Divide")

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def validate_type_and_operands(cls, values: dict) -> dict:
        t = values.get("type")
        if not t or t not in {"Add", "Sub", "Multiply", "Divide"}:
            raise ValidationError(f"Invalid type: {t}. Must be one of Add, Sub, Multiply, Divide", model=cls)
        # prevent division by zero on create
        if t == "Divide" and values.get("b") == 0:
            raise ValueError("Division by zero is not allowed")
        return values


class CalculationCreate(CalculationBase):
    """Schema for creating a calculation. Accepts a, b and type."""
    pass


class CalculationRead(CalculationBase):
    id: UUID
    result: Optional[float]

    model_config = ConfigDict(from_attributes=True)
