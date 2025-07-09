import os

from django.core.management import BaseCommand
from finance_bot.agents.factory import AgentFactory
from finance_bot.agents.finance_agent import FinanceAgent
from finance_bot.agents.config import AgentConfiguration
from finance_bot.logging import get_logger


class Command(BaseCommand):
    help = "Runs the Langchain Chat Agent"
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=str,
            default=os.getenv("USER_ID", "1"),
            help='User ID for the chat session',
        )
        parser.add_argument(
            '--user-name',
            type=str,
            default=os.getenv("USER_NICKNAME", "Admin"),
            help='User name for the chat session',
        )

    def handle(self, *args, **options):
        logger = get_logger('LangchainChatAgent')
        
        try:
            # Register the FinanceAgent with the factory
            AgentFactory.register_agent('finance', FinanceAgent)
            
            # Get user-specific configuration
            config = AgentConfiguration.get_agent_config(user_id=options['user_id'])
            
            # Create the agent instance
            agent = AgentFactory.create('finance', config)
            
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
                    
                    # Invoke the agent with the proper context
                    response = agent.invoke({
                        'user_id': options['user_id'],
                        'user_name': options['user_name'],
                        'input': user_input
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
