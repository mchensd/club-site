import pytz
from .mylog import *
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from .forms import RegisterForm, AnnouncementForm, CommentForm, ModifyContestInfoForm, AddContestUserForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .models import Profile, Comment, Announcement, Contest, Score
from django.core.exceptions import PermissionDenied
from json import dumps, loads
from datetime import date, datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
# Create your views here.
class IndexView(generic.FormView, generic.ListView):
    #TODO: Pagination
    template_name="ClubInfo/index.html"
    context_object_name = "announcements"
    form_class = AnnouncementForm
    success_url = '/cca_programming'

    def get_queryset(self):
         return Announcement.objects.order_by('-pub_date')

    def form_valid(self, form):
        a = Announcement(title=form.cleaned_data['title'], text=form.cleaned_data['body'])
        a.save()
        return super(IndexView, self).form_valid(form)

class ProfileView(generic.DetailView):
    template_name = "ClubInfo/profiles.html"
    context_object_name = 'user'
    model = User


class AnnouncementView(generic.FormView, generic.DetailView):
    template_name = "ClubInfo/announcement.html"
    context_object_name = 'ann'
    form_class =CommentForm
    model=Announcement
    success_url = '/cca_programming/'

    def form_valid(self, form):
        c = Comment(announcement=Announcement.objects.get(pk=form.cleaned_data['ann_id']), text=form.cleaned_data['body'], author=self.request.user)
        c.save()
        return redirect('clubinfo:announcement', c.announcement.pk)
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def delete(request, ann_id):
    if not request.user.is_staff:
        raise PermissionDenied

    ann = get_object_or_404(Announcement, pk=ann_id)
    request.session['ann_undo_title'] = ann.title
    request.session['ann_undo_text'] = ann.text
    request.session['ann_undo_date'] = dumps(ann.pub_date, default=json_serial)
    request.session['ann_undo_auth_id'] = ann.author_id
    request.session['undo'] = True
    ann.delete()
    messages.info(request, 'Announcement deleted')
    messages.info(request, "<a href='/cca_programming/undo_announcement'>undo</a>", extra_tags='safe')

    return redirect('clubinfo:index')

def delete_session_keys(request):
    for key in list(request.session.keys()):
        del request.session[key]

def undo_announcement(request):
    a = Announcement(title=request.session['ann_undo_title'], pub_date=loads(request.session['ann_undo_date']),
                     text=request.session['ann_undo_text'], author_id=request.session['ann_undo_auth_id'])
    a.save()
    # request.session.flush()
    # delete_session_keys(request)
    request.session['undo'] = False
    messages.info(request,"Announcement delete undone")
    return redirect('clubinfo:index')

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False) # Creates object using fields in the form
            user.is_active = False
            user.save()
            current_site = get_current_
            return redirect('clubinfo:index')


    return render(request, 'registration/register.html', {'form': form})
    # if request.method == 'POST':
    #     form = RegisterForm(request.POST)
    #
    #     if form.is_valid():
    #         form_data = form.cleaned_data
    #         user = User.objects.create_user(username=form_data['username'], first_name=form_data['first_name'],
    #                                         last_name=form_data['last_name'], password=form_data['password'], email=form_data['email'])
    #         user.save()
    #         g = Group.objects.get(name='Normal Users')
    #         g.user_set.add(user)
    #         messages.info(request, 'You have successfully registered!')
    #         messages.debug(request, "Created user with username {} first_name {} last_name {}".format(form_data['username'],
    #                                                                                                   form_data['first_name'],
    #                                                                                                   form_data['last_name']))
    #         return redirect('clubinfo:login')
    # else:
    #     form = RegisterForm(request.POST or None)
    #     return render(request, "ClubInfo/register.html", {'form': form})

def contest_home(request):
    contests = Contest.objects.all().order_by('-date')
    return render(request, 'ClubInfo/contest_home.html', {'contests':contests})

def contest_details(request, pk):

    contest = get_object_or_404(Contest, pk=pk)
    return render (request, 'ClubInfo/contest_details.html', {'contest':contest})

@require_GET
def modify_contest(request, pk):
    #https://stackoverflow.com/questions/866272/how-can-i-build-multiple-submit-buttons-django-form
    if not request.user.is_staff:
        raise PermissionDenied

    contest = get_object_or_404(Contest, pk=pk)
    data = {'date': datetime.strftime(contest.date, '%m-%d-%Y'), 'name': contest.name}
    info_form = ModifyContestInfoForm(request.session.get('info_form_errors', None), initial=data)
    # debug(request.session.get("info_form_errors", None))

    # debug("Contest id {}".format(pk))
    adduser_form = AddContestUserForm(request.session.get('adduser_form_errors', None), contest_id=pk)
    # debug(adduser_form.form_contest_id)
    skip = {}
    for score in contest.score_set.all():
        skip[score.taker.pk] = True

    adduser_list = [u for u in User.objects.order_by('last_name') if not skip.get(u.pk, False)]
    # debug([u.username for u in adduser_list])
    request.session.pop('info_form_errors', None)
    request.session.pop('adduser_form_errors', None)
    return render(request, "ClubInfo/modify_contest.html", {"info_form": info_form,
                                                            "adduser_form":adduser_form,
                                                            "adduser_list": adduser_list,
                                                            "contest": contest})

# def modify_contest(request, pk):
#     #https://stackoverflow.com/questions/866272/how-can-i-build-multiple-submit-buttons-django-form
#     if not request.user.is_staff:
#         raise PermissionDenied
#
#     contest = get_object_or_404(Contest, pk=pk)
#     data = {'date': datetime.strftime(contest.date, '%m-%d-%Y'), 'name': contest.name}
#     form = ModifyContestInfoForm(request.POST or None, initial=data)
#     # debug(request.session.get("form_errors", None))
#     debug(form.is_valid())
#     debug(request.POST)
#     if form.is_valid():
#         form_data = form.cleaned_data
#         contest.date = (form_data['date'])
#         contest.name = form_data['name']
#         contest.save()
#         messages.info(request, "Successfully modified contest")
#         return redirect('clubinfo:modify_contest', pk)
#         # print(form_data['name'])
#         # print(contest.name)
#     # del request.session['form_errors']
#     # form = ModifyContestInfoForm()
#     return render(request, "ClubInfo/modify_contest.html", {"form": form, "contest": contest})

@require_POST
def mod_contest_info(request, pk):
    contest = get_object_or_404(Contest, pk=pk)
    form = ModifyContestInfoForm(request.POST)

    if form.is_valid():
        form_data = form.cleaned_data
        contest.date = (form_data['date'])
        contest.name = form_data['name']
        contest.save()
        messages.info(request, "Successfully modified contest")
        # print(form_data['name'])
        # print(contest.name)

    else:
        request.session['info_form_errors'] = request.POST


    return redirect('clubinfo:modify_contest', pk=pk)

@require_POST
def mod_contest_add_user(request, user_pk, contest_pk):
    user = get_object_or_404(User, pk=user_pk)
    contest = get_object_or_404(Contest, pk=contest_pk)
    form = AddContestUserForm(request.POST, contest_id=contest_pk)
    if form.is_valid():
        score = Score(taker=user, contest=contest, score=form.cleaned_data['score'])
        score.save()
        messages.info(request, "Added User {}".format(user.username))
    else:
        request.session['adduser_form_errors'] = request.POST

    return redirect("clubinfo:modify_contest", pk=contest_pk)

@require_POST
def mod_contest_del_user(request, score_pk):
    score = get_object_or_404(Score, pk=score_pk)
    user = score.taker
    contest = score.contest
    score.delete()
    messages.info(request, "Successfully deleted User: {}".format(user.profile.full_name))
    return redirect('clubinfo:modify_contest', pk=contest.pk)





#TODO: real user registration: emails
#TODO: give admin priviges - find out how groups/privilleges work?
#TODO: unique values in models
#TODO: Are you sure ... ?