# 作   者：林枭熠
# 开发时间:2024/6/19 下午7:06
from random import choice


class VerifyCode:
    """
    验证码生成器
    """
    def __init__(self):
        self.number_seeds = "1234567890"
        self.number_letter_seeds = "1234567890abcdefghijklmnopqrstuvwxyz"

    def generate_verifycode(self, length=4, only_number=False):
        """
        生成k位随机数字,或数字加字母的验证码的验证码字符串
        """
        if only_number:
            seeds = self.number_seeds
        else:
            seeds = self.number_letter_seeds
        random_str = []
        for i in range(length):
            random_str.append(choice(seeds))

        return "".join(random_str)
