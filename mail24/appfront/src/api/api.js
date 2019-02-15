import axios from 'axios';
import store from '../store/index';


let host = '/api';
// let host = 'http://192.168.1.39:9999/api';
//登录
export const login = params => { return axios.post(`${host}/login/`, params) }
//获取欢迎页面信息
export const welcome = params => { return axios.get(`${host}/core/welcome/`, { params: params }) }
//锁屏
export const lockscreen = params => { return axios.post(`${host}/core/lockscreen/`,  params ) }
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
export const getMailMessage = params => { return axios.get(`${host}/mail/message/`, { params: params,cancelToken: new axios.CancelToken(function executor(c) {
          store.dispatch('setSourceA',c);
        }) }) }

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
// 删除附件 /api/mail/attach/batchdelete/
export const mailAttachDelete = params => { return axios.post(`${host}/mail/attach/batchdelete/`,params)};
//发信/存草稿 /api/mail/message/sent/
export const mailSent = params =>{ return axios.post(`${host}/mail/message/sent/`,params) };
//下载附件 /api/mail/attach/{id}/
export const downloadAttach = params => { return axios.get(`${host}/mail/attach/0/`, { params: params,responseType:'blob' }) };
//下载来往附件 /api/mail/attach/{id}/
export const downloadAttach2 = (signatureID, params) => { return axios.get(`${host}/mail/attach/`+signatureID+'/', { params: params,responseType:'blob' }) };
// 保存附件到个人网盘
export const moveAttach2Netdisk = params =>{ return axios.post(`${host}/mail/attach/move-to-disk/`,params) };
//下载附件 /api/mail/attach/{id}/
export const downloadZipAttach = params => { return axios.get(`${host}/mail/attach/download/`, { params: params, responseType:'blob' }) };
//文件续期
export const RenewalAttach = (signatureID, params) => { return axios.post(`${host}/mail/attach/`+signatureID+'/renewal/',params) };

//写信  获取当前用户参数设置 /api/setting/users/get-param-bool/
export const getParamBool = params => { return axios.get(`${host}/setting/users/get-param-bool/`) };
//邮件解密 /api/mail/message/password/
export const mailDecode = params =>{ return axios.post(`${host}/mail/message/password/`,params) };
//发送邮件后邮件召回 /api/mail/message/send-recall/
export const sendRecall = params =>{ return axios.post(`${host}/mail/message/send-recall/`,params) };
//查看邮件状态 /api/mail/message/status/
export const getMessageStatus = params => { return axios.get(`${host}/mail/message/status/`, { params: params }) };
//拒收邮件 /api/mail/message/reject/
export const rejectMessage = params =>{ return axios.post(`${host}/mail/message/reject/`,params) };
//彻底（直接）删除邮件 /api/mail/message/prune/
export const pruneMessage = params =>{ return axios.post(`${host}/mail/message/prune/`,params) };
//打包下载邮件 /api/mail/message/zip/
export const zipMessage = params => { return axios.get(`${host}/mail/message/zip/`, { params: params,responseType:'blob'  }) };
//下载某个邮件 /api/mail/message/eml/
export const emlMessage = params => { return axios.get(`${host}/mail/message/eml/`, { params: params,responseType:'blob'  }) };
//添加到个人通讯录 /api/mail/message/pab/
export const pabMessage = params => { return axios.post(`${host}/mail/message/pab/`,  params) };
//查看邮件的 召回邮件 /api/mail/message/recall/
export const messageRecall = params =>{ return axios.post(`${host}/mail/message/recall/`,params) };
//发送回执 /api/mail/message/notify/
export const notifyMessage = params =>{ return axios.post(`${host}/mail/message/notify/`,params) };
//拉取新邮件 /api/mail/message/new/
export const newMessage = () => { return axios.get(`${host}/mail/message/new/`) };
//获取用户模板信列表 /api/setting/template/
export const getTemplateList = (params) => { return axios.get(`${host}/setting/template/`,{params:params}) };
//获取单个模板信 /api/setting/template/{id}/
export const getTemplateById = (id) => { return axios.get(`${host}/setting/template/${id}/`) };
//获取部门邮箱 /api/contact/to/?ctype=oab&cid=0
export const getDeptMail = (params) => { return axios.get(`${host}/contact/to/`,{params:params}) };
//查看邮件页面直接回复 /api/mail/message/reply/
export const replayMessage = params =>{ return axios.post(`${host}/mail/message/reply/`,params) };

//密码重置密码第一步 /api/setting/secret-reset/1/
export const resetSecret1 = params =>{ return axios.post(`${host}/setting/secret-reset/1/`,params) };
//密保重置密码第二步 /api/setting/secret-reset/2/
export const resetSecret2 = params =>{ return axios.post(`${host}/setting/secret-reset/2/`,params) };
//密保重置密码第三步 /api/setting/secret-reset/3/
export const resetSecret3 = params =>{ return axios.post(`${host}/setting/secret-reset/3/`,params) };
//将附件保存到个人网盘 /api/mail/message/save-attach/
export const saveNetAttach = params =>{ return axios.post(`${host}/mail/message/save-attach/`,params) };


/* ***********************  设置中心 *********************** */
// 展现
export const settingShow = params => { return axios.get(`${host}/setting/show/`, { params: params })}
// 获取个人资料
export const settingUsersGet = params => { return axios.get(`${host}/setting/users/get/`, { params: params }) }
// 更新个人资料
export const settingUsersUpdate = params => { return axios.post(`${host}/setting/users/set/`, params) }
// 修改密码
export const settingUsersGetpassword = params => { return axios.get(`${host}/setting/users/get-password/`,  { params: params }) }
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

// 模板信
export const settingTemplateGet = params => { return axios.get(`${host}/setting/template/`, { params: params })}
export const settingTemplateCreate = params => { return axios.post(`${host}/setting/template/`, params)}
export const settingTemplateDelete = signatureID => { return axios.delete(`${host}/setting/template/`+signatureID+'/') }
export const settingTemplateUpdate = (signatureID, params) => { return axios.patch(`${host}/setting/template/`+signatureID+'/', params) }
export const settingTemplateGetSingle = (signatureID, params) => { return axios.get(`${host}/setting/template/`+signatureID+'/', { params: params }) }

// 自动转发、自动回复
export const settingRefwGet = params => { return axios.get(`${host}/setting/refw/`, { params: params })}
export const settingRefwCreate = params => { return axios.post(`${host}/setting/refw/`, params)}
export const settingRefwDelete = signatureID => { return axios.delete(`${host}/setting/refw/`+signatureID+'/') }
export const settingRefwUpdate = (signatureID, params) => { return axios.patch(`${host}/setting/refw/`+signatureID+'/', params) }
export const settingRefwGetSingle = (signatureID, params) => { return axios.get(`${host}/setting/refw/`+signatureID+'/', { params: params }) }

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
///api/core/shareusers/import/
export const settingRelateImport = ( params) => {
  return axios.post(`${host}/core/shareusers/import/`, params, {headers:{ 'Content-Type': 'multipart/form-data' }}) }
//导出关联共享邮箱 /api/core/shareusers/tutorial/
export const settingRelateTutorial = () => { return axios.get(`${host}/core/shareusers/tutorial/`, { responseType:'blob'})  }

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
export const netdiskFileDownload = (signatureID, params) => { return axios.get(`${host}/netdisk/netdisks/`+signatureID+'/download/', { params: params,responseType:'blob' }) };
// zip下载
export const netdiskZipDownload = params => { return axios.get(`${host}/netdisk/netdisks/zip/`, { params: params, responseType:'blob' }) };


// 企业网盘
// 获取文件夹以及文件夹下的文件
export const companyDiskGet = params => { return axios.get(`${host}/netdisk/company/`, { params: params })}
// 获取个人网盘容量
export const companyDiskCapacityGet = params => { return axios.get(`${host}/netdisk/company/capacity/`, { params: params })}
// 获取所有文件夹的路径
export const companyDiskPathGet = params => { return axios.get(`${host}/netdisk/company/paths/`, { params: params })}
// 创建文件夹
export const companyDiskFolderCreate = params => { return axios.post(`${host}/netdisk/company/folders/`, params)}
// 文件夹重命名
export const companyDiskFolderUpdate = (signatureID, params) => { return axios.post(`${host}/netdisk/company/`+signatureID+'/folders/', params) }
// 文件上传
export const companyDiskFileUpload = (params) => { return axios.post(`${host}/netdisk/company/files/`, params, {headers:{ 'Content-Type': 'multipart/form-data' }}) }
// 文件重命名
export const companyDiskFileUpdate = (signatureID, params) => { return axios.post(`${host}/netdisk/company/`+signatureID+'/files/', params) }
// 删除文件或文件夹
export const companyDiskDelete = params => { return axios.post(`${host}/netdisk/company/delete/`, params)}
// 批量删除文件或文件夹
export const companyDiskBatchDelete = params => { return axios.post(`${host}/netdisk/company/batchdelete/`, params)}
// 移动文件或文件夹
export const companyDiskMove = params => { return axios.post(`${host}/netdisk/company/batchmove/`, params)}
// 批量移动文件或文件夹
export const companyDiskBatchMove = params => { return axios.post(`${host}/netdisk/company/batchmove/`, params)}
// 文件下载
export const companyDiskFileDownload = (signatureID, params) => { return axios.get(`${host}/netdisk/company/`+signatureID+'/download/', { params: params,responseType:'blob' }) };
// zip下载
export const companyDiskZipDownload = params => { return axios.get(`${host}/netdisk/company/zip/`, { params: params, responseType:'blob' }) };
//企业网盘添加权限 /api/netdisk/perm/
export const permNetdisk = params => { return axios.post(`${host}/netdisk/perm/`, params)}
//赋予网盘管理员 /api/netdisk/perm/add-super/
export const superNetdisk = params => { return axios.post(`${host}/netdisk/perm/add-super/`, params)}
//获取文件夹树结构 /api/netdisk/company/tree/
export const companyTree = () => { return axios.get(`${host}/netdisk/company/tree/`)}
//文件夹的权限成员列表  /api/netdisk/perm/
export const permList = (params) => { return axios.get(`${host}/netdisk/perm/`,{params:params} )}
//批量删除权限 /api/netdisk/perm/batch-delete/
export const batchDelete = params => { return axios.post(`${host}/netdisk/perm/batch-delete/`, params)}
//更新权限 /api/netdisk/perm/{id}/
export const updatePerm = (id,params) => { return axios.put(`${host}/netdisk/perm/${id}/`, params) };
//删除权限 /api/netdisk/perm/{id}/
export const deletePerm= id => { return axios.delete(`${host}/netdisk/perm/${id}/`) }



//日历
//获取日程列表 /api/calendars/calendars/
export const getCalendarsList = () => { return axios.get(`${host}/schedule/calendars/`)}
//获取具体某个日程信息 /api/calendars/calendars/{id}/
export const getCalendarById = (id) => { return axios.get(`${host}/schedule/calendars/${id}/`)}
//创建日程 /api/calendars/calendars/
export const createCalendar = params => { return axios.post(`${host}/schedule/calendars/`, params) };
//删除日程 /api/calendars/calendars/{id}/    delete
export const deleteCalendar = id => { return axios.delete(`${host}/schedule/calendars/${id}/`) }
//删除共享给我的日程  /api/calendars/calendars/{id}/delete-invitor/
export const deleteInvitorCalendar = id => { return axios.post(`${host}/schedule/calendars/${id}/delete-invitor/`) }
//更新日程  /api/calendars/calendars/{id}/  put
export const updateCalendar = (id,params) => { return axios.put(`${host}/schedule/calendars/${id}/`, params) };
//显示或隐藏共享日程 /api/calendars/calendars/show/
export const showCalendar = params => { return axios.post(`${host}/schedule/calendars/show/`, params) };
//获取事件列表 /api/calendars/events/
export const getEvents = params => { return axios.get(`${host}/schedule/events/`, { params: params }) }
//创建事件  /api/calendars/events/
export const createEvent = params => { return axios.post(`${host}/schedule/events/`, params) };
//获取某个事件 /api/calendars/events/{id}/ get
export const getEventById = (id,process_id) => { return axios.get(`${host}/schedule/events/${id}/`,{params:{process_id:process_id}})}
//修改事件 PUT /api/calendars/events/{id}/
export const updateEvent = (id,params) => { return axios.put(`${host}/schedule/events/${id}/`, params) };
//删除事件 /api/calendars/events/{id}/
export const deleteEvent = id => { return axios.delete(`${host}/schedule/events/${id}/`) }
//取消邀请 /api/calendars/events/{id}/cancel-invitor/
export const cancelInvitorEvent = id => { return axios.post(`${host}/schedule/events/${id}/cancel-invitor/`) }
//修改参与者状态 /api/calendars/events/{id}/status/
export const setStatus = (id,params) => { return axios.post(`${host}/schedule/events/${id}/status/`, {status:params}) };
//根据邮箱获取用户ID，并验证是不是系统内邮箱 /api/calendars/calendars/target_id/
export const getTargetId = params => { return axios.get(`${host}/schedule/calendars/target_id/`, { params: params }) }


//自助查询
//登录查询  /api/center/login/
export const getLoginList = params => { return axios.get(`${host}/center/login/`, { params: params }) }
//发信查询 /api/center/sendlog/
export const getSendlog = params => { return axios.get(`${host}/center/sendlog/`, { params: params }) }
//收信查询 /api/center/maillog/
export const getMaillog = params => { return axios.get(`${host}/center/maillog/`, { params: params }) }
//删信查询  /api/center/deletelog/
export const getDeletellog = params => { return axios.get(`${host}/center/deletelog/`, { params: params }) }


//邮件列表  /api/contact/lab/
export const getContactLab = params => { return axios.get(`${host}/contact/lab/`, { params: params }) }

//分片上传查询 /api/netdisk/upload/check/
export const uploadCheck = params => { return axios.post(`${host}/netdisk/upload/check/`, params) };
//分片上传 /api/netdisk/upload/chunk/
export const uploadChunk = params => { return axios.post(`${host}/netdisk/upload/chunk/`, params,{headers:{ 'Content-Type': 'multipart/form-data' }}) };
//上传成功 /api/netdisk/upload/success/
export const uploadSuccess = params => { return axios.post(`${host}/netdisk/upload/success/`, params) };

//预览文件 /api/netdisk/openoffice/
export const getOpenoffice = params => { return axios.get(`${host}/netdisk/openoffice/`, { params: params }) }

//审核邮件查询 /api/mail/review/
export const mailReview = params => { return axios.get(`${host}/mail/review/`, { params: params }) }
//更新审核邮件状态 /api/mail/review/{id}/
export const updateReview = (id,params) => { return axios.put(`${host}/mail/review/${id}/`, params) };
//批量审核 /api/mail/review/batch/
export const uploadReviews = params => { return axios.post(`${host}/mail/review/batch/`, params) };
//查看审核邮件 /api/mail/review/{id}/
export const readReview = id => { return axios.get(`${host}/mail/review/${id}/`) }
//下载审核邮件真实附件（sid） /api/mail/review/dowload/
export const reviewDowload = params => { return axios.get(`${host}/mail/review/dowload/`, { params: params, responseType:'blob' }) };
//当前用户是否展现审核邮件界面 以及 获取未审核邮件数量 GET /api/mail/review/show/
export const reviewShow = () => { return axios.get(`${host}/mail/review/show/`) }

//清空文件夹 POST /api/mail/message/expunge/
export const messageExpunge = params => { return axios.post(`${host}/mail/message/expunge/`, params) };

//日志查询单个收件人召回 POST /api/mail/message/log-recall/
export const logRecall = params => { return axios.post(`${host}/mail/message/log-recall/`, params) };

//获取登录前设置  /api/core/login-before/
export const loginBefore = params => { return axios.get(`${host}/core/login-before/`,{ params: params }) }
//获取登录后设置 GET /api/core/login-after/
export const loginAfter = () => { return axios.get(`${host}/core/login-after/`)}

//获取单个用户签名 url?replace=1: 表示替换变量 GET /api/setting/signatures/{id}/
export const singleSignatures = id => { return axios.get(`${host}/setting/signatures/${id}/`,{ params: {replace:1} }) }


//日程转为ics文件 GET /api/schedule/events/{id}/ics/
export const eventsIcs = id => { return axios.get(`${host}/schedule/events/${id}/ics/`) }

//用户资料 换肤 POST /api/setting/users/set-skin/
export const setSkin = params => { return axios.post(`${host}/setting/users/set-skin/`, params) };

//获取用户是否开通了谷歌验证、手机短信等两步验证 GET /api/twofactor/show/
export const twofactorShow = () => { return axios.get(`${host}/twofactor/show/`)}
//获取二维码key，以及用作备份密码登录 GET /api/twofactor/google/secret/
export const googleSecret = () => { return axios.get(`${host}/twofactor/google/secret/`)}
//生成动态身份验证二维码 GET /api/twofactor/google/qrcode/
export const googleQrcode = (params) => { return axios.get(`${host}/twofactor/google/qrcode/`,{ params: params })}
//验证扫码二维码是否通过 POST /api/twofactor/google/verify/
export const googleVerify = params => { return axios.post(`${host}/twofactor/google/verify/`, params) };
//解除谷歌验证 POST /api/twofactor/google/release/
export const googleRelease = params => { return axios.post(`${host}/twofactor/google/release/`, params) };
//绑定手机发送短信 POST /api/twofactor/phone/sms/
export const phoneSms = params => { return axios.post(`${host}/twofactor/phone/sms/`, params) };
//绑定手机验证 POST /api/twofactor/phone/verify/
export const phoneVerify = params => { return axios.post(`${host}/twofactor/phone/verify/`, params) };
//解除手机验证 POST /api/twofactor/phone/release/
export const phoneRelease = params => { return axios.post(`${host}/twofactor/phone/release/`, params) };
//解除手机验证发送短信 POST /api/twofactor/phone/release-sms/
export const releaseSms = params => { return axios.post(`${host}/twofactor/phone/release-sms/`, params) };
//用户谷歌验证、手机短信等两步验证 POST /api/twofactor/login/
export const twofactorLogin = params => { return axios.post(`${host}/twofactor/login/`, params) };
//手机短信验证发送验证码 POST /api/twofactor/login/sms/
export const loginSms = params => { return axios.post(`${host}/twofactor/login/sms/`, params) };


//用户申请 协议获取、密码规则、部门获取 GET /api/setting/register/agreement/
export const registerAgreement = params => { return axios.get(`${host}/setting/register/agreement/`,{ params: params })}
//注册申请 POST /api/setting/register/post/
export const register = params => { return axios.post(`${host}/setting/register/post/`, params) };

//语言保存，用于底层使用POST /api/setting/users/set-lang/
export const setLang = () => { return axios.post(`${host}/setting/users/set-lang/`) };

//导出日程 GET /api/schedule/events/{id}/export-ics/
export const exportIcs = id => { return axios.get(`${host}/schedule/events/${id}/export-ics/`, { responseType:'blob' }) };

//邮件全文搜索 GET /api/mail/message/search/
export const mailSearch = (params) => { return axios.get(`${host}/mail/message/search/`,{ params: params })}

//这不是垃圾邮件 POST /api/mail/message/not-spam/
export const notSpam = params => { return axios.post(`${host}/mail/message/not-spam/`, params) };
