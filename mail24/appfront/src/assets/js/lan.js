//设置cookie,增加到vue实例方便全局调用
//vue全局调用的理由是，有些组件所用到的接口可能需要session验证，session从cookie获取
//当然，如果session保存到vuex的话除外
//全局引入vue
import zh_hans from './zh_hans'
import zh_hant from './zh_hant'
import en from './en'
var lan = {
    //简体中文
    zh:zh_hans,

    //繁体中文
    zh_tw:zh_hant,

    //英文
    en:en
  }
  
  export default lan;
