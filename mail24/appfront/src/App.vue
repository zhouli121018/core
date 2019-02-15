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
  .text_to_password input{
    -webkit-text-security:disc;
    text-security:disc;
  }
  .uploader-file-info .uploader-file-size{
    min-width:66px;
  }
  div.el-dialog__header {
    height: 21px;
    line-height: 21px;
    padding: 9px 18px;
    font-size: 14px;
    border-bottom: 1px solid #e4e4e5;
    font-weight: bold;
    background: #f5f6f7;
 }
  *{
    /*box-sizing:border-box;*/
  }
  .no_border .el-input__inner{
    border:none;
    text-align: right;
  }
  .safe_box .el-tabs__header{
    margin:0;
  }
  .clear:after{
    content:"";
    display:block;
    clear:both;
  }

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    width:100%;
    height:100%;
  }
  .svg_box svg{
    width:126px;
    height:122px;
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
    min-width: 1000px;
    overflow: auto !important;
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
  #treeMenuBar .el-tree-node__content{
    text-align:left;
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
  #app .ke-toolbar{
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
  #app .el-badge__content{
    border:none;
  }
  .uploader-file[status=success] .uploader-file-remove {
       display: block !important;
  }
  /*.uploader-example {*/
    /*width: 100%;*/
    /*box-sizing: border-box;*/
    /*padding: 15px;*/
    /*margin: 10px auto 0;*/
    /*font-size: 12px;*/
    /*box-shadow: 0 0 10px rgba(0, 0, 0, .4);*/
  /*}*/
  /*.uploader-example .uploader-btn {*/
    /*margin-right: 4px;*/
  /*}*/
  /*.uploader-example .uploader-list {*/
    /*max-height: 440px;*/
    /*overflow: auto;*/
    /*overflow-x: hidden;*/
    /*overflow-y: auto;*/
  /*}*/
  .uploader-example .uploader-list{
    /*padding: 15px;*/
    /* margin: 40px auto 0; */
    font-size: 12px;
    box-shadow: 0 0 10px rgba(0, 0, 0, .4);
    /* margin-right: 4px; */
    max-height: 440px;
    overflow: auto;
    overflow-x: hidden;
    overflow-y: auto;
  }
  /*.el-carousel__item h3 {*/
    /*color: #475669;*/
    /*font-size: 14px;*/
    /*opacity: 0.75;*/
    /*line-height: 150px;*/
    /*margin: 0;*/
  /*}*/

  /*.el-carousel__item:nth-child(2n) {*/
     /*background-color: #99a9bf;*/
  /*}*/

  /*.el-carousel__item:nth-child(2n+1) {*/
     /*background-color: #d3dce6;*/
  /*}*/
  .el-pager>li.number{
    display:none !important;
  }
  .el-pager>li.number.active{
    display:inline-block !important;
  }
  @media screen and (max-width:1080px) {
    /*.el-pagination__total,.el-pagination__sizes,.el-pagination__jump,*/
    .el-pagination__jump{
      display:none !important;
    }
  }
  section.m-read .full-info table .info-item, .m-thread .full-info table .info-item{
    width: 70px;
  }
</style>
