
def char_multiplier(coefficient):
    return lambda string: ''.join(char*coefficient for char in string)

if __name__ == '__main__':
    out = []

    out.append(char_multiplier(3)('Bob'))
    char_doubler = char_multiplier(2)
    out.append(char_doubler('Double me up baby.'))
    out.append(char_doubler('Twice over.'))
    
    for line in out:
        print(line)
