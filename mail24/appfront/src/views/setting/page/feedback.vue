<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{plang.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{plang.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{plang.SETTING_INDEX_FEEDBACK_MENU}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>

    <el-alert :title="plang.SETTING_FEEDBACK_DESC" type="success" :closable="false"></el-alert>

    <section class="content content-list height100" style="background-color: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;">

      <el-form :model="createForm" :rules="createFormRules" ref="createForm" label-width="120px" style="margin-left:13px;margin-right:13px;margin-top: 13px" size="mini">

        <el-row>
          <el-col :span="12">
            <el-form-item :label="plang.SETTING_FEEDBACK_NAME" prop="name">
              <el-input v-model.trim="createForm.name" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item :label="plang.SETTING_FEEDBACK_EMAIL" prop="email">
              <el-input v-model.trim="createForm.email" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item :label="plang.SETTING_FEEDBACK_PHONE" prop="mobile">
              <el-input v-model.trim="createForm.mobile" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item :label="plang.SETTING_FEEDBACK_NOTE" prop="content">
              <el-input v-model.trim="createForm.content" auto-complete="off" type="textarea"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </el-form-item>
      </el-form>

    </section>
  </div>
</template>
<script>
  import {settingFeedbackSet} from '@/api/api'

  export default {
    data() {
      let _self = this;
      var isEmail = function(rule,value,callback){
        if( /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/.test(value) == true ){
          callback();
        }else{
          callback(new Error(_self.$parent.lan.SETTING_WHITE_EMAIL_RULE2));
        }
      };
      return {
        plang:_self.$parent.lan,
        createFormLoading: false,
        createForm: {name: '', email: '', mobile: '', content: ''},
        createFormRules: {
          email: [
            { required: true, message: _self.$parent.lan.SETTING_WHITE_EMAIL_RULE1, trigger: 'blur' },
            {validator: isEmail, trigger: 'blur'}
          ],
          content: [ { required: true, message: _self.$parent.lan.SETTING_FEEDBACK_NOTE_RULE, trigger: 'blur' } ]
        },

      }
    },
    mounted: function () {
      this.createForm.email = this.$store.state.userInfo.name;
    },

    methods: {

      createFormSubmit: function () {
        this.$refs.createForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.createFormLoading = true;
              let para = Object.assign({}, this.createForm);

              this.$message({message: this.plang.SETTING_FEEDBACK_MSG, type: 'success'});
              this.$refs['createForm'].resetFields();
              this.createForm.email = this.$store.state.userInfo.name;

              settingFeedbackSet(para)
                .then((res) => {
                  this.createFormLoading = false;
                })
                .catch(function (error) {
                  this.createFormLoading = false;
                  console.log(error);
                });
            });
          }
        });
      }

    },

  }
</script>
