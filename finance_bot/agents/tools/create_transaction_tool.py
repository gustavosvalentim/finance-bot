from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from finance_bot.finance.models import Transaction


class CreateTransactionToolInput(BaseModel):
    """
    Input model for the CreateTransactionTool.
    """
    user: str = Field(description="User that owns the transaction.")
    category: int = Field(description="ID of the category")
    amount: float = Field(description="Amount of the transaction.")
    date: str = Field(description="Date of the transaction in YYYY-MM-DD format.")
    description: str = Field(description="The transaction description")


class CreateTransactionTool(BaseTool):
    """
    Tool to create a transaction.
    """
    name: str = "CreateTransactionTool"
    description: str = "Creates a transaction."
    args_schema: type[BaseModel] = CreateTransactionToolInput

    def _run(
        self,
        user: str,
        category: int,
        amount: float,
        date: str,
        description: str
    ) -> str:
        transaction = Transaction.objects.create(
            user=user,
            category_id=category,
            amount=amount,
            date=date,
            description=description
        )
        return f"Transaction created with ID {transaction.id}"
