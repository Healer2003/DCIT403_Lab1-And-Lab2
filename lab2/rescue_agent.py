from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from spade.template import Template
import asyncio

class Idle(State):
    async def run(self):
        print("RescueAgent is idle, waiting for disaster events...")
        msg = await self.receive(timeout=10)
        if msg:
            print(f"RescueAgent received disaster: {msg.body}")
            self.set_next_state("RESPOND")
        else:
            self.set_next_state("IDLE")  # stay idle if no message

class Respond(State):
    async def run(self):
        print("RescueAgent responding to disaster...")
        await asyncio.sleep(3)
        print("Rescue completed.")
        self.set_next_state("REPORT")

class Report(State):
    async def run(self):
        print("RescueAgent reporting task completion...")
        await asyncio.sleep(1)
        print("Report sent.")
        self.set_next_state("IDLE")

class RescueAgent(Agent):
    async def setup(self):
        fsm = FSMBehaviour()
        fsm.add_state(name="IDLE", state=Idle(), initial=True)
        fsm.add_state(name="RESPOND", state=Respond())
        fsm.add_state(name="REPORT", state=Report())
        fsm.add_transition(source="IDLE", dest="RESPOND")
        fsm.add_transition(source="RESPOND", dest="REPORT")
        fsm.add_transition(source="REPORT", dest="IDLE")
        fsm.add_transition(source="IDLE", dest="IDLE")
        self.add_behaviour(fsm)

        # Template to receive INFORM messages only
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(fsm, template)

async def main():
    agent = RescueAgent("rescueagent47@xmpp.jp", "123456")
    await agent.start()
    print("RescueAgent started!")

    try:
        while agent.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping RescueAgent...")
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())