import subprocess
import soundfile
import speech_recognition as sr
from aiogram import types

from loader import dp, bot

recognizer = sr.Recognizer()


# Обработчик для голосовых сообщений
@dp.message_handler(content_types=types.ContentTypes.VOICE)
async def recognizer_audio(message: types.Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    download_file = await bot.download_file(file.file_path)

    # Сохраняем голосовое сообщение в файл audio.ogg
    with open('audio.ogg', 'wb') as new_voice:
        new_voice.write(download_file.getvalue())

    # Преобразуем файл audio.ogg в файл audio.wav
    try:
        subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])
    except FileNotFoundError:
        await message.answer(f'Файл не найден, обратитесь к администратору!')

    # Распознаем текст в голосовом сообщении и отправляем ответ
    file_wav = sr.AudioFile('audio.wav')
    with file_wav as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language='ru_RU')
        await message.reply(text)


# Обработчик для аудио сообщений, пересланных из WhatsApp
@dp.message_handler(content_types=types.ContentTypes.AUDIO)
async def recognizer_audio(message: types.Message):
    file_id = message.audio.file_id
    file = await bot.get_file(file_id)

    if '.m4a' in file.file_path:
        download_file = await bot.download_file(file.file_path)

        # Сохраняем голосовое сообщение в файл audio.m4a
        with open('audio.m4a', 'wb') as new_voice:
            new_voice.write(download_file.getvalue())

        # Преобразуем файл audio.ogg в файл audio.wav
        try:
            subprocess.run(['ffmpeg', '-i', 'audio.m4a', 'audio_m4a.wav', '-y'])
        except FileNotFoundError:
            await message.answer(f'Файл не найден, обратитесь к администратору!')

        # Меняем кодировку
        data, samplerate = soundfile.read('audio_m4a.wav')
        soundfile.write('audio_m4a_new.wav', data, samplerate, subtype='PCM_16')

        # Распознаем текст в голосовом сообщении и отправляем ответ
        file_wav = sr.AudioFile('audio_m4a_new.wav')
        with file_wav as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='ru_RU')
            await message.reply(text)
