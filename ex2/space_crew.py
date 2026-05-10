from pydantic import BaseModel, Field, ValidationError, model_validator
from typing_extensions import Self 
from datetime import datetime
from enum import Enum

class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"
    

class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date : datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1, le=10000)


    @model_validator(mode='after')
    def validation_mission(self) -> Self:
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
        
        if not any(Rank.captain in grad or Rank.commander in grad for grad in self.crew):
            raise ValueError("Must have at least one Commander or Captain")
    
        # if self.duration_day > 365:
        #     raise ValueError("Telepathic contact requires at least 3 witnesses")

        # if not any(self.is_active in for member in self.crew_list):
        #     raise ValueError("Strong signals (> 7.0) should include received messages")
 
        return self
    

    def display(self) -> None:
        print(f"""Valid mission created:
Mission: {self.mission_name}
ID: {self.mission_id}
Destination: {self.destination}
Duration: {self.duration_days} days
Budget: {self.budget_millions}M
Crew size: {len(self.crew)}
Crew members:
        """)
        for member in self.crew:
            print(f" - {member.name} ({member.rank.value})  - {member.specialization}")
   

def main() -> None:
    valid_crew = [
    CrewMember(
        member_id="SC001",
        name="Sarah Connor",
        rank=Rank.commander,
        age=35,
        specialization="Mission Command",
        years_experience=10
    ),
    CrewMember(
        member_id="JS002",
        name="John Smith",
        rank=Rank.lieutenant,
        age=28,
        specialization="Navigation",
        years_experience=6
    ),
    CrewMember(
        member_id="AJ003",
        name="Alice Johnson",
        rank=Rank.officer,
        age=30,
        specialization="Engineering",
        years_experience=7
    ),
    ]

    bad_crew = [
    CrewMember(
        member_id="SC001",
        name="Sarah Connor",
        rank=Rank.officer,
        age=35,
        specialization="Mission Command",
        years_experience=10
    ),
    CrewMember(
        member_id="JS002",
        name="John Smith",
        rank=Rank.officer,
        age=28,
        specialization="Navigation",
        years_experience=6
    ),
    CrewMember(
        member_id="AJ003",
        name="Alice Johnson",
        rank=Rank.officer,
        age=30,
        specialization="Engineering",
        years_experience=7
    ),
    ]

    try:
        valid_mission = SpaceMission(
        mission_name="Mars Colony Establishment",
        mission_id="M2024_MARS",
        destination="Mars",
        duration_days=900,
        budget_millions=2500.0,
        crew=valid_crew,
        launch_date=datetime.now()
        )

        valid_mission.display()
    
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])


    print("========================================")
    print("Excepted validation error:")

    try:
        false_mission = SpaceMission(
        mission_name="Mars Colony Establishment",
        mission_id="M2024_MARS",
        destination="Mars",
        duration_days=900,
        budget_millions=2500.0,
        crew=bad_crew,
        launch_date=datetime.now()
        )

        false_mission.display()
    
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])



if __name__ == "__main__":
    print("Space Mission Crew Validation")
    print("======================================")
    
    main()
