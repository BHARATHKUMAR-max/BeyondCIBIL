import pytest

from app.services.banking.contracts import BankProviderError
from app.services.banking.mock_connector import MockBankConnector


def test_mock_connector_completes_the_expected_flow() -> None:
    connector = MockBankConnector()
    assert {bank.code for bank in connector.list_supported_banks()} == {"axis", "hdfc", "icici", "sbi"}

    challenge = connector.authenticate("hdfc", "demo-user", "demo-password")
    connector.verify_otp(challenge.provider_reference, "123456")
    account = connector.connect_account(challenge.provider_reference)

    assert account.currency == "INR"
    assert account.account_mask == "1234"


def test_mock_connector_rejects_an_invalid_otp() -> None:
    connector = MockBankConnector()
    challenge = connector.authenticate("sbi", "demo-user", "demo-password")

    with pytest.raises(BankProviderError):
        connector.verify_otp(challenge.provider_reference, "000000")
