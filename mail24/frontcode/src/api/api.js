import axios from 'axios';


let host = '/api';
//登录
export const login = params => {
    return axios.post(`${host}/login/`, params)
}
  
//获取欢迎页面信息
export const welcome = params => {
    return axios.get(`${host}/welcome/`)
}

export const lockscreen = params => {
    return axios.post(`${host}/api/lockscreen/`)
}
