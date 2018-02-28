from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from blog.models import Post


post_detail_url = HyperlinkedIdentityField(
    view_name='blog-api:detail',
    lookup_field='slug'
)


class PostListSerializer(ModelSerializer):
    url = post_detail_url
    author = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'author',
            'title',
            'slug',
            'content',
            'meta_description',
            'keywords',
            'categories',
            'tags',
            'publish',
        ]

    def get_author(self, obj):
        return str(obj.author)


class PostDetailSerializer(ModelSerializer):
    author = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'slug',
            'content',
            'meta_description',
            'keywords',
            'categories',
            'tags',
            'publish',
        ]

    def get_author(self, obj):
        return str(obj.author)


class PostCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'meta_description',
            'keywords',
            'tags',
            'categories',
            'publish',
        ]
