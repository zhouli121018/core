<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{plang.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{plang.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{plang.SETTING_INDEX_ACCCANCEL_MENU}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>

    <el-alert :title="plang.SETTING_ACCCANCEL_ALERT" type="warning" :closable="false" v-if="sForm.status=='wait'"></el-alert>

    <section class="content content-list height100" style="background-color: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;">
      <el-form :model="sForm" label-width="120px" :rules="sFormRules" ref="sForm" size="mini" style="margin-left:13px;margin-right:13px;margin-top: 13px">
        <el-row><el-col :span="24"><div class="demo-block-control"><p style="margin-bottom: 3px; margin-left: 13px">{{plang.SETTING_ACCCANCEL_TITLE}}</p></div></el-col></el-row>
        <el-row><el-col :span="16"><el-form-item :label="plang.SETTING_ACCCANCEL_REMARK" prop="remark"><el-input type="textarea" v-model.trim="sForm.remark" :disabled="sForm.status=='wait'"></el-input></el-form-item></el-col></el-row>
        <el-row v-if="sForm.status!='wait'"><el-form-item label=""><el-button type="primary" @click.native="sFormSubmit()" :loading="sFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button></el-form-item></el-row>
      </el-form>
    </section>
  </div>
</template>
<script>
  import {settingUsersGetCancel, settingUsersSetCancel} from '@/api/api'

  export default {
    data() {
      let _self = this;
      return {
        plang:_self.$parent.lan,
        sFormLoading: false,
        sForm: {
          remark: '',
          status: '',
        },

        sFormRules: {
          remark: [{ required: true, message: _self.$parent.lan.SETTING_ACCCANCEL_REMARK_RULE, trigger: 'blur' }],
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
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.sFormLoading = true;
              let para = Object.assign({}, this.sForm);
              settingUsersSetCancel(para).then((res) => {
                // this.$refs['sForm'].resetFields();
                this.getSetting()
                this.sFormLoading = false;
                this.$message({message: this.plang.SETTING_ACCCANCEL_MSG, type: 'success'});
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
