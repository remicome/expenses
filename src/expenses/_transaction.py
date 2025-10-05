import dataclasses
import datetime
import typing

from ._member import Member


@dataclasses.dataclass
class Transaction:
    """A transaction paid by one member for one or more other members of the group.

    Args:
        * value: the currency value of this transaction
        * description: a human-readable description
        * date: the date of the transaction
        * payer: the group member who actually paid
        * weights: optional ratios of the debt which should be paid by each member
        * members: the group members for which the transaction was issued.
    """

    value: float
    payer: Member
    members: typing.Set[Member]
    description: str = ""
    weights: None | typing.Mapping[Member, float] = dataclasses.field(default=None)
    date: datetime.date = dataclasses.field(default_factory=datetime.date.today)

    def __post_init__(self):
        if self.weights is None:
            self.weights = {member: 1.0 for member in self.members}


@dataclasses.dataclass
class Food(Transaction):
    """A food transaction, which has a special weighting rule.

    These are weighted according to the member's discount ratio and duration of stay.
    """

    def __post_init__(self):
        self.weights = {
            member: member.discount.value * member.stay_duration
            for member in self.members
        }


@dataclasses.dataclass
class Housing(Transaction):
    """A housing transaction, which has a special weighting rule.

    These are weighted according to the member's discount ratio. Each member pays for
    the maximum number of nights (the logic being that we have to rent a big place for
    everyone). An exception is made for members staying less than 60% of the maximum
    stay duration: in that case, the price to pay is weighed by the member's duration of
    stay.
    """

    def __post_init__(self):
        maximum_stay_duration = max(member.stay_duration for member in self.members)

        def duration_weight(member):
            if member.stay_duration < 0.6 * maximum_stay_duration:
                return member.stay_duration
            else:
                return maximum_stay_duration

        self.weights = {
            member: member.discount.value * duration_weight(member)
            for member in self.members
        }
