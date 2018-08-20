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
export const contactPabGroups = params => { return axios.get(`${host}/contact/pabgroup/`, { params: params })}
//删除某个商品的购物记录
export const deleteContactPabGroups = pabGroupsID => { return axios.delete(`${host}/contact/pabgroup/`+pabGroupsID+'/') }
//更新购物车商品信息
// export const updateShopCart = (goodsId, params) => { return axios.patch(`${host}/shopcarts/`+goodsId+'/', params) }

// 获取 当前域 部门数据
export const contactDepartment = params => { return axios.get(`${host}/contact/department/`, { params: params })}
// 获取 企业通讯录 数据
export const contactOab = params => { return axios.get(`${host}/contact/oab/`, { params: params }) }

//获取邮件列表
export const getMailMessage = params => { return axios.get(`${host}/mail/message/`, { params: params }) }

//获取文件夹列表
export const getFloder = params => { return axios.get(`${host}/mail/floder/`, { params: params }) };

//读邮件
export const readMail = params => { return axios.get(`${host}/mail/message/${params}/`) };
