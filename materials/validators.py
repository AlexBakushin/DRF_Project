import re
from rest_framework.serializers import ValidationError


class DescriptionValidator:

    def __init__(self, field):
        self.fiend = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.fiend)
        links = re.findall(r'(https?://\S+)', tmp_val)
        for link in links:
            if "youtube.com" in link:
                if "/watch?v=" in link:
                    return value
                else:
                    raise ValidationError("В описание нельзя использовать личные ссылки, кроме видео на youtube")

            else:
                raise ValidationError("В описание нельзя использовать личные ссылки, кроме видео на youtube")
