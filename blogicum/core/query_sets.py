from blog.models import Post, Category
from django.utils import timezone


def post_query():
    """Вернуть результат запроса к таблице blog_post."""
    date_now = timezone.now()
    query_set = (
        Post.objects.select_related(
            "category",
            "location",
            "author",
        )
        .only(
            "title",
            "text",
            "pub_date",
            "author__username",
            "category__title",
            "category__slug",
            "location__name",
        )
        .filter(
            pub_date__lte=date_now,
            is_published=True,
            category__is_published=True,
        )
    )
    return query_set


def category_query():
    """Вернуть результат запроса к таблице blog_category."""
    query_set = Category.objects.values("title", "description").filter(
        is_published=True
    )
    return query_set
