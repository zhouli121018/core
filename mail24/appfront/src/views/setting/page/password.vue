<template>
  <div class="j-module-content j-maillist mllist-list height100 ">

    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{this.$parent.lan.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{this.$parent.lan.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{this.$parent.lan.SETTING_INDEX_PASSWORD_MENU}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>

    <section class="content content-list height100" style="background: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;">
      <el-form :model="passeordForm" label-width="180px" :rules="passeordFormRules" ref="passeordForm" size="mini" style="margin-left:13px;margin-right:13px;margin-top: 13px">
        <el-row>
          <el-col :span="24"><div class="demo-block-control"><p style="margin-bottom: 3px; margin-left: 13px">{{this.$parent.lan.SETTING_INDEX_PASSWORD_MENU}}</p></div></el-col>
          <el-col :span="16"><el-form-item :label="this.$parent.lan.COMMON_SRC_PASSWORD" prop="password" :error="password_error"><el-input type="password" v-model.trim="passeordForm.password" auto-complete="off"></el-input></el-form-item></el-col><br>
          <el-col :span="16"><el-form-item :label="this.$parent.lan.COMMON_NEW_PASSWORD" prop="new_password" :error="new_password_error"><el-input type="password" v-model.trim="passeordForm.new_password" auto-complete="off"></el-input></el-form-item></el-col><br>
          <el-col :span="16"><el-form-item :label="this.$parent.lan.COMMON_CONFIRM_PASSWORD" prop="confirm_password" :error="confirm_password_error"><el-input type="password" v-model.trim="passeordForm.confirm_password" auto-complete="off"></el-input></el-form-item></el-col>
        </el-row>
        <el-row><el-col :span="16">
          <div style="margin-left: 100px">
            <strong style="color: red">{{this.$parent.lan.COMMON_PASSWORD_NOTICE}}</strong>
            <ul style="margin-left: 26px;">
              <li style="list-style-type:circle;">{{this.$parent.lan.COMMON_PASSWORD_NOTICE_1}}{{passwordRules.passwd_size2}}{{this.$parent.lan.COMMON_PASSWORD_NOTICE_2}}</li>
              <li v-if="passwordRules.passwd_type==2" style="list-style-type:circle;">{{this.$parent.lan.COMMON_PASSWORD_NOTICE_3}}</li>
              <li v-if="passwordRules.passwd_type==3" style="list-style-type:circle;">{{this.$parent.lan.COMMON_PASSWORD_NOTICE_4}}</li>
              <li v-if="passwordRules.passwd_type==4" style="list-style-type:circle;">{{this.$parent.lan.COMMON_PASSWORD_NOTICE_5}}</li>
              <li v-if="passwordRules.passwd_digital" style="list-style-type:circle;">{{this.$parent.lan.COMMON_PASSWORD_NOTICE_6}}</li>
              <li v-if="passwordRules.passwd_name" style="list-style-type:circle;">{{this.$parent.lan.COMMON_PASSWORD_NOTICE_7}}</li>
              <li v-if="passwordRules.passwd_name2" style="list-style-type:circle;">{{this.$parent.lan.COMMON_PASSWORD_NOTICE_8}}</li>
              <li v-if="passwordRules.passwd_letter" style="list-style-type:circle;">{{this.$parent.lan.COMMON_PASSWORD_NOTICE_9}}</li>
              <li v-if="passwordRules.passwd_letter2" style="list-style-type:circle;">{{this.$parent.lan.COMMON_PASSWORD_NOTICE_10}}</li>
            </ul>
          </div>
        </el-col>
        </el-row>
        <el-row><el-col :span="24"><el-form-item style="margin-top: 13px;"><el-button type="primary" @click.native="passeordFormSubmit()" :loading="passeordFormLoading">{{this.$parent.lan.COMMON_BUTTON_ALTER}}</el-button></el-form-item></el-col></el-row>
      </el-form>

      <el-form :model="securityForm" label-width="100px" :rules="securityFormRules" ref="securityForm" size="mini" style="margin-left:13px;margin-right:13px;margin-top: 13px">
        <el-row><el-col :span="24"><div class="demo-block-control"><p style="margin-bottom: 3px; margin-left: 13px">{{this.$parent.lan.SETTING_PASSWORD_SECURITY_TITLE}}</p></div></el-col></el-row>
        <el-row>
          <el-col :span="16">
            <el-form-item :label="this.$parent.lan.SETTING_PASSWORD_SECURITY_Q1" prop="security_question1" :error="security_question1_error">
              <el-select v-model="securityForm.security_question1" :placeholder="this.$parent.lan.SETTING_PASSWORD_SECURITY_QP" style="width: 100%">
                <el-option v-for="item in security_questions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
          </el-col><br>
          <el-col :span="16" v-if="securityForm.security_question1=='custom'">
            <el-form-item :label="this.$parent.lan.SETTING_PASSWORD_SECURITY_QS" prop="security_custom1" :error="security_custom1_error"><el-input v-model.trim="securityForm.security_custom1" auto-complete="off"></el-input></el-form-item>
          </el-col><br>
          <el-col :span="16"><el-form-item :label="this.$parent.lan.SETTING_PASSWORD_SECURITY_QA" prop="security_answer1" :error="security_answer1_error"><el-input v-model.trim="securityForm.security_answer1" auto-complete="off"></el-input></el-form-item></el-col><br>
        </el-row>

        <el-row>
          <el-col :span="16">
            <el-form-item :label="this.$parent.lan.SETTING_PASSWORD_SECURITY_Q2" prop="security_question2" :error="security_question2_error">
              <el-select v-model="securityForm.security_question2" :placeholder="this.$parent.lan.SETTING_PASSWORD_SECURITY_QP" style="width: 100%">
                <el-option v-for="item in security_questions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
          </el-col><br>
          <el-col :span="16" v-if="securityForm.security_question2=='custom'"><el-form-item :label="this.$parent.lan.SETTING_PASSWORD_SECURITY_QS" prop="security_custom2" :error="security_custom2_error"><el-input v-model.trim="securityForm.security_custom2" auto-complete="off"></el-input></el-form-item></el-col><br>
          <el-col :span="16"><el-form-item :label="this.$parent.lan.SETTING_PASSWORD_SECURITY_QA" prop="security_answer2" :error="security_answer2_error"><el-input v-model.trim="securityForm.security_answer2" auto-complete="off"></el-input></el-form-item></el-col><br>
        </el-row>

        <el-row>
          <el-col :span="16">
            <el-form-item :label="this.$parent.lan.SETTING_PASSWORD_SECURITY_Q3" prop="security_question3" :error="security_question3_error">
              <el-select v-model="securityForm.security_question3" :placeholder="this.$parent.lan.SETTING_PASSWORD_SECURITY_QP" style="width: 100%">
                <el-option v-for="item in security_questions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
          </el-col><br>
          <el-col :span="16" v-if="securityForm.security_question3=='custom'"><el-form-item :label="this.$parent.lan.SETTING_PASSWORD_SECURITY_QS" prop="security_custom3" :error="security_custom3_error"><el-input v-model.trim="securityForm.security_custom3" auto-complete="off"></el-input></el-form-item></el-col><br>
          <el-col :span="16"><el-form-item :label="this.$parent.lan.SETTING_PASSWORD_SECURITY_QA" prop="security_answer3" :error="security_answer3_error"><el-input v-model.trim="securityForm.security_answer3" auto-complete="off"></el-input></el-form-item></el-col><br>
        </el-row>


        <el-row>
          <el-col :span="24">
            <el-form-item>
              <el-button type="primary" @click.native="securityFormSubmit()" :loading="securityFormLoading">{{this.$parent.lan.COMMON_BUTTON_ALTER}}</el-button>
            </el-form-item>
          </el-col>
        </el-row>

      </el-form>

    </section>

  </div>
</template>

<script>
  import cookie from '@/assets/js/cookie';
  import {
    settingUsersGetpassword,
    settingUsersGetSecurity,
    settingUsersSetpassword,
    settingUsersSetSecurity
  } from '@/api/api'

  export default {
    data() {
      return {
        passeordFormLoading: false,
        // 密码规则
        passwordRules:{
          "passwd_type": 2,
          "passwd_size2": 8,
          "passwd_digital": false,
          "passwd_name": false,
          "passwd_name2": false,
          "passwd_letter": false,
          "passwd_letter2": false,
        },
        // 错误信息展示
        password_error:'',
        new_password_error:'',
        confirm_password_error:'',
        passeordForm: {
          password: '',
          new_password: '',
          confirm_password: '',
        },
        passeordFormRules: {
          password: [
            { required: true, message: this.$parent.lan.COMMON_SRC_PASSWORD_RULE, trigger: 'blur' },
            { min: 1, message: this.$parent.lan.COMMON_SRC_PASSWORD_RULE_LEN, trigger: 'blur' }
          ],
          new_password: [
            { required: true, message: this.$parent.lan.COMMON_NEW_PASSWORD_RULE, trigger: 'blur' },
            { min: 8, max: 20, message: this.$parent.lan.COMMON_PASSWORD_RULE_LEN, trigger: 'blur' }
          ],
          confirm_password: [
            { required: true, message: this.$parent.lan.COMMON_CONFIRM_PASSWORD_RULE, trigger: 'blur' },
            { min: 8, max: 20, message: this.$parent.lan.COMMON_PASSWORD_RULE_LEN, trigger: 'blur' }
          ]
        },

        securityFormLoading: false,
        security_question1_error: '',
        security_custom1_error: '',
        security_answer1_error: '',
        security_question2_error: '',
        security_custom2_error: '',
        security_answer2_error: '',
        security_question3_error: '',
        security_custom3_error: '',
        security_answer3_error: '',
        securityForm: {
          security_question1: '',
          security_custom1: '',
          security_answer1: '',
          security_question2: '',
          security_custom2: '',
          security_answer2: '',
          security_question3: '',
          security_custom3: '',
          security_answer3: '',
        },
        securityFormRules:{},
        security_questions: [{
          value: '1',
          label: this.$parent.lan.CONMON_PASSWORD_SECURITY_QD1
        }, {
          value: '2',
          label: this.$parent.lan.CONMON_PASSWORD_SECURITY_QD2
        }, {
          value: '3',
          label: this.$parent.lan.CONMON_PASSWORD_SECURITY_QD3
        }, {
          value: '4',
          label: this.$parent.lan.CONMON_PASSWORD_SECURITY_QD4
        }, {
          value: '5',
          label: this.$parent.lan.CONMON_PASSWORD_SECURITY_QD5
        }, {
          value: '6',
          label: this.$parent.lan.CONMON_PASSWORD_SECURITY_QD6
        }, {
          value: '7',
          label: this.$parent.lan.CONMON_PASSWORD_SECURITY_QD7
        }, {
          value: '8',
          label: this.$parent.lan.CONMON_PASSWORD_SECURITY_QD8
        }, {
          value: 'custom',
          label: this.$parent.lan.CONMON_PASSWORD_SECURITY_QS
        }],


      }
    },
    mounted: function(){
      this.getPassword();
      this.getSecurity();
    },
    methods: {
      getPassword: function(){
        settingUsersGetpassword().then(res=>{
          this.passwordRules = res.data;
        });
      },
      getSecurity: function(){
        settingUsersGetSecurity().then(res=>{
          this.securityForm = res.data.results;
        });
      },

      // 提交
      passeordFormSubmit: function () {
        this.password_error = '';
        this.new_password_error = '';
        this.confirm_password_error = '';
        this.$refs.passeordForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.$parent.lan.COMMON_BUTTON_CONFIRM_SUBMIT, this.$parent.lan.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.passeordFormLoading = true;
              let para = Object.assign({}, this.passeordForm);
              settingUsersSetpassword(para).then((res) => {
                cookie.setCookie('token',res.data.token, 7);
                this.$refs['passeordForm'].resetFields();
                this.passeordFormLoading = false;
                this.$message({message: this.$parent.lan.COMMON_ALTER_SUCCESS, type: 'success'});
              }, (data)=>{
                console.log(data)
                this.passeordFormLoading = false;
                if("password" in data) {
                  this.password_error = data.password[0];
                }
                if("new_password" in data) {
                  this.new_password_error = data.new_password[0];
                }
                if("confirm_password" in data) {
                  this.confirm_password_error = data.confirm_password[0];
                }
              }).catch(function (error) {
                console.log(error);
                this.passeordFormLoading = false;
              });
            });
          }
        });
      },

      securityFormSubmit: function () {
        this.security_question1_error = '';
        this.security_custom1_error = '';
        this.security_answer1_error = '';
        this.security_question2_error = '';
        this.security_custom2_error = '';
        this.security_answer2_error = '';
        this.security_question3_error = '';
        this.security_custom3_error = '';
        this.security_answer3_error = '';
        this.$refs.securityForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.$parent.lan.COMMON_BUTTON_CONFIRM_SUBMIT, this.$parent.lan.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.securityFormLoading = true;
              let para = Object.assign({}, this.securityForm);
              settingUsersSetSecurity(para).then((res) => {
                // this.$refs['securityForm'].resetFields();
                this.securityFormLoading = false;
                this.$message({message: this.$parent.lan.COMMON_ALTER_SUCCESS, type: 'success'});
                // this.getSecurity();
              }, (data)=>{
                this.securityFormLoading = false;
                if("security_question1" in data) { this.security_question1_error = data.security_question1[0]; }
                if("security_custom1" in data) { this.security_custom1_error = data.security_custom1[0]; }
                if("security_answer1" in data) { this.security_answer1_error = data.security_answer1[0]; }

                if("security_question2" in data) { this.security_question2_error = data.security_question2[0]; }
                if("security_custom2" in data) { this.security_custom2_error = data.security_custom2[0]; }
                if("security_answer2" in data) { this.security_answer2_error = data.security_answer2[0]; }

                if("security_question3" in data) { this.security_question3_error = data.security_question3[0]; }
                if("security_custom3" in data) { this.security_custom3_error = data.security_custom3[0]; }
                if("security_answer3" in data) { this.security_answer3_error = data.security_answer3[0]; }
              }).catch(function (error) {
                console.log(error);
                this.securityFormLoading = false;
              });
            });
          }
        });
      }



    }
  }

</script>
