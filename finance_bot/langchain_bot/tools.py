from datetime import datetime
from typing import Any, Type
from django.utils import timezone
from pydantic import BaseModel, Field, field_validator
from langchain.tools import BaseTool
from finance_bot.finance.models import Category, Transaction
from finance_bot.logging import get_logger

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

        logger = get_logger('CreateCategoryTool')

        normalized = category_name.strip().upper()
        logger.debug(f"Creating category '{normalized}' for user '{user}'")
        
        query = Category.objects.filter(normalized_name__icontains=normalized)
        category = None
        if query.exists():
            category = query.first()
        else:
            category = Category.objects.create(user=user, name=category_name)

        logger.debug(f"Category created: id={category.id}, name={category.name}")

        return (f"Category ID: {category.id}"
                f"Category Name: {category.name}")


class CreateTransactionToolInput(BaseModel):
    """
    Input model for the CreateTransactionTool.
    """
    user: str = Field(description="User that owns the transaction.")
    category: int = Field(description="ID of the category")
    amount: float = Field(description="Amount of the transaction.")
    date: datetime | None = Field(default=None, description="Date of the transaction in YYYY-MM-DD format. If none, then use today as date")
    description: str | None = Field(default=None, description="Optional description")

    @field_validator("amount")
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive.")
        return v


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
        date: datetime | None = None,
        description: str | None = None,
    ) -> str:
        """Create a new transaction."""

        logger = get_logger('CreateTransactionTool')

        if date is None:
            date = timezone.now()

        logger.debug(f"Creating transaction"
                     f"User: {user}\n"
                     f"Category ID: {category}\n "
                     f"Amount: {amount}\n "
                     f"Date: {date}\n "
                     f"Description: {description}\n")

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

        logger = get_logger('SearchCategoryTool')

        logger.debug(f"Searching for category '{category_name}' for user '{user}'")

        categories = Category.objects.filter(normalized_name__icontains=category_name.upper(), user=user)
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
    category: str | None = Field(default=None, description="Name of the category to search for transactions (optional).")
    start_date: datetime | None = Field(default=None, description="Start date to search for transactions (optional).")
    end_date: datetime | None = Field(default=None, description="End date to search for transactions (optional).")
    limit: int | None = Field(default=None, description="Max number of transactions to return, newest first (optional)",)


class SearchTransactionsTool(BaseTool):
    """Searches the transactions from a user."""
    name: str = "SearchTransactionsTool"
    description: str = "Searches the transactions from a user."
    args_schema: Type[BaseModel] = SearchTransactionsToolInput

    def _run(self, user: str, category: str | None = None, start_date: datetime | None = None, end_date: datetime | None = None, limit: int | None = None) -> str:
        """Search for transactions by user and date range."""

        logger = get_logger('SearchTransactionsTool')

        if not user:
            logger.error("User can't be empty or null")
            return "No transactions were found."

        filters: dict[str, Any] = {"user": user}
        if start_date:
            filters['date__gte'] = timezone.make_aware(start_date)
        
        if end_date:
            filters['date__lte'] = timezone.make_aware(end_date)

        if category:
            filters['category__normalized_name__icontains'] = category.upper()

        logger.debug(f"Searching transactions for user '{user}' with filters: {filters}")

        qs = Transaction.objects.filter(**filters).order_by("-date")
        if limit:
            qs = qs[:limit]

        if not qs:
            return "Nenhuma transação encontrada."

        transactions = Transaction.objects.filter(**filters) 

        return "\n---\n".join([f"Transaction ID: {transaction.id}\n"
                              f"Transaction Amount: {transaction.amount}\n"
                              f"Category: {transaction.category.name}\n"
                              f"Transaction Date: {transaction.date}\n"
                              f"Transaction Description: {transaction.description}\n"
                              for transaction in transactions])


class UpdateTransactionToolInput(BaseModel):
    """Parameters for update transaction."""
    user: str = Field(description="Name of the user that owns the categories.")
    transaction: int = Field(description="Name of the transaction to update.")
    amount: int = Field(description="New amount of the transaction.")


class UpdateTransactionTool(BaseTool):
    """Updates a transaction."""
    name: str = "UpdateTransactionTool"
    description: str = "Updates a transaction."
    args_schema: Type[BaseModel] = UpdateTransactionToolInput

    def _run(self, user: str, transaction: int, amount: int) -> str:
        transaction = Transaction.objects.filter(id=transaction, user=user).first()

        if transaction is None:
            return "Transaction was not found."

        transaction.amount = amount
        transaction.save()

        return "Transaction updated successfully."


class DeleteTransactionToolInput(BaseModel):
    """Parameters to delete a transaction. """
    user_id: str = Field(description="ID of the user deleting the transaction.")
    transaction_id: str = Field(description="ID of the transaction to delete.")


class DeleteTransactionTool(BaseTool):
    """Deletes a transaction. """
    name: str = "DeleteTransactionTool"
    description: str = "Deletes a transaction"
    args_schema: Type[BaseModel] = DeleteTransactionToolInput

    def _run(self, user_id: str, transaction_id: str) -> str:
        transaction = Transaction.objects.filter(user=user_id, id=transaction_id).first()

        if transaction is None:
            return "Transaction was not found."
        
        transaction.delete()

        return f"Transaction {transaction.id} was deleted successfuly."
    

class DeleteCategoryToolInput(BaseModel):
    """Parameters to delete a category. """
    user_id: str = Field(description="ID of the user deleting the category.")
    category_name: str = Field(description="Name of the category to delete.")


class DeleteCategoryTool(BaseTool):
    """Deletes a category. """
    name: str = "DeleteCategoryTool"
    description: str = "Deletes a category. "
    args_schema: Type[BaseModel] = DeleteCategoryToolInput

    def _run(self, user_id: str, category_name: str) -> str:
        category = Category.objects.filter(normalized_name=category_name.upper(), user=user_id).first()

        if category is None:
            return "Category was not found."
        
        category.delete()

        return f"Category {category.name} was deleted successfuly."
    

class UpdateCategoryToolInput(BaseModel):
    """Parameters for updating a category. """
    user_id: str = Field(description="ID of the user updating the category.")
    category_name: str = Field(description="Name of the category to delete.")
    new_name: str = Field(description="New category name.")


class UpdateCategoryTool(BaseTool):
    """Updates a category. """
    name: str = "UpdateCategoryTool"
    description: str = "Updates a category."
    args_schema: Type[BaseModel] = UpdateCategoryToolInput

    def _run(self, user_id: str, category_name: str, new_name: str) -> str:
        category = Category.objects.filter(normalized_name=category_name.upper(), user=user_id).first()

        if category is None:
            return "Category was not found."
        
        category.name = new_name
        category.normalized_name = new_name.upper()
        category.save()

        return f"Category {category.name} was updated successfuly."
