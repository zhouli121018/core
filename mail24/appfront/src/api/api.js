import axios from 'axios';


let host = '/api/api';
//登录
export const login = params => { return axios.post(`${host}/login/`, params) }

//获取欢迎页面信息
export const welcome = params => { return axios.get(`${host}/core/welcome/`, { params: params }) }

export const lockscreen = params => { return axios.post(`${host}/core/lockscreen/`, { params: params }) }

// 获取 当前域 部门数据
export const contactDepartment = params => { return axios.get(`${host}/contact/department/`, { params: params })}

// 获取 企业通讯录 数据
export const contactOab = params => { return axios.get(`${host}/contact/oab/`, { params: params }) }

export const getMailMessage = params => { return axios.get(`${host}/mail/message/`, { params: params }) }
