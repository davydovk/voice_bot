import subprocess

import speech_recognition as sr
from aiogram import types

from loader import dp, bot

recognizer = sr.Recognizer()


@dp.message_handler(content_types=types.ContentTypes.VOICE)
async def recognizer_audio(message: types.Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    download_file = await bot.download_file(file.file_path)

    with open('audio.ogg', 'wb') as new_voice:
        new_voice.write(download_file.getvalue())

    try:
        subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])
    except FileNotFoundError:
        await message.answer(f'Файл не найден, обратитесь к администратору!')

    file_wav = sr.AudioFile('audio.wav')
    with file_wav as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language='ru_RU')
        await message.reply(text)
