from pydantic import BaseModel, Field, EmailStr, ValidationError
from typing import List, Optional

# Define Validation Schema
class CustomerData(BaseModel):
    customer_id: int = Field(..., gt=0, description="Unique customer ID")
    name: str = Field(..., min_length=1, max_length=100, description="Customer name")
    email: EmailStr = Field(..., description="Customer email address")
    signup_date: str = Field(..., pattern=r"\d{4}-\d{2}-\d{2}", description="Signup date in YYYY-MM-DD format")
    is_active: Optional[bool] = Field(default=True, description="Is the customer active")

# Validation Function
async def validate_data(rows: List[dict]) -> List[dict]:
    validated_data = []
    errors = []

    for i, row in enumerate(rows):
        try:
            validated_data.append(CustomerData(**row).model_dump())
        except ValidationError as e:
            errors.append({"row": i + 1, "errors": e.errors()})
    
    if errors:
        raise ValueError(f"Validation failed: {errors}")

    return validated_data