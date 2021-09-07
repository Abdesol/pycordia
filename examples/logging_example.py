from pycordia import events, models
import pycordia
import dotenv
import os

dotenv.load_dotenv()
client = pycordia.Client(intents=pycordia.Intents.all())
LOGS_CHANNEL: str = ""  # Change this to a suitable channel's ID


@client.event
async def on_ready(event: events.ReadyEvent):
    """The bot is up and running! Yippee!"""
    print(f"{event.user} ready to do stuff!", client.intents)


@client.event
async def on_channel_create(channel: models.Channel):
    """Be the first to send a message in any channel!"""
    await models.Message.create(
        content=f"First to send a message in {channel.mention}!"
    ).send(client, channel.id)


@client.event
async def on_channel_update(channel: models.Channel):
    """Notify people when a channel was updated"""
    await models.Message.create(
        content=f"Whoops! It looks like someone updated {channel.mention}!\n"
                + "Why don't you take a look at the audit logs to view the changes?"
    ).send(client, LOGS_CHANNEL)


@client.event
async def on_channel_delete(channel: models.Channel):
    await models.Message.create(
        content=f"A channel was deleted! - {channel}"
    ).send(client, LOGS_CHANNEL)


@client.event
async def on_message_create(_: models.Message):
    """
        We need this event to listen to messages
        Otherwise pycordia won't cache messages
        and our `on_message_update` and `on_message_delete`
        events won't be triggered
    """
    pass


@client.event
async def on_message_update(before: models.Message, after: models.Message):
    """Log edited messages, for moderation purposes"""
    embed = models.Embed.create(
        title="Edited Message!",
        description=f"**Before**: {before.content}\n**After**: {after.content}",
        color=0xFFAAAA
    )
    await models.Message.create(
        embeds=[embed]
    ).send(client, LOGS_CHANNEL)


@client.event
async def on_message_delete(message: pycordia.events.MessageDeleteEvent):

    deleted_messages = []
    for id_ in message.message_ids:
        message = client.message_cache.get(id_)
        if message:
            deleted_messages.append(f"Author - {message.author}\nContent - {message.content}")

    embed = models.Embed.create(
        title="Message(s) Deleted!",
        description="\n\n".join(deleted_messages),
        color=0xAA12DD
    )

    await models.Message.create(
        embeds=[embed]
    ).send(client, LOGS_CHANNEL)


client.run(os.getenv("DISCORD_TOKEN"))
