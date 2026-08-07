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
