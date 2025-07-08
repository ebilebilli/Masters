import logging
from rest_framework import serializers
from django.core.validators import FileExtensionValidator

from reviews.models.review_models import Review
from reviews.models.review_img_model import ReviewWorkImage
from .review_img_serializer import ReviewImageSerializer


logger = logging.getLogger(__name__)

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
        fields = '__all__'

    def validate(self, data):
        logger.debug("Validating review data: %s", data)
        required_fields = ['comment', 'rating']
        for field in required_fields:
            if not data.get(field):
                logger.warning("Required field %s is missing", field)
                raise serializers.ValidationError("Zəhmət olmasa bütün məcburi sahələri doldurun.")

        if not data.get('comment'):
            logger.warning("Comment field is missing")
            raise serializers.ValidationError('Rəy mətni tələb olunur')
        
        rating = data.get('rating')
        if rating < 0 or rating > 5:
            logger.warning("Rating value is out of bounds: %s", rating)
            raise serializers.ValidationError('1-5 arasında olmalıdır')
        
        username = data.get('username')
        if username and len(username) > 20:
            logger.warning("Username too long: %s", username)
            raise serializers.ValidationError('Max 20 simvol daxil edə bilərsiz')
        
        rating_fields = [
            data.get('responsible'),
            data.get('neat'),
            data.get('time_management'),
            data.get('communicative'),
            data.get('punctual'),
            data.get('professional'),
            data.get('experienced'),
            data.get('efficient'),
            data.get('agile'),
            data.get('patient'),
        ]
        
        if all(value in [None, ''] for value in rating_fields):
            logger.warning("No rating tags provided")
            raise serializers.ValidationError("Zəhmət olmasa ən azı bir etiket seçin.")

        filled = [field for field in rating_fields if data.get(field) is not None]
        if len(filled) > 5:
            logger.warning("Too many rating fields filled: %d", len(filled))
            raise serializers.ValidationError('Ən çox 5 sahəyə dəyər verə bilərsiniz.')
        
        logger.debug("Validation successful")
        return data

    def validate_review_images(self, value):
        logger.debug("Validating review images, count: %d", len(value))
        for img in value:
            if img.size > 5 * 1024 * 1024:
                logger.warning("Image too large: %d bytes", img.size)
                raise serializers.ValidationError('Hər şəkil 5 MB-dan böyük ola bilməz.')

        if len(value) > 3:
            logger.warning("Too many images uploaded: %d", len(value))
            raise serializers.ValidationError('Maksimum 3 şəkil yükləyə bilərsiniz')

        return value

    def update(self, instance, validated_data):
        review_images = validated_data.pop('review_images', None)
        logger.info("Updating review id=%s with data: %s", instance.id, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if review_images is not None:
            logger.debug("Updating images for review id=%s", instance.id)
            instance.images.all().delete()
            for idx, image in enumerate(review_images):
                ReviewWorkImage.objects.create(review=instance, image=image, order=idx)

        return instance

    def create(self, validated_data):
        master = self.context['master']
        review_images = validated_data.pop('review_images', [])
        logger.info("Creating review for master=%s with data: %s", master.id, validated_data)

        review = Review.objects.create(master=master, **validated_data)

        for idx, image in enumerate(review_images):
            ReviewWorkImage.objects.create(review=review, image=image, order=idx)
            logger.debug("Image #%d created for review id=%s", idx, review.id)

        return review