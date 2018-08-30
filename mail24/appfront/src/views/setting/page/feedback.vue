<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>邮箱意见反馈</el-breadcrumb-item></el-breadcrumb>
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
      return {
        sFormLoading: false,
        sForm: {
          // remark: '',
          // status: 'wait',
        },

        sFormRules: {
          // remark: [{ required: true, message: '请填写申请注销原因', trigger: 'blur' }],
        },

      }
    },

    mounted: function () {

    },

    methods: {

      sFormSubmit: function () {

      }

    },

  }
</script>
