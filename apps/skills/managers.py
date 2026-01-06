from django.db import models
from django.db.models import Q, Count, Avg


class SkillOfferQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
    def by_category(self, category_slug):
        return self.filter(category__slug=category_slug)
    
    def by_delivery(self, delivery_method):
        return self.filter(
            Q(delivery_method=delivery_method) | 
            Q(delivery_method='both')
        )
    
    def search(self, query):
        return self.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    def with_stats(self):
        from apps.reviews.models import Review
        return self.annotate(
            avg_rating=Avg('user__reviews_received__rating'),
            review_count=Count('user__reviews_received')
        )


class SkillOfferManager(models.Manager):
    def get_queryset(self):
        return SkillOfferQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def by_category(self, category_slug):
        return self.get_queryset().by_category(category_slug)
    
    def by_delivery(self, delivery_method):
        return self.get_queryset().by_delivery(delivery_method)
    
    def search(self, query):
        return self.get_queryset().search(query)


# Add to SkillOffer model:
# objects = SkillOfferManager()