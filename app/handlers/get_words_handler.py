from random_word import RandomWords

def random_word_generator():
    r = RandomWords()
    num_of_words = 50
    a = []
    for _ in range(num_of_words):
        a.append(r.get_random_word())

    return ' '.join(a)