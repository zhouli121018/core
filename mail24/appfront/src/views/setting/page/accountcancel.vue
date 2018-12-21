<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>申请注销用户</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>

    <el-alert title="提示：注销申请已提交，请耐心等待审核" type="warning" :closable="false" v-if="sForm.status=='wait'"></el-alert>

    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">
      <el-form :model="sForm" label-width="120px" :rules="sFormRules" ref="sForm" size="mini" style="margin-left:13px;margin-right:13px;margin-top: 13px">
        <el-row><el-col :span="24"><div class="demo-block-control"><p style="margin-bottom: 3px; margin-left: 13px"> 申请注销</p></div></el-col></el-row>
        <el-row><el-col :span="16"><el-form-item label="申请注销原因：" prop="remark"><el-input type="textarea" v-model.trim="sForm.remark" :disabled="sForm.status=='wait'"></el-input></el-form-item></el-col></el-row>
        <el-row v-if="sForm.status!='wait'"><el-form-item label=""><el-button type="primary" @click.native="sFormSubmit()" :loading="sFormLoading">提交</el-button></el-form-item></el-row>
      </el-form>
    </section>
  </div>
</template>
<script>
  import {settingUsersGetCancel, settingUsersSetCancel} from '@/api/api'

  export default {
    data() {
      return {
        sFormLoading: false,
        sForm: {
          remark: '',
          status: '',
        },

        sFormRules: {
          remark: [{ required: true, message: '请填写申请注销原因', trigger: 'blur' }],
        },

      }
    },

    mounted: function () {
      this.getSetting();
    },

    methods: {
      getSetting: function(){
        settingUsersGetCancel().then(res=>{
          if ( res.data.results != null ){
            this.sForm = res.data.results;
          }
        });
      },

      sFormSubmit: function () {
        this.$refs.sForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.sFormLoading = true;
              let para = Object.assign({}, this.sForm);
              settingUsersSetCancel(para).then((res) => {
                // this.$refs['sForm'].resetFields();
                this.getSetting()
                this.sFormLoading = false;
                this.$message({message: '申请已提交，请等待审核', type: 'success'});
              }, (data)=>{
                this.sFormLoading = false;
              }).catch(function (error) {
                this.sFormLoading = false;
                console.log(error);
              });
            });
          }
        });
      }

    },

  }
</script>
