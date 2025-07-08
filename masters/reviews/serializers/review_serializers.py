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
                logger.warning("Validation error: '%s' field is missing", field)
                raise serializers.ValidationError("Zəhmət olmasa bütün məcburi sahələri doldurun.")

        if not data.get('comment'):
            logger.warning("Validation error: 'comment' is required")
            raise serializers.ValidationError('Rəy mətni tələb olunur')
        
        rating = data.get('rating')
        if rating < 0 or rating > 5:
            logger.warning("Validation error: rating (%s) is out of bounds", rating)
            raise serializers.ValidationError('1-5 arasında olmalıdır')
        
        username = data.get('username')
        if username and len(username) > 20:
            logger.warning("Validation error: username too long (%s)", username)
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
            logger.warning("Validation error: no rating tags selected")
            raise serializers.ValidationError("Zəhmət olmasa ən azı bir etiket seçin.")

        filled = [field for field in rating_fields if field is not None]

        if len(filled) > 5:
            logger.warning("Validation error: more than 5 rating tags selected")
            raise serializers.ValidationError('Ən çox 5 sahəyə dəyər verə bilərsiniz.')

        logger.debug("Validation passed")
        return data

    def validate_review_images(self, value):
        logger.debug("Validating uploaded images")
        for img in value:
            if img.size > 5 * 1024 * 1024:  
                logger.warning("Image too large: %s bytes", img.size)
                raise serializers.ValidationError('Hər şəkil 5 MB-dan böyük ola bilməz.')
            
        if len(value) > 3:
            logger.warning("Too many images uploaded: %d", len(value))
            raise serializers.ValidationError('Maksimum 3 şəkil yükləyə bilərsiniz')

        logger.debug("Images validated successfully")
        return value
    
    def update(self, instance, validated_data):
        logger.info("Updating review ID %s", instance.id)
        review_images = validated_data.pop('review_images', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        logger.debug("Updated fields: %s", validated_data)

        if review_images is not None:
            logger.debug("Updating images for review ID %s", instance.id)
            instance.images.all().delete()
            for idx, image in enumerate(review_images):
                ReviewWorkImage.objects.create(review=instance, image=image, order=idx)
                logger.debug("Created ReviewWorkImage idx=%s", idx)

        logger.info("Review ID %s updated successfully", instance.id)
        return instance

    def create(self, validated_data):
        master = self.context['master']
        logger.info("Creating review for master ID %s", master.id)
        review_images = validated_data.pop('review_images', [])

        review = Review.objects.create(master=master, **validated_data)
        logger.debug("Review created with ID %s", review.id)

        for idx, image in enumerate(review_images):
            ReviewWorkImage.objects.create(review=review, image=image, order=idx)
            logger.debug("Created ReviewWorkImage idx=%s", idx)

        logger.info("Review with ID %s created successfully", review.id)
        return review
