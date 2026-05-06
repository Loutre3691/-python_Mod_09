
from pydantic import BaseModel, Field
# from pydantic import ValidatorError


class SpaceStation(BaseModel):
        name: str
        id: str
        crew: int
        power: float
        oxygen: float
        status: bool

    
if __name__ == "__main__":
    print("Space Station Data Validation\n"
          "========================================")

    valid_station = SpaceStation(
    name="ISS001",
    id="International Space Station",
    crew=6,
    power=85.5,
    oxygen=92.3,
    status="Operational"
    )

    print(valid_station.crew)
    
    #@model_validator(mode=’after’)
    #Field(...)