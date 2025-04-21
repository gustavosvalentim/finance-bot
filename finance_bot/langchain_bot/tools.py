from datetime import datetime
from typing import Type
from django.utils import timezone
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from finance_bot.finance.models import Category, Transaction


class CreateCategoryToolInput(BaseModel):
    """Input schema for CreateCategoryTool."""
    user: str = Field(description="User who is creating the category")
    category_name: str = Field(description="Name of the category to create")


class CreateCategoryTool(BaseTool):
    name: str = "CreateCategoryTool"
    description: str = "Creates a new category in the database."
    args_schema: Type[BaseModel] = CreateCategoryToolInput

    def _run(self, user: str, category_name: str) -> str:
        """Create a new category."""
        
        category = Category.objects.get_or_create(user=user, name=category_name)

        return f"Category '{category_name}' created successfully."


class CreateTransactionToolInput(BaseModel):
    """
    Input model for the CreateTransactionTool.
    """
    user: str = Field(description="User that owns the transaction.")
    category: int = Field(description="ID of the category")
    amount: float = Field(description="Amount of the transaction.")
    date: datetime = Field(description="Date of the transaction in YYYY-MM-DD format.")
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
        date: datetime,
        description: str
    ) -> str:
        """Create a new transaction."""

        transaction = Transaction.objects.create(
            user=user,
            category_id=category,
            amount=amount,
            date=timezone.make_aware(date),
            description=description
        )

        return f"Transaction created with ID {transaction.id}"


class SearchCategoryToolInput(BaseModel):
    """Input schema for SearchCategoryTool."""
    category_name: str = Field(description="Name of the category to search")
    user: str = Field(description="User who owns the category")


class SearchCategoryTool(BaseTool):
    name: str = "SearchCategoryTool"
    description: str = "Searches for categories in the database."
    args_schema: Type[BaseModel] = SearchCategoryToolInput

    def _run(self, category_name: str, user: str) -> str:
        """Search for a category by name."""
        categories = Category.objects.filter(name__icontains=category_name, user=user)
        if categories.exists():
            category = categories.first()
            return f"Category ID: {category.id}\nCategory Name: {category.name}\n"
        else:
            return f"No categories found with the name '{category_name}'."


class SearchUserCategoriesToolInput(BaseModel):
    """Search for all users categories."""
    user: str = Field(description="Name of the user that owns the categories.")


class SearchUserCategoriesTool(BaseTool):
    """Searches the categories from a user."""
    name: str = "SearchUserCategoriesTool"
    description: str = "Searches the categories from a user."
    args_schema: Type[BaseModel] = SearchUserCategoriesToolInput

    def _run(self, user: str) -> str:
        categories = Category.objects.filter(user=user)
        output = ""

        for category in categories:
            output += f"Category ID: {category.id}\n"
            output += f"Category Name: {category.name}\n"
            output += f"Category Is Income: {category.is_income}\n"
            output += f"Category Amount Limit: {category.limit}\n"

        return output


class SearchTransactionsToolInput(BaseModel):
    """Search for all users transactions."""
    user: str = Field(description="Name of the user that owns the transactions.")
    category: str = Field(default=None, description="Name of the category to search for transactions.")
    start_date: datetime = Field(description="Start date to search for transactions.")
    end_date: datetime = Field(description="End date to search for transactions.")


class SearchTransactionsTool(BaseTool):
    """Searches the transactions from a user."""
    name: str = "SearchTransactionsTool"
    description: str = "Searches the transactions from a user."
    args_schema: Type[BaseModel] = SearchTransactionsToolInput

    def _run(self, user: str, category: str, start_date: datetime, end_date: datetime) -> str:
        """Search for transactions by user and date range."""

        filters = {'user': user}

        if start_date:
            filters['date__gte'] = timezone.make_aware(start_date)
        
        if end_date:
            filters['date__lte'] = timezone.make_aware(end_date)

        if category:
            filters['category__name__icontains'] = category

        transactions = Transaction.objects.filter(**filters)
        output = ""

        for transaction in transactions:
            output += f"Transaction ID: {transaction.id}\n"
            output += f"Transaction Amount: {transaction.amount}\n"
            output += f"Transaction Date: {transaction.date}\n"
            output += f"Transaction Description: {transaction.description}\n"

        return output
