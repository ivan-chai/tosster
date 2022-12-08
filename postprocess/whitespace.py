import random
import string


def gen_comment():
    return "#" + "".join(random.sample(string.ascii_letters, random.randint(1, 20)))


def update_whitespace(text, level=1.0):
    if random.random() > level:
        return text
    rows = list(text.split("\n"))
    for _ in range(int(len(rows) * level)):
        index = random.randint(0, len(rows))
        new_row = " " * random.randint(0, 5)
        if random.random() < 0.05:
            new_row = new_row + gen_comment()
        rows = rows[:index] + [new_row] + rows[index:]
    for _ in range(int(len(rows) * 0.1 * level)):
        index = random.randint(0, len(rows) - 1)
        rows[index] = rows[index] + gen_comment()
    return "\n".join(rows)
