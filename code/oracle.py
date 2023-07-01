# docker run --rm -v "%CD%":/cd -w /cd pyratzlabs/pymich compile oracle.py michelson
# docker run --rm -v "%CD%":/cd -w /cd pyratzlabs/pymich compile oracle.py michelson n> oracle.tz
from dataclasses import dataclass
from pymich.michelson_types import *


@dataclass
class OHLC(Record):
    open: Nat
    close: Nat
    low: Nat
    high: Nat


@dataclass
class PushData(Record):
    key: String
    ohlc: OHLC


@dataclass(kw_only=True)
class Oracle(BaseContract):
    admin: Address
    ohlc: BigMap[String, OHLC]
    name: String

    def push_data(self, param: PushData) -> None:
        if Tezos.sender != self.admin:
            raise Exception("Unauthorized")

        self.ohlc[param.key] = param.ohlc

    def update_admin(self, new_admin: Address) -> None:
        if Tezos.sender != self.admin:
            raise Exception("Unauthorized")

        self.admin = new_admin
