import os
from dotenv import load_dotenv

import pandas as pd
from pandasai import Agent

load_dotenv()
api_key = os.getenv("PANDASAI_API_KEY")
print(api_key)

agent = Agent(df)
agent.chat('Who are you?')
