from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from finance_bot.finance.models import Category


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
