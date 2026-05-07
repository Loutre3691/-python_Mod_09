
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0, le=100)
    oxygen_level: float = Field(ge=0, le=100)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(max_length=200, default=None)

    def display(self) -> None:
        status = "Operational" if self.is_operational else "Non operational"
        print(f"""Valid station created:
        ID: {self.station_id}
        Name: {self.name}
        Crew: {self.crew_size} people
        Power: {self.power_level}%
        Oxygen: {self.oxygen_level}%
        Status: {status}
        Notes: {self.notes}""")

def main() -> None:
    try:
        valid_station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime.now(),
        is_operational=True,
        notes="👽 the aliens are here 👽"
        )

        valid_station.display()
      
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])
    
    print("\n========================================")
    print("Excepted validation error:")

    try:
        false_station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=21,
        power_level=80,
        oxygen_level=120,
        last_maintenance=datetime.now(),
        is_operational=True,
        notes="hello"
        )

        false_station.display()

    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])

if __name__ == "__main__":
    print("Space Station Data Validation\n"
    "========================================")

    main()