from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import re


def photo_path1(instance, filename):
    from time import gmtime, strftime
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    # return '{}/{}/{}.{}'.format(strftime('post/%Y/%m/%d/'), instance.author.username, pid, extension)
    return '{}/{}.{}'.format(strftime('post/'), pid, extension)

def photo_path2(instance, filename):
    from time import gmtime, strftime
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return '{}/{}.{}'.format(strftime('result/'), pid, extension)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    photo = ProcessedImageField(upload_to=photo_path1,
                                options={'quality': 90})
    content = models.CharField(max_length=140, help_text="최대 140자 입력 가능")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag_set = models.ManyToManyField('Tag', blank=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,
                                           related_name='like_user_set',
                                           through='Like')  # post.like_set 으로 접근 가능

    class Meta:
        ordering = ['-created_at']  # 정렬해줌

    # NOTE: content에서 tags를 추출하여, Tag 객체 가져오기, 신규 태그는 Tag instance 생성, 본인의 tag_set에 등록,
    def tag_save(self):
        tags = re.findall(r'#(\w+)\b', self.content)

        if not tags:
            return

        for t in tags:
            tag, tag_created = Tag.objects.get_or_create(name=t)
            self.tag_set.add(tag)  # NOTE: ManyToManyField 에 인스턴스 추가

    @property
    def like_count(self):
        return self.like_user_set.count()

    def __str__(self):
        return self.content


class Tag(models.Model):
    name = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.name

class Learning_Result(models.Model):
    author_id = models.IntegerField()
    user_id = models.IntegerField()
    result_img = ProcessedImageField(upload_to=photo_path2,
                                     options={'quality': 90})
    def __str__(self):
        return self.user_id

class Photo_Labeling(models.Model):
    post_id = models.IntegerField()
    post_label = models.CharField(max_length=255)

    def __str__(self):
        return self.post_id

class Google_Result(models.Model):
    author_id = models.IntegerField()
    user_id = models.IntegerField()
    google_img = models.CharField(max_length=255)
    google_src = models.CharField(max_length=510)
    def __str__(self):
        return self.user_id

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ( # user와 post 변수가 유일한 값을 갖도록 unique 속성을 추가
            ('user', 'post')
        )

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    content = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']  # 정렬해줌

    def __str__(self):
        return self.content

class link(models.Model):
    name = models.CharField(max_length=255)
    photo = ProcessedImageField(upload_to='')
    price = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    site = models.CharField(max_length=255, default='')

    class Meta:
        ordering = ['-id']