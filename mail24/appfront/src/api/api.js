import axios from 'axios';


let host = '/api/api';
//登录
export const login = params => { return axios.post(`${host}/login/`, params) }
//获取欢迎页面信息
export const welcome = params => { return axios.get(`${host}/core/welcome/`, { params: params }) }
//锁屏
export const lockscreen = params => { return axios.post(`${host}/core/lockscreen/`, { params: params }) }
// 设置联系人数据
export const getContactInfo = params => { return axios.get(`${host}/core/contactinfo/`, { params: params }) }

// 获取个人通讯录组
// 获取个人通讯录数据
export const contactPabGroupsGet = params => { return axios.get(`${host}/contact/pab/groups/`, { params: params })}
// 创建个人通讯录数据
export const contactPabGroupsCreate = params => { return axios.post(`${host}/contact/pab/groups/`, params)}
// 删除联系人分组
export const contactPabGroupsDelete = groupID => { return axios.delete(`${host}/contact/pab/groups/`+groupID+'/') }
// 更新联系人分组信息
export const contactPabGroupsUpdate = (groupID, params) => { return axios.patch(`${host}/contact/pab/groups/`+groupID+'/', params) }
// 获取 个人通讯录分组信息 已分组
export const contactPabMembersGet = params => { return axios.get(`${host}/contact/pab/members/`, { params: params }) }
// 获取 个人通讯录分组信息 未分组
export const contactPabMembersNoGet = params => { return axios.get(`${host}/contact/pab/members/no/`, { params: params }) }
// 删除个人通讯录联系人
export const contactPabMembersNoDelete = contactID => { return axios.delete(`${host}/contact/pab/members/no/`+contactID+'/') }
// 批量删除个人通讯录
export const contactPabMembersNoBatchDelete = params => { return axios.post(`${host}/contact/pab/members/no/batch_delete/`, params) }
// 批量将联系人添加至联系组
export const contactPabMembersNoDistribute = params => { return axios.post(`${host}/contact/pab/members/no/distribute_add/`, params) }
// 导出联系人
export const contactPabMembersNoExport = (groupID, params) => { return axios.get(`${host}/contact/pab/members/no/`+groupID+'/export/', { params: params }) }
// 新增个人通讯录联系人
export const contactPabMembersNoCreate = params => { return axios.post(`${host}/contact/pab/members/no/`, params) }
// 修改个人通讯录联系人
export const contactPabMembersNoUpdate= (contactID, params) => { return axios.patch(`${host}/contact/pab/members/no/`+contactID+'/', params) }

// 获取 当前域 部门数据
export const contactOabDepartsGet = params => { return axios.get(`${host}/contact/oab/departs/`, { params: params })}
// 获取 企业通讯录 数据
export const contactOabMembersGet = params => { return axios.get(`${host}/contact/oab/members/`, { params: params }) }

//获取邮件列表
export const getMailMessage = params => { return axios.get(`${host}/mail/message/`, { params: params }) }

//获取文件夹列表
export const getFloder = params => { return axios.get(`${host}/mail/floder/`, { params: params }) };

//读邮件
export const readMail = params => { return axios.get(`${host}/mail/message/${params}/`) };
