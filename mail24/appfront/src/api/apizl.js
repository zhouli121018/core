import axios from 'axios';


let host = '/api/api';
//登录
export const login = params => { return axios.post(`${host}/login/`, params) }

//获取欢迎页面信息
export const welcome = params => { return axios.get(`${host}/core/welcome/`, { params: params }) }

//锁屏
export const lockscreen = params => { return axios.post(`${host}/core/lockscreen/`, { params: params }) }

// 获取个人通讯录组
// 获取个人通讯录数据
export const contactPabGroupsGet = params => { return axios.get(`${host}/contact/pab/groups/`, { params: params })}
// 删除联系人分组
export const contactPabGroupsDelete = groupID => { return axios.delete(`${host}/contact/pab/groups/`+groupID+'/') }
// 更新联系人分组信息
export const contactPabGroupsUpdate = (groupID, params) => { return axios.patch(`${host}/contact/pab/groups/`+groupID+'/', params) }
// 获取联系人分组下的列表( 未分组， 已分组 )
export const contactPabGroupsTransformGet = (groupID, params) => { return axios.get(`${host}/contact/pab/transform/`+groupID+'/', { params: params })}
// 获取 个人通讯录分组信息
export const contactPabMembersGet = params => { return axios.get(`${host}/contact/pab/members/`, { params: params }) }

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
