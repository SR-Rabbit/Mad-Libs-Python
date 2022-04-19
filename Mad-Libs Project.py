# Mad libs
# Obtains an input from the user

import pprint
import re


# Allows the user to choose either to provide their own template or use a pre-made one.
def user_story_choice():
    print("Option A: Use your own template\nOption B: Use pre-made template\nOption C: Type your own template")
    while True:
        user_choice = input("Enter Option: ")
        if user_choice.upper() == "A" or user_choice.upper() == "B" or user_choice.upper() == "C":
            return user_choice
        print("--INVALID - ONLY OPTIONS A, B or C CAN BE CHOSEN!--")


# Opens the proper template file - Allows users to enter their own template file
def template_file_open(option):
    if option.upper() == "A":
        while True:
            try:
                user_story = input("Please Enter template file name: ")
                file_handler = open(user_story)
            except OSError:
                print("--UNABLE TO OPEN FILE--")
                continue
            return file_handler

    if option.upper() == "B":
        file_handler = open("mad-lib-templates.txt")

    if option.upper() == "C":
        file_handler = input("Enter Story:\n")
    return file_handler


# Handles processing the file and assigns template into dictionary
def file_processor(file, option):
    word_list = []
    word_result = []
    template_dict = dict()
    counts = 1
    if option.upper() == "C":
        return file

    for line in file:
        x = re.compile("(.+:\s)")  # Used to remove first 3 characters in pre-made template.
        x = x.match(line)
        if x is not None:
            line = line[3:]
        if not line.rstrip():  # Skips blank lines but also keeps count of how many blank lines in the file.
            counts += 1
        line = line.rstrip()
        if line:  # Appends multi-line string together, up until blank line.
            word_list.append(line)
        else:
            if word_list:
                word_result.append(" ".join(word_list))
                word_list = []

    if word_list:
        word_result.append(" ".join(word_list))
        word_list = []

    for key, item in zip(range(counts, 0, -1), word_result):
        template_dict[counts-key+1] = item
    pprint.pprint(template_dict)

    return template_dict


# Allows user to select one of the templates in pre-made templates to use.
def premade_choice(dictionary, option):
    key_length = len(dictionary)

    if option.upper() == "C":
        return dictionary

    if key_length == 1:
        return dictionary[1]

    if key_length > 0:
        while True:
            number_choice = input(f"Enter option - 1 to {key_length}: ")
            if number_choice.isalpha():
                print("--INVALID - Option cannot be a alphabetical character!--")
                continue
            if int(number_choice) <= 0 or int(number_choice) >= key_length + 1:
                print(f"--INVALID - Option can only be between 1 to {key_length}!--")
                continue
            if int(number_choice) > 0 or int(number_choice) < key_length + 1:
                break

    return dictionary[int(number_choice)]


#  Allows users to choose the words to replace the placeholders with, as well as replaces the entire template.
def replace_words(template, user_option):
    replace_dictionary = {}
    brace_check = re.compile("(\{[a-zA-Z\u0080-\uFFFF]+\})")  # Matches any unicode characters with curly braces
    num = 0
    if user_option.upper() == "B":
        for item in brace_check.finditer(template):
            num += 1
            original_word = item.group()  # Copy of original word to compare against
            placeholder_word = item.group()[:len(item.group())-1] + str(num) + item.group()[-1:]
            template = template.replace(original_word, placeholder_word, 1)
            print("Placeholder word: ", placeholder_word)
            replace_dictionary[placeholder_word] = input("Enter word to replace it with: ")
            if " " in replace_dictionary[placeholder_word] or " " in placeholder_word:  # Allows only 1 word
                print("--INVALID - Only 1 word allowed for placeholder or replacement!--")
                print("--DEFAULTING TO ORIGINAL WORD--")
                replace_dictionary[placeholder_word] = original_word

    else:
        print("Please select the word(s) to replace - Case sensitivity is important!\nEnter 'done' twice to exit")
        while True:
            change = input("Enter placeholder word: ")
            new_word = input("Enter word to replace it with: ")
            if change.lower() == "done" and new_word.lower() == "done":
                break
            if change not in template.split():
                print("--INVALID - Placeholder word is not available in chosen template!--")
                continue
            if " " in new_word or " " in change:
                print("--INVALID - Only 1 word allowed for placeholder or replacement!--")
                continue
            replace_dictionary[change] = new_word

    for key, value in replace_dictionary.items():
        template = template.replace(key, value)

    return template


user_input_choice = user_story_choice()
file_handle = template_file_open(user_input_choice)
process_file = file_processor(file_handle, user_input_choice)
chosen_template = premade_choice(process_file, user_input_choice)
final_replace = replace_words(chosen_template, user_input_choice)
pprint.pprint(final_replace)
