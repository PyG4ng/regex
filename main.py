import re
import csv

import pandas as pd


def get_data(file):
    # contacts_list = pd.read_csv("phonebook_raw.csv")
    with open(file) as f:
        rows = csv.reader(f, delimiter=",")
        return list(rows)


def cleaning_data(file):
    contacts_list_clean = []
    contacts = get_data(file)

    for contact in contacts[1:]:
        name = re.findall(r"\w+", " ".join(contact[:3]))
        lastname = name[0]
        firstname = name[1]
        if len(name) == 3:
            surname = name[2]
        else:
            surname = ''

        organization = contact[3]
        position = contact[4]
        phone = contact[5]

        phone_pattern = r"\+?(\d)\s?\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{2})[- ]?(\d{2})"
        phone_substitution_pattern = r"+7(\2)\3-\4-\5"
        new_phone = re.sub(phone_pattern, phone_substitution_pattern, phone)

        dop_pattern = r"\(?доб\.\s(\d{4})\)?"
        dop_sub_pattern = r"доб.\1"
        new_phone_with_dop = re.sub(dop_pattern, dop_sub_pattern, new_phone)

        email = contact[6]

        contacts_list_clean.append([lastname, firstname, surname, organization, position, new_phone_with_dop, email])

    cleaned_phonebook = pd.DataFrame(contacts_list_clean)
    cleaned_phonebook.columns = ["lastname", "firstname", "surname", "organization", "position", "phone", "email"]
    cleaned_phonebook = cleaned_phonebook.groupby(['lastname', 'firstname']).agg(
        {'surname': 'max', 'organization': 'max', 'position': 'max',
         'phone': 'max', 'email': 'max'}).reset_index()
    cleaned_phonebook.to_csv('cleaned_phonebook.csv', index=False)
    return cleaned_phonebook


if __name__ == '__main__':
    phonebook = cleaning_data("phonebook_raw.csv")
    print(phonebook)
