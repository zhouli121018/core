<template>
  <div class="j-module-content j-maillist mllist-list height100 ">

    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>换肤</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>

    <section class="content content-list height100" style="background-color: rgba(255,255,255,0.3);;padding-bottom: 13px;">
        <div style="padding-left:10px;">
          <div class="hC0">主题皮肤</div>
          <div v-for="(m,k) in imgs" :key="k" class="rp0"  :class="{il0:m.url == $store.getters.getSkinOrder}" @click="checkImg(m)" :style="{background:'url(/static/img/'+m.url+'_small.jpg)'}">
            <a class="nd0">
              <b class="ng0 mN1"></b>
              <span class="nk0">{{m.title}}</span>
            </a>
            <div class="lj0 gv0">
              <div class="gu0">
                <b class="nui-ico nui-ico-done nui-ico-done-white"></b>
              </div>
            </div>
          </div>
        </div>

    </section>

  </div>
</template>

<script>
  import cookie from '@/assets/js/cookie';
  import {
    setSkin
  } from '@/api/api'

  export default {
    data() {
      return {
        imgs:[
          {url:'jingdianlan',title:'经典蓝（默认）'},
          {url:'chunzhihua',title:'春之花'},
          {url:'yanyujiangnan',title:'烟雨江南'},
          {url:'hetangyuese',title:'荷塘月色'},
          {url:'qingxinlu',title:'清新绿'},
          {url:'haishuilan',title:'海水蓝'},
          {url:'zhongguofeng',title:'中国风'},
        ]
      }
    },
    mounted: function(){
      // if(this.$store.getters.getSkinOrder && this.$store.getters.getSkinOrder.length>0){
      //   this.checkName = this.$store.getters.getSkinOrder;
      // }
    },
    methods: {
      checkImg(m){
        let param = {skin_name:m.url};
        setSkin(param).then(res=>{
          this.$store.dispatch('setSkinOrderA',m.url)
          this.$message({
            type:'success',
            message:'邮箱皮肤设置成功！'
          })
        }).catch(err=>{
          console.log(err)
        })

      },
    }
  }

</script>
<style>
  .hC0 {
    font-size: 14px;
    color: #999;
    line-height: 34px;
    font-weight: 700;
  }
  .rp0 {
    margin: 0 20px 20px 0;
    width: 200px;
    height: 120px;
    position: relative;
    float: left;
    zoom: 1;
    background: #CCC;
    cursor:pointer;
  }
  .nd0 {
    overflow: hidden;
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
  }
  .nk0 {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    line-height: 2;
    background: #000;
    background: rgba(0,0,0,.5);
    color: #fff;
    text-align: center;
  }
  .il0 .lj0 {
    visibility: visible;
  }

  .lj0 {
    border: #458138 2px solid;
    visibility: hidden;
    width: 196px;
    height: 116px;
    position: absolute;
    left: 0;
    top: 0;
  }
  .gu0 {
    width: 30px;
    height: 30px;
    position: absolute;
    bottom: 0;
    right: 0;
    background: #458138;
  }
  .gu0 .nui-ico {
    margin: 10px 0 0 8px;
  }

  .nui-ico-done-white {
      background: url(/static/img/check.png) no-repeat;
  }
  .nui-ico{
    display: inline-block;
    vertical-align: middle;
    font-family: nui!important;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    line-height: normal!important;
    -webkit-font-smoothing: antialiased;
    font-weight: 400;
    text-align: center;
    line-height: normal;
    overflow: hidden;
    width: 15px;
    height: 12px;
  }
  .nd0:hover {
    border: 2px solid #0F6099;
    left: 0;
    top: 0;
    width: 196px;
    height: 116px;
  }
  .nd0:hover .nk0 {
    bottom: -2px;
  }
</style>
