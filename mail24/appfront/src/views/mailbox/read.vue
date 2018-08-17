<template>
    <div>
        <section class="m-mail">
          <MailAside></MailAside>
          <Read></Read>
        </section>
    </div>
</template>

<script>
import router from '@/router'
import Read from './components/read'
import MailAside from './components/MailAside'
export default {
    components:{
      MailAside,
      Read
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
