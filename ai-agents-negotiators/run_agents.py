import time

from agno.agent import Agent
from agno.models.google.gemini import Gemini
from agno.models.ollama import Ollama

# OLLAMA_MODEL = "qwen2.5:0.5b"
# OLLAMA_MODEL = "deepseek-r1"
OLLAMA_MODEL = "phi4"

buyer = Agent(
  model=Gemini(id="gemini-1.5-flash"),
  # model = Ollama(id=OLLAMA_MODEL),
  description="""
You are a buyer that wants to buy an egg. The most you can pay is 8 dollars,
but anything under is profit. Start low and work your way up. You can also ask
questions about the egg. Be as sneaky as you can and don't let the seller know
your max price.

Keep it short and don't use too many tokens. Don't get too personal.

You are interested in buying a single egg, no more, no less.

When the final price is agreed upon print 'EXIT'.
""",
  name="Buyer",
  markdown=True,
  add_history_to_messages=True,
)

seller = Agent(
  model=Gemini(id="gemini-1.5-flash"),
  # model = Ollama(id=OLLAMA_MODEL),
  description="""
You are a seller that wants to sell an egg. The lowest you can get is 2 dollars,
but anything over is profit. Start high and work your way down. Be as sneaky as
you can and don't let the buyer know your min price.

Keep it short and don't use too many tokens. Don't get too personal.

When the final price is agreed upon print'EXIT'.
""",
  name="Seller",
  markdown=True,
  add_history_to_messages=True,
)

started = False

SELLER_FIRST = True

FIRST_MESSAGE_WITHOUT_SUGGESTION = "You start the negotiation. Ask for the other's price, don't suggest."

FIRST_MESSAGE_WITH_SUGGESTION = "You start the negotiation. Suggest a price."

FIRST_MESSAGE = FIRST_MESSAGE_WITHOUT_SUGGESTION

if SELLER_FIRST:
  while True:
    if not started:
      message = FIRST_MESSAGE
      started = True
    else:
      # message = f'Buyer says: "{response.content}"'
      message = f'{response.content}'

    response = seller.run(message)

    print(f'\n\nSeller says: "{response.content}"')

    if 'EXIT' in response.content:
      break

    message = f'Seller says: "{response.content}"'

    response = buyer.run(message)

    print(f'\n\nBuyer says: "{response.content}"')

    if 'EXIT' in response.content:
      break

    time.sleep(10)
else:
  while True:
    if not started:
      message = FIRST_MESSAGE
      started = True
    else:
      # message = f'Seller says: "{response.content}"'
      message = f'{response.content}'

    response = buyer.run(message)

    print(f'\n\nBuyer says: "{response.content}"')

    if 'EXIT' in response.content:
      break

    message = f'Buyer says: "{response.content}"'

    response = seller.run(message)

    print(f'\n\nSeller says: "{response.content}"')

    if 'EXIT' in response.content:
      break

    time.sleep(10)

response = seller.run("Print all suggested prices by both the buyer and seller in a python list.")

print(f'\n\nSummary: "{response.content}"')
