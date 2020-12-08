# 2015244044 이준희
# 이메일 인증번호를 30글자로 랜덤으로 출력
import string
import random

def generate_random_string(length=30):
    choice_set = string.ascii_letters + string.digits
    return ''.join(random.choices(choice_set, k=length))


