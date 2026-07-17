from dataclasses import dataclass
from typing import Protocol


class BankProviderError(Exception):
    """Raised when a banking provider rejects or cannot complete an operation."""


@dataclass(frozen=True)
class SupportedBank:
    code: str
    name: str


@dataclass(frozen=True)
class AuthenticationChallenge:
    provider_reference: str


@dataclass(frozen=True)
class ConnectedAccount:
    external_account_id: str
    institution_name: str
    account_name: str
    account_mask: str
    currency: str


class BankConnector(Protocol):
    """Stable port implemented by mock and future Account Aggregator adapters."""

    def list_supported_banks(self) -> list[SupportedBank]: ...

    def authenticate(self, bank_code: str, customer_id: str, password: str) -> AuthenticationChallenge: ...

    def verify_otp(self, provider_reference: str, otp: str) -> None: ...

    def connect_account(self, provider_reference: str) -> ConnectedAccount: ...
