# -*- coding:utf-8 -*-
__author__ = 'sandy'
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import ModelForm
from django import forms
from blog.models import Tsecfield, Tseclass,Tpolicy,Tmeta,Tusersecfieldrelation
import datetime


class FieldForm(ModelForm):
    fieldsname=[]
    AllFieldids = []
    AllFieldNames=[]
    sefieldid = []
    sefieldid.append(0)
    fieldsname.append('主范畴')
    fields = Tsecfield.objects.filter(parent_secfd_id=0)#the names of null
    for field in fields:#[音乐 相声]
        secfid = Tsecfield.objects.get(secfield_name=field).secfield_id#[1,7]
        sefieldid.append(secfid) #the secfield_ids which the parent_secfd_id is null
        fieldsname.append(field)#the secfield_names which the parent_secf_id is null
        secondname = Tsecfield.objects.filter(parent_secfd_id=secfid) #[1:2 5]
        for second in secondname:
            secfidid = Tsecfield.objects.get(secfield_name=second).secfield_id
            sefieldid.append(secfidid)
            fieldsname.append(second)
    fieldinfo = zip(sefieldid, fieldsname)
    choise = tuple(zip(sefieldid, fieldsname))
    idparent = forms.ChoiceField(label='所属范畴', required=True, choices=choise)
    secfieldname = forms.CharField(label='范畴名字', max_length=30, required=True)
    '''
    Get all the secfield information for use.
    '''
    a = Tsecfield.objects.all()
    for i in a:
        AllFieldids.append(i.secfield_id)
        AllFieldNames.append(i.secfield_name)
    AllFieldsinfo = zip(AllFieldids, AllFieldNames)
    allfieldsinfo = tuple(AllFieldsinfo)
    class Meta:
        model = Tsecfield
        fields = ('idparent', 'secfieldname')


class ClassForm(ModelForm):
    classesname = []
    classid = []
    AllClassids = []
    AllClassNames = []
    classesname.append('主分类')
    classid.append(0)
    classes = Tseclass.objects.filter(parent_secl_id=0)#the names of null
    for clas in classes:#[音乐 相声]
        clsid = Tseclass.objects.get(seclass_name=clas).seclass_id#[1,7]
        classid.append(clsid) #the secfield_ids which the parent_secfd_id is null
        classesname.append(clas)#the secfield_names which the parent_secf_id is null
        secondname = Tseclass.objects.filter(parent_secl_id=clsid) #[1:2 5]
        for second in secondname:
            secfidid = Tseclass.objects.get(seclass_name=second).seclass_id
            classid.append(secfidid)
            classesname.append(second)
    classinfo = zip(classid, classesname)
    choise1 = tuple(classinfo)
    #idsecfield = forms.IntegerField(label='范畴ID', required=True)
    '''get all class info for user'''
    a = Tseclass.objects.all()
    for i in a:
        AllClassids.append(i.seclass_id)
        AllClassNames.append(i.seclass_name)
    AllClassinfo = zip(AllClassids, AllClassNames)
    allclassinfo = tuple(AllClassinfo)
    csparent = forms.ChoiceField(label='所属分类', required=True, choices=choise1)
    secclassname = forms.CharField(label='分类名字', max_length=30, required=True)
    class Meta:
        model = Tseclass
        fields = ('csparent', 'secclassname')


def fd(req):
    return HttpResponseRedirect('/field')


def showfield(req):
    a=Tsecfield.objects.all()
    fieldinfo={}
    for i in range(a.count()):
        fieldid = a.values()[i]['secfield_id']
        parentid = a.values()[i]['parent_secfd_id']
        if parentid == 0:
            parentname='主范畴'
        else:
            parentname = Tsecfield.objects.get(secfield_id=parentid)
        fieldname = a.values()[i]['secfield_name']
        name=[fieldid, fieldname, parentname]
        fieldinfo[fieldid]=name
    return render_to_response('show_fields.html', {'fieldinfo': fieldinfo})


def addfield(req):
    head = u'添加范畴'
    fieldinfo = Tsecfield()
    if req.method == 'POST':
        af = FieldForm(req.POST)
        if af.is_valid():
            parentname = req.POST['idparent'].encode('utf-8')
            fieldname = req.POST['secfieldname'].encode('utf-8')
            fieldinfo.parent_secfd_id = int(parentname)
            fieldinfo.secfield_name = fieldname
            fieldinfo.gen_time = datetime.datetime.now()
            try:
                fieldinfo.save()
            except Exception as e:
                return HttpResponse(e)
            return HttpResponseRedirect('/showfields')
    else:
        af = FieldForm()
    return render_to_response('field_classadd3.html', {'af': af, 'head': head})



def delfield(req, id):
    #print id
    field_info = Tsecfield.objects.get(secfield_id=id)
    users=Tusersecfieldrelation.objects.filter(secfield_id__contains=id)
    secfieldinfo = {}
    for i in range(users.count()):
        uid = users.values()[0]['idtusersecfieldrelation']
        tuid = users.values()[0]['tu_id']
        secfid = users.values()[0]['secfield_id'].split(',')
        secfid.remove(id)
        if secfid:
            secfid = ",".join(secfid)
            Tusersecfieldrelation.objects.filter(idtusersecfieldrelation=uid).update(secfield_id=secfid)
        else :
            #print "Only one",secfid
            Tusersecfieldrelation.objects.filter(idtusersecfieldrelation=uid).delete()
    #delete policy
    try:
        policy = Tpolicy.objects.get(secfield_id=id).delete()
    except:
        print "No Policy"
    #delete secfield 
    field_info.delete()
    return HttpResponseRedirect('/field')


def showfid(req, id):
    uf = FieldForm().fieldinfo
    field_info = Tsecfield.objects.get(secfield_id=id)
    fieldname = field_info.secfield_name
    field_id = field_info.secfield_id
    parent_name = field_info.parent_secfd_id
    field = [fieldname, field_id, parent_name]
    for k,v in uf:
        if k == field[2]:
            print k
    return render_to_response('updatefield.html', {'field': field, 'uu': uf})


def updatefield(req):
    print req.POST
    fieid = req.POST['field_id']
    fiename = req.POST['field_name']
    parentname = req.POST['parent_name']
    print parentname
    print parentname != u'主范畴'
    # print Tsecfield.objects.get(secfield_name=parentname)
    gentime = datetime.datetime.now()
    if parentname != u'主范畴':
        parid = Tsecfield.objects.get(secfield_name=parentname).secfield_id
        print '###', parid
        Tsecfield.objects.filter(secfield_id=fieid).update(secfield_id=fieid, secfield_name=fiename, parent_secfd_id=parid)
    else:
        Tsecfield.objects.filter(secfield_id=fieid).update(secfield_id=fieid, secfield_name=fiename, parent_secfd_id=0)
    return HttpResponseRedirect('/field')


def cs(req):
    return HttpResponseRedirect('/class')


def showclass(req):
    sc = Tseclass.objects.all()
    classinfo = {}
    for i in range(sc.count()):
        classid = sc.values()[i]['seclass_id']
        parentid = sc.values()[i]['parent_secl_id']
        if parentid == 0:
            parent_name='主分类'
        else:
            parent_name = Tseclass.objects.get(seclass_id = parentid)
        classname = sc.values()[i]['seclass_name']
        name = [classid, classname, parent_name]
        classinfo[classid] = name
    return render_to_response('show_classes.html', {'classinfo':classinfo})


def addclass(req):
    '''
    :param req: we use the same templates with the secfieldadd function.
    :return:
    '''
    head = u'添加媒资分类'
    classinfo = Tseclass()
    print "addclass"
    if req.method == 'POST':
        parentname = req.POST['csparent'].encode('utf-8')
        classname = req.POST['secclassname'].encode('utf-8')
        print parentname,classname
        af = ClassForm(req.POST)
        '''if af.is_valid():
            parentname = req.POST['csparent'].encode('utf-8')
            classname = req.POST['secclassname'].encode('utf-8')
            print parentname,classname
            classinfo.parent_secl_id = int(parentname)
            classinfo.seclass_name = classname
            classinfo.gen_time = datetime.datetime.now()
            try:
                classinfo.save()
            except Exception as e:
                return HttpResponse(e)
            return HttpResponseRedirect('/class')'''
        classinfo.parent_secl_id = int(parentname)
        classinfo.seclass_name = classname
        classinfo.gen_time = datetime.datetime.now()
        try:
            classinfo.save()
        except Exception as e:
            return HttpResponse(e)
        return HttpResponseRedirect('/class')
    else:
        af = ClassForm()
    classesname = []
    classid = []
    AllClassids = []
    AllClassNames = []
    classesname.append('主分类')
    classid.append(0)
    classes = Tseclass.objects.filter(parent_secl_id=0)#the names of null
    for clas in classes:#[音乐 相声]
        clsid = Tseclass.objects.get(seclass_name=clas).seclass_id#[1,7]
        classid.append(clsid) #the secfield_ids which the parent_secfd_id is null
        classesname.append(clas)#the secfield_names which the parent_secf_id is null
        secondname = Tseclass.objects.filter(parent_secl_id=clsid) #[1:2 5]
        for second in secondname:
            secfidid = Tseclass.objects.get(seclass_name=second).seclass_id
            classid.append(secfidid)
            classesname.append(second)
    classinfo = zip(classid, classesname)
    vin = tuple(classinfo)
    #print "vin",vin
    return render_to_response('field_classadd2.html', {'af': af,'uu3':vin, 'head': head})
    #return render_to_response('secclassadd.html', {'cf':cf,'head':head})


def delclass(req, id):
    class_info = Tseclass.objects.get(seclass_id=id)
    parid = Tseclass.objects.get(seclass_id=id).parent_secl_id
    print "delclass"
    print class_info,id,parid
    if class_info!= u'主分类':
        subclass=Tseclass.objects.filter(parent_secl_id=id)#select Allclass where parent_secl_id=id
        print "subclass:",subclass
        for classes in subclass:
            print "classe:",classes
            clsid = Tseclass.objects.get(seclass_name=classes).seclass_id
            Tseclass.objects.filter(seclass_id=clsid).update(seclass_id=clsid,parent_secl_id=parid)    
        #class_info.delete()
        submeta=Tmeta.objects.filter(parent_secl_id=id)
        print "submeta:",submeta
        for metas in submeta:
            print "meta:",metas
        Tmeta.objects.filter(parent_secl_id=id).update(parent_secl_id=parid)
        sp = Tpolicy.objects.all()
        policyinfo = {}
        for tp in sp:
            policyid = tp.idtusersecfieldrelation
            secname = Tsecfield.objects.get(secfield_id=tp.secfield_id).secfield_name
            classname = []
            classids = tp.seclass_id.split(',')
            vincent = []
            #print "classids",classids
            global has_classid
            has_classid=False
            for classid in classids:
                if classid is None or classid == '':
                    continue
                if int(classid) == int(id):
                    has_classid = True
                else:
                    vincent.append(classid)
            if has_classid == True:
                print "TRUE:",vincent
	        changeclassnames = ','.join(vincent)
                Tpolicy.objects.filter(idtusersecfieldrelation=policyid).update(idtusersecfieldrelation=policyid,seclass_id=changeclassnames)
        class_info.delete()
        #print "classids",sp
    return HttpResponseRedirect('/class')


def showcid(req, id):
    classf = ClassForm().classinfo
    class_info = Tseclass.objects.get(seclass_id=id)
    class_name = class_info.seclass_name
    class_id = class_info.seclass_id
    parent_name = class_info.parent_secl_id
    clas = [class_name, class_id, parent_name]
    return render_to_response('updateclass.html', {'clas': clas, 'classf': classf})


def updateclass(req):
    '''
    :param req: The post content should be matched with the updateclass.html(the name of the <input..name="class_id">).
    :return:
    '''
    print req.POST
    classid = req.POST['class_id']
    classname = req.POST['class_name']
    parentname = req.POST['parent_name']
    gentime = datetime.datetime.now()
    if parentname != u'主分类':
        parid = Tseclass.objects.get(seclass_name=parentname).seclass_id
        print '###', parid
        Tseclass.objects.filter(seclass_id=classid).update(seclass_id=classid, seclass_name=classname, parent_secl_id=parid)
    else:
        Tseclass.objects.filter(seclass_id=classid).update(seclass_id=classid, seclass_name=classname, parent_secl_id=0)
    return HttpResponseRedirect('/class')

