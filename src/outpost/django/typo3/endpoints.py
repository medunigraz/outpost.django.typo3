from . import api

v1 = [
    (r"typo3/language", api.LanguageViewSet, "typo3-language"),
    (r"typo3/category", api.CategoryViewSet, "typo3-category"),
    (r"typo3/calendar", api.CalendarViewSet, "typo3-calendar"),
    (r"typo3/eventcategory", api.EventCategoryViewSet, "typo3-eventcategory"),
    (r"typo3/event", api.EventViewSet, "typo3-event"),
    (r"typo3/search/event", api.EventSearchViewSet, "typo3-event-search"),
    (r"typo3/news", api.NewsViewSet, "typo3-news"),
    (r"typo3/search/news", api.NewsSearchViewSet, "typo3-news-search"),
]
