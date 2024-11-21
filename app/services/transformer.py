from datetime import datetime
from typing import List

async def transform_data(validated_data: List[dict]) -> List[dict]:
    transformed_data = []

    for record in validated_data:
        transformed_record = {
            "id": record["customer_id"],
            "full_name": record["name"],
            "contact_email": record["email"],
            "registration_date": datetime.strptime(record["signup_date"], "%Y-%m-%d").isoformat(),
            "active_status": "active" if record["is_active"] else "inactive"
        }
        transformed_data.append(transformed_record)

    return transformed_data