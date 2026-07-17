"""Mock bank service for generating realistic banking data."""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

POPULAR_BANKS = [
    "SBI",
    "HDFC",
    "ICICI",
    "Axis",
    "Kotak",
    "Canara",
    "Punjab National Bank",
    "Union Bank",
    "Indian Bank",
    "Bank of Baroda"
]

TRANSACTION_CATEGORIES = [
    "SALARY",
    "UPI",
    "CARD_TRANSACTION",
    "ATM_WITHDRAWAL",
    "BILL_PAYMENT",
    "SHOPPING",
    "FUEL",
    "FOOD",
    "EMI",
    "SUBSCRIPTION",
    "TRANSFER",
    "CASH_DEPOSIT"
]


class MockBankService:
    """Service for generating mock banking data for testing."""
    
    def __init__(self):
        self.customers = {}  # In-memory storage for mock customers
        self._initialize_pre_populated_data()
    
    def _initialize_pre_populated_data(self):
        """Initialize with pre-populated mock customer data."""
        
        # Customer 1: High income, low expenses, excellent credit
        self.customers['9876543210'] = self._generate_customer_profile(
            phone_number='9876543210',
            bank_name='HDFC',
            monthly_income=150000,
            expense_ratio=0.4,
            account_balance=500000
        )
        
        # Customer 2: Medium income, medium expenses, good credit
        self.customers['9876543211'] = self._generate_customer_profile(
            phone_number='9876543211',
            bank_name='ICICI',
            monthly_income=75000,
            expense_ratio=0.6,
            account_balance=200000
        )
        
        # Customer 3: Low income, high expenses, poor credit
        self.customers['9876543212'] = self._generate_customer_profile(
            phone_number='9876543212',
            bank_name='SBI',
            monthly_income=35000,
            expense_ratio=0.85,
            account_balance=25000
        )
        
        # Customer 4: High income, very high expenses, medium credit
        self.customers['9876543213'] = self._generate_customer_profile(
            phone_number='9876543213',
            bank_name='Axis',
            monthly_income=120000,
            expense_ratio=0.75,
            account_balance=100000
        )
        
        # Customer 5: Medium income, low expenses, excellent credit
        self.customers['9876543214'] = self._generate_customer_profile(
            phone_number='9876543214',
            bank_name='Kotak',
            monthly_income=60000,
            expense_ratio=0.35,
            account_balance=350000
        )
        
        # Customer 6: Low income, very low expenses, good credit
        self.customers['9876543215'] = self._generate_customer_profile(
            phone_number='9876543215',
            bank_name='Canara',
            monthly_income=40000,
            expense_ratio=0.45,
            account_balance=150000
        )
        
        # Customer 7: Very high income, medium expenses, excellent credit
        self.customers['9876543216'] = self._generate_customer_profile(
            phone_number='9876543216',
            bank_name='Punjab National Bank',
            monthly_income=200000,
            expense_ratio=0.5,
            account_balance=800000
        )
        
        # Customer 8: Medium income, high expenses, poor credit
        self.customers['9876543217'] = self._generate_customer_profile(
            phone_number='9876543217',
            bank_name='Union Bank',
            monthly_income=55000,
            expense_ratio=0.8,
            account_balance=40000
        )
        
        # Customer 9: Low income, medium expenses, medium credit
        self.customers['9876543218'] = self._generate_customer_profile(
            phone_number='9876543218',
            bank_name='Indian Bank',
            monthly_income=45000,
            expense_ratio=0.65,
            account_balance=80000
        )
        
        # Customer 10: High income, low expenses, excellent credit with high savings
        self.customers['9876543219'] = self._generate_customer_profile(
            phone_number='9876543219',
            bank_name='Bank of Baroda',
            monthly_income=180000,
            expense_ratio=0.3,
            account_balance=1200000
        )
    
    def _generate_customer_profile(
        self,
        phone_number: str,
        bank_name: str,
        monthly_income: float,
        expense_ratio: float,
        account_balance: float
    ) -> Dict[str, Any]:
        """Generate a customer profile with specific parameters."""
        
        total_expense = monthly_income * expense_ratio
        savings = monthly_income - total_expense
        
        # Generate transaction history
        transactions = self._generate_transaction_history(
            monthly_income,
            total_expense,
            12
        )
        
        # Generate EMIs
        emis = self._generate_emis(monthly_income)
        
        # Generate recurring payments
        recurring_payments = self._generate_recurring_payments()
        
        # Calculate derived metrics
        transaction_frequency = len(transactions) / 365
        savings_ratio = savings / monthly_income if monthly_income > 0 else 0
        
        # Calculate income consistency
        salary_credits = [t for t in transactions if t['category'] == 'SALARY']
        income_consistency = self._calculate_income_consistency(salary_credits)
        
        return {
            "customer_id": f"CUST_{phone_number[-6:]}",
            "phone_number": phone_number,
            "bank_name": bank_name,
            "account_number": f"{random.randint(1000000000, 9999999999)}",
            "account_type": random.choice(["Savings", "Current"]),
            "account_balance": account_balance,
            "monthly_income": monthly_income,
            "total_expense": total_expense,
            "savings": savings,
            "savings_ratio": round(savings_ratio, 4),
            "transaction_frequency": round(transaction_frequency, 4),
            "income_consistency": round(income_consistency, 4),
            "transactions": transactions,
            "emis": emis,
            "recurring_payments": recurring_payments,
            "account_opened_date": (datetime.now() - timedelta(days=random.randint(365, 1825))).isoformat(),
            "last_transaction_date": datetime.now().isoformat()
        }
    
    def generate_customer_data(
        self, 
        phone_number: str, 
        bank_name: str
    ) -> Dict[str, Any]:
        """Generate realistic customer banking data."""
        
        # Generate base income (between 25000 and 150000)
        monthly_income = random.uniform(25000, 150000)
        
        # Generate expense ratio (between 0.4 and 0.8 of income)
        expense_ratio = random.uniform(0.4, 0.8)
        total_expense = monthly_income * expense_ratio
        
        # Generate savings
        savings = monthly_income - total_expense
        
        # Generate transaction history for last 12 months
        transactions = self._generate_transaction_history(
            monthly_income, 
            total_expense, 
            12
        )
        
        # Generate EMIs
        emis = self._generate_emis(monthly_income)
        
        # Generate recurring payments
        recurring_payments = self._generate_recurring_payments()
        
        # Calculate derived metrics
        transaction_frequency = len(transactions) / 365  # per day
        savings_ratio = savings / monthly_income if monthly_income > 0 else 0
        
        # Calculate income consistency (based on salary credits)
        salary_credits = [t for t in transactions if t['category'] == 'SALARY']
        income_consistency = self._calculate_income_consistency(salary_credits)
        
        customer_data = {
            "customer_id": f"CUST_{phone_number[-6:]}",
            "phone_number": phone_number,
            "bank_name": bank_name,
            "account_number": f"{random.randint(1000000000, 9999999999)}",
            "account_type": random.choice(["Savings", "Current"]),
            "account_balance": round(random.uniform(50000, 500000), 2),
            "monthly_income": round(monthly_income, 2),
            "total_expense": round(total_expense, 2),
            "savings": round(savings, 2),
            "savings_ratio": round(savings_ratio, 4),
            "transaction_frequency": round(transaction_frequency, 4),
            "income_consistency": round(income_consistency, 4),
            "transactions": transactions,
            "emis": emis,
            "recurring_payments": recurring_payments,
            "account_opened_date": (datetime.now() - timedelta(days=random.randint(365, 1825))).isoformat(),
            "last_transaction_date": datetime.now().isoformat()
        }
        
        # Store in memory
        self.customers[phone_number] = customer_data
        
        logger.info(f"Generated mock data for customer {customer_data['customer_id']}")
        return customer_data
    
    def get_customer_data(
        self, 
        phone_number: str, 
        bank_name: str
    ) -> Dict[str, Any]:
        """Get customer data, generate if not exists."""
        
        if phone_number in self.customers:
            logger.info(f"Retrieved existing customer data for {phone_number}")
            return self.customers[phone_number]
        
        logger.info(f"Generating new mock customer data for {phone_number}")
        return self.generate_customer_data(phone_number, bank_name)
    
    def _generate_transaction_history(
        self, 
        monthly_income: float, 
        total_expense: float, 
        months: int
    ) -> List[Dict[str, Any]]:
        """Generate realistic transaction history."""
        
        transactions = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        # Generate salary credits (monthly)
        current_date = start_date
        while current_date <= end_date:
            # Salary credit (1st of each month)
            salary_day = current_date.replace(day=1)
            if salary_day <= end_date:
                transactions.append({
                    "date": salary_day.isoformat(),
                    "amount": round(monthly_income, 2),
                    "category": "SALARY",
                    "description": "Salary Credit",
                    "type": "CREDIT"
                })
            
            current_date += timedelta(days=30)
        
        # Generate daily transactions
        current_date = start_date
        daily_expense = total_expense / 30
        
        while current_date <= end_date:
            # Skip weekends for some transactions
            if current_date.weekday() < 5:
                # Generate 1-5 transactions per day
                num_transactions = random.randint(1, 5)
                
                for _ in range(num_transactions):
                    category = random.choice(TRANSACTION_CATEGORIES)
                    
                    if category == "SALARY":
                        continue  # Already handled above
                    
                    amount = self._get_transaction_amount(category, daily_expense)
                    
                    transactions.append({
                        "date": current_date.isoformat(),
                        "amount": round(amount, 2),
                        "category": category,
                        "description": self._get_transaction_description(category),
                        "type": "DEBIT" if amount > 0 else "CREDIT"
                    })
            
            current_date += timedelta(days=1)
        
        # Sort by date
        transactions.sort(key=lambda x: x['date'])
        
        return transactions
    
    def _get_transaction_amount(
        self, 
        category: str, 
        daily_expense: float
    ) -> float:
        """Get realistic transaction amount based on category."""
        
        multipliers = {
            "UPI": random.uniform(0.1, 0.3),
            "CARD_TRANSACTION": random.uniform(0.2, 0.5),
            "ATM_WITHDRAWAL": random.uniform(0.1, 0.4),
            "BILL_PAYMENT": random.uniform(0.3, 0.8),
            "SHOPPING": random.uniform(0.2, 0.6),
            "FUEL": random.uniform(0.05, 0.15),
            "FOOD": random.uniform(0.1, 0.3),
            "EMI": random.uniform(0.5, 1.5),
            "SUBSCRIPTION": random.uniform(0.05, 0.2),
            "TRANSFER": random.uniform(0.1, 0.5),
            "CASH_DEPOSIT": random.uniform(0.1, 0.5)
        }
        
        return daily_expense * multipliers.get(category, 0.2)
    
    def _get_transaction_description(self, category: str) -> str:
        """Get realistic transaction description."""
        
        descriptions = {
            "UPI": "UPI Transfer to Merchant",
            "CARD_TRANSACTION": "Card Payment",
            "ATM_WITHDRAWAL": "ATM Withdrawal",
            "BILL_PAYMENT": "Bill Payment",
            "SHOPPING": "Shopping",
            "FUEL": "Fuel Station",
            "FOOD": "Food & Dining",
            "EMI": "Loan EMI",
            "SUBSCRIPTION": "Subscription Renewal",
            "TRANSFER": "Fund Transfer",
            "CASH_DEPOSIT": "Cash Deposit"
        }
        
        return descriptions.get(category, "Transaction")
    
    def _generate_emis(self, monthly_income: float) -> List[Dict[str, Any]]:
        """Generate EMI information."""
        
        num_emis = random.randint(0, 3)
        emis = []
        
        for i in range(num_emis):
            emi_amount = monthly_income * random.uniform(0.15, 0.35)
            emis.append({
                "loan_type": random.choice(["Home Loan", "Car Loan", "Personal Loan"]),
                "amount": round(emi_amount, 2),
                "remaining_tenure": random.randint(12, 180),
                "interest_rate": round(random.uniform(8.5, 12.5), 2)
            })
        
        return emis
    
    def _generate_recurring_payments(self) -> List[Dict[str, Any]]:
        """Generate recurring payment information."""
        
        payments = [
            {
                "name": "Netflix",
                "amount": round(random.uniform(149, 649), 2),
                "frequency": "Monthly"
            },
            {
                "name": "Electricity Bill",
                "amount": round(random.uniform(1000, 3000), 2),
                "frequency": "Monthly"
            },
            {
                "name": "Mobile Recharge",
                "amount": round(random.uniform(299, 999), 2),
                "frequency": "Monthly"
            }
        ]
        
        return payments
    
    def _calculate_income_consistency(
        self, 
        salary_credits: List[Dict[str, Any]]
    ) -> float:
        """Calculate income consistency score."""
        
        if len(salary_credits) < 2:
            return 0.5
        
        amounts = [t['amount'] for t in salary_credits]
        avg_amount = sum(amounts) / len(amounts)
        
        # Calculate variance
        variance = sum((x - avg_amount) ** 2 for x in amounts) / len(amounts)
        std_dev = variance ** 0.5
        
        # Consistency score (inverse of coefficient of variation)
        if avg_amount > 0:
            cv = std_dev / avg_amount
            consistency = max(0, min(1, 1 - cv))
        else:
            consistency = 0.5
        
        return round(consistency, 4)
    
    def get_transaction_summary(
        self, 
        customer_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get transaction summary for dashboard display."""
        
        transactions = customer_data.get('transactions', [])
        
        # Category-wise spending
        category_spending = {}
        for t in transactions:
            if t['type'] == 'DEBIT':
                category = t['category']
                category_spending[category] = category_spending.get(category, 0) + t['amount']
        
        # Monthly averages
        total_debit = sum(t['amount'] for t in transactions if t['type'] == 'DEBIT')
        total_credit = sum(t['amount'] for t in transactions if t['type'] == 'CREDIT')
        
        months = 12  # Assuming 12 months of data
        
        return {
            "total_transactions": len(transactions),
            "total_debit": round(total_debit, 2),
            "total_credit": round(total_credit, 2),
            "average_monthly_debit": round(total_debit / months, 2),
            "average_monthly_credit": round(total_credit / months, 2),
            "category_spending": {
                k: round(v, 2) for k, v in category_spending.items()
            },
            "spending_categories": list(category_spending.keys()),
            "top_spending_category": max(category_spending.items(), key=lambda x: x[1])[0] if category_spending else None
        }


# Singleton instance
mock_bank_service = MockBankService()
