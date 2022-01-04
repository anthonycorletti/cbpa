import time
from enum import Enum, unique
from typing import Dict, List

from pydantic import BaseModel, PositiveInt, StrictStr, validator
from pydantic.class_validators import root_validator

from coinbasepro_scheduler.schemas.account import Account
from coinbasepro_scheduler.schemas.buy import Buy


@unique
class Frequency(str, Enum):
    seconds = "seconds"
    daily = "daily"
    weekly = "weekly"


@unique
class DayName(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class BaseSchedule(BaseModel):
    pass


class SpecificTimeSchedule(BaseSchedule):
    time: StrictStr

    @validator("time", pre=True, always=True)
    def valid_time_format(cls: BaseSchedule, v: str) -> str:
        """Validate 00:00 format"""
        time.strptime(v, "%H:%M")
        return v


class EverySecondSchedule(BaseSchedule):
    repeat_every: PositiveInt


class EveryDaySchedule(SpecificTimeSchedule):
    time: StrictStr
    repeat_every: PositiveInt


class EveryWeekSchedule(SpecificTimeSchedule):
    day: DayName
    time: StrictStr


class Scheduler(BaseModel):
    name: StrictStr
    frequency: Frequency
    schedule: Dict
    account: Account
    buys: List[Buy]

    @root_validator(pre=True)
    def validate_schedule_frequency(cls: BaseModel, values: Dict) -> Dict:
        if values["frequency"] == Frequency.daily:
            EveryDaySchedule(**values["schedule"])
        elif values["frequency"] == Frequency.weekly:
            EveryWeekSchedule(**values["schedule"])
        elif values["frequency"] == Frequency.seconds:
            EverySecondSchedule(**values["schedule"])
        return values
