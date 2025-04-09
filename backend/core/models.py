from django.db import models
from .helpers.translator_utils import Translator

# Create your models here.

class Logo(models.Model):

    logo = models.ImageField(upload_to='logo', verbose_name='Logo')
    description = models.CharField(max_length=100, verbose_name='Descripción')
    text_alt = models.CharField(max_length=100, verbose_name='Texto Alternativo')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Logo'
        verbose_name_plural = 'Logo'


    def __str__(self):
        return self.description
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()

class Nav(models.Model):
    name_es = models.CharField(max_length=100, verbose_name='Nombre Pagina')
    name_en  = models.CharField(max_length=100, blank=True, null=True, verbose_name='Page Name')
    url = models.CharField(max_length=150, verbose_name='URL')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Navegación'
        verbose_name_plural = 'Navegación'

    def __str__(self):
        return self.name_es
    
    def save(self, *args, **kwargs):
        # Traducir automáticamente si PageName está lleno y PageName_en está vacío
        if self.name_es and not self.name_en:
            translator = Translator()
            self.name_en = translator.translate(self.name_es)
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()


class Slider(models.Model):
    slider = models.ImageField(upload_to='slider', verbose_name='Slider')
    title_es = models.CharField(max_length=100, blank=True, null=True, verbose_name='Titulo')
    description_es = models.CharField(max_length=100, blank=True, null=True, verbose_name='Descripción')
    title_en = models.CharField(max_length=100,blank=True, null=True, verbose_name='Title')
    description_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='Description')
    text_alt = models.CharField(max_length=100, verbose_name='Texto Alternativo')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'Slider'

    def __str__(self):
        return self.title_es
    
    def save(self, *args, **kwargs):
        # Traducir automáticamente si PageName está lleno y PageName_en está vacío
        translator = Translator()
        if self.title_es and not self.title_en:
             self.title_en = translator.translate(self.title_es)

        if self.description_es and not self.description_en:
             self.description_en = translator.translate(self.description_es)    
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()

class IntroductionService(models.Model):

    image = models.ImageField(upload_to='introduction-services')
    title_es = models.CharField(max_length=100,blank=True, null=True, verbose_name='Titulo')
    description_es = models.CharField(max_length=100,blank=True, null=True, verbose_name='Descripción')
    title_en = models.CharField(max_length=100,blank=True, null=True, verbose_name='Title')
    description_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='Description')
    text_alt = models.CharField(max_length=100, verbose_name='Texto Alternativo')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Introducción Servicios'
        verbose_name_plural = 'Introducción Servicios'

    def __str__(self):
        return self.title_es
    
    def save(self, *args, **kwargs):
        # Traducir automáticamente si PageName está lleno y PageName_en está vacío
        translator = Translator()
        if self.title_es and not self.title_en:
             self.title_en = translator.translate(self.title_es)

        if self.description_es and not self.description_en:
             self.description_en = translator.translate(self.description_es) 
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()

class BeforeAndAfter(models.Model):

    image = models.ImageField(upload_to='before-after')
    title_es = models.CharField(max_length=100, blank=True, null=True, verbose_name='Titulo')
    description_es = models.CharField(max_length=100,blank=True, null=True, verbose_name='Descripción')
    title_en = models.CharField(max_length=100,blank=True, null=True, verbose_name='Title')
    description_en = models.CharField(max_length=100,blank=True, null=True, verbose_name='Description')
    text_alt = models.CharField(max_length=100, verbose_name='Texto Alternativo')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Antes y Despues'
        verbose_name_plural = 'Antes y Despues'

    def __str__(self):
        return self.title_es
    
    def save(self, *args, **kwargs):
        # Traducir automáticamente si PageName está lleno y PageName_en está vacío
        translator = Translator()
        if self.title_es and not self.title_en:
             self.title_en = translator.translate(self.title_es)

        if self.description_es and not self.description_en:
             self.description_en = translator.translate(self.description_es) 
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()

class WhoWeAre(models.Model):

    title_es = models.CharField(max_length=100, blank=True, null=True, verbose_name='Titulo')
    description_es = models.CharField(max_length=100, blank=True, null=True, verbose_name='Descripción')
    title_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='Title')
    description_en = models.CharField(max_length=100,blank=True, null=True, verbose_name='Description')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Quienes Somos'
        verbose_name_plural = 'Quienes Somos'

    def __str__(self):
        return self.title_es
    
    def save(self, *args, **kwargs):
        # Traducir automáticamente si PageName está lleno y PageName_en está vacío
        translator = Translator()
        if self.title_es and not self.title_en:
             self.title_en = translator.translate(self.title_es)

        if self.description_es and not self.description_en:
             self.description_en = translator.translate(self.description_es) 
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()

class AllService(models.Model):

    image = models.ImageField(upload_to='all-services')
    title_es = models.CharField(max_length=100, verbose_name='Titulo')
    description_es = models.CharField(max_length=100, verbose_name='Descripción')
    title_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='Title')
    description_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='Description')
    text_alt = models.CharField(max_length=100, verbose_name='Texto Alternativo')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Todos los Servicios'
        verbose_name_plural = 'Todos los servicios'

    def __str__(self):
        return self.title_es
    
    def save(self, *args, **kwargs):
        # Traducir automáticamente si PageName está lleno y PageName_en está vacío
        translator = Translator()
        if self.title_es and not self.title_en:
             self.title_en = translator.translate(self.title_es)

        if self.description_es and not self.description_en:
             self.description_en = translator.translate(self.description_es) 
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()

class TestimonyPatients(models.Model):

    title_es = models.CharField(max_length=100, verbose_name='Titulo')
    description_es = models.CharField(max_length=100, verbose_name='Descipción')
    title_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='Title')
    description_en = models.CharField(max_length=100,blank=True, null=True, verbose_name='Description')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Testimonios'
        verbose_name_plural = 'Testimonios'

    def __str__(self):
        return self.title_es
    
    def save(self, *args, **kwargs):
        # Traducir automáticamente si PageName está lleno y PageName_en está vacío
        translator = Translator()
        if self.title_es and not self.title_en:
             self.title_en = translator.translate(self.title_es)

        if self.description_es and not self.description_en:
             self.description_en = translator.translate(self.description_es) 
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()

class InfoPlans(models.Model):

    image = models.ImageField(upload_to='all-services')
    title_es = models.CharField(max_length=100, verbose_name='Titulo')
    title_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='Title')
    price = models.CharField(max_length=100, verbose_name='Precio')
    text_alt = models.CharField(max_length=100, verbose_name='Texto Alternativo')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Información Planes'
        verbose_name_plural = 'Información Planes'

    def __str__(self):
        return self.title_es
    
    def save(self, *args, **kwargs):
        # Traducir automáticamente si PageName está lleno y PageName_en está vacío
        translator = Translator()
        if self.title_es and not self.title_en:
             self.title_en = translator.translate(self.title_es)

        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()

class DetailPlans(models.Model):

    detail_es = models.CharField(max_length=100, verbose_name='Titulo')
    detail_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='Title')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Detalles Planes'
        verbose_name_plural = 'Detalles Planes'

    def __str__(self):
        return self.detail_es
    
    def save(self, *args, **kwargs):
        # Traducir automáticamente si PageName está lleno y PageName_en está vacío
        translator = Translator()
        if self.detail_es and not self.detail_en:
             self.detail_en = translator.translate(self.detail_es)

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()




    
    

