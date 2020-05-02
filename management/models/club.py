from django.db import models
from django.utils import timezone

# TODO Examination part of club
# TODO Communicate part (include display some news)
# TODO activities of club

STATUS_OF_CLUB = [
    ("sh", "审核中"),
    ("dj", "冻结"),
    ("cx", "撤销"),
    ("zc", "正常")
]

CATEGORY_OF_CLUB = [
    ("wyty", "文娱体育"),
    ("whzh", "文化综合"),
    ("gysj", "公益实践"),
    ("xsll", "学术理论"),
]


class Club(models.Model):
    # Status of a club
    name = models.CharField(verbose_name="社团名称", max_length=15)
    club_category = models.CharField(choices=CATEGORY_OF_CLUB, verbose_name="社团类别", max_length=4)
    create_time = models.DateField(verbose_name="成立时间")
    running_year = models.IntegerField(verbose_name="运行年份", default=timezone.now().year)
    description = models.CharField(verbose_name="社团描述", max_length=50)
    purpose = models.CharField(verbose_name="社团宗旨", max_length=50)
    icon = models.ImageField(verbose_name="社团图标")
    last_modify = models.DateTimeField(verbose_name="上次修改时间", auto_now=True)

    is_active = models.BooleanField(default=True)
    club_status = models.CharField(choices=STATUS_OF_CLUB, verbose_name="社团状态", max_length=2)

    def check_status_of_club(self):
        if self.club_status == "cx":
            self.is_active = False

    # @staticmethod
    # def get_student_number_of_club(, club):
    #     # todo error! Student is not wrong, at present I didn't use Student model
    #     return Student.object.filter(particular_year=particular_year, club=club).count()

    def __str__(self):
        return self.name
