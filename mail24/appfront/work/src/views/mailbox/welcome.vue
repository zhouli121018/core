<template>
    <div>
        <section class="m-mail">
          <MailAside></MailAside>
          <Home></Home>
        </section>
    </div>
</template>
<script>
import router from '@/router'
import Home from './components/home'
import MailAside from './components/MailAside'
export default {
    components:{
      MailAside,
      Home
    },
    data:function(){
        return{


        }
    },
    methods:{

    }
}
</script>

<style>
/*.mltabview-content{*/
    /*top:0!important;*/
/*}*/
</style>
