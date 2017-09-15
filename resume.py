# -*- coding: utf-8 -*-
import requests


API_TOKEN = 'P23VEDBPKL4PQ1ESR0LI9LA0OLK3HHD9T2KVROV6760TTJ8FDNJ6V1ALOBG3JMBP'


def create_or_update_resume(json, resume_id=None):
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
    return create_or_update_resume({'first_name': first_name})


def add_first_name(last_name, resume_id):
    return create_or_update_resume({'last_name': last_name}, resume_id)