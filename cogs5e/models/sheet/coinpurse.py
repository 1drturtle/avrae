from cogs5e.models.errors import InvalidArgument
from .mixins import HasIntegrationMixin

CoinTypes = {
    "pp": {
        "icon": "<:DDBPlatinum:948681049326624849>",
        "name": "Platinum",
        "gSheet": {
            "v14": "D72",
            "v2": "D15",
        }
    },
    "gp": {
        "icon": "<:DDBGold:948681049221775370>",
        "name": "Gold",
        "gSheet": {
            "v14": "D69",
            "v2": "D12",
        }
    },
    "ep": {
        "icon": "<:DDBElectrum:948681048932364401>",
        "name": "Electrum",
        "gSheet": {
            "v14": "D66",
            "v2": "D9",
        }
    },
    "sp": {
        "icon": "<:DDBSilver:948681049288867930>",
        "name": "Silver",
        "gSheet": {
            "v14": "D63",
            "v2": "D6",
        }
    },
    "cp": {
        "icon": "<:DDBCopper:948681049217597480>",
        "name": "Copper",
        "gSheet": {
            "v14": "D60",
            "v2": "D3",
        }
    }
}


class Coinpurse(HasIntegrationMixin):
    def __init__(self, pp=0, gp=0, ep=0, sp=0, cp=0):
        super().__init__()
        self.pp = pp
        self.gp = gp
        self.ep = ep
        self.sp = sp
        self.cp = cp

    def __str__(self):
        return "\n".join(self.str_styled(coin_type) for coin_type in CoinTypes)

    def str_styled(self, coin_type):
        if coin_type not in ("compact", "pp", "gp", "ep", "sp", "cp"):
            raise ValueError("coin_type must be in ('compact', 'pp', 'gp', 'ep', 'sp', 'cp')")

        if coin_type == 'compact':
            coin_value = self.total
            coin_type = 'gp'
        else:
            coin_value = getattr(self, coin_type)
        return f"{CoinTypes[coin_type]['icon']} {coin_type}: {coin_value:,}"

    @property
    def total(self):
        total = self.gp
        total += self.pp * 10
        total += self.ep * 0.5
        total += self.sp * 0.1
        total += self.cp * 0.01
        return total

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return {
            "pp": self.pp, "gp": self.gp, "ep": self.ep, "sp": self.sp, "cp": self.cp
        }

    def update_currency(self, pp: int = 0, gp: int = 0, ep: int = 0, sp: int = 0, cp: int = 0):
        if not all((
            isinstance(pp, int),
            isinstance(gp, int),
            isinstance(ep, int),
            isinstance(sp, int),
            isinstance(cp, int)
        )):
            raise TypeError("All values must be numeric.")

        if not all((
            True if (self.pp + pp ) >= 0 else False,
            True if (self.gp + gp ) >= 0 else False,
            True if (self.ep + ep ) >= 0 else False,
            True if (self.sp + sp ) >= 0 else False,
            True if (self.cp + cp ) >= 0 else False
        )):
            raise InvalidArgument("You cannot put a currency into negative numbers.")

        self.pp += pp
        self.gp += gp
        self.ep += ep
        self.sp += sp
        self.cp += cp

        if self._live_integration:
            self._live_integration.sync_coins()

    def set_currency(self, pp: int = 0, gp: int = 0, ep: int = 0, sp: int = 0, cp: int = 0):
        if not all((
            isinstance(pp, int),
            isinstance(gp, int),
            isinstance(ep, int),
            isinstance(sp, int),
            isinstance(cp, int)
        )):
            raise TypeError("All values must be numeric.")

        if not all((
            True if pp >= 0 else False,
            True if gp >= 0 else False,
            True if ep >= 0 else False,
            True if sp >= 0 else False,
            True if cp >= 0 else False
        )):
            raise InvalidArgument("You cannot put a currency into negative numbers.")

        self.pp = pp
        self.gp = gp
        self.ep = ep
        self.sp = sp
        self.cp = cp

        if self._live_integration:
            self._live_integration.sync_coins()
