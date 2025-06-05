from django.core.validators import RegexValidator



# Azərbaycan dilində hərf validatoru (Ad və soyad üçün)
az_letter_validator = RegexValidator(
    regex=r'^[A-Za-zƏəÖöĞğÜüÇçŞşİı ]+$',
    message="Yalnız Azərbaycan hərfləri ilə yazılmalıdır."
)

# Mobil nömrə validatoru
phone_validator = RegexValidator(
    regex=r'^\+994(50|51|55|70|77|99)[0-9]{7}$',
    message="Mobil nömrə düzgün daxil edilməyib. 50 123 45 67 formatında daxil edin."
)
