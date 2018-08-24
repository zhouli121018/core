# -*- coding: utf-8 -*-
from django.core.cache import cache

def get_remove_deptid2(dataDept, dpt_id, pid, current_dpt_id):
    if pid not in (0, -1):
        if pid == current_dpt_id:
            return dpt_id
        else:
            pid = dataDept[pid]['parent']
            return get_remove_deptid2(dataDept, dpt_id, pid, current_dpt_id)
        return None
    return None

def get_remove_deptid(dataDept, current_dpt_id):
    ids = []
    for dpt_id, value in dataDept.iteritems():
        if dpt_id == current_dpt_id:
            ids.append(dpt_id)
        else:
            dpt_id2 = get_remove_deptid2(dataDept, dpt_id, dataDept[dpt_id]['parent'], current_dpt_id)
            if dpt_id2:
                ids.append( dpt_id2 )
    for dptid in list(set(ids)):
        del dataDept[dptid]
    return dataDept

def get_dept_list(lists_dpt, current_dpt_id=None):
    dataDept = {}
    for obj in lists_dpt:
        dpt_id = obj.id
        value = {
            "id": dpt_id,
            "name": obj.title,
            "parent": obj.parent_id,
            "order": obj.order,
        }
        dataDept[dpt_id] = value
        # {child: 1, id: 1, parent: 225, name: "四合院事业部"}
    if current_dpt_id:
        current_dpt_id = int(current_dpt_id)
        dataDept = get_remove_deptid(dataDept, current_dpt_id)
    for sub_id in dataDept.keys():
        sub = dataDept[sub_id]
        parent_id = int(sub["parent"])
        if parent_id in (0, -1):
            continue
        if parent_id in dataDept:
            dataDept[parent_id]["child"] = 1
    return [ v for k, v in
             sorted(dataDept.items(), key=lambda v: v[1]['order'], reverse=False)
             ]

def get_cache_dept(domain_id, lists_dpt):
    key = "linux-operation-cache-department:{}".format(domain_id)
    content = cache.get(key, None)
    if not content:
        content = get_dept_list(lists_dpt, None)
        if content:
            cache.set(key, content, 5*3600)
    return content

def clear_cache_dept(domain_id):
    key = "linux-operation-cache-department:{}".format(domain_id)
    cache.delete(key)

def clear_cache_dept_signal(sender, instance, **kwargs):
    # instance = kwargs['instance']
    # domain_id = kwargs['instance'].domain_id
    key = "linux-operation-cache-department:{}".format(instance.domain_id)
    cache.delete(key)


