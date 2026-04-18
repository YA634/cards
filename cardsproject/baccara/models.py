from django.db import models
from django.conf import settings
# Create your models here.

WINNER = (
    ('banker', 'バンカー'),
    ('player', 'プレイヤー'),
    ('tie', '引き分け')
)

# class Item(models.Model):
#     consecutive_count = models.IntegerField(default=1, verbose_name='連勝回数')

# class ItemList(models.Model):
#     winner = models.CharField(
#         max_length=10,
#         choices=WINNER
#     )
#     items = models.ManyToManyField(Item, related_name='lists')

class RoadMap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='baccara_roadmaps')
    winner = models.CharField(max_length=10, choices=WINNER, verbose_name='勝者')
    consecutive_count = models.IntegerField(default=1, verbose_name='連勝回数')
    tie_positions = models.JSONField(default=list, verbose_name='引き分けの位置') 
    column_position = models.IntegerField(verbose_name='列の位置')
    
    class Meta:
        ordering = ['column_position']
        # verbose_name = '罫線'
        # verbose_name_plural = '罫線'
