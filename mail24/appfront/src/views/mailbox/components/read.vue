<template>
  <article class="mlmain mltabview">
    <div class="mltabview-panel">
      <div class="m-mlwelcome" data-view-cid="view-5" data-view-name="mail.welcome">
        <div class="container">
          读邮件
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
    mounted(){
      readMail(14294);
    }
  }
</script>
