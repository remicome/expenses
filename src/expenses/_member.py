import dataclasses
import enum


class Discount(enum.Enum):
    """Self-declared discount on special items (food and housing)."""

    P1 = 0.75
    P2 = 1
    P3 = 1.25


@dataclasses.dataclass(frozen=True, repr=False)
class Member:
    """A member of the group whose expenses should be shared.

    Args:
        * discount: discount category for this member
        * stay_duration: stay duration (in days)
    """

    name: str
    discount: Discount = dataclasses.field(hash=False, default=Discount.P2)
    stay_duration: int = 0

    def __repr__(self) -> str:
        return self.name
