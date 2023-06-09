
import urllib.request
import telebot
import os
import cv2
import urllib.request
import speech_recognition as sr
from pydub import AudioSegment
from telebot import types

TOKEN = '6255032320:AAH3gCZv1NfR8mcqbKQb4h_dLbw1Sjbqs8M'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['video_note'])
def handle_video_note(message):
    # Получаем информацию о видео-заметке
    video_note = message.video_note
    video_note_path = bot.get_file_url(video_note.file_id)
    print('Есть видос!!!!')

    # Создаем папку для сохранения кадров
    frames_folder = 'frames'
    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)

    # Загружаем видео-заметку
    video_note_filename = 'video_note.mp4'
    video_note_filepath = os.path.join(frames_folder, video_note_filename)
    urllib.request.urlretrieve(video_note_path, video_note_filepath)

    # Открываем видео-файл с помощью OpenCV
    cap = cv2.VideoCapture(video_note_filepath)
    print('Работаю!!!!')

    # Считываем кадры из видео и сохраняем их в формате PNG
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Создаем путь для сохранения кадра
        frame_path = os.path.join(frames_folder, f'frame_{frame_count}.png')

        # Сохраняем кадр в формате PNG
        cv2.imwrite(frame_path, frame)

        # Увеличиваем счетчик кадров
        frame_count += 1

    # Закрываем видео-файл
    cap.release()
    print('Отправляем!!!!')
    # Отправляем кадры в чат
    for i in range(frame_count):
        frame_path = os.path.join(frames_folder, f'frame_{i}.png')
        with open(frame_path, 'rb') as frame_file:
            bot.send_photo(message.chat.id, frame_file)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    def handle_voice(message):
        # Получаем информацию о голосовом сообщении
        voice = message.voice
        voice_path = bot.get_file_url(voice.file_id)
        # Скачиваем голосовое сообщение
        voice_filename = 'voice_message.ogg'
        voice_filepath = os.path.join('.', voice_filename)
        urllib.request.urlretrieve(voice_path, voice_filepath)
        # Конвертируем в WAV
        wav_filename = 'voice_message.wav'
        wav_filepath = os.path.join('.', wav_filename)
        sound = AudioSegment.from_ogg(voice_filepath)
        sound.export(wav_filepath, format='wav')

        # Распознаем речь в голосовом сообщении
        r = sr.Recognizer()
        with sr.AudioFile(wav_filepath) as source:
            audio = r.record(source)

        # Переводим распознанный текст
        text = r.recognize_google(audio, language='ru')

        # Отправляем текстовый результат обратно в чат
        bot.reply_to(message, text)

        # Удаляем временные файлы
        os.remove(voice_filepath)
        os.remove(wav_filepath)
bot.infinity_polling()
