from django.test import TestCase

from rango.models import Category


class CategoryMethodTests(TestCase):
    # def test_ensure_views_are_positive(self):
    #     """
    #     ensure_views_are_positive 函数在分类的查看次数
    #     为零或正数时应该返回 True
    #     """
    #     cat = Category(name='test', views=-1, likes=0)
    #     cat.save()
    #     self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        slug_line_creation 确保添加分类时创建的别名格式是正确的
        例如 "Random Category String" -> "random-category-string"
        """
        cat = Category('Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')
