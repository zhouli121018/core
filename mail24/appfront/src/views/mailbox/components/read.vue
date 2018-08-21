<template>
  <article class="mlmain mltabview">
    <div class="mltabview-panel">
      <div class="m-mlwelcome" data-view-cid="view-5" data-view-name="mail.welcome">
        <div class="container">
          {{msg}}
        </div><!-- end container -->
        <div class="footer small text-gray">Coremail. © Copyright 2000 - 2016 Mailtech.</div>

      </div>
    </div>
  </article>
</template>

<script>
  import {readMail} from '@/api/api';
  export default  {
    name:'Read',
    data(){
      return {
        msg:''
      }
    },
    mounted:function(){
      console.log(this.$route.params.id)
      console.log('innerbox')
      // this.test();
      readMail(this.$route.params.id).then((data)=>{
        // this.msg = data.data.html_text
        this.msg = data.data
      });


    },
  }
</script>
