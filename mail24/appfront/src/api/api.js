import axios from 'axios';


let host = '/api/api';
// let host = 'http://192.168.1.39:9999/api';
//登录
export const login = params => { return axios.post(`${host}/login/`, params) }
//获取欢迎页面信息
export const welcome = params => { return axios.get(`${host}/core/welcome/`, { params: params }) }
//锁屏
export const lockscreen = params => { return axios.post(`${host}/core/lockscreen/`, { params: params }) }
// 设置联系人数据
export const getContactInfo = params => { return axios.get(`${host}/core/contact/`, { params: params }) }

/* ***********************  个人通讯录 *********************** */
// 获取个人通讯录数据
export const contactPabGroupsGet = params => { return axios.get(`${host}/contact/pab/groups/`, { params: params })}
// 创建个人通讯录数据
export const contactPabGroupsCreate = params => { return axios.post(`${host}/contact/pab/groups/`, params)}
// 删除联系人分组
export const contactPabGroupsDelete = groupID => { return axios.delete(`${host}/contact/pab/groups/`+groupID+'/') }
// 更新联系人分组信息
export const contactPabGroupsUpdate = (groupID, params) => { return axios.patch(`${host}/contact/pab/groups/`+groupID+'/', params) }
// 获取 个人通讯录分组信息 已分组
export const contactPabMapsGet = params => { return axios.get(`${host}/contact/pab/maps/`, { params: params }) }
// 获取 个人通讯录分组信息 未分组
export const contactPabMembersGet = params => { return axios.get(`${host}/contact/pab/members/`, { params: params }) }
// 删除个人通讯录联系人
export const contactPabMembersDelete = contactID => { return axios.delete(`${host}/contact/pab/members/`+contactID+'/') }
// 批量删除个人通讯录
export const contactPabMembersBatchDelete = params => { return axios.post(`${host}/contact/pab/members/batch_delete/`, params) }
// 批量将联系人添加至联系组
export const contactPabMembersDistribute = params => { return axios.post(`${host}/contact/pab/members/distribute_add/`, params) }
// 导出联系人
export const contactPabMembersExport = (groupID, params) => { return axios.get(`${host}/contact/pab/members/`+groupID+'/export/', { responseType:'blob',params: params }) }
// 新增个人通讯录联系人
export const contactPabMembersCreate = params => { return axios.post(`${host}/contact/pab/members/`, params) }
// 修改个人通讯录联系人
export const contactPabMembersUpdate= (contactID, params) => { return axios.patch(`${host}/contact/pab/members/`+contactID+'/', params) }
// 批量将组织通讯录成员添加至个人通讯录
export const contactPabMembersOabAdd = params => { return axios.post(`${host}/contact/pab/members/oab_add/`, params) }
// 批量将公共通讯录成员添加至个人通讯录
export const contactPabMembersCabAdd = params => { return axios.post(`${host}/contact/pab/members/cab_add/`, params) }
// 批量将其他通讯录成员添加至个人通讯录
export const contactPabMembersSoabAdd = params => { return axios.post(`${host}/contact/pab/members/soab_add/`, params) }
// 批量导入邮箱至个人通讯录
export const contactPabMembersImport = (groupID, params) => {
  return axios.post(`${host}/contact/pab/members/`+groupID+'/import/', params, {headers:{ 'Content-Type': 'multipart/form-data' }}) }

/* ***********************  组织通讯录 *********************** */
// 获取 当前域 部门数据
export const contactOabDepartsGet = params => { return axios.get(`${host}/contact/oab/departs/`, { params: params })}
// 获取 企业通讯录 数据
export const contactOabMembersGet = params => { return axios.get(`${host}/contact/oab/members/`, { params: params }) }
// 导出联系人
export const contactOabMembersExport = (departID, params) => { return axios.get(`${host}/contact/oab/members/`+departID+'/export/', { responseType:'blob',params: params }) }
// 导出Foxmail格式
export const contactOabMembersFoxmailExport = (departID, params) => { return axios.get(`${host}/contact/oab/members/`+departID+'/foxmail/', { responseType:'blob',params: params }) }
// 导出Outlook格式
export const contactOabMembersOutlookExport = (departID, params) => { return axios.get(`${host}/contact/oab/members/`+departID+'/outlook/', { responseType:'blob',params: params }) }
// 导出Outlook格式
export const contactOabMembersTutorialExport = (departID, params) => { return axios.get(`${host}/contact/oab/members/tutorial/`, { responseType:'blob',params: params }) }

/* ***********************  公共通讯录 *********************** */
// 公共通讯录分类
export const contactCabGroupsGet = params => { return axios.get(`${host}/contact/cab/groups/`, { params: params }) }
// 公共通讯录成员
export const contactCabMembersGet = params => { return axios.get(`${host}/contact/cab/members/`, { params: params }) }

/* ***********************  其他域通讯录 *********************** */
// 其他域通讯录 域名
export const contactSoabDomainsGet = params => { return axios.get(`${host}/contact/soab/domains/`, { params: params }) }
// 其他域通讯录 部门
export const contactSoabGroupsGet = (domainID, params) => { return axios.get(`${host}/contact/soab/domains/`+domainID+'/groups/', { params: params }) }
// 其他域通讯录 成员
export const contactSoabMembersGet = params => { return axios.get(`${host}/contact/soab/members/`, { params: params }) }


/* ***********************  邮件列表 *********************** */
//获取邮件列表
export const getMailMessage = params => { return axios.get(`${host}/mail/message/`, { params: params }) }

//获取文件夹列表
export const getFloder = params => { return axios.get(`${host}/mail/folder/`, { params: params }) };
//获取某文件夹数据
export const getFloderMsg = params => { return axios.get(`${host}/mail/folder/${params}/`) };

//读邮件
export const readMail = (params,folder) => { return axios.get(`${host}/mail/message/${params}/`,{params:folder}) };
// 删除邮件
export const deleteMail = params => {return axios.post(`${host}/mail/message/delete/`,params)};
// 创建文件夹
export const creatFolder = params => {return axios.post(`${host}/mail/folder/`,params)}
// 删除文件夹
export const deleteFolder = params => {return axios.delete(`${host}/mail/folder/${params}/`)};
// 移动邮件
export const moveMails = params => {return axios.post(`${host}/mail/message/move/`,params)}




/* ***********************  设置中心 *********************** */
// 展现
export const settingShow = params => { return axios.get(`${host}/setting/show/`, { params: params })}
// 获取个人资料
export const settingUsersGet = params => { return axios.get(`${host}/setting/users/get/`, { params: params }) }
// 更新个人资料
export const settingUsersUpdate = params => { return axios.post(`${host}/setting/users/set/`, params) }
// 修改密码
export const settingUsersSetpassword = params => { return axios.post(`${host}/setting/users/set-password/`, params) }
// 获取密保
export const settingUsersGetSecurity = params => { return axios.get(`${host}/setting/users/get-security/`, { params: params }) }
// 设置密保
export const settingUsersSetSecurity = params => { return axios.post(`${host}/setting/users/set-security/`, params) }
// 获取参数
export const settingUsersGetParam = params => { return axios.get(`${host}/setting/users/get-param/`, { params: params }) }
// 设置参数
export const settingUsersSetParam = params => { return axios.post(`${host}/setting/users/set-param/`, params) }
// 获取注销申请
export const settingUsersGetCancel = params => { return axios.get(`${host}/setting/users/get-cancel/`, { params: params }) }
// 设置注销申请
export const settingUsersSetCancel = params => { return axios.post(`${host}/setting/users/set-cancel/`, params) }
// 获取签名列表
export const settingSignatureGet = params => { return axios.get(`${host}/setting/signatures/`, { params: params })}
// 创建签名
export const settingSignatureCreate = params => { return axios.post(`${host}/setting/signatures/`, params)}
// 删除签名
export const settingSignatureDelete = signatureID => { return axios.delete(`${host}/setting/signatures/`+signatureID+'/') }
// 更新签名
export const settingSignatureUpdate = (signatureID, params) => { return axios.patch(`${host}/setting/signatures/`+signatureID+'/', params) }
// 更新签名默认值
export const settingSignatureDefaultlSet = params => { return axios.post(`${host}/setting/signatures/set-default/`, params) }
