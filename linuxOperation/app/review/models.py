# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals

import json
from django.db import models
from django.utils.translation import ugettext_lazy as _

from app.review import constants
from app.core.models import Mailbox, Department

class Review(models.Model):
    """
    主审、副审、下一级审核人
    """
    name = models.CharField(_(u'审核人'), max_length=250, null=False, blank=True)
    # next = models.ForeignKey('self', null=True, blank=True, db_index=True, help_text=u'下一级审核')
    next_id = models.IntegerField(_(u'下一级审核'), default=0)
    master_review = models.ForeignKey(Mailbox, related_name='master_review', db_column='master_review',
                                    on_delete=models.SET_NULL, db_index=True, null=True, blank=True, verbose_name=_(u"主审"))
    assist_review = models.IntegerField(_(u'副审'), default=0, db_column='assist_review')
    wait_next_time = models.IntegerField(_(u'自动转换等待时间'), default=0, help_text=u'自动把副审转换为审核人的等待时间，单位为分钟，=0为永不转移')

    def __unicode__(self):
        return self.name

    class Meta:
        managed = False
        db_table = u'ext_review_new'
        verbose_name = _(u'审核人列表')

    def delete(self, using=None, keep_parents=False):
        super(Review, self).delete(using=using, keep_parents=keep_parents)

    def foundWithoutEcludeIDs(self):
        exclude_ids=set()
        exclude_ids.add(self.id)
        parent_objs = Review.objects.filter(next_id=self.pk)
        Review.loopParentFoundRootID(parent_objs, exclude_ids)
        return Review.objects.exclude(id__in=exclude_ids)

    @staticmethod
    def check_master_review(obj):
        try:
            return obj.master_review
        except:
            return ""

    @staticmethod
    def check_assist_review(obj):
        try:
            if obj.assist_review <=0:
                return ""
            obj = Mailbox.objects.filter(id=obj.assist_review).first()
            return obj if obj else ""
        except Exception,err:
            return "None"

    @staticmethod
    def loopParentFoundRootID(parent_objs, exclude_ids):
        if not parent_objs:
            return exclude_ids
        for obj in parent_objs:
            exclude_ids.add(obj.id)
            parent_objs = Review.objects.filter(next_id=obj.pk)
            Review.loopParentFoundRootID(parent_objs, exclude_ids)
        return exclude_ids


    @staticmethod
    def getReviewList():
        lists = []
        next_ids = Review.objects.filter(next_id__gt=0).values_list('next_id', flat=True)
        firstReviewLists = Review.objects.exclude(id__in=next_ids)
        for obj in firstReviewLists:
            level = 0
            pk = '{}'.format(obj.id)
            lists.append(
                # id, pid, level, name, master, assist, wait_time, real_id
                ( pk, '0', level, obj.name, Review.check_master_review(obj), Review.check_assist_review(obj), obj.wait_next_time, obj.id),
            )
            Review.loopChildLists(obj, obj.id, pk, level, lists)
        return lists

    @staticmethod
    def loopChildLists(obj, id, pid, level=0, lists=None):
        next_pk = obj.next_id
        next_obj = Review.objects.filter(pk=next_pk).first()
        if not next_obj:
            return lists
        level += 1
        pk = '{}_{}'.format(pid, next_pk)
        lists.append(
            # id, pid, level, name, master, assist, wait_time, real_id
            (pk, pid, level, next_obj.name, Review.check_master_review(next_obj), Review.check_assist_review(next_obj), next_obj.wait_next_time, next_pk)
        )
        return Review.loopChildLists(next_obj, next_pk, pk, level, lists)


class ReviewRule(models.Model):
    """
    审核规则表
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, db_index=True, null=False, blank=False, verbose_name=_(u"审核人"))
    name = models.CharField(_(u'规则名称'), max_length=250, null=False, blank=True)
    workmode = models.CharField(_(u'审核类型'), max_length=20, choices=constants.REVIEWRULE_WORKMODE, default='outbount')
    cond_logic = models.CharField(_(u'逻辑条件'), max_length=20, choices=constants.REVIEWRULE_LOGIC, default='all')
    pre_action = models.CharField(_(u'审核预设'), max_length=20, null=True, blank=True, choices=constants.REVIEWRULE_PREACTION)
    # target_dept 目前作为兼容字段存在
    target_dept = models.IntegerField(_(u'发信人部门'), default=0, help_text=u'需要审核的部门ID')
    sequence = models.IntegerField(_(u'权重'), default=999, help_text=u'数值越小优先级越高,数值相等时主键越小优先级越高')
    disabled = models.IntegerField(_(u'状态'), default=-1, choices=constants.REVIEWRULE_DISABLED)

    def __unicode__(self):
        return self.name

    class Meta:
        managed = False
        db_table = u'ext_review_new_rule'
        verbose_name = _(u'审核规则')

    @property
    def department(self):
        obj = Department.objects.filter(pk=self.target_dept).first()
        return obj and obj.title or ''

    @property
    def getConditionDesc(self):
        lists = []
        rule_list = ReviewCondition.objects.filter(rule=self).order_by('id')
        options = dict(constants.REVIEWRULE_OPTION_TYPE)
        actions = dict(constants.REVIEWRULE_OPTION_CONDITION_ACTION_ALL)
        for obj in rule_list:
            if obj.option in ("sender_dept","cc_dept","rcpt_dept"):
                try:
                    v = json.loads(obj.value)
                    v = {} if not isinstance(v, dict) else v
                except:
                    v = {}
                dept_id = v.get("id","-1")
                dept_id = int(dept_id) if (dept_id and str(dept_id).isdigit()) else -1
                dept_name = Department.objects.filter(id=dept_id).first()
                dept_name = dept_name.title if dept_name else u"已删除部门_{}".format(dept_id)
                dept_sub = u"包含子部门" if v.get("sub","-1") == "1" else u"仅当前部门"
                desc = dept_name + u" , " + dept_sub
                value = (options.get(obj.option, ''), actions.get(obj.action, ''), desc)
            else:
                value = ( options.get(obj.option, ''), actions.get(obj.action, ''), obj.value )
            lists.append( value )
        return lists

    def getConditionList(self):
        def getCond(obj_cond, is_sub=0):
            if obj_cond.option in ("sender_dept","cc_dept","rcpt_dept"):
                try:
                    value = json.loads(obj_cond.value)
                    value = {} if not isinstance(value, dict) else value
                except:
                    value = {}
                dept_id = value.get("id","-1")
                dept_id = int(dept_id) if (dept_id and str(dept_id).isdigit()) else -1
                dept_name = Department.objects.filter(id=dept_id).first()
                dept_name = dept_name.title if dept_name else u"已删除部门_{}".format(dept_id)
                desc = dept_name
            else:
                try:
                    value = json.loads(obj_cond.value)
                except:
                    value = obj_cond.value
                desc = value
            data = {
                "id"        :   obj_cond.id,
                "option"    :   obj_cond.option,
                "action"    :   obj_cond.action,
                "value"     :   value,
                "value_desc":   desc,
            }
            if not is_sub:
                data["rule_id"] = self.id
                data["logic"]   = obj_cond.logic
                data["sub"]     = []
            return data
        #end def
        lists = []
        cond_list = ReviewCondition.objects.filter(rule=self, parent_id=0).order_by('id')
        for obj in cond_list:
            info = getCond(obj, is_sub=0)
            for obj_sub in obj.get_sub_conditions():
                info["sub"].append( getCond(obj_sub, is_sub=1) )
            lists.append( info )
        return lists

    def getNoInputOptionList(self):
        return dict(constants.REVIEWRULE_OPTION_NO_INPUT).values()

class ReviewCondition(models.Model):
    rule = models.ForeignKey(ReviewRule, on_delete=models.CASCADE, db_index=True, null=False, blank=False, verbose_name=_(u"审核规则"))
    parent_id = models.IntegerField(blank=True, null=True, default=0, verbose_name=_(u"审核父条件"))
    logic = models.CharField(u'子条件逻辑关系', max_length=20, choices=constants.REVIEWRULE_LOGIC, default='all')
    option = models.CharField(_(u'条件'), max_length=50, null=True, blank=True)
    action = models.CharField(_(u'匹配动作'), max_length=20, null=True, blank=True)
    value = models.CharField(_(u'参数'), max_length=250, null=True, blank=True)

    class Meta:
        managed = False
        db_table = u'ext_review_new_condition'
        verbose_name = _(u'审核条件')

    def get_sub_conditions(self):
        return ReviewCondition.objects.filter(parent_id=self.id).all().order_by("id")

class ReviewMail(models.Model):
    """
    原审核邮件存放表
    """
    subject = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        managed = False
        db_table = u'ext_review_mail'
        verbose_name = _(u'审核邮件列表')


class ReviewProcess(models.Model):
    """
    审核进度表，表明当前某个邮件现在是给谁在审核
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, db_index=True, null=False, blank=False, db_column='review_id')
    mail = models.ForeignKey(ReviewMail, on_delete=models.CASCADE, null=True, blank=True, db_column='mail_id')
    reviewer = models.ForeignKey(Mailbox, on_delete=models.CASCADE, null=True, blank=True, db_column='reviewer_id')
    status = models.CharField(max_length=20, default='wait', choices=constants.REVIEWPROCESS_STATUS)
    start_time = models.DateTimeField(_(u'创建时间'), auto_now_add=True)
    last_update = models.DateTimeField(_(u'更新时间'), auto_now=True)

    class Meta:
        managed = False
        db_table = u'ext_review_new_process'
        unique_together = ((u'review', u"mail"),)
        verbose_name = _(u'审核进度')


class ReviewConfig(models.Model):
    """
    服务器综合设置表
    """
    domain_id = models.IntegerField(_(u'域名ID'), default=0, help_text=u'域名ID',db_column='domain_id')
    co_type = models.CharField(_(u'类型'),max_length=20, blank=True, db_column='type')
    item = models.CharField(_(u'键'),max_length=35, blank=True, db_column='item')
    value = models.TextField(_(u'值'),null=True, blank=True, db_column='value')

    class Meta:
        managed = False
        db_table = 'core_domain_attr'
        unique_together = (
            ('domain_id', 'co_type','item')
        )
        verbose_name = _(u'审核配置')

    @staticmethod
    def use_review_new():
        obj = ReviewConfig.objects.filter(item="sw_use_review_new",co_type="system",domain_id=0).first()
        if not obj:
            obj = ReviewConfig.objects.create(
                item="sw_use_review_new", co_type="system",
                domain_id=0, value='0',
            )
        return obj

    @staticmethod
    def open_review_new():
        obj = ReviewConfig.objects.filter(item="sw_use_review_new",co_type="system",domain_id=0).first()
        if not obj:
            obj = ReviewConfig.objects.create(
                item="sw_use_review_new", co_type="system",
                domain_id=0, value='1',
            )
        obj.value = "1"
        obj.save()
        return obj

    @staticmethod
    def result_notify_option():
        obj = ReviewConfig.objects.filter(item="review_notify_result",co_type="system",domain_id=0).first()
        if not obj:
            obj = ReviewConfig.objects.create(
                item="review_notify_result",
                co_type="system",
                domain_id=0,
                value=constants.REVIEWCONFIG_RESULT_NOTIFY_DEFAULT,
            )
        return obj

    @staticmethod
    def reviewer_notify_option():
        obj = ReviewConfig.objects.filter(item="reviewer_no_mail",co_type="system",domain_id=0).first()
        if not obj:
            obj = ReviewConfig.objects.create(
                item="reviewer_no_mail",
                co_type="system",
                domain_id=0,
                value=constants.REVIEWCONFIG_REVIEWER_NOTIFY_DEFAULT,
            )
        return obj

from auditlog.registry import auditlog
auditlog.register(Review,include_fields=['id','name','next_id','master_review','assist_review','wait_next_time'])
auditlog.register(ReviewRule,include_fields=['id','name','workmode','cond_logic','pre_action','target_dept','sequence','disabled'])
auditlog.register(ReviewConfig,include_fields=['id','domain_id','co_type','item','value'])
