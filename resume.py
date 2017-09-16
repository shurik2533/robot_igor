# -*- coding: utf-8 -*-
import requests
import re


API_TOKEN = 'P23VEDBPKL4PQ1ESR0LI9LA0OLK3HHD9T2KVROV6760TTJ8FDNJ6V1ALOBG3JMBP'


def create_or_update_resume(json, resume_id=None):
    print 'API request: ', json
    headers = {
        'Authorization': 'Bearer {}'.format(API_TOKEN),
        'User-Agent': 'Robot-igor'
    }
    if resume_id:
        r = requests.put('https://api.hh.ru.ts31.pyn.ru/resumes/{}'.format(resume_id), headers=headers, verify=False, json=json)
        if r.status_code != 204:
            print r.status_code
            print r.json()
    else:
        r = requests.post('https://api.hh.ru.ts31.pyn.ru/resumes', headers=headers, verify=False, json=json)
        if r.status_code != 201:
            print r.status_code
            print r.json()
        else:
            resume_id = r.headers['Location'].replace('/resumes/', '')
    return resume_id


def add_first_name(first_name):
    return create_or_update_resume({'first_name': first_name.decode('utf-8').capitalize()})


def add_last_name(last_name, resume_id):
    return create_or_update_resume({'last_name': last_name.decode('utf-8').capitalize()}, resume_id)


def add_title(title, resume_id):
    return create_or_update_resume({'title': title.decode('utf-8').capitalize()}, resume_id)


def add_salary(amount, resume_id):
    amount = re.sub('[^0-9]', '', amount)
    return create_or_update_resume({"salary": {
        "amount": amount,
        "currency": "RUR"
    }}, resume_id)


def add_phone(phone, resume_id):
    return create_or_update_resume({"contact": [
        {
            "comment": "",
            "type": {
                "id": "cell"
            },
            "preferred": True,
            "value": {
                "country": "7",
                "city": "123",
                "number": "4567890",
            }
        },
        {
            "type": {
                "id": "email"
            },
            "preferred": False,
            "value": "applicant@example.com"
        }
    ]}, resume_id)