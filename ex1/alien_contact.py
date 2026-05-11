
from pydantic import BaseModel, Field, ValidationError, model_validator
from typing_extensions import Self
from datetime import datetime
from enum import Enum


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0, le=10)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(max_length=500, default=None)
    is_verified: bool = False

    @model_validator(mode='after')
    def validate_contact(self) -> Self:
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID  must start with 'AC'")

        if (self.contact_type == ContactType.physical
                and not self.is_verified):
            raise ValueError("Physical contact reports must be verified")

        if (self.contact_type == ContactType.telepathic
                and self.witness_count < 3):
            raise ValueError("Telepathic contact requires at "
                             "least 3 witnesses")

        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError("Strong signals (> 7.0) should include "
                             "received messages")

        return self

    def display(self) -> None:
        print(f"""Valid contact report:
            ID: {self.contact_id}
            Type: {self.contact_type.value}
            Location: {self.location}
            Signal: {self.signal_strength}/10
            Duration: {self.duration_minutes} minutes
            Witnesses: {self.witness_count}
            Message: {self.message_received}
        """)


def main() -> None:
    try:
        valid_station = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="aera 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="'Greetings from Zeta Reticuli'"
        )

        valid_station.display()

    except ValidationError as e:
        for error in e.errors():
            print(error["msg"].replace("Value error, ", ""))

    print("========================================")
    print("Excepted validation error:")

    try:
        false_station = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location=" aers 51, Nevada",
            contact_type=ContactType.telepathic,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=1,
            message_received="Greetings from Zeta Reticuli"
        )

        false_station.display()

    except ValidationError as e:
        for error in e.errors():
            print(error["msg"].replace("Value error, ", ""))


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("======================================")

    main()
