import os

from django.core.management import BaseCommand

from finance_bot.logging import get_logger
from finance_bot.finance.agent import FinanceAgent


class Command(BaseCommand):
    help = "Runs the Langchain Chat Agent"
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=str,
            default=os.getenv("USER_ID", "1"),
            help='User ID for the chat session',
            required=True,
        )
        parser.add_argument(
            '--user-name',
            type=str,
            default=os.getenv("USER_NICKNAME", "Admin"),
            help='User name for the chat session',
            required=True,
        )

    def handle(self, *args, **options):
        logger = get_logger('LangchainChatAgent')
        
        try:
            agent = FinanceAgent()

            self.stdout.write(self.style.SUCCESS('Finance Agent initialized. Type "bye" to exit.'))
            self.stdout.write("=" * 50)
            
            while True:
                try:
                    user_input = input("\nYou: ").strip()
                    
                    if not user_input:
                        continue
                        
                    if user_input.lower() in ('bye', 'exit', 'quit'):
                        self.stdout.write(self.style.SUCCESS("\nExiting..."))
                        break
                    
                    response = agent.invoke({
                        'user_id': options['user_id'],
                        'user_name': options['user_name'],
                        'input': user_input,
                    })
                    
                    self.stdout.write(f"\n{self.style.HTTP_INFO('Agent:')} {response}")
                    
                except KeyboardInterrupt:
                    self.stdout.write(self.style.WARNING("\nExiting..."))
                    break
                except Exception as err:
                    logger.error("An error occurred: %s", str(err), exc_info=True)
                    self.stderr.write(self.style.ERROR(f"Error: {str(err)}"))
                    
        except Exception as e:
            logger.critical("Failed to initialize agent: %s", str(e), exc_info=True)
            self.stderr.write(self.style.ERROR(f"Failed to initialize agent: {str(e)}"))
            return
