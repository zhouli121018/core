<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="toolbar" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>外发邮件中转</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">

    </section>
  </div>
</template>
<script>
  import {settingUsersGetParam, settingUsersSetParam} from '@/api/api'

  export default {
    data() {
      return {}
    },

    mounted: function () {

    },

    methods: {

    },

  }
</script>
