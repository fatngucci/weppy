from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


# Create your models here.
class Snack(models.Model):
    name = models.CharField(max_length=50)  # z.B. Chilli Chips Extra Hot
    gewicht = models.IntegerField()  # z.B. 400g
    beschreibung = models.CharField(max_length=1000, blank=True)  # zutaten usw.
    bilder = models.ImageField(upload_to='snack_pictures/', blank=True, null=True,
                               default='snack_pictures/white-background-2.jpg')
    produkt_info = models.FileField(upload_to='uploaded_files/', blank=True, null=True,
                                    default='uploaded_files/empty.pdf')
    artikelnummer = models.CharField(max_length=100)
    hersteller = models.ForeignKey(settings.AUTH_USER_MODEL,  # Private User, Firma, usw. muss eigenes Profil haben
                                   on_delete=models.CASCADE,
                                   related_name='Hersteller',
                                   related_query_name='Hersteller'
                                   )
    preis = models.DecimalField(decimal_places=2, max_digits=10)  # in € z.B. 2.50 €
    erstellungs_zeitstempel = models.DateTimeField(auto_now_add=True)
    #produkt_bewertung = models.DecimalField(decimal_places=1, max_digits=10, default=0)  # pass auf!
    produkt_bewertung = models.FloatField(default=0)

    class Meta:
        ordering = ['erstellungs_zeitstempel', 'name']
        verbose_name = 'Snacks'
        verbose_name_plural = 'Snacks'

    def __str__(self):
        return self.name + ' / ' + str(self.gewicht) + ' / ' + str(self.preis)

    def __repr__(self):
        return self.name + ' / ' + self.artikelnummer + ' / ' + self.hersteller

    def get_bewertung(self):
        comments = Comment.objects.filter(snack=self)
        bewertung = 0
        if comments:
            for c in comments:
                bewertung += float(c.sternbewertung)
            bewertung = bewertung / len(comments)

        self.produkt_bewertung = round(bewertung,1)
        self.save()
        return self.produkt_bewertung


# Rezensionen
class Comment(models.Model):
    STERN_BEWERTUNG = [tuple([x, x]) for x in range(0, 6)]
    text = models.TextField(max_length=500)
    sternbewertung = models.IntegerField(choices=STERN_BEWERTUNG, default=5)
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

    def get_reports_count(self):
        reports = Report.objects.filter(comment=self)
        return len(reports)

    def get_sterne(self):
        list = []
        for x in range(self.sternbewertung):
            list.append(True)

        for y in range(5 - self.sternbewertung):
            list.append(False)
        return list

    def vote(self, user, up_or_down):
        vote = Vote.objects.filter(voter=user,
                                   comment=self
                                   )
        if vote:
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

    def report(self, user):
        report = Report.objects.filter(subject=user,
                                       comment=self)
        if report:
            # already reported
            return

        report = Report.objects.create(subject=user,
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


class Report(models.Model):
    subject = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='Subject',
                                related_query_name='Subjects'
                                )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment.get_comment_prefix() + ' / reported by ' + self.subject.username + ' on ' + str(
            self.timestamp)

    # Sources
    # https://stackoverflow.com/questions/42425933/how-do-i-set-a-default-max-and-min-value-for-an-integerfield-django
