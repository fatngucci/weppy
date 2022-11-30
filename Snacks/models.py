from django.db import models
from django.conf import settings

# Create your models here.
class Snack(models.Model):
    name = models.CharField(max_length=50) # z.B. Chilli Chips Extra Hot
    gewicht = models.IntegerField() # z.B. 400g
    beschreibung = models.CharField(max_length=1000, blank=True) # zutaten usw.
    pictures = models.ImageField(upload_to='snack_pictures/', blank=True, null=True)
    artikelnummer = models.CharField(max_length=100)
    hersteller = models.ForeignKey(settings.AUTH_USER_MODEL, # Private User, Firma, usw. muss eigenes Profil haben
                                   on_delete=models.CASCADE,
                                   related_name='Hersteller',
                                   related_query_name='Hersteller'
                                   )
    preis = models.FloatField() # in € z.B. 2.50 €
    erstellungs_zeitstempel = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['erstellungs_zeitstempel', 'name']
        verbose_name = 'Snacks'
        verbose_name_plural = 'Snacks'

    def __str__(self):
        return self.name + ' / ' + str(self.gewicht) + ' / ' + str(self.preis)

    def __repr__(self):
        return self.name + ' / ' + self.artikelnummer + ' / ' + self.hersteller


# Rezensionen
class Comment(models.Model):
    text = models.TextField(max_length=500)
    poster = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='Poster',
                               related_query_name='Posters'
                               )
    timestamp = models.DateTimeField(auto_now_add=True)
    snack = models.ForeignKey(Snack, on_delete=models.CASCADE)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def get_comment_prefix(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

    def __str__(self):
        return self.get_comment_prefix() + ' (' + self.poster.username + ')'

    def __repr__(self):
        return self.get_comment_prefix() + ' (' + self.poster.username + ' / ' + str(self.timestamp) + ')'

    def get_upvotes(self):
        upvotes = Vote.objects.filter(up_or_down='U',
                                      comment=self)
        return upvotes

    def get_upvotes_count(self):
        return len(self.get_upvotes())

    def get_downvotes(self):
        downvotes = Vote.objects.filter(up_or_down='D',
                                        comment=self)
        return downvotes

    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def vote(self, user, up_or_down):
        vote = Vote.objects.filter(voter=user,
                                   comment=self
                                   )
        if(vote):
            up_or_down_before = vote.last().get_up_or_down_display()
            vote.delete()
            if up_or_down_before == up_or_down:
                return

        U_or_D = 'U'
        if up_or_down == 'down':
            U_or_D = 'D'
        vote = Vote.objects.create(up_or_down=U_or_D,
                                   voter=user,
                                   comment=self
                                   )

# Vote
class Vote(models.Model):
    VOTE_TYPES = [
        ('U', 'up'),
        ('D', 'down'),
    ]

    up_or_down = models.CharField(max_length=1,
                                  choices=VOTE_TYPES,
                                  )
    timestamp = models.DateTimeField(auto_now_add=True)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='Voter',
                              related_query_name='Voters'
                              )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.up_or_down + ' on ' + self.comment.__str__() + ' by ' + self.voter.username

