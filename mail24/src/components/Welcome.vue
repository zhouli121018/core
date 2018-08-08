<template>
  <div class="welcome_box">
      <div class="mlsidebar">
          <Menubar></Menubar>
      </div>
      <div class="mlmain">
            <router-view></router-view>    
      </div>
  </div>
</template>
<script>
import store from '../store'
export default {
    data() {
        return {
        }
      },
      // 计算属性
      computed: {
        list() { // 获取store中的数据
            return this.$store.state.isLogin;
        }
      },
      beforeMounted:function(){
          console.log(this.$store.state)
        //   if(!this.list){
        //       router.push('/login')
        //   }else{
        //       router.push('/welcome')
        //   }
     }   
}
</script>
<style>
.welcome_box{
    width:100%;
    height:100%;
    position:relative;
}
.mlsidebar {
    position: relative;
    width: 199px;
    height: 100%;
    border-right: 1px solid #d4d7d9;
    text-align: center;
}
.mlmain {
    position: absolute;
    left: 200px;
    right: 0;
    top: 0;
    bottom: 0;
}
</style>

