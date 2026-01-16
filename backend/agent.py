from livekit.agents import Agent, AgentSession, AgentServer, JobContext, cli
from livekit.plugins.xai import realtime
from livekit.plugins.xai.realtime import WebSearch, XSearch
from dotenv import load_dotenv
from requests import session

load_dotenv()


class ResearchAssistant(Agent):
    def __init__(self):
        super().__init__(
            instructions="""You are a research assistant with access to web search and X search.

- Use web search for general queries and current information
- Use X search when users ask about posts or what people are saying on X/Twitter

Always mention your sources when providing information.""",
        )


server = AgentServer()


@server.rtc_session()
async def entrypoint(ctx: JobContext):
    await ctx.connect()
    session = AgentSession(
        llm=realtime.RealtimeModel(voice="ara"),
        tools=[
            WebSearch(),
            XSearch(),
        ],
    )
    await session.start(room=ctx.room, agent=ResearchAssistant())


if __name__ == "__main__":
    cli.run_app(server)