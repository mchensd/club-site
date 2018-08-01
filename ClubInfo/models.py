from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
# Create your models here.



class Profile(models.Model):
    # create a user first, then the profile will be created and can be edited
    # reverse also works: create profile, set p.user to some user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fake_col = models.CharField(max_length=128)
    full_name = models.CharField(max_length=128, default="")
    email_confirmed = models.BooleanField(default = False)
    
    @staticmethod
    def create_member():
        username = input("Username: ")
        first_name = input("First name: ")
        last_name = input("Last name: ")
        email = input("Email: ")
        password = input("Password: ")
        conf = input("Confirm password: ")
        while (password != conf):
            password = input("Password: ")
            conf = input("Confirm password: ")
        fake_col = input("Fake col: ")
        user = User(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        user.save()
        user.profile.fake_col = fake_col
        user.profile.gen_full_name()

    def gen_full_name(self):
        self.full_name = "{} {}".format(self.user.first_name, self.user.last_name).strip()
        self.save() # save when modifying

    def get_total_score(self):
        ret = 0
        for score in self.user.score_set.all():
            ret += score.score
        return ret

    def __str__(self):
        return "{}".format(self.user.username)

class Announcement(models.Model):
    def __str__(self):
        return self.title
    # print('ASDFASDFADSFADFADFADFADF ' + str(User.objects.filter(is_staff=True)[0].pk))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=User.objects.filter(is_staff=True)[0].pk)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=512)

class Comment(models.Model):
    class Meta:
        ordering = ['date']
    def __str__(self):
        return self.author.first_name + " " + self.author.last_name + " at " + str(self.date)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=User.objects.filter(is_staff=True)[0].pk)
    date = models.DateTimeField('date published', default=timezone.now)
    text = models.CharField(max_length=256)
    announcement = models.ForeignKey(Announcement,on_delete=models.CASCADE)

class Contest(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField('Date Taken', default=timezone.now)
    official = models.BooleanField(default=False)
    out_of = models.IntegerField(default=5)

    def __str__(self):
        return self.name

class Score(models.Model):
    # lets us use one contest, but multiple scores for each contest
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    taker = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return "{} {} {}".format(self.taker.username, self.contest.name, self.score)


# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
# https://coderwall.com/p/ktdb3g/django-signals-an-extremely-simplified-explanation-for-beginners -- signals
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()