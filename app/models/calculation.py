from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.database import Base


class Calculation(Base):
    """SQLAlchemy model for arithmetic calculations.

    Fields:
    - id: UUID primary key
    - a, b: numeric operands (stored as floats)
    - type: one of 'Add', 'Sub', 'Multiply', 'Divide'
    - user_id: optional FK to users.id

    The `result` is not persisted; it's computed on-demand via a hybrid_property.
    This avoids storing stale results while keeping the value accessible from ORM objects.
    """

    __tablename__ = "calculations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(String(20), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # Optional relationship to User if the user model is present
    user = relationship("User", backref="calculations", lazy="joined")

    def __repr__(self) -> str:  # pragma: no cover - small helper
        return f"<Calculation(id={self.id}, type={self.type}, a={self.a}, b={self.b})>"

    @hybrid_property
    def result(self) -> Optional[float]:
        """Compute the calculation result on demand.

        Returns None for invalid operations (e.g., division by zero).
        """
        try:
            if self.type == "Add":
                return self.a + self.b
            if self.type == "Sub":
                return self.a - self.b
            if self.type == "Multiply":
                return self.a * self.b
            if self.type == "Divide":
                if self.b == 0:
                    return None
                return self.a / self.b
        except Exception:
            return None
