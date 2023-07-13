from django.db import models
from common.models import CommonModel

from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

from taggit.managers import TaggableManager

class PossibleBoard(CommonModel):
    """
    특허 등록 가능성 검토 게시판
    제목, 신청자 이름, 개인/기업, 이메일, 비번, 키워드, 내용, 첨부파일
    """

    # 제목 / 발명의 명칭(키워드) / 최대 5단어 / 띄어쓰기 금지 / 쉼표로 구분
    title = models.CharField(
        max_length=30,
        blank=False,
    )

    # 신청자 이름 == OK
    name = models.CharField(
        max_length=10,
        blank=False,
    )
    
    # 휴대폰 번호 == OK
    telephone = models.CharField(
        max_length=20,
        blank=False,
    )

    # 신청자 이메일 == OK
    email = models.EmailField(
        max_length=50,
        blank=False,
    )

    # 신청 시 간단한 비밀번호 == OK
    password = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        validators=[
            RegexValidator(
                regex=r"^[a-z0-9]+$",
                message="비밀번호는 영문 소문자와 숫자를 조합하여 7글자 이내로 입력해주세요.",
            ),
        ],
    )
    
    # 특허 내용(최대한 자세히 서술하기) == OK
    description = models.TextField(max_length=300, blank=False)
    
    # 상담 받고자 하는 내용
    counsling = models.TextField(max_length=200, blank=False)

    # 첨부파일
    file = models.FileField(upload_to="possible/", blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
