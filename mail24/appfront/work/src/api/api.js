import axios from 'axios';


let host = '/api';
// let host = 'http://192.168.1.39:9999/api';
//登录
export const login = params => { return axios.post(`${host}/login/`, params) }
//获取欢迎页面信息
export const welcome = params => { return axios.get(`${host}/core/welcome/`, { params: params }) }
//锁屏
export const lockscreen = params => { return axios.post(`${host}/core/lockscreen/`, { params: params }) }
// 设置联系人数据
export const getContactInfo = params => { return axios.get(`${host}/contact/show/`, { params: params }) }

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
//标记
export const messageFlag = params => { return axios.post(`${host}/mail/message/flag/`,params)};
//上传附件 /api/mail/attach/
export const postAttach = (params) => {
  return axios.post(`${host}/mail/attach/`, params, {headers:{ 'Content-Type': 'multipart/form-data' }}) }
// 删除附件
export const deleteAttach = params => {return axios.delete(`${host}/mail/attach/${params}/`)};
//获取附件列表 /api/mail/attach/
export const getAttach = params => { return axios.get(`${host}/mail/attach/`, { params: params }) };
//发信/存草稿 /api/mail/message/sent/
export const mailSent = params =>{ return axios.post(`${host}/mail/message/sent/`,params) };
//下载附件 /api/mail/attach/{id}/
export const downloadAttach = params => { return axios.get(`${host}/mail/attach/0`, { params: params,responseType:'blob' }) };
//下载来往附件 /api/mail/attach/{id}/
export const downloadAttach2 = (signatureID, params) => { return axios.get(`${host}/mail/attach/`+signatureID+'/', { params: params,responseType:'blob' }) };
// 保存附件到个人网盘
export const moveAttach2Netdisk = params =>{ return axios.post(`${host}/mail/attach/move-to-disk/`,params) };
//下载附件 /api/mail/attach/{id}/
export const downloadZipAttach = params => { return axios.get(`${host}/mail/attach/download/`, { params: params, responseType:'blob' }) };

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
// 获取单个用户签名
export const settingSignatureGetSingle = (signatureID, params) => { return axios.get(`${host}/setting/signatures/`+signatureID+'/', { params: params }) }
// 邮箱意见反馈
export const settingFeedbackSet = params => { return axios.post(`${host}/setting/users/set-feedback/`, params) }


// 获取白名单
export const settingWhiteGet = params => { return axios.get(`${host}/setting/whiters/`, { params: params })}
// 创建白名单
export const settingWhiteCreate = params => { return axios.post(`${host}/setting/whiters/`, params)}
// 删除白名单
export const settingWhiteDelete = signatureID => { return axios.delete(`${host}/setting/whiters/`+signatureID+'/') }
// 更新白名单
export const settingWhiteUpdate = (signatureID, params) => { return axios.patch(`${host}/setting/whiters/`+signatureID+'/', params) }
// 更新白名单状态
export const settingWhiteStatusSet = (signatureID, params) => { return axios.post(`${host}/setting/whiters/`+signatureID+'/set-disabled/', params) }
// 获取单个白名单
export const settingWhiteGetSingle = (signatureID, params) => { return axios.get(`${host}/setting/whiters/`+signatureID+'/', { params: params }) }


// 获取黑名单
export const settingBlackGet = params => { return axios.get(`${host}/setting/blackers/`, { params: params })}
// 创建黑名单
export const settingBlackCreate = params => { return axios.post(`${host}/setting/blackers/`, params)}
// 删除黑名单
export const settingBlackDelete = signatureID => { return axios.delete(`${host}/setting/blackers/`+signatureID+'/') }
// 更新黑名单
export const settingBlackUpdate = (signatureID, params) => { return axios.patch(`${host}/setting/blackers/`+signatureID+'/', params) }
// 更新黑名单状态
export const settingBlackStatusSet = (signatureID, params) => { return axios.post(`${host}/setting/blackers/`+signatureID+'/set-disabled/', params) }
// 获取单个黑名单
export const settingBlackGetSingle = (signatureID, params) => { return axios.get(`${host}/setting/blackers/`+signatureID+'/', { params: params }) }


// 邮件召回
export const settingZhaohuiGet = params => { return axios.get(`${host}/setting/zhaohui/`, { params: params })}
// 收件短信通知
export const settingSmsGet = params => { return axios.get(`${host}/setting/users/get-sms/`, { params: params })}
// 设置收件短信通知
export const settingSmsSet = params => { return axios.post(`${host}/setting/users/set-sms/`, params) }
// 获取收件短信通知白名单
export const settingSmsWhiterGet = params => { return axios.get(`${host}/setting/smswhiters/`, { params: params })}
// 创建收件短信通知白名单
export const settingSmsWhiterCreate = params => { return axios.post(`${host}/setting/smswhiters/`, params)}
// 删除收件短信通知白名单
export const settingSmsWhiterDelete = signatureID => { return axios.delete(`${host}/setting/smswhiters/`+signatureID+'/') }
// 更新收件短信通知白名单
export const settingSmsWhiterUpdate = (signatureID, params) => { return axios.patch(`${host}/setting/smswhiters/`+signatureID+'/', params) }
// 更新收件短信通知白名单状态
export const settingSmsWhiterStatusSet = (signatureID, params) => { return axios.post(`${host}/setting/smswhiters/`+signatureID+'/set-disabled/', params) }
// 获取单个收件短信通知白名单
export const settingSmsWhiterGetSingle = (signatureID, params) => { return axios.get(`${host}/setting/smswhiters/`+signatureID+'/', params) }

// 外发邮件中转
export const settingTransferGet = params => { return axios.get(`${host}/setting/transefers/`, { params: params })}
export const settingTransferCreate = params => { return axios.post(`${host}/setting/transefers/`, params)}
export const settingTransferDelete = signatureID => { return axios.delete(`${host}/setting/transefers/`+signatureID+'/') }
export const settingTransferUpdate = (signatureID, params) => { return axios.patch(`${host}/setting/transefers/`+signatureID+'/', params) }
export const settingTransferGetSingle = (signatureID, params) => { return axios.get(`${host}/setting/transefers/`+signatureID+'/', { params: params }) }

// 邮箱搬家
export const settingMovingGet = params => { return axios.get(`${host}/setting/movings/`, { params: params })}
export const settingMovingCreate = params => { return axios.post(`${host}/setting/movings/`, params)}
export const settingMovingDelete = signatureID => { return axios.delete(`${host}/setting/movings/`+signatureID+'/') }
export const settingMovingUpdate = (signatureID, params) => { return axios.patch(`${host}/setting/movings/`+signatureID+'/', params) }
export const settingMovingGetSingle = (signatureID, params) => { return axios.get(`${host}/setting/movings/`+signatureID+'/', { params: params }) }
export const settingMovingReceive = (signatureID, params) => { return axios.post(`${host}/setting/movings/`+signatureID+'/receive/', params) }

// 关联邮箱共享
export const settingRelateGet = params => { return axios.get(`${host}/core/shareusers/`, { params: params })}
export const settingRelateCreate = params => { return axios.post(`${host}/core/shareusers/`, params)}
export const settingRelateDelete = signatureID => { return axios.delete(`${host}/core/shareusers/`+signatureID+'/') }
export const settingRelateGetSingle = (signatureID, params) => { return axios.get(`${host}/core/shareusers/`+signatureID+'/', { params: params }) }
export const settingRelateShared = params => { return axios.get(`${host}/core/shareusers/shared/`, { params: params })}
export const shareLogin = params => { return axios.post(`${host}/share-login/`,params)};
export const backLogin = () => { return axios.post(`${host}/back-login/`)};

// 内容过滤
export const settingFilterGet = params => { return axios.get(`${host}/setting/filters/`, { params: params })}
export const settingFilterCreate = params => { return axios.post(`${host}/setting/filters/`, params)}
export const settingFilterDelete = signatureID => { return axios.delete(`${host}/setting/filters/`+signatureID+'/') }
export const settingFilterUpdate = (signatureID, params) => { return axios.patch(`${host}/setting/filters/`+signatureID+'/', params) }
export const settingFilterGetSingle = (signatureID, params) => { return axios.get(`${host}/setting/filters/`+signatureID+'/', { params: params }) }

// 个人网盘
// 获取文件夹以及文件夹下的文件
export const netdiskGet = params => { return axios.get(`${host}/netdisk/netdisks/`, { params: params })}
// 获取个人网盘容量
export const netdiskCapacityGet = params => { return axios.get(`${host}/netdisk/netdisks/capacity/`, { params: params })}
// 获取所有文件夹的路径
export const netdiskPathGet = params => { return axios.get(`${host}/netdisk/netdisks/paths/`, { params: params })}
// 创建文件夹
export const netdiskFolderCreate = params => { return axios.post(`${host}/netdisk/netdisks/folders/`, params)}
// 文件夹重命名
export const netdiskFolderUpdate = (signatureID, params) => { return axios.post(`${host}/netdisk/netdisks/`+signatureID+'/folders/', params) }
// 文件上传
export const netdiskFileUpload = (params) => { return axios.post(`${host}/netdisk/netdisks/files/`, params, {headers:{ 'Content-Type': 'multipart/form-data' }}) }
// 文件重命名
export const netdiskFileUpdate = (signatureID, params) => { return axios.post(`${host}/netdisk/netdisks/`+signatureID+'/files/', params) }
// 删除文件或文件夹
export const netdiskDelete = params => { return axios.post(`${host}/netdisk/netdisks/delete/`, params)}
// 批量删除文件或文件夹
export const netdiskBatchDelete = params => { return axios.post(`${host}/netdisk/netdisks/batchdelete/`, params)}
// 移动文件或文件夹
export const netdiskMove = params => { return axios.post(`${host}/netdisk/netdisks/batchmove/`, params)}
// 批量移动文件或文件夹
export const netdiskBatchMove = params => { return axios.post(`${host}/netdisk/netdisks/batchmove/`, params)}
// 文件下载
export const netdiskFileDownload = params => { return axios.get(`${host}/netdisk/netdisks/`+signatureID+'/download/', { params: params,responseType:'blob' }) };
// zip下载
export const netdiskZipDownload = params => { return axios.post(`${host}/netdisk/netdisks/zip/`, params, { responseType:'blob' }) };
