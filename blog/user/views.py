__author__ = 'sandy'
from django.shortcuts import render_to_response
from blog.models import Tuser, Tusersecfieldrelation
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

ONE_PAGE_OF_DATA = 10

def showuser(req):
    try:
        curPage = int(req.GET.get('curPage','1'))
        allPage = int(req.GET.get('allPage','1'))
        pageType = str(req.GET.get('pageType',''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    # charge pageup or pagedown
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA
    posts = Tuser.objects.all()[startPos:endPos]
    a = posts
    #a = Tuser.objects.all()
    userinfo = {}
    for i in range(a.count()):
        tuid = a.values()[i]['tu_id']
        uname = a.values()[i]['username']
        mobile = a.values()[i]['mobile']
        email = a.values()[i]['email']
        gen_time = a.values()[i]['gen_time']
        # ulogin = a.values()[i]['login_name']
        selevel = a.values()[i]['seclevel']
        name = [tuid, uname, selevel, mobile, email, gen_time]
        userinfo[tuid] = name
    
    if curPage == 1 and allPage == 1:
        allPostCounts = Tuser.objects.count()
        allPage = allPostCounts / ONE_PAGE_OF_DATA
        remainPost = allPostCounts % ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1

    #return render_to_response('show_user.html', {'userinfo': userinfo,'posts':posts,'allPage':allPage,'curPage':curPage},context_instance=RequestContext(req))
    return render_to_response('show_user.html', {'userinfo': userinfo,'posts':posts,'allPage':allPage,'curPage':curPage})


def beginAdduser(req):
    return render_to_response('adduser.html')


@csrf_exempt
def adduser(req):
    login_name = req.POST['login_name']
    password = req.POST['passwd']
    name = req.POST['name']
    seclevel = req.POST['level']
    st = Tuser()

    st.login_name = login_name
    st.username = name
    st.seclevel = seclevel
    st.password = password
    st.save()
    return HttpResponseRedirect("/user")


def updateuser(req):
    loginname = req.POST['login_name']
    password = req.POST['passwd']
    name = req.POST['name']
    seclevel = req.POST['level']
    st = Tuser()

    st.login_name = loginname
    st.username = name
    st.seclevel = seclevel
    st.password = password
    Tuser.objects.filter(login_name=loginname).update(login_name=loginname, username=name, seclevel=seclevel)
    return HttpResponseRedirect("/user")


def deluByID(request):
    uid = request.GET['id']
    bb = Tuser.objects.get(tu_id=uid)
    try:
        user_field_relation = Tusersecfieldrelation.objects.get(tu_id=uid)
        user_field_relation.delete()
    except Exception as e:
        pass
    bb.delete()
    return HttpResponseRedirect("/user")


def showUid(req):
    tuid = req.GET['id']
    next_tuid = int(tuid)+1
    bb = Tuser.objects.get(tu_id=tuid)
    return render_to_response('updateuser.html', {'data':bb, 'nextid': next_tuid})
