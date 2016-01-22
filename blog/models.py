# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
# -*-coding: utf-8-*-
from __future__ import unicode_literals

from django.db import models


class Tgroup(models.Model):
    idtgroup = models.IntegerField(db_column='idTGroup', primary_key=True)
    tg_id = models.IntegerField(unique=True)
    group_name = models.CharField(max_length=64, blank=True)
    parent_tg_id = models.IntegerField(blank=True, null=True)
    gen_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=256, blank=True)

    class Meta:
        managed = False
        db_table = 'TGroup'

    def __unicode__(self):
        return self.group_name


class Tgroupsecfieldrelation(models.Model):
    idtgroupsecfieldrelation = models.IntegerField(db_column='idTGroupSecfieldRelation', primary_key=True) # Field name made lowercase.
    tg = models.ForeignKey(Tgroup, blank=True, null=True)
    secfield = models.ForeignKey('Tsecfield', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TGroupSecfieldRelation'

    def __unicode__(self):
        return self.tg


class Tseclass(models.Model):
    seclass_id = models.IntegerField(unique=True, primary_key=True)
    parent_secl_id = models.IntegerField(blank=True, null=True)
    seclass_name = models.CharField(max_length=64, blank=True)
    gen_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TSeclass'

    def __unicode__(self):
        return self.seclass_name


class Tmeta(models.Model):
    object_id = models.IntegerField(unique=True, primary_key=True)
    object_name = models.CharField(max_length=64, blank=True)
    parent_secl_id = models.IntegerField(blank=True, null=True)
    obj_seclevel = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=64, blank=True)
    gen_time = models.DateTimeField(blank=True, null=True)
    path = models.CharField(max_length=64, blank=True)
    type = models.CharField(max_length=64, blank=True)
    subject = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=256, blank=True)
    language = models.CharField(max_length=64, blank=True)
    source = models.CharField(max_length=256, blank=True)

    class Meta:
        managed = False
        db_table = 'TMeta'
        app_label = 'Admin'
        verbose_name = "Meta"

    def __unicode__(self):
        return self.object_name


class Tpolicy(models.Model):
    idtusersecfieldrelation = models.IntegerField(db_column='idTUserSecfieldRelation', primary_key=True) # Field name made lowercase.
    secfield_id = models.IntegerField(unique=True)
    seclass_id = models.CharField(max_length=64, blank=True)

    class Meta:
        managed = False
        db_table = 'TPolicy'

    def __unicode__(self):
        return str(self.idtusersecfieldrelation)


class Tsecfield(models.Model):
    secfield_id = models.IntegerField(unique=True, primary_key=True)
    parent_secfd_id = models.IntegerField(blank=True, null=True)
    secfield_name = models.CharField(max_length=64, blank=True)
    gen_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TSecfield'

    def __unicode__(self):
        return self.secfield_name


class Tuser(models.Model):
    # idtuser = models.IntegerField(db_column='idTUser', primary_key=True) # Field name made lowercase.
    tu_id = models.IntegerField(unique=True, primary_key=True)
    uniqueid = models.CharField(max_length=64)
    user_id_code = models.CharField(max_length=64)
    login_name = models.CharField(unique=True, max_length=64)
    password = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    seclevel = models.IntegerField()
    mobile = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=64, blank=True)
    gen_time = models.DateTimeField()
    login_time = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'TUser'
        verbose_name = "User"
        # verbose_name_plural = "Users"
        app_label = "Admin"

    def __unicode__(self):
        return self.username


class Tusergrouprelation(models.Model):
    idtusergrouprelation = models.IntegerField(db_column='idTUserGroupRelation', primary_key=True)  # Field name made lowercase.
    tu = models.ForeignKey(Tuser, blank=True, null=True)
    tg = models.ForeignKey(Tgroup, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TUserGroupRelation'
        app_label = "Admin"

    def __unicode__(self):
        return str(self.idtusergrouprelation)


class Tusersecfieldrelation(models.Model):
    idtusersecfieldrelation = models.IntegerField(db_column='idTUserSecfieldRelation', primary_key=True) # Field name made lowercase.
    tu_id = models.IntegerField(unique=True)
    secfield_id = models.CharField(max_length=64, blank=True)

    class Meta:
        managed = False
        db_table = 'TUserSecfieldRelation'

    def __unicode__(self):
        return str(self.idtusersecfieldrelation)
