"""
autonote - A program to automatically take notes in textbooks.
"""
from string import punctuation
import re

# List of stopwords
STOPWORDS = """i 
me
my
myself
we
our
ours
ourselves
you
your
yours
yourself
yourselves
he
him
his
himself
she
her
hers
herself
it
its
itself
they
them
their
theirs
themselves
what
which
who
whom
this
that
these
those
am
is
are
was
were
be
been
being
have
has
had
having
do
does
did
doing
a
an
the
and
but
if
or
because
as
until
while
of
at
by
for
with
about
against
between
into
through
during
before
after
above
below
to
from
up
down
in
out
on
off
over
under
again
further
then
once
here
there
when
where
why
how
all
any
both
each
few
more
most
other
some
such
no
nor
not
only
own
same
so
than
too
very
s
t
can
will
just
don
should
now""".split('\n')



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

stopw = STOPWORDS

def sent_tok(para):
    """A function using regex to split a paragraph into words. """
    return re.split(r'[.”] ')

def word_tok(sent): 
    """A more readable wrapper around split()"""
    return sent.split()
    

def prep(text):
    text = text.replace('\r\n', ' ')
    text = [
        word.lower() for word in word_tok if word.lower() not in stopw
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
        sents = sent_tok(para)
        maxSent = len(sents) - 3 if len(sents) > 3 else 1
        totalSent = 0

        # Get summary of paragraph
        freqs = {}
        sentweights = {}
        for word in prep(para):

            freqs.setdefault(word, 0)
            freqs[word] += 0.2

        for sent in sents:
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
        for sent in sents:
            
            if '“' in sent or '”' in sent:
                if sent not in notes and totalSent <= maxSent:
                    notes.append(sent)
                    totalSent += 1
                    continue
            for word in word_tok(sent):
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
