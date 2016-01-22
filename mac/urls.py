from django.conf.urls import patterns, include, url
from django.contrib import admin
from mac import settings

urlpatterns = patterns('',
                       (r'^collected_static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.STATIC_PATH}),
                       url(r'^main/$', 'blog.views.frame'),
                       url(r'^test/$', 'blog.views.test'),
                       url(r'info/$', 'blog.views.info'),
                       url(r'^addmeta.html$', 'blog.views.beginAddmeta'),
                       url(r'^addmeta$', 'blog.views.addmeta'),
                       url(r'^updatemeta$', 'blog.views.updatemeta'),
                       url(r'deletemeta/mtid=(\d+)/name=(\w+)/id=(\d+)$', 'blog.views.delmByID'),
                       url(r'showmid$', 'blog.views.showMid'),
                       url(r'^meta/id=(\d+)/name=(\w+)', 'blog.views.showmeta'),
                       url(r'^top/$', 'blog.views.top'),
                       url(r'^$', 'blog.views.login'),
                       url(r'^metaadd$', 'blog.views.metaadd'),
                       url(r'^gettoken', 'blog.views.gettoken'),
                       url(r'^admin/', include(admin.site.urls)),
                       )

# access control
urlpatterns += patterns('blog.Access_control',
                        url(r'^user_field', 'views.showuserfield'),
                        url(r'^addsefield/', 'views.adduserfield'),
                        url(r'^delufrelation/id=(\d+)$', 'views.delufrelation'),
                        url(r'^showrelation/id=(\d+)$', 'views.showrelation'),
                        url(r'^updateufrelation$', 'views.updateufrelation'),
                        url(r'^policy', 'views.showpolicy'),
                        url(r'^addpolicy', 'views.addpolicy'),
                        url(r'^delpolicy/id=(\d+)', 'views.delpolicy'),
                        url(r'^showapolicy/id=(\d+)', 'views.showapolicy'),
                        url(r'^updatepolicy$', 'views.updatepolicy'),
                        )

# User control
urlpatterns += patterns('blog.user',
                        url(r'^user/$', 'views.showuser'),
                        url(r'^adduser.html$', 'views.beginAdduser'),
                        url(r'^adduser$', 'views.adduser'),
                        url(r'deleteuser$', 'views.deluByID'),
                        url(r'showuid$', 'views.showUid'),
                        url(r'^updateuser$', 'views.updateuser'),
                        )

# secure_field and secure_class management
urlpatterns += patterns('blog.field_class',
                        url(r'^field/', 'views.showfield'),
                        url(r'^showfields$', 'views.fd'),
                        url(r'^addfield$', 'views.addfield'),
                        url(r'^delfield/id=(\d+)$', 'views.delfield'),
                        url(r'^showfieldid/id=(\d+)$', 'views.showfid'),
                        url(r'^updatefield$', 'views.updatefield'),
                        url(r'^class/', 'views.showclass'),
                        url(r'^showclasses$', 'views.cs'),
                        url(r'^addclass$', 'views.addclass'),
                        url(r'^showclassid/id=(\d+)$', 'views.showcid'),
                        url(r'^updateclass$', 'views.updateclass'),
                        url(r'^delclass/id=(\d+)$', 'views.delclass'),
                        )
