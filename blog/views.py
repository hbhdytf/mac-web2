# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from blog.models import Tseclass, Tuser, Tmeta, Tusersecfieldrelation, Tsecfield
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from os import popen
from blog.forms import MetaForm
from django.core.cache import cache
import re
from swiftclient import client
from django.contrib import messages
from django.utils.translation import ugettext as _
import os
import time

def main(req):
    a = Tseclass.objects.filter(parent_secl_id=None)
    det = {}
    for i in range(a.count()):
        seclassid = a.values()[i]['seclass_id']
        name = a.values()[i]['seclass_name']
        aa = Tseclass.objects.filter(parent_secl_id=seclassid)
        detdet = {}
        for ii in range(aa.count()):
            seclassidid = aa.values()[ii]['seclass_id']
            name1 = aa.values()[ii]['seclass_name']
            d = Tseclass.objects.filter(parent_secl_id=seclassidid)
            detdet[name1] = d
        det[name] = detdet
    return render_to_response('main.html', {'det': det})


def test(req):
    uname = req.GET['id'].encode('utf-8')
    
    a = Tseclass.objects.filter(parent_secl_id=0)
    #先用三级显示，下面不带父类ID
    det = {}
    tmp = {}
    for i in range(a.count()):
        seclassid = a.values()[i]['seclass_id']
        name = a.values()[i]['seclass_name']
        aa = Tseclass.objects.filter(parent_secl_id=seclassid)
        detdet = {}
        for ii in range(aa.count()):
            seclassidid = aa.values()[ii]['seclass_id']
            name1 = aa.values()[ii]['seclass_name']
            d = Tseclass.objects.filter(parent_secl_id=seclassidid)
            detdetdet = {}
            for iii in range(d.count()):
                seclassididid = d.values()[iii]['seclass_id']
                name11 = d.values()[iii]['seclass_name']
                detdetdet[name11] = seclassididid
            #tmp[name1] = seclassidid
            detdet[(name1,seclassidid)] = detdetdet
        det[(name,seclassid)] = detdet
    print "det====",det
    return render_to_response('test.html', {'det': det, 'uname': str(uname)})
    '''
    root = Tseclass.objects.filter(parent_secl_id=0)
    tree = {}
    for i in range(root.count()):
        id_st = root.values()[i]['secfield_id']
        name_st = root.values()[i]['secfield_name']
    '''        


def beginAddmeta(req):
    return render_to_response('addmeta.html')


@csrf_exempt
def addmeta(req):
    obj_id =req.POST['obj_id']
    obj_name = req.POST['obj_name']
    obj_secl_id = req.POST['obj_secl_id']
    obj_level = req.POST['obj_level']
    st = Tmeta()

    st.object_id = obj_id
    st.object_name = obj_name
    st.parent_secl_id = obj_secl_id
    st.obj_seclevel = obj_level
    st.save()
    return HttpResponseRedirect("/meta?id=%s" % obj_id)


def delmByID(request, me_id, uname, id):
    """
    :param request:
    :param me_id: the parent_secl_id of Tmeta database,we can return the page after we delete the id of meta.
    :param uname: the user's name
    :param id: the meta object_id
    :return: return to the page of before we execute delete.
    """
    name_token = '_'.join([uname, 'token'])
    name_url = '_'.join([uname, 'url'])
    try:
        auth_token = cache.get(name_token).split(':')[-1]
        storage_url = cache.get(name_url)
    except Exception as e:
        return HttpResponse("<h1>You have no token!</h1></ br><p>Please Press 获取token Button!</p>")
    bb = Tmeta.objects.get(object_id=id)
    print "bb",bb.path.split('/',1)[0],bb.path.split('/',1)[1]
    container = bb.path.split('/',1)[0] 
    objectname = bb.path.split('/',1)[1]
    print "DELETE============"
    print storage_url
    print objectname.split('/')[-1]
    try:
        client.delete_object(storage_url, auth_token, container, objectname)
        #values=(path, name, secfiled, seclevel, stype, token, str(url)+'/%s' % path)
        #print values
        #content = popen("curl -X DELETE -D- -H 'object_name:%s' -H 'parent_secl_id:%s' -H 'obj_seclevel:%s' -H 'Content-Type:%s' -H '%s' %s" % values).readlines()
        bb.delete()
        print "DELETE SUCESS"
        messages.add_message(request, messages.INFO, _("Object deleted."))
    except client.ClientException as e:
        print "DELETE fail",e
        messages.add_message(request, messages.ERROR, _("Access denied."))
        return HttpResponse(e)
    return HttpResponseRedirect("/meta/id=%s/name=%s" % (me_id, uname))


def showMid(req):
    obj_id = req.GET['id']
    bb = Tmeta.objects.get(object_id=obj_id)
    return render_to_response('updatemeta.html', {'data': bb})


def showmeta(request, meid, uname):
    mt = Tmeta.objects.filter(parent_secl_id=meid)
    metainfo = {}
    for i in range(mt.count()):
        objectid = mt.values()[i]['object_id']
        name = mt.values()[i]['object_name']
        paseclid = mt.values()[i]['parent_secl_id']
        paseclname = Tseclass.objects.get(seclass_id=paseclid).seclass_name
        objseclevel = mt.values()[i]['obj_seclevel']
        author = mt.values()[i]['author']
        objpath = mt.values()[i]['path']
        name = [objectid, name, paseclname, objseclevel, author, objpath]
        metainfo[objectid] = name
    return render_to_response('show_meta.html', {'metainfo': metainfo, 'uname': uname, 'mt_id': meid})


def frame(req):
    """
    :param req: we can add charge whether the user is admin or normal users. then go to the different html.
    :return:
    """
    return render_to_response('MyFrame.html')


def showsecfield(req):
    sf = Tusersecfieldrelation.objects.all()
    secfieldinfo = {}
    for i in range(sf.count()):
        secfield_names = []
        id = sf.values()[i]['idtusersecfieldrelation']
        tuid = sf.values()[i]['tu_id']
        secfid = sf.values()[i]['secfield_id'].split(',')
        name = Tuser.objects.get(tu_id=tuid).username
        for ids in secfid:
            secfield_names.append(Tsecfield.objects.get(secfield_id=ids).secfield_name.encode('utf-8'))
        info = [id, name, secfield_names]
        secfieldinfo[id] = info
    return render_to_response('showuserfield.html', {'secfieldinfo': secfieldinfo})


def top(req):
    name = req.GET['id']
    if not name:
        name = cache.get(name)
    cache.set(name, name)
    return render_to_response('top.html', {'name': name})


def login(req):
    if req.method == 'POST':
        name = req.POST.get('uname', '')
        passwd = req.POST.get('upasswd', '')
        nm = Tuser.objects.filter(login_name__exact='%s' % name, password__exact='%s' % passwd)
        if nm:
            return render_to_response('MyFrame.html', {'name': name})
    return render_to_response('login.html', {'document_root': '~/sun/django/mac/blog/templates/images'})


def metaadd(req):
    """
    :param req:
    :return:
    """
    header = {}
    if req.method=='GET':
        uname=req.GET['id'].encode('utf-8')
    if req.method=='POST':
        uname = req.POST['id'].encode('utf-8')
    name_token = '_'.join([uname, 'token'])
    print "metaadd===============:"
    name_url = '_'.join([uname, 'url'])
    token = cache.get(name_token)
    '''url = cache.get(name_url)'''
    url = 'http://127.0.0.1:8080/v1/AUTH_mac'
    pattern = re.compile('\(.+\)')
    print req.method
    if req.method == 'POST':
        mf = MetaForm(req.POST, req.FILES)
        if mf.is_valid():
            filename = handle_upload_file(req.FILES['path'])
            if not filename:
                return HttpResponse("Upload Failed!")
            name = req.POST.get('object_name').encode('utf-8')
            secfiled = req.POST.get('parent_secl_id').encode('utf-8')
            seclevel = req.POST.get('obj_seclevel').encode('utf-8')
            meta_info = dict(req.FILES).values()[0]
            stype = pattern.findall(str(meta_info))[0].strip('()')
            #path = str(meta_info).split(' ')[1]
            path = filename
            header['object_name'] = name
            header['parent_secl_id'] = secfiled
            header['obj_seclevel'] = seclevel
            print "path=========="+path 
	        #print "name=========="+name
            #print "secfiled======"+secfiled
            #print "seclevel======"+seclevel
	        #print "Url==========="+url
            #print meta_info
            # tt = client.put_object(url, token, contents=mf.cleaned_data['path'], headers=header)
            # return HttpResponse(tt)
            if token is None:
                return HttpResponse("Token is timeout, Please try to regain token.")
            values = (path, name, secfiled, seclevel, stype, token, str(url)+'/ytf%s' % path)
            print values
            content = popen("curl -X PUT -T %s -D- -H 'object_name:%s' -H 'parent_secl_id:%s' -H \
            'obj_seclevel:%s' -H 'Content-Type:%s' -H '%s' %s" % values).readlines()
            return HttpResponse('<h1>%s</h1></ br><p>%s</p>' % (content[0], content[-1]))
    else:
        mf = MetaForm()
    return render_to_response('addmetadb.html', {'mf': mf,'uname':uname})

def handle_upload_file(f):
    filename = ""
    try:
        path = "/tmp/file" + time.strftime('/%Y/%m/%d/%H/%M/%S/')
        if not os.path.exists(path):
            os.makedirs(path)
            filename = path + f.name
            print filename
            destination = open(filename, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    except Exception as e:
        print e
    return filename

def updatemeta(req):
    obj_id = req.POST['obj_id']
    obj_name = req.POST['obj_name']
    obj_secl_id = req.POST['obj_secl_id']
    obj_seclevel = req.POST['obj_level']
    Tmeta.objects.filter(object_id=obj_id).update(object_name=obj_name, parent_secl_id=obj_secl_id, obj_seclevel=obj_seclevel)
    return HttpResponseRedirect("/user")


def gettoken(req):
    """
    :param the attribute: we should know the user name .and then use the api to get the token with
     popen function.
    :return:still in the page.but we have stored the token and url in the cache.
    """
    name = req.GET['id'].encode('utf-8')
    content = popen("curl -D- -H 'X-Storage-User:%s' http://127.0.0.1:8080/auth/v1.0" % name).readlines()
    # token = content[2].split(':', 1)[-1].strip()  this is only AUTH_tk....don't have X-Storage-Token
    token = content[2].strip()
    url = content[1].split(':', 1)[-1].strip()
    # url = content[1].strip()
    name_token = '_'.join([name, 'token'])
    name_url = '_'.join([name, 'url'])
    cache.set(name_token, token, 88600)
    cache.set(name_url, url, 88600)
    print "token========:"+token
    return HttpResponseRedirect("/top?id=%s" % name)


def info(req):
    """
    :param req:
    :return: the i of this web.
    """
    return render_to_response('Information.html', {})
