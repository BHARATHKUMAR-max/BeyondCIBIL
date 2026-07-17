from __future__ import annotations

import hashlib
import re
from dataclasses import replace
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import Iterable

from app.schemas.preprocessing import CleanTransaction, RawTransaction, RejectedTransaction


class CleaningService:
    """Normalizes provider input and removes invalid or duplicate records."""

    _date_formats = ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y")
    _merchant_noise = re.compile(r"\b(?:upi|pos|card|payment|txn|transaction)\b", re.IGNORECASE)
    _non_word = re.compile(r"[^A-Za-z0-9& ]+")
    _whitespace = re.compile(r"\s+")

    def clean(self, records: Iterable[RawTransaction]) -> tuple[list[CleanTransaction], list[RejectedTransaction]]:
        cleaned: list[CleanTransaction] = []
        rejected: list[RejectedTransaction] = []
        seen: set[str] = set()
        for index, record in enumerate(records):
            try:
                transaction = self._clean_record(record)
                fingerprint = self._fingerprint(transaction)
                if fingerprint in seen:
                    continue
                seen.add(fingerprint)
                cleaned.append(transaction)
            except ValueError as exc:
                rejected.append(RejectedTransaction(index=index, reason=str(exc)))
        return cleaned, rejected

    def _clean_record(self, record: RawTransaction) -> CleanTransaction:
        amount = self._normalise_amount(record.amount)
        occurred_at = self.normalise_date(record.occurred_at)
        transaction_type = (record.transaction_type or "").strip().lower()
        if transaction_type not in {"credit", "debit"}:
            raise ValueError("transaction_type must be credit or debit")
        currency = (record.currency or "INR").strip().upper()
        if not re.fullmatch(r"[A-Z]{3}", currency):
            raise ValueError("currency must be a three-letter ISO code")
        merchant_name = self.normalise_merchant(record.merchant_name)
        description = self._normalise_text(record.description)
        external_id = (record.external_transaction_id or "").strip()
        if not external_id:
            external_id = self._generated_id(amount, transaction_type, occurred_at, merchant_name)
        category = self._normalise_optional_text(record.category)
        return CleanTransaction(
            external_transaction_id=external_id,
            amount=amount,
            currency=currency,
            transaction_type=transaction_type,
            occurred_at=occurred_at,
            merchant_name=merchant_name,
            description=description,
            category=category,
        )

    @staticmethod
    def _normalise_amount(value: Decimal | float | int | str | None) -> Decimal:
        if value is None or str(value).strip() == "":
            raise ValueError("amount is required")
        try:
            amount = Decimal(str(value)).quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("amount is invalid") from exc
        if amount < 0:
            raise ValueError("amount must be non-negative")
        return amount

    def normalise_date(self, value: datetime | str | None) -> datetime:
        if value is None:
            raise ValueError("occurred_at is required")
        if isinstance(value, datetime):
            parsed = value
        else:
            candidate = value.strip()
            if not candidate:
                raise ValueError("occurred_at is required")
            try:
                parsed = datetime.fromisoformat(candidate.replace("Z", "+00:00"))
            except ValueError:
                parsed = self._parse_known_date(candidate)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)

    def _parse_known_date(self, value: str) -> datetime:
        for date_format in self._date_formats:
            try:
                return datetime.strptime(value, date_format).replace(tzinfo=UTC)
            except ValueError:
                continue
        raise ValueError("occurred_at has an unsupported date format")

    def normalise_merchant(self, value: str | None) -> str:
        normalized = self._normalise_text(value)
        if not normalized:
            return "Unknown Merchant"
        normalized = self._merchant_noise.sub(" ", normalized)
        normalized = self._non_word.sub(" ", normalized)
        normalized = self._whitespace.sub(" ", normalized).strip()
        return normalized.title() if normalized else "Unknown Merchant"

    def _fingerprint(self, transaction: CleanTransaction) -> str:
        # A provider-supplied external ID is authoritative; generated IDs are deterministic.
        return transaction.external_transaction_id

    @staticmethod
    def _generated_id(amount: Decimal, transaction_type: str, occurred_at: datetime, merchant: str) -> str:
        value = f"{amount}|{transaction_type}|{occurred_at.isoformat()}|{merchant.lower()}"
        return f"generated-{hashlib.sha256(value.encode()).hexdigest()[:24]}"

    @staticmethod
    def _normalise_text(value: str | None) -> str:
        return " ".join((value or "").strip().split())

    def _normalise_optional_text(self, value: str | None) -> str | None:
        normalized = self._normalise_text(value).lower()
        return normalized or None
