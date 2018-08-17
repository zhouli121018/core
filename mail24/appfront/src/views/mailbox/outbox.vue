<template>
    <div>
        <section class="m-mail">
          <MailAside></MailAside>
          <Outbox></Outbox>
        </section>
    </div>
</template>

<script>
import router from '@/router'
import Outbox from './components/outbox'
import MailAside from './components/MailAside'
export default {
    components:{
      MailAside,
      Outbox
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
