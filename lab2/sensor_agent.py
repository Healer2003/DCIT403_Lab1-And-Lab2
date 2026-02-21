from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
import asyncio
from environment import DisasterEnvironment

class SensorAgent(Agent):
    class MonitorBehaviour(PeriodicBehaviour):
        def __init__(self, env, period):
            super().__init__(period=period)
            self.env = env

        async def run(self):
            event = self.env.generate_event()
            print(f"Sensor detected {event['event']} with severity {event['severity']}")

           
            msg = Message(to="rescueagaent47@xmpp.jp") 
            msg.set_metadata("performative", "inform")
            msg.body = f"{event['event']} with severity {event['severity']}"
            await self.send(msg)
            print("Sensor sent disaster info to RescueAgent.")

    async def setup(self):
        print(f"{self.jid} starting...")
        env = DisasterEnvironment()
        b = self.MonitorBehaviour(env, period=5) 
        self.add_behaviour(b)

async def main():
    agent = SensorAgent("sensoragent23@xmpp.jp", "#Password1")
    await agent.start()
    print("SensorAgent started!")

    try:
        while agent.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping SensorAgent...")
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
