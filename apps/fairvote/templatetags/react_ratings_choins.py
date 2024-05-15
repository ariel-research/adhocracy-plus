import json

from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html

from adhocracy4.ratings import models as rating_models

register = template.Library()


@register.simple_tag(takes_context=True)
def react_ratings_choins(context, obj):
    request = context["request"]
    user = request.user
    contenttype = ContentType.objects.get_for_model(obj)
    # permission = "a4ratings.rate_idea".format(ct=contenttype)
    has_rate_permission = True

    would_have_rate_permission = True

    if user.is_authenticated:
        authenticated_as = user.username
    else:
        authenticated_as = None
    user_rating = rating_models.Rating.objects.filter(
        content_type=contenttype, object_pk=obj.pk, creator=user.pk
    ).first()
    if user_rating:
        user_rating_value = user_rating.value
        user_rating_id = user_rating.pk
    else:
        user_rating_value = None
        user_rating_id = -1

    attributes = {
        "contentType": contenttype.pk,
        "objectId": obj.pk,
        "ideaStatus": obj.moderator_status,
        "authenticatedAs": authenticated_as,
        "positiveRatings": obj.positive_rating_count,
        "negativeRatings": obj.negative_rating_count,
        "userRating": user_rating_value,
        "userRatingId": user_rating_id,
        "isReadOnly": (not has_rate_permission and not would_have_rate_permission),
        "style": "ideas",
    }

    return format_html(
        '<div data-aplus-widget="ratings" data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )