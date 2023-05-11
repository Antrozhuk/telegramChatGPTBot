import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from telegramChatGPTBot.openai_helper import OpenAIHelper


class ChatGPT3TelegramBot:
    """
    Class representing a Chat-GPT3 Telegram Bot.
    """

    def __init__(self, config: dict, openai: OpenAIHelper):
        """
        Ініціалізує бот конфігурацією та GPT-3 налаштуваннями.
        :param config: Словник з конфігурацією бота
        :param openai: OpenAIHelper обʼєкт
        :param disallowed_message: Повідомлення про відсутність доступу
        """
        self.config = config
        self.openai = openai
        self.disallowed_message = "Вибачте, але вам не дозволено користуватись цим ботом."

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Показує допоміжне повідомлення.
        """
        await update.message.reply_text("/reset - Оновлює бесіду\n"
                                        "[Будь яке повідомлення] - Відправляє ваше повідомлення до AI\n"
                                        "/help - Меню помічника\n\n",
                                        disable_web_page_preview=True)

    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Оновлює бесіду.
        """
        if not await self.is_allowed(update):
            logging.warning(f'User {update.message.from_user.name} is not allowed to reset the conversation')
            await self.send_disallowed_message(update, context)
            return

        logging.info(f'Resetting the conversation for user {update.message.from_user.name}...')

        chat_id = update.effective_chat.id
        self.openai.reset_chat_history(chat_id=chat_id)
        await context.bot.send_message(chat_id=chat_id, text='Done!')

    async def prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        React to incoming messages and respond accordingly.
        """
        if not await self.is_allowed(update):
            logging.warning(f'User {update.message.from_user.name} is not allowed to use the bot')
            await self.send_disallowed_message(update, context)
            return

        logging.info(f'New message received from user {update.message.from_user.name}')
        #  TODO: Add logic for prompt method

    async def send_disallowed_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Відправляє повідомлення про відсутність доступів до користувача.
        """
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.disallowed_message,
            disable_web_page_preview=True
        )

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Відловлює всі помилки.
        """
        logging.debug(f'Exception while handling an update: {context.error}')

    async def is_allowed(self, update: Update) -> bool:
        """
        Перевіряє чи дозволено юзеру користуватись даним ботом.
        """
        pass
        #  TODO: Add logic for is_allowed method

    def run(self):
        """
        Запускає бот доки користувач не натисне Ctrl+C
        """
        application = ApplicationBuilder().token(self.config['token']).build()

        application.add_handler(CommandHandler('start', self.help))

        application.add_handler(CommandHandler('help', self.help))

        application.add_handler(CommandHandler('reset', self.reset))

        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.prompt))

        application.add_error_handler(self.error_handler)

        application.run_polling()
