//设置cookie,增加到vue实例方便全局调用
//vue全局调用的理由是，有些组件所用到的接口可能需要session验证，session从cookie获取
//当然，如果session保存到vuex的话除外
//全局引入vue
var lan = {
    //简体中文
    zh_hans:{
      user_login:'用户登录',
      user_name:'用户名',
      placeholder_user_name:'请输入用户名',
      please_choose:'请选择',
      password:'密码',
      forget_password:'忘记密码？',
      login:'登 录',
      reset_password:'重置密码',
      placeholder_validation_code:'请输入验证码: ',
      cancel:'取 消',
      sure:'确 定',
      new_password:'新密码',
      confirm_password:'确认密码',
      condition_title:'密码必须满足以下条件：',
      password_length:'密码长度为',
      to_16:'至 16 位；',
    },

    //繁体中文
    zh_hant:{
      user_login:'用戶登錄',
      user_name:'用户名',
      placeholder_user_name:'請輸入用戶名',
      please_choose:'請選擇',
      password:'密碼',
      forget_password:'忘記密碼？',
      login:'登 入',
      reset_password:'重置密碼',
      placeholder_validation_code:'請輸入驗證碼：',
      cancel:'取 消',
      sure:'確 定',
      new_password:'新密碼',
      confirm_password:'確認密碼',
      condition_title:'密碼必須滿足以下條件：',
      password_length:'密碼長度為',
      to_16:'至 16 比特；'
    },

    //英文
    en:{
      user_login:'User login',
      user_name:'User name',
      placeholder_user_name:'enter one user name',
      please_choose:'Please choose',
      password:'Password',
      forget_password:'Forget password?',
      login:'Sign in',
      reset_password:'reset password',
      placeholder_validation_code:'Please enter the validation code:',
      cancel:'cancel',
      sure:'Sure?',
      new_password:'New password',
      confirm_password:'Confirm password',
      condition_title:'The password must satisfy the following conditions:',
      password_length:'The length of the password is',
      to_16:'To 16 place;'
    }
  }
  
  export default lan;
