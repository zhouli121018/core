<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
  import store from './store'
  export default {
    name: 'App',
    mounted:function(){
      // console.log(this.$store);
    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    width:100%;
    height:100%;
  }
  body,html{
    padding:0;
    margin:0;
    width:100%;
    height:100%;
    font-size: 14px;
    line-height: 1.42857143;
    color: #333;
    background-color: #fff;
    /*overflow: hidden;*/
    min-width: 980px;
    overflow: auto;
  }
  ul,li,p,h1,h2,h3,h4{
    padding:0;
    margin:0;
  }
  ul,li{
    list-style:none;
  }
  .fl_r{
    float:right;
  }
  .fl_l{
    float:left;
  }
  .vibility_hide{
    visibility: hidden;
  }
  .vibility_show{
    visibility: visible;
  }
  #app .el-tree-node__content{
    height:36px;
  }
  .toolbar {
    background: #f2f2f2;
    /*padding: 10px;*/
    border-bottom: 1px solid #dfe6ec;
    /*margin: 10px 0px;*/
    padding-left: 10px;
    padding-right: 10px;
  }
  /*.el-form-item {*/
    /*margin-bottom: 10px;*/
  /*}*/
  .breadcrumb-container {
    margin-top: 7px;
    margin-bottom: 7px;
    margin-left: 7px;
  }
  /*修改editor toolbar 背景颜色*/
  .ke-toolbar{
    background:#fff;
    font-size:16px;
  }
  .compose_editor .ke-toolbar>span{
    margin:6px 4px;
  }
  .ke-dialog-body .ke-textarea{
    border-color:#e0e0e0;
  }
  .ke-dialog-header{
    background:#f5f6f7;
  }
  .ke-button-common{
    background:#057ab8;
    color:#fff;
    border-color:#057ab8;
  }
  .inline_block{
    display:inline-block;
  }
  .el-table{
    color:#222;
  }
  .clear:after{
    content:"";
    display:block;
    clear:both;
  }
  .vertical_align_top td{
    vertical-align:top;
  }
  .plan_style{
    font-size: 12px;
    color: #777;
  }
  .text-center{
    text-align:center;
  }

</style>
