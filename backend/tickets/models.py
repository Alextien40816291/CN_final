# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from common.models import BaseModel
from workflows.models import *
from systems.models import User


class Ticket(BaseModel):
    """
    工单记录
    """
    name = models.CharField(u'标题', max_length=112, blank=True, default='')
    sn = models.CharField(u'流水号', max_length=25, blank=True, help_text="工单的流水号")
    create_user = models.ForeignKey(User, verbose_name='创建者', blank=True, null=True, on_delete=models.SET_NULL)
    participant = models.CharField('当前处理人', max_length=50, default='', blank=True)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name='工作流')
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='当前状态')
    transition = models.ForeignKey(Transition, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='进行状态')
    customfield = models.TextField('所有表单数据', default=[])
    relation = models.TextField('工单关联人', default='', blank=True, help_text='创建人、处理人，用于查询')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工单记录'
        verbose_name_plural = verbose_name


intervene_type = {
    0: '转交操作',
    1: '接单操作',
    2: '评论操作',
    3: '删除操作',
    4: '强制关闭操作',
    5: '强制修改状态操作',
    6: '撤回',
}


class TicketFlowLog(BaseModel):
    """
    工单流转日志
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='工单')
    suggestion = models.CharField('审批意见', max_length=140, blank=True)
    transition = models.ForeignKey(Transition, on_delete=models.CASCADE, verbose_name='流转')
    participant = models.CharField('处理人', max_length=50, default='', blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='当前状态')
    intervene_type = models.CharField(max_length=1, choices=tuple(intervene_type.items()), default=0,
                                      verbose_name='干预类型')

    class Meta:
        verbose_name = '工单流转日志'
        verbose_name_plural = verbose_name


field_type = {
    10: '字符串',
    15: '整形',
    20: '浮点型',
    25: '布尔',
    30: '日期',
    35: '时间',
    40: '日期时间',
    45: '单选框',
    50: '多选框',
    55: '下拉列表',
    60: '多选下拉列表',
    65: '文本域',
    70: '用户名',
    75: '多选的用户名',
}


class TicketCustomField(BaseModel):
    """
    工单自定义字段， 工单自定义字段实际的值。
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='工单')
    customfield = models.ForeignKey(CustomField, on_delete=models.CASCADE, verbose_name='字段')
    field_value = models.TextField('字段值', default='', blank=True)

    class Meta:
        verbose_name = '工单自定义字段值'
        verbose_name_plural = verbose_name


class TicketUser(BaseModel):
    """
    工单关系人, 用于加速待办工单及关联工单列表查询
    """
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.SET_NULL)
    username = models.CharField('关系人', max_length=100)
    in_process = models.BooleanField('待处理中', default=False)
    worked = models.BooleanField('处理过', default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '工单关系人'
        verbose_name_plural = verbose_name
