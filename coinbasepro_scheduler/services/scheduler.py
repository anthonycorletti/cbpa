import schedule

from coinbasepro_scheduler.schemas.scheduler import Frequency, Scheduler
from coinbasepro_scheduler.services.account import AccountService
from coinbasepro_scheduler.services.buy import BuyService


class SchedulerService:
    def __init__(self) -> None:
        pass

    def set_schedules(
        self,
        scheduler: Scheduler,
        buy_service: BuyService,
        account_service: AccountService,
    ) -> None:
        if scheduler.frequency == Frequency.seconds:
            schedule.every(scheduler.schedule["repeat_every"]).seconds.do(
                buy_service.recurring_buy,
                scheduler=scheduler,
                account_service=account_service,
            )
        elif scheduler.frequency == Frequency.daily:
            schedule.every(scheduler.schedule["repeat_every"]).days.at(
                scheduler.schedule["time"]
            ).do(
                buy_service.recurring_buy,
                scheduler=scheduler,
                account_service=account_service,
            )
        elif scheduler.frequency == Frequency.weekly:
            getattr(schedule.every(), scheduler.schedule["day"]).at(
                scheduler.schedule["time"]
            ).do(
                buy_service.recurring_buy,
                scheduler=scheduler,
                account_service=account_service,
            )
