from django.core.management import BaseCommand
from langchain_core.messages import SystemMessage, HumanMessage
from finance_bot.langchain_bot.agent import agent_executor


class Command(BaseCommand):
    help = "Runs the Langchain Chat Agent"

    def handle(self, *args, **options):
        config = {
            'configurable': {
                'thread_id': '1234567890',
            }
        }
        messages = [SystemMessage(content="""
            The user identification is 51994709234.

            If the user is trying to create a transaction, the agent should follow the steps below:
                1. Search for the category of the transaction using the SearchCategoryTool.
                2. If the category was not found, the agent should create a new category using the CreateCategoryTool.
                3. Create the transaction using the CreateTransactionTool, using the Category ID as category instead of the name.
                4. Output a message saying that the transaction was created successfully, including the transaction description and ID.

            If the user is trying to create a category, the agent should follow the steps below:
                1. Search for the category in the database using the SearchCategoryTool.
                2. If the category was not found, create the category using the CreateCategoryTool.

            If the user wants to list all his categories, the agent should follow the steps below:
                1. Search for the categories in the database using the SearchUserCategoriesTool.
                2. Output a list with all the categories found.
                3. If no categories were found, output a message saying that no categories were found.

            Observations:
                - If the user wants to list his categories, don't create anything, only list the categories.
                - After you use the SearchUserCategoriesTool, output the result to the user and stop the task.
                - Try to match the category name even if the user misspells it.""")]

        while True:
            try:
                user_input = input("You: ")
                output = agent_executor.invoke({'messages': [*messages, HumanMessage(user_input)]}, config=config)
                
                for message in output['messages']:
                    print(message.content)
                    print("===" * 20, end="\n\n")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
