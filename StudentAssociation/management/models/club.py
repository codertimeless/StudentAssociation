from ..models.student import Student
from ..management.models.unit import Unit
from ..models.teacher import Teacher

from django.db import models


# TODO Examination part of club
# TODO Communicate part (include display some news)
# TODO activities of club

STATUS_OF_CLUB = [
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
    club_status = models.CharField(choices=STATUS_OF_CLUB, verbose_name="社团状态", max_length=2)
    club_category = models.CharField(choices=CATEGORY_OF_CLUB, verbose_name="社团类别", max_length=4)
    create_time = models.DateField(verbose_name="成立时间")
    particular_year = models.CharField(verbose_name="运行年份", max_length=4)
    description = models.CharField(verbose_name="社团描述", max_length=50)
    purpose = models.CharField(verbose_name="社团宗旨", max_length=50)
    icon = models.ImageField(verbose_name="社团图标")

    # People in club
    president = models.ForeignKey(Student, on_delete=models.DO_NOTHING, verbose_name="会长", related_name="president")
    vice_president1 = models.ForeignKey(Student, on_delete=models.DO_NOTHING, verbose_name="副会长", related_name="vicePresident")
    vice_president2 = models.ForeignKey(Student, on_delete=models.DO_NOTHING, verbose_name="副会长2",
                                        related_name="vicePresident2", blank=True, null=True)
    vice_president3 = models.ForeignKey(Student, on_delete=models.DO_NOTHING, verbose_name="副会长3",
                                        related_name="vicePresident3", blank=True, null=True)

    affiliated_units = models.ForeignKey(Unit, on_delete=models.DO_NOTHING, verbose_name="挂靠单位")
    affiliated_units2 = models.ForeignKey(Unit, on_delete=models.DO_NOTHING, verbose_name="挂靠单位2",
                                          blank=True, null=True)

    guidance_teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, verbose_name="指导老师",
                                         blank=True, null=True)
    guidance_teacher2 = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, verbose_name="指导老师2",
                                          blank=True, null=True)

    def get_particular_year_count(self, particular_year, club):
        return Student.object.filter(particular_year=particular_year, club=club).count()

    def __str__(self):
        return self.name
