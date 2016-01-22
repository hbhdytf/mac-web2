# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tgroup',
            fields=[
            ],
            options={
                'db_table': 'TGroup',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tgroupsecfieldrelation',
            fields=[
            ],
            options={
                'db_table': 'TGroupSecfieldRelation',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tpolicy',
            fields=[
            ],
            options={
                'db_table': 'TPolicy',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tsecfield',
            fields=[
            ],
            options={
                'db_table': 'TSecfield',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tseclass',
            fields=[
            ],
            options={
                'db_table': 'TSeclass',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tusersecfieldrelation',
            fields=[
            ],
            options={
                'db_table': 'TUserSecfieldRelation',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
