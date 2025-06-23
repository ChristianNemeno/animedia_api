import django_filters
from .models import TradeItem

class TradeItemFilter(django_filters.FilterSet):
    created_at_min = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    created_at_max = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = TradeItem
        fields = ['status', 'owner', 'created_at_min', 'created_at_max','title']