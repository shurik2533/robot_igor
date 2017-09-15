# -*- coding: utf-8 -*-
import speech_kit
import  mic_input
import resume


TOPIC_NAMES = 'names'
# queries
# maps
# dates
# names
# numbers
# music
# buying

speech_kit.play_text('Здравствуйте! Меня зовут робот Игорь. Я помогу вам создать резюме. Назовите ваше имя')
file_name = mic_input.listen_for_speech(1)[0];
user_answer = speech_kit.sound_to_text(filename=file_name, topic=TOPIC_NAMES)[0]
speech_kit.play_text('Вы сказали {}. Д+а или нет?'.format(user_answer.encode('utf-8')))