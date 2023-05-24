from rest_framework.exceptions import ValidationError

from social_app.settings import REST_FRAMEWORK


def validate_pagination(request):
    """
    This function is created for validate limit and offset.
    """
    offset = request.GET.get("page")
    if offset:
        try:
            int(offset)
        except:
            raise ValidationError({"error": "Please pass integer value for size/page."})
    limit = request.GET.get("size")
    if limit:
        try:
            int(limit)
        except:
            raise ValidationError({"error": "Please pass integer value for size/page."})
    if offset is None:
        offset = 1
    if limit is None:
        limit = REST_FRAMEWORK.get("PAGE_SIZE")
    offset = (int(offset) - 1) * int(limit)
    limit = int(offset) + int(limit)
    return limit, offset
