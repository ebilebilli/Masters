from django.db import models
from django.core.validators import(
    MinValueValidator, 
    MaxValueValidator, 
    MaxLengthValidator, 
    MinLengthValidator
    )

from utils.validators import az_letters_validator, not_only_whitespace


class Review(models.Model):
    # user =  models.ForeignKey(       # real customer user will add in product level
    #     'users.CustomUser', 
    #     on_delete=models.CASCADE, 
    #     related_name='comments'
    #     )
    master = models.ForeignKey(
        'users.CustomUser', 
        on_delete=models.CASCADE, 
        related_name='reviews'
        ) 
    username = models.CharField(
        max_length=20,
        validators=[az_letters_validator],
        default='Anonim hesab'
        )

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(5)]
    )
    comment = models.TextField(
        max_length=1000,
        validators=[
            az_letters_validator, 
            not_only_whitespace,
            MinLengthValidator(3),
            MaxLengthValidator(1000),
        ]
    )
    
    experienced = models.BooleanField(default=False, verbose_name="Təcrübəli")
    professional = models.BooleanField(default=False, verbose_name="Peşəkar")
    patient = models.BooleanField(default=False, verbose_name="Səbirli")
    punctual = models.BooleanField(default=False, verbose_name="Dəqiq")
    responsible = models.BooleanField(default=False, verbose_name="Məsuliyyətli")
    neat = models.BooleanField(default=False, verbose_name="Səliqəli")
    time_management = models.BooleanField(default=False, verbose_name="Vaxta nəzarət")
    communicative = models.BooleanField(default=False, verbose_name="Ünsiyyətcil")
    efficient = models.BooleanField(default=False, verbose_name="Səmərəli")
    agile = models.BooleanField(default=False, verbose_name="Çevik")

    @property
    def tag_list(self):
        tags = {
            "Təcrübəli": self.experienced,
            "Peşəkar": self.professional,
            "Səbirli": self.patient,
            "Dəqiq": self.punctual,
            "Məsuliyyətli": self.responsible,
            "Səliqəli": self.neat,
            "Vaxta nəzarət": self.time_management,
            "Ünsiyyətcil": self.communicative,
            "Səmərəli": self.efficient,
            "Çevik": self.agile,
        }
        return [name for name, value in tags.items() if value]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     unique_together = ('master', 'user')

