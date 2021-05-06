phrase = "I am the very model of a modern major general! Something something something something something, I don't know the rest."
phrase2 = "What if I was to go out to sea, and explore the world? Would you wait for me? I don't know that I would want you to... it wouldn't be fair"

def fix_phrase(text, max_characters=20):
    cut_spot = max_characters
    output_list = []
    segments = len(text)/max_characters

    while len(text) > max_characters:
        parsing_cut_spot = True

        while parsing_cut_spot:
            if text[cut_spot] != " ":
                cut_spot -= 1
            if text[cut_spot] == " ":
                output_list.append(text[0: cut_spot])
                text = text[cut_spot+1: len(text)]
                parsing_cut_spot = False
                cut_spot = max_characters

    output_list.append(text)
    return output_list




