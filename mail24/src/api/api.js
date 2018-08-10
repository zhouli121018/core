import axios from 'axios';


let host = '/api';
//登录
export const login = params => {
    return axios.post(`${host}/login/`, params)
}
  