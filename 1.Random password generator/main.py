import random
import string
import numpy as np

def shuffle_password(lists,number):
    random.shuffle(lists)
    lists_2 = "".join(lists)
    return "".join(random.sample(str(lists_2),number))

def password_generator(n):
    while True:
        l = np.random.randint(low= 1 ,high = n, size= 4)
        res = sum(l)
        if res == n:
            break
    no_of_up,no_of_lo,no_of_dig,no_of_pnc = l

    upper_case_1 = random.sample(string.ascii_uppercase,no_of_up)
    upper_case_2 = random.sample(string.ascii_uppercase,no_of_up)

    lower_case_1 = random.sample(string.ascii_lowercase,no_of_lo)
    lower_case_2 = random.sample(string.ascii_lowercase,no_of_lo)

    digits_1 = random.sample(string.digits,no_of_dig)
    digits_2 = random.sample(string.digits,no_of_dig)

    punctuation_1 = random.sample(string.punctuation,no_of_pnc)
    punctuation_2 = random.sample(string.punctuation,no_of_pnc)

    before_password = upper_case_1 +   upper_case_2 + lower_case_1 +  lower_case_2 \
               + digits_2 + digits_1 + punctuation_2 + punctuation_1

    return list(before_password),n

length_of_password = int(input("Enter the lenth of password: "))
l,k = password_generator(length_of_password)
print(shuffle_password(l,k))