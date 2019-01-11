<template>
  <div style="height:100%;overflow: auto;">
    <pre v-text="message" style="padding:10px;"></pre>
  </div>
</template>

<script>

  import {readMail} from '@/api/api';
  export default  {
    name:'message-info',

    data(){
      return{
        message:'',
        loding:false,
      }
    },
    methods:{
      getReadMail(){
        let uid = this.$route.params.uid;
        let params = this.$route.query;
        readMail(uid,params).then(res=>{
          let value = res.data;
          let reg = new RegExp("\r\n", "g");//g,表示全部替换
          this.message = value;
        }).catch(err=>{
          console.log(err)
        })

      }
    },
    created:function(){
      this.getReadMail();

    },
  }
</script>
