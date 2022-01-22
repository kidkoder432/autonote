"""
autonote - A program to automatically take notes in textbooks.
"""
import nltk  # Import NLTK for language processing
from string import punctuation

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)

def multiinput(prompt):
    print(prompt)
    print("Press Ctrl+C to finish.\n")
    contents = []
    while True:
        try:
            line = input()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        contents.append(line)
    return contents

stopw = nltk.corpus.stopwords.words()


def prep(text):
    text = text.replace('\r\n', ' ')
    text = [
        word.lower() for word in text.split() if word.lower() not in stopw
    ]  # Remove unnecessary words
    # text = [char for char in text if char not in punctuation]  # Remove punctuation
    return text


def extract(text):
    notes = []
    for para in text:  # Extractor
        if not para or para == "":
            continue  # Skip blank lines
        if ">>" in para:
            notes.append(para)  # Append headings; we'll render them later
            continue
        maxSent = len(nltk.sent_tokenize(para)) - 3 if len(nltk.sent_tokenize(para)) > 2 else 1
        topicSent = nltk.sent_tokenize(para)[0]  # para[0:para.find('. ')]
        totalSent = 1
        # Use the first sentence of each paragraph as a topic sentence (if it isn't already in the notes)
        if topicSent not in notes:
            notes.append(topicSent)

        # Get summary of paragraph
        freqs = {}
        sentweights = {}
        for word in prep(para):

            freqs.setdefault(word, 0)
            freqs[word] += 0.2

        for sent in nltk.sent_tokenize(para):
            for word in freqs:
                if word in sent:
                    sentweights.setdefault(sent, 0)
                    sentweights[sent] += freqs[word]

        sentweights = {
            k: v for k, v in sorted(sentweights.items(), key=lambda item: item[1])
        }  # One-liner from SO: sort dict by value
        
        summSent = list(sentweights.keys())[-1]
        if summSent not in notes and totalSent <= maxSent:
            notes.append(summSent)
            totalSent += 1

        # Get uncommon but noteworthy info
        unexp = list(sentweights.keys())[0]
        if unexp not in notes and totalSent <= maxSent:
            notes.append(unexp)
            totalSent += 1



        # Get quotes & numerical info
        for sent in nltk.sent_tokenize(para):
            
            if '“' in sent or '”' in sent:
                if sent not in notes and totalSent <= maxSent:
                    notes.append(sent)
                    totalSent += 1
                    continue
            for word in nltk.word_tokenize(sent):
                word = "".join(
                    [char for char in word if char not in punctuation]
                )  # Remove punctuation (so 100,000 is read as 100000)
                if word[:-1].isnumeric():  # We're using word[:-1] so that words such as 1800s are valid
                    if sent not in notes and totalSent <= maxSent:
                        notes.append(sent)  # Add the sentence to the notes list if it is not already there.
                        totalSent += 1


    return notes

if __name__ == '__main__':
    
    # Get text from user input
    text = multiinput("Enter text to take notes on: ")
    
    with open("notes.md", "w", encoding="utf8") as f:
        print("\033[1m\033[1mHISTORY CLASS NOTES")
        f.write('# **History Class Notes**\n\n')
    
        title = "The Republicans Take Power"
        f.write(f"## **{title}**\n")
        print(title + '\033[0m')
        
        for note in extract(text):
        
            if not note:
                continue
        
            if note.startswith('>>'):
                print(f'\n\033[1m{note[2:]}\033[0m')  # Make headings bold
                f.write(f'\n### {note[2:]}\n\n')
        
            else:
                f.write(f'- {note}\n')

    f.close()