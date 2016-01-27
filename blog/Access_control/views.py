# coding:utf-8
__author__ = 'sandy'
from django.shortcuts import render_to_response
from blog.models import Tusersecfieldrelation, Tuser, Tsecfield, Tpolicy, Tseclass
from django.forms import ModelForm
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
import sys

sys.path.append('..')
from blog.field_class import views


class SefieldForm(ModelForm):
    """
    :param req: First we get the secfield_id and secfield_name of the parent_secfd_id
     which is Null and the parent_secfd_id is Null.like we chose Null and 1.
     This way is to give us choices to chose when we add secfield.
     Main idea:
     1.we get the first secfield_ids which parent_secfd_id is null.
     2.we continue get the second secfield_ids which parent_secfd_id is in the first secfield_ids.
     fields:#the names of null
    :return:to the show secure field html
    """
    fieldsname = []
    sefieldid = []
    fields = Tsecfield.objects.filter(parent_secfd_id=0)
    for field in fields:
        secfid = Tsecfield.objects.get(secfield_name=field).secfield_id
        sefieldid.append(secfid)
        fieldsname.append(field)
        secondname = Tsecfield.objects.filter(parent_secfd_id=secfid)
        for second in secondname:
            secfidid = Tsecfield.objects.get(secfield_name=second).secfield_id
            sefieldid.append(secfidid)
            fieldsname.append(second)
    fieldinfo = zip(sefieldid, fieldsname)
    choise = tuple(fieldinfo)
    idsecfield = forms.IntegerField(label='范畴ID', required=True)
    idparent = forms.ChoiceField(label='所属范畴', required=True, choices=choise)
    secfieldname = forms.CharField(label='范畴名字', max_length=30, required=True)

    class Meta:
        model = Tsecfield
        fields = ('idsecfield', 'secfieldname', 'idparent')


class Sefield_Form(ModelForm):
    #a = Tuser.objects.all().values('tu_id','username')
    a = Tuser.objects.all()
    uid = []
    uname = []
    AllFieldids = []
    AllFieldNames=[]
    userinfo = []
    a1 = Tsecfield.objects.all()
    for i in a1:
        AllFieldids.append(i.secfield_id)
        AllFieldNames.append(i.secfield_name)
    AllFieldsinfo = zip(AllFieldids, AllFieldNames)
    allfieldsinfo = tuple(AllFieldsinfo) 
    for i in a:
        uid.append(i.tu_id)
        uname.append(i.username)
    userinfo = tuple(zip(uid, uname))
    #print Tuser.objects.all().values('tu_id','username') 
    # fields_info = views.FieldForm().allfieldsinfo
    nameofusers = forms.ChoiceField(label='用户名', required=True, choices=userinfo)
    #nameoffields = forms.MultipleChoiceField(label='范畴名', required=True, choices=allfieldsinfo, \
    #                                         widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Tuser
        #fields = ('nameofusers', 'nameoffields',)
        fields = ('nameofusers', )


class PolicyForm(ModelForm):
    AllClassids = []
    AllClassNames = []
    AllFieldids = []
    AllFieldNames = []
    sec_fields = Tsecfield.objects.all()
    for i in sec_fields:
        AllFieldids.append(i.secfield_id)
        AllFieldNames.append(i.secfield_name)
    fields_info = zip(AllFieldids, AllFieldNames)
    allfieldsinfo = tuple(fields_info)
    sec_classes = Tseclass.objects.all()
    for i in sec_classes:
        AllClassids.append(i.seclass_id)
        AllClassNames.append(i.seclass_name)
    classes_info = zip(AllClassids, AllClassNames)
    allclassinfo = tuple(classes_info)
    field = forms.ChoiceField(label=u'范畴名', choices=allfieldsinfo, required=True)
    classes = forms.MultipleChoiceField(label=u'分类名称', choices=allclassinfo, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Tpolicy
        fields = ('field', 'classes')


def showuserfield(req):
    sf = Tusersecfieldrelation.objects.all()
    secfieldinfo = {}
    for i in range(sf.count()):
        secfield_names = []
        id = sf.values()[i]['idtusersecfieldrelation']
        tuid = sf.values()[i]['tu_id']
        secfid = sf.values()[i]['secfield_id'].split(',')
        name = Tuser.objects.get(tu_id=tuid).login_name
        for sid in secfid:
            secfield_names.append(Tsecfield.objects.get(secfield_id=sid).secfield_name.encode('utf-8'))
        info = [id, name, secfield_names]
        secfieldinfo[id] = info
    return render_to_response('showuserfield.html', {'secfieldinfo': secfieldinfo})


def adduserfield(req):
    head = u'范畴用户关系'
    if req.method == 'POST':
        af = Sefield_Form(req.POST)
        if af.is_valid():
            uid = req.POST.get('nameofusers')
            cc = req.POST.getlist('nameoffields')
            secfieldid = ','.join(cc)
            try:
                Tusersecfieldrelation.objects.create(tu_id=int(uid), secfield_id=secfieldid)
            except Exception as e:
                if e[0]==1062:
                    return HttpResponse("该用户已存在，如需更新，请点击更新按钮！")
                return HttpResponse(e)
            return HttpResponseRedirect('/user_field')
    else:
        af = Sefield_Form()
    #print "af",af
    AllFieldids = []
    AllFieldNames=[]
    a = Tsecfield.objects.all()
    for i in a:
        AllFieldids.append(i.secfield_id)
        AllFieldNames.append(i.secfield_name)
    AllFieldsinfo = zip(AllFieldids, AllFieldNames)
    vin = tuple(AllFieldsinfo)
    return render_to_response('field_classadd.html', {'af': af,'uu2': vin,'head': head})


def delufrelation(req, id):
    user_field = Tusersecfieldrelation.objects.get(idtusersecfieldrelation=id)
    user_field.delete()
    return HttpResponseRedirect('/user_field')


def showrelation(req, id):
    """
    :param req: we send the id and uname to the html.and the checkbox of Secfield_form.
    :param id:kk includes all the secfield_name from the file of field_class.views.py
    :return:
    """
    info = [u'用户范畴更新', u'编号', u'用户名', u'范畴名']
    kk = views.FieldForm().allfieldsinfo
    sf = Tusersecfieldrelation.objects.all()
    # ufrealtion={}
    relationinfo = Tusersecfieldrelation.objects.get(idtusersecfieldrelation=id)
    tu_name = Tuser.objects.get(tu_id=relationinfo.tu_id).username
    secfield_ids = relationinfo.secfield_id.split(',')
    secfield_names = []
    for sid in secfield_ids:
        secfield_names.append(Tsecfield.objects.get(secfield_id=sid).secfield_name)
    ufrealtion = [id, tu_name, secfield_names]
    '''print "showrelation:tu_name:",tu_name,"relationinfo:",relationinfo,"secfield_ids:",secfield_ids,"secfield_names"'''
    #print "kk",kk
    AllFieldids = []
    AllFieldNames=[]
    a = Tsecfield.objects.all()
    for i in a:
        AllFieldids.append(i.secfield_id)
        AllFieldNames.append(i.secfield_name)
    AllFieldsinfo = zip(AllFieldids, AllFieldNames)
    vin = tuple(AllFieldsinfo)
    #print "vin",vin
    return render_to_response('updateusfandpolicy.html', {'ufrealtion': ufrealtion, 'uu': vin, 'info': info})



def updateufrelation(req):
    usfid = req.POST['field_id']
    uname = req.POST.get('name')
    tu_id = Tuser.objects.get(username=uname).tu_id
    secfieldnames = ','.join(req.POST.getlist('field_names'))
    Tusersecfieldrelation.objects.filter(idtusersecfieldrelation=usfid).update(idtusersecfieldrelation=usfid, \
                                                                               tu_id=tu_id, secfield_id=secfieldnames)
    return HttpResponseRedirect('/user_field')


def showpolicy(req):
    sp = Tpolicy.objects.all()
    policyinfo = {}
    for tp in sp:
        policyid = tp.idtusersecfieldrelation
        secname = Tsecfield.objects.get(secfield_id=tp.secfield_id).secfield_name
        classname = []
        classids = tp.seclass_id.split(',')
        for classid in classids:
            if classid is None or classid == '':
                classname.append('')
                continue 
            elif int(classid) == 0:
                classname.append('主分类')
            classname.append(Tseclass.objects.get(seclass_id=classid).seclass_name)
        policyinfo[policyid] = [policyid, secname, classname]
    return render_to_response('show_policy.html', {'policyinfo': policyinfo})


def addpolicy(req):
    head = u'添加决策'
    if req.method == 'POST':
        poli = PolicyForm(req.POST)
        #if poli.is_valid():
        print req.POST
        secfield = req.POST.get('field')
        seclass = ','.join(req.POST.getlist('classes'))
        try:
            Tpolicy.objects.create(secfield_id=int(secfield), seclass_id=seclass)
        except Exception as e:
            return HttpResponse(e)
        return HttpResponseRedirect('/policy')
    else:
        poli = PolicyForm()
    AllClassids = []
    AllClassNames = []
    AllFieldids = []
    AllFieldNames = []
    sec_fields = Tsecfield.objects.all()
    for i in sec_fields:
        AllFieldids.append(i.secfield_id)
        AllFieldNames.append(i.secfield_name)
    fields_info = zip(AllFieldids, AllFieldNames)
    allfieldsinfo = tuple(fields_info)
    sec_classes = Tseclass.objects.all()
    for i in sec_classes:
        AllClassids.append(i.seclass_id)
        AllClassNames.append(i.seclass_name)
    classes_info = zip(AllClassids, AllClassNames)
    allclassinfo = tuple(classes_info)
    #print "poli",poli
    return render_to_response('field_classadd4.html', {'af': poli, 'head': head,'uu3':allclassinfo,'uu4':allfieldsinfo})


def delpolicy(req, id):
    tpolicy = Tpolicy.objects.get(idtusersecfieldrelation=id)
    tpolicy.delete()
    return HttpResponseRedirect('/policy')


def showapolicy(req, id=None):
    info = [u'决策更新', u'编号', u'范畴名', u'分类名']
    #allclassinfo = views.ClassForm.allclassinfo
    AllClassids = []
    AllClassNames = []
    sec_classes = Tseclass.objects.all()
    for i in sec_classes:
        AllClassids.append(i.seclass_id)
        AllClassNames.append(i.seclass_name)
    classes_info = zip(AllClassids, AllClassNames)
    allclassinfo = tuple(classes_info)
    #print "allclassinfo",allclassinfo
    
    apolicy = Tpolicy.objects.get(idtusersecfieldrelation=id)
    fieldname = Tsecfield.objects.get(secfield_id=apolicy.secfield_id).secfield_name
    classids = apolicy.seclass_id.split(',')
    classnames = []
    for classid in classids:
        if classid is None or classid == '':
            continue
        classnames.append(Tseclass.objects.get(seclass_id=classid).seclass_name)
    policy = [id, fieldname, classnames]
    return render_to_response('updateusfandpolicy.html', {'ufrealtion': policy, 'uu': allclassinfo, 'info': info})


def updatepolicy(req):
    policyid = req.POST.get('field_id')
    fieldname = req.POST.get('name')
    secfield_id = Tsecfield.objects.get(secfield_name=fieldname).secfield_id
    classnames = ','.join(req.POST.getlist('field_names'))
    #print "classnames",classnames
    Tpolicy.objects.filter(idtusersecfieldrelation=policyid).update(idtusersecfieldrelation=policyid, \
                                                                    secfield_id=secfield_id, seclass_id=classnames)
    return HttpResponseRedirect('/policy')
