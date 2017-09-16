# -*- coding: utf-8 -*-
import speech_kit
import  mic_input
import resume
import re


TOPIC_NAMES = 'names'
TOPIC_BUYING = 'buying'
TOPIC_QUERIES = 'queries'
TOPIC_NUMBERS = 'numbers'
# queries
# maps
# dates
# names
# numbers
# music
# buying


def start():
    while True:
        file_name = mic_input.listen_for_speech(1)[0];
        user_answers = speech_kit.sound_to_text(filename=file_name, topic=TOPIC_QUERIES)
        if len(user_answers) > 0:
            print 'On start: {}'.format(user_answers[0].encode('utf-8').lower())
            if user_answers[0].encode('utf-8').lower() in ['окей игорь', 'ок игорь']:
                speech_kit.play_text('Привет! Давайте создадим резюме!')
                return


def get_answer(question, topic):
    speech_kit.play_text(question)
    file_name = mic_input.listen_for_speech(1)[0];
    user_answers = speech_kit.sound_to_text(filename=file_name, topic=topic)
    while len(user_answers) == 0:
        speech_kit.play_text('Я не расслышал. {}'.format(question))
        file_name = mic_input.listen_for_speech(1)[0];
        user_answers = speech_kit.sound_to_text(filename=file_name, topic=topic)
    return user_answers[0].encode('utf-8')


def get_confirm(text_for_confirm):
    fanswer = get_answer('Вы сказали {}. Д+а или нет?'.format(text_for_confirm), TOPIC_BUYING)
    print 'Confirm answer: {}'.format(fanswer)
    if fanswer.lower() in ['да', 'ага', 'угу']:
        return True
    elif fanswer.lower() in ['нет', 'не', 'неа']:
        return False
    else:
        speech_kit.play_text('Я не расслышал')
        return get_confirm(text_for_confirm)


def add_resume_field(question, topic, function, r_id=None, convert_function=None):
    confirmed = False
    while not confirmed:
        answer = get_answer(question=question, topic=topic)
        print 'Field answer: {}'.format(answer)
        confirmed = get_confirm(answer)
        print 'Подтверждено', confirmed
    speech_kit.play_text('Сохраняю')
    if convert_function:
        answer = convert_function(answer)
    if r_id is not None:
        return function(answer, r_id)
    else:
        return function(answer)


def convert_phone(phone):
    phone = re.sub('[^0-9]', '', phone)
    res = {
        'city': None,
        'number': None,
        'error': None
    }
    if len(phone) < 10:
        res['error'] = 'Номер слишком короткий'
        return res
    if len(phone) > 11:
        res['error'] = 'Номер слишком длинный'
    if len(phone) == 11:
        phone = phone[1:]
    if len(phone) == 12:
        phone = phone[2:]

    res['city'] = phone[0:3]
    res['number'] = phone[3:]
    return res

start()
resume_id = add_resume_field('Назовите ваше имя', TOPIC_NAMES, resume.add_first_name)
# resume_id = '0bdba3adff04068aac0039ed1f376179477772'
print 'Created resume with id {}'.format(resume_id)
add_resume_field('Назовите вашу фамилию', topic=TOPIC_NAMES, function=resume.add_last_name, r_id=resume_id)
add_resume_field('Продиктуйте название резюме', topic=TOPIC_QUERIES, function=resume.add_title, r_id=resume_id)
add_resume_field('Сколько вы хотите зарабатывать в месяц в рублях?', topic=TOPIC_QUERIES, function=resume.add_salary, r_id=resume_id)
add_resume_field('Продиктуйте номер телефона для связи', topic=TOPIC_NUMBERS, function=resume.add_phone,
                 r_id=resume_id, convert_function=convert_phone)
speech_kit.play_text('Остальное как-нибудь сами. У меня л+аапки. Всем пока!')
