<template>
  <div>
    {{msg}}
  </div>
</template>

<script>
  import router from '@/router'
export default{
  data(){
    return{
      msg:'rrread'
    }
  },
  mounted(){
    this.msg = this.$route.params.id
  },
  watch: {
      $route: function (val) {
        this.msg = this.$route.params.id;
      },
    }

}
</script>
