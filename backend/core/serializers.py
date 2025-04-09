from rest_framework import serializers
from django.conf import settings
from .models import (
    Nav,
    Slider,
    Logo,
    IntroductionService,
    BeforeAndAfter,
    WhoWeAre,
    AllService,
    TestimonyPatients,
    InfoPlans,
    DetailPlans,
)


class BaseImageSerializer(serializers.ModelSerializer):
    def get_image_url(self, obj, image_field):
        """
        Retorna la URL completa de una imagen.
        """
        if hasattr(obj, image_field) and getattr(obj, image_field):
            request = self.context.get("request")
            image = getattr(obj, image_field)
            return (
                request.build_absolute_uri(image.url)
                if request
                else f"{settings.MEDIA_URL}{image.url}"
            )
        return None  # Si no hay imagen


class LogoSerializers(BaseImageSerializer):

    class Meta:
        model = Logo
        fields = [
            "id",
            "logo",
            "description",
            "text_alt",
        ]

    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        return self.get_image_url(obj, "logo")


class NavSerializers(serializers.ModelSerializer):

    
    class Meta:
        model = Nav
        fields = [
            "id",
            "name_es",
            "name_en",
            "url",
        ]

    name_es = serializers.SerializerMethodField()

    def get_name_es(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.name_en if language == 'en' else obj.name_es
    


class SliderSerializers(BaseImageSerializer):

    class Meta:
        model = Slider
        fields = [
            "id",
            "slider",
            "title_es",
            "description_es",
            "title_en",
            "description_en",
            "text_alt",
        ]

    slider = serializers.SerializerMethodField()
    title_es = serializers.SerializerMethodField()
    description_es = serializers.SerializerMethodField()

    def get_slider(self, obj):
        return self.get_image_url(obj, "slider")  # 🔥 Reutiliza la función base
    
    def get_title_es(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.title_en if language == 'en' else obj.title_es
    
    def get_description_es(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.description_en if language == 'en' else obj.description_es


class IntroductionServiceSerializers(BaseImageSerializer):

    class Meta:
        model = IntroductionService
        fields = [
            "id",
            "image",
            "title_es",
            "description_es",
            "title_en",
            "description_en",
            "text_alt",
        ]

    image = serializers.SerializerMethodField()
    title_es = serializers.SerializerMethodField()
    description_es = serializers.SerializerMethodField()

    def get_image(self, obj):
        return self.get_image_url(obj, "image")
    
    def get_title_es(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.title_en if language == 'en' else obj.title_es
    
    def get_description_es(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.description_en if language == 'en' else obj.description_es


class BeforeAndAfterSerializers(BaseImageSerializer):
    class Meta:
        model = BeforeAndAfter
        fields = [
            "id",
            'title_es',
            "image",
            "description_es",
            "title_en",
            "description_en",
            "text_alt",
        ]

    image = serializers.SerializerMethodField()
    title_es = serializers.SerializerMethodField()
    description_es = serializers.SerializerMethodField()

    def get_image(self, obj):
        return self.get_image_url(obj, "image")
    
    def get_title_es(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.title_en if language == 'en' else obj.title_es
    
    def get_description_es(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.description_en if language == 'en' else obj.description_es


class WhoWeAreSerializers(serializers.ModelSerializer):
    class Meta:
        model = WhoWeAre
        fields = [
            "id",
            "title_es",
            "description_es",
            "title_en",
            "description_en",
        ]

    title_es = serializers.SerializerMethodField()
    description_es = serializers.SerializerMethodField()

    def get_title_es(self, obj):
        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.title_en if language == 'en' else obj.title_es
    
    def get_description_es(self, obj):
        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.description_en if language == 'en' else obj.description_es


class AllServiceSerializers(BaseImageSerializer):

    class Meta:
        model = AllService
        fields = [
            "id",
            "image",
            "title_es",
            "description_es",
            "title_en",
            "description_en",
            "text_alt",
        ]

    image = serializers.SerializerMethodField()
    title_es = serializers.SerializerMethodField()
    description_es = serializers.SerializerMethodField()

    def get_image(self, obj):
        return self.get_image_url(obj, "image")  # 🔥 Reutiliza la función base

    def get_title_es(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.name_en if language == 'en' else obj.title_es
    
    def get_description_es(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.description_en if language == 'en' else obj.description_es

class TestimonyPatientsSerializers(BaseImageSerializer):

    class Meta:
        model = TestimonyPatients
        fields = [
            "id",
            "title_es",
            "description_es",
            "title_en",
            "description_en",
        ]


    title_es = serializers.SerializerMethodField()
    description_en = serializers.SerializerMethodField()

    def get_title_es(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.title_en if language == 'en' else obj.title_es
    
    def get_description_en(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.description_en if language == 'en' else obj.description_es



class InfoPlansSerializers(BaseImageSerializer):

    class Meta:
        model = InfoPlans
        fields = [
            "id",
            "image",
            "title_es",
            "title_en",
            "price",
            "text_alt",
        ]

    image = serializers.SerializerMethodField()
    title_es = serializers.SerializerMethodField()

    def get_image(self, obj):
        return self.get_image_url(obj, "image")  # 🔥 Reutiliza la función base
    
    def get_title_es(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.title_en if language == 'en' else obj.title_es


class DetailPlansSerializers(serializers.ModelSerializer):
    class Meta:
        model = DetailPlans
        fields = [
            "id",
            "detail_es",
            "detail_en",
        ]

    detail_es = serializers.SerializerMethodField()

    def detail_es(self, obj):

        # Obtiene el idioma del contexto
        language = self.context.get('language', 'es')  # Por defecto, español
        return obj.detail_en if language == 'en' else obj.detail_es
