from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
import asyncio

class HelloAgent(Agent):
    class SayHelloBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"Hello. I am {self.agent.jid}, just a basic agent")

    async def setup(self):
        print(f"{self.jid} starting...")
        b = self.SayHelloBehaviour()
        self.add_behaviour(b)

async def main():
    agent = HelloAgent("m31dev@xmpp.jp", "#Password1")
    await agent.start()
    print("Agent started.")

    try:
        while agent.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping agent...")
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
