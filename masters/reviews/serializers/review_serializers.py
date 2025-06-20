from rest_framework import serializers
from django.core.validators import FileExtensionValidator

from reviews.models.review_models import Review
from reviews.models.review_img_model import ReviewWorkImage
from .review_img_serializer import ReviewImageSerializer


class ReviewSerializer(serializers.ModelSerializer):
    review_images = serializers.ListField(
        child=serializers.ImageField(
            validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])]
        ),
        max_length=3,
        required=False,
        allow_null=True,
        write_only=True
    )
    master = serializers.PrimaryKeyRelatedField(read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Review
        exclude = ['user']

    def validate(self, data):
        required_fields = ['comment', 'rating']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError("Zəhmət olmasa bütün məcburi sahələri doldurun.")

        if not data.get('comment'):
            raise serializers.ValidationError('Rəy mətni tələb olunur')
        
        rating = data.get('rating')
        if rating < 0 or rating > 5:
            raise serializers.ValidationError('1-5 arasında olmalıdır')
        
        username = data.get('username')
        if username and len(username) > 20:
            raise serializers.ValidationError('Max 20 simvol daxil edə bilərsiz')

        return data
    
    def validate_count_of_label(self, data):
        rated_fields = [
        'responsible', 'neat', 'time_management', 'communicative', 'punctual',
        'professional', 'experienced', 'efficient', 'agile', 'patient'
    ]
        filled = [field for field in rated_fields if data.get(field) is not None]

        if len(filled) > 5:
            raise serializers.ValidationError('Ən çox 5 sahəyə dəyər verə bilərsiniz.')
        
        return data

    def validate_review_images(self, value):
        for img in value:
            if img.size > 5 * 1024 * 1024:  
                raise serializers.ValidationError('Hər şəkil 5 MB-dan böyük ola bilməz.')
            
        if len(value) > 3:
            raise serializers.ValidationError('Maksimum 3 şəkil yükləyə bilərsiniz')

        return value
    
    def update(self, instance, validated_data):
        review_images = validated_data.pop('review_images', None)

     
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if review_images is not None:
            instance.images.all().delete()
            for idx, image in enumerate(review_images):
                ReviewWorkImage.objects.create(review=instance, image=image, order=idx)

        return instance
        
    def create(self, validated_data):
        user = self.context['user']  # burada user instance olmalıdır (CustomUser obj)
        master = self.context['master']
        review_images = validated_data.pop('review_images', [])

        review = Review.objects.create(user=user, master=master, **validated_data)

        for idx, image in enumerate(review_images):
            ReviewWorkImage.objects.create(review=review, image=image, order=idx)

        return review
        