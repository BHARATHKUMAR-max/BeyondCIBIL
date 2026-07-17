import hashlib
import uuid

from app.services.banking.contracts import (
    AuthenticationChallenge,
    BankProviderError,
    ConnectedAccount,
    SupportedBank,
)


class MockBankConnector:
    """Deterministic mock provider; never contacts a real banking system."""

    _banks = {
        "hdfc": "HDFC Bank",
        "icici": "ICICI Bank",
        "sbi": "State Bank of India",
        "axis": "Axis Bank",
    }
    mock_otp = "123456"

    def list_supported_banks(self) -> list[SupportedBank]:
        return [SupportedBank(code=code, name=name) for code, name in self._banks.items()]

    def authenticate(self, bank_code: str, customer_id: str, password: str) -> AuthenticationChallenge:
        if bank_code not in self._banks:
            raise BankProviderError("Unsupported bank")
        if not customer_id.strip() or len(password) < 1:
            raise BankProviderError("Invalid bank credentials")
        reference = hashlib.sha256(f"{bank_code}:{customer_id}:{uuid.uuid4()}".encode()).hexdigest()
        return AuthenticationChallenge(provider_reference=reference)

    def verify_otp(self, provider_reference: str, otp: str) -> None:
        if not provider_reference or otp != self.mock_otp:
            raise BankProviderError("Invalid OTP")

    def connect_account(self, provider_reference: str) -> ConnectedAccount:
        if not provider_reference:
            raise BankProviderError("Invalid authentication state")
        bank_code = next((code for code in self._banks if code in provider_reference), None)
        # The provider reference is opaque; account details remain deterministic and non-sensitive.
        return ConnectedAccount(
            external_account_id=f"mock-{provider_reference[:16]}",
            institution_name="Mock Bank",
            account_name="Mock Savings Account",
            account_mask="1234",
            currency="INR",
        )
