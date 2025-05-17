from django.db import models
import uuid

class Patient(models.Model):
    code = models.CharField(max_length=32, unique=True)  # 匿名 ID
    name = models.CharField(max_length=64, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    insurance_number = models.CharField(max_length=20, verbose_name="保険者番号", blank=True)
    first_visit_date = models.DateField(verbose_name="初診日", null=True, blank=True)
    admission_date = models.DateField(verbose_name="入院日", null=True, blank=True)

    def __str__(self):
        return self.code

class VitalSigns(models.Model):
    patient   = models.ForeignKey(Patient, on_delete=models.CASCADE)
    measured  = models.DateTimeField(verbose_name="測定日時")
    celsius   = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="体温(℃)")
    pulse     = models.PositiveSmallIntegerField(verbose_name="脈拍(回/分)", null=True, blank=True)
    systolic  = models.PositiveSmallIntegerField(verbose_name="収縮期血圧(mmHg)", null=True, blank=True)
    diastolic = models.PositiveSmallIntegerField(verbose_name="拡張期血圧(mmHg)", null=True, blank=True)
    weight    = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="体重(kg)", null=True, blank=True)

    class Meta:
        ordering = ["measured"]
        verbose_name = "バイタルサイン"
        verbose_name_plural = "バイタルサイン"