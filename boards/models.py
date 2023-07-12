from django.db import models
from common.models import CommonModel

from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

from taggit.managers import TaggableManager

class PossibleBoard(CommonModel):
    """
    특허 등록 가능성 검토 게시판
    제목, 신청자이름, 개인/기업, 이메일, 비번, 키워드, 내용, 첨부파일
    """

    class PositionChoices(models.TextChoices):
        Personal = "Personal"  # 개인
        Business = "Business"  # 기업

    # 제목
    title = models.CharField(
        max_length=50,
        blank=False,
    )

    # 신청자 이름
    name = models.CharField(
        max_length=10,
        blank=False,
    )

    # 개인 or 기업
    position = models.CharField(
        max_length=20,
        blank=False,
        choices=PositionChoices.choices,
    )

    # 신청자 이메일
    email = models.EmailField(
        max_length=50,
        blank=False,
    )

    # 신청 시 간단한 비밀번호
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

    # 특허 키워드 (발명의 명칭)
    keywords = TaggableManager(
        blank=False,
        verbose_name="keywords",
    )

    # 특허 내용(최대한 자세히 서술하기)
    description = models.TextField(max_length=300, blank=False)

    # 첨부파일
    file = models.FileField(upload_to="possible/", blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

        # 키워드 소문자로 변환
        for keyword in self.keywords.all():
            if keyword.name.lower() != keyword.name:
                self.keywords.remove(keyword.name)
                self.keywords.add(keyword.name.lower())
                
    def get_keywords(self):
        return ", ".join([key.name for key in self.keywords.all()])

    def __str__(self):
        return self.title
