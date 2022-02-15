from datetime import date
from calendar import monthrange

class MessageCreator():
    RED_ALERT_AMOUNT = 4000
    NOTIFICATION_DAYS = [2, 8, 14, 21, 25, 28, 29, 30, 31]

    def __init__(self, 
                money_collected: int, 
                money_needed: int):
        self.money_collected: int = money_collected
        self.money_needed: int = money_needed

        self._calculate_month_and_days_left()

    def _calculate_month_and_days_left(self):
        today = date.today()

        self.today = today
        self.month: str = today.strftime("%B")
        # The first number is the weekday of the first day of the month, 
        # the second number is the number of days in said month.
        self.days_left: int = monthrange(today.year, today.month)[1] \
                                                                - today.day

    def should_notify(self) -> bool:
        if self.today.day in self.NOTIFICATION_DAYS:
            return True
        elif self.month == "February" and self.days_left < 5:
            return True
        return False

    def create_message(self) -> str:
        difference = self.money_needed - self.money_collected
        message = \
        f"We have gathered {self.money_collected} out of {self.money_needed} rubles. We need to collect {difference} rubles more and we have {self.days_left} days left. Let's close the {self.month} together!"
        if self.days_left < 4 and difference > self.RED_ALERT_AMOUNT:
            message = "RED ALERT!!!!! " + message
        elif self.days_left < 6:
            message = "Hey guys! Yellow Alert!!! " + message
        else:
            message = "Hey guys! " + message
        return message
