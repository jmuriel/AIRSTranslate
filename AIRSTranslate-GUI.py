import os
from google.cloud import translate
from nltk import word_tokenize
from nltk import pos_tag
from sys import argv
from Tkinter import *
from tkFileDialog import askopenfilename

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "AIRSTranslate-cd28fb93cf7c.json"

def do_input(input_file):
    f = open(input_file, 'r')
    document_text = f.read()
    f.close
    return document_text

def make_dictionaries(document):
    # get the document as text
    document_text = document
    # create empty dictionaries
    unique_nouns = {}
    unique_adjectives = {}
    unique_verbs = {}
    unique_adverbs = {}
    #convert the document text to lowercase
    lowered_text = document_text.lower()
    # split the words up
    split_text = word_tokenize(lowered_text)
    # tag the words
    tagged_text = pos_tag(split_text)
    # populate the dictionaries
    for (word, tag) in tagged_text:
        if tag[0] == "N":
            unique_nouns[word] = None
        elif tag[0] == "J":
            unique_adjectives[word] = None
        elif tag[0] == "V":
            unique_verbs[word] = None
        elif tag[0] == "R":
            unique_adverbs[word] = None
    # return the results
    return unique_nouns, unique_adjectives, unique_verbs, unique_adverbs

def get_translation(of):
    translator = translate.Client()
    source_language ='en'
    target_language = gui_language.get()
    text = of 
    translation = translator.translate(text, source_language=source_language, 
                  target_language=target_language)
    items = translation.items()
    return items[0][1]

def store_translations((unique_nouns, unique_adjectives, unique_verbs, 
                       unique_adverbs)):
    complete_nouns = {}
    complete_adjectives = {}
    complete_verbs = {}
    complete_adverbs = {}
    for word in unique_nouns.keys():
        translation = get_translation(word)
        complete_nouns[word] = translation
    for word in unique_adjectives.keys():
        translation = get_translation(word)
        complete_adjectives[word] = translation
    for word in unique_verbs.keys():
        translation = get_translation(word)
        complete_verbs[word] = translation
    for word in unique_adverbs.keys():
        translation = get_translation(word)
        complete_adverbs[word] = translation
    return complete_nouns, complete_adjectives, complete_verbs, complete_adverbs

def do_output((complete_nouns, complete_adjectives, complete_verbs, complete_adverbs), output_language):
    output_file = name_language(output_language) + "_Vocabulary_List.txt"
    f = open(output_file, 'w')
    # write the nouns
    f.write("Nouns:\n\n")
    for word in sorted(complete_nouns.keys()):
        f.write(word + "\t" + complete_nouns[word].encode('utf-8') + "\n")
    # write the adjectives
    f.write("\nAdjectives:\n\n")
    for word in sorted(complete_adjectives.keys()):
        f.write(word + "\t" + complete_adjectives[word].encode('utf-8') + "\n")
    # write the verbs
    f.write("\nVerbs:\n\n")
    for word in sorted(complete_verbs.keys()):
        f.write(word + "\t" + complete_verbs[word].encode('utf-8') + "\n")
    # write the adverbs
    f.write("\nAdverbs:\n\n")
    for word in sorted(complete_adverbs.keys()):
        f.write(word + "\t" + complete_adverbs[word].encode('utf-8') + "\n")
    f.close()

def main():
    print("\nHi! I'm working...\n\n")
    input_file = gui_input.get()
    language = gui_language.get()
    output_file = gui_language.get().title() + "_Vocabulary_List.txt"
    f = do_input(input_file)
    dictionaries = make_dictionaries(f)
    print("I'm talking to Google. This could take a minute...!\n\n")
    translated_dictionaries = store_translations(dictionaries)
    do_output(translated_dictionaries, language)
    print("Done. Please enjoy your vocabulary list. \n\nKeep in mind that Google Translate is not perfect. Now you should check with a native speaker, or at least an old-fashioned dictionary, to make sure the results make sense.\n")

root = Tk()
root.title("AIRS Translate v. 0.90")

# Create GUI Inputs
gui_language = StringVar()
gui_language.set("L")
gui_input = StringVar()
gui_input.set("L")


def set_input_filename():
    gui_input.set(askopenfilename())
    return 

def name_language(language_code):
    if language_code == "es":
        return "Spanish"
    if language_code == "ar":
        return "Arabic"
    if language_code == "fa":
        return "Farsi"
    if language_code == "sw":
        return "Swahili"

# Draw GUI

# Draw Frames
upperframe = Frame(root)
upperframe.pack()
lowerframe = Frame(root)
lowerframe.pack()

# Instructions
airs_message = """
Welcome to AIRSTranslate! 

This program is simple to use. Just follow these steps:

1. Find a nice story you want the students to work on with you. I recommend Aesop's Fables.

2. Save the plain text to a .txt file. I recommend using Notepad for this.

3. Click on "INPUT" above, and select the .txt file you just created.

4. Click on the button for the language that your students speak.

5. Click on "GO" above.

6. Next to your .txt file, there should now be a new .txt file with the vocabulary list in it. You can copy and paste the list to Word if you want to beautify it.

That's all there is to it! The program figures out the part of speech of each word, so all the nouns are together, then all the verbs, and so on. Keep in mind that this is basically light artificial intelligence, so it's not perfect. You should check the list yourself as an English teacher to make sure it makes sense.

Also, this program talks to Google Translate for the actual translation work. Google Translate is not perfect either, so if you can, you should have a native speaker look over the list, or at least use an old-fashioned dictionary to make sure you got the best translation. It's pretty good, though, and it sure does save you a lot of time.

This is version 0.90 written by Jorge Muriel (copyright 2017, all rights reserved) for Arizona Immigrant and Refugee Services. This is an automated vocabulary list builder to aid in English as a Second Language instruction."""

Button(upperframe, text = "QUIT", command = root.quit).pack(anchor = W, fill = BOTH, side = LEFT)
Button(upperframe, text = "INPUT", command = set_input_filename).pack(anchor = W, fill = BOTH, side = LEFT)
Button(upperframe, text= "GO", command = main).pack(anchor = W, fill = BOTH, side = LEFT)
Radiobutton(upperframe, text = "Arabic", variable = gui_language, value = "ar").pack(anchor = W)
Radiobutton(upperframe, text = "Farsi", variable = gui_language, value = "fa").pack(anchor = W)
Radiobutton(upperframe, text = "Spanish", variable = gui_language, value = "es").pack(anchor = W)
Radiobutton(upperframe, text = "Swahili", variable = gui_language, value = "sw").pack(anchor = W)

# Put in a scrollbar
scrollbar = Scrollbar(lowerframe)
scrollbar.pack(side = RIGHT, fill = Y)

T = Text(lowerframe, height = 20, width = 45, yscrollcommand = scrollbar.set)
scrollbar.config(command = T.yview)
T.pack(side = BOTTOM)
T.insert(INSERT, airs_message)
T.config(state=DISABLED, wrap = WORD)

# Do other Tkinter stuff
root.mainloop()
root.destroy()
