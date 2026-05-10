# Objectif : Maîtriser la validation 
# personnalisée à l’aide de @model_validator pour 
# les règles métier complexes

from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum

class ContactType(Enum):
    def radio(self) -> None:
        pass

    def visual(self) -> None:
        pass

    def physical(self) -> None:
        pass

    def telepathic(self) -> None:
        pass


class AlienContact(BaseModel):
    # @model_validator(mode=’after’)
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: int = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0, le=10)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(max_length=500, default=None)
    is_verfified: bool = False


    @model_validator()

    def display(self) -> None:
        
    


def main() -> None:
    try:
        valid_station = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location=51,
            contact_type=ContactType,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received='Greetings from Zeta Reticuli'
        )




if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("======================================")
    
    main()