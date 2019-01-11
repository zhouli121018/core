<template>
  <div class="j-module-content j-maillist mllist-list height100 ">

    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{this.$parent.lan.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{this.$parent.lan.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{this.$parent.lan.SETTING_INDEX_PERSONAL_MENU}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>

    <el-alert :title="this.$parent.lan.SETTING_USER_NOTICE" type="warning" :closable="false" v-if="need_alert"></el-alert>

    <section class="content content-list height100" style="background: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;">
      <el-form :model="editform" :rules="formRules" ref="editform" label-width="150px" style="margin-left:13px;margin-right:13px;margin-top: 13px" size="mini">

        <el-row>
          <el-col :span="24">
            <div class="demo-block-control">
              <p style="margin-bottom: 3px; margin-left: 13px">{{this.$parent.lan.SETTING_USER_TITLE_1}}</p>
            </div>
          </el-col>
          <el-col :span="8"><el-form-item :label="this.$parent.lan.COMMON_XINGMING" prop="realname"><el-input v-model.trim="editform.realname" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
          <el-col :span="8"><el-form-item :label="this.$parent.lan.SETTING_USER_ENGNAME"><el-input v-model.trim="editform.engname" auto-complete="off" :disabled="!can_modify" ></el-input></el-form-item></el-col>
          <el-col :span="8"><el-form-item :label="this.$parent.lan.SETTING_USER_EENUMBER"><el-input v-model.trim="editform.eenumber" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
          <el-col :span="8"><el-form-item :label="this.$parent.lan.COMMON_EMAIL2"><span>{{editform.email}}</span></el-form-item></el-col>
          <el-col :span="8"><el-form-item :label="this.$parent.lan.COMMON_DEPARTMENT"><span>{{editform.department}}</span></el-form-item></el-col>
          <el-col :span="8"><el-form-item :label="this.$parent.lan.COMMON_POSITION"><span>{{editform.position}}</span></el-form-item></el-col>
          <el-col :span="8"><el-form-item :label="this.$parent.lan.COMMON_MOBILE2"><el-input v-model.trim="editform.tel_mobile" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
          <el-col :span="8"><el-form-item :label="this.$parent.lan.COMMON_BIRTHDAY"><el-date-picker type="date" :placeholder="this.$parent.lan.COMMON_SELECT_DATE" v-model="editform.birthday" style="width: 100%;" value-format="yyyy-MM-dd" auto-complete="off" :disabled="!can_modify"></el-date-picker></el-form-item></el-col>
          <el-col :span="8">
            <el-form-item :label="this.$parent.lan.COMMON_GENDER">
              <el-radio-group v-model="editform.gender" :disabled="!can_modify">
                <el-radio label="male">{{this.$parent.lan.COMMON_GENDER_M}}</el-radio>
                <el-radio label="female">{{this.$parent.lan.COMMON_GENDER_F}}</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>


        <div class="demo-block-control-ext-top" @click="extendInfoShow=!extendInfoShow" v-if="!extendInfoShow">
          <i :class="[extendInfoShow ? 'el-icon-caret-top':'el-icon-caret-bottom']"></i>
          <span>{{extendInfoShow?this.$parent.lan.SETTING_USER_BUTTON_HIDE:this.$parent.lan.SETTING_USER_BUTTON_SHOW}}</span>
          <button type="button" class="el-button control-button el-tooltip el-button--text el-button--small" style="display: none;" aria-describedby="el-tooltip-7026" tabindex="0"></button>
        </div>

        <div v-show="extendInfoShow">
          <el-row>
            <el-col :span="24">
              <div class="demo-block-control">
                <p style="margin-bottom: 3px; margin-left: 13px">{{this.$parent.lan.SETTING_USER_TITLE_2}}</p>
              </div>
            </el-col>
            <el-col :span="8"><el-form-item :label="this.$parent.lan.COMMON_TELWORK"><el-input v-model.trim="editform.tel_work" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item :label="this.$parent.lan.COMMON_TELWORKEXT"><el-input v-model.trim="editform.tel_work_ext" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item :label="this.$parent.lan.COMMON_TELGROUP"><el-input v-model.trim="editform.tel_group" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item :label="this.$parent.lan.SETTING_USER_TELHOME"><el-input v-model.trim="editform.tel_home" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="QQ"><el-input v-model.trim="editform.im_qq" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="MSN"><el-input v-model.trim="editform.im_msn" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="16"><el-form-item :label="this.$parent.lan.SETTING_USER_HOMEPAGE"><el-input v-model.trim="editform.homepage" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
          </el-row>

          <el-row>
            <el-col :span="24">
              <div class="demo-block-control">
                <p style="margin-bottom: 3px; margin-left: 13px">{{this.$parent.lan.SETTING_USER_TITLE_3}}</p>
              </div>
            </el-col>

            <el-col :span="8"><el-form-item :label="this.$parent.lan.SETTING_USER_CONTRY"><el-input v-model.trim="editform.addr_country" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item :label="this.$parent.lan.SETTING_USER_STATE"><el-input v-model.trim="editform.addr_state" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item :label="this.$parent.lan.SETTING_USER_CITY"><el-input v-model.trim="editform.addr_city" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item :label="this.$parent.lan.SETTING_USER_ZIP"><el-input v-model.trim="editform.addr_zip" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="16"><el-form-item :label="this.$parent.lan.SETTING_USER_ADDRESS"><el-input v-model.trim="editform.addr_address" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
          </el-row>

          <el-row>
            <el-col :span="24">
              <div class="demo-block-control">
                <p style="margin-bottom: 3px; margin-left: 13px">{{this.$parent.lan.COMMON_REMARK}}</p>
              </div>
            </el-col>
            <el-col :span="16"><el-form-item :label="this.$parent.lan.COMMON_REMARK"><el-input type="textarea" v-model.trim="editform.remark" :disabled="!can_modify"></el-input></el-form-item></el-col>
          </el-row>
        </div>

        <div class="demo-block-control-ext-bottom" @click="extendInfoShow=!extendInfoShow"  v-if="extendInfoShow">
          <i :class="[extendInfoShow ? 'el-icon-caret-top':'el-icon-caret-bottom']"></i>
          <span>{{extendInfoShow?this.$parent.lan.SETTING_USER_BUTTON_HIDE:this.$parent.lan.SETTING_USER_BUTTON_SHOW}}</span>
          <button type="button" class="el-button control-button el-tooltip el-button--text el-button--small" style="display: none;" aria-describedby="el-tooltip-7026" tabindex="0"></button>
        </div>

        <el-row>
          <el-col :span="24">
            <el-form-item>
              <el-button type="primary" @click.native="onSubmit()" v-if="can_modify" :loading="saveFormLoading">{{need_review?this.$parent.lan.SETTING_USER_BUTTON_SHENHE:this.$parent.lan.COMMON_BUTTON_SAVE}}</el-button>
            </el-form-item>
          </el-col>
        </el-row>

      </el-form>

    </section>

  </div>
</template>

<script>
  import { settingUsersGet, settingUsersUpdate } from '@/api/api'

  export default {
    data() {
      return {
        can_modify: false,
        need_alert: false,
        extendInfoShow: false,
        saveFormLoading: false,
        need_review: false,
        editform: {
          realname: 'test',
          engname: 'test',
          eenumber: '123',
          email: 'test@test.com',
          department: "test",
          position: "test",
          birthday: 'test',
          gender: "",
          tel_mobile: "",
          tel_work: '',
          tel_work_ext: '',
          tel_group: '',
          tel_home: '',
          im_qq: '',
          im_msn: '',
          homepage: '',
          addr_country: '',
          addr_state: '',
          addr_city: '',
          addr_zip: '',
          addr_address: '',
          remark: '',
        },
        formRules: {
          realname: [
            { required: true, message: this.$parent.lan.SETTING_USER_NAME_RULE, trigger: 'blur' },
            { min: 1, max: 35, message: this.$parent.lan.SETTING_USER_NAME_RULE_LEN, trigger: 'blur' }
          ]
        },

      }
    },
    created: function(){
      this.getUserInfo();
    },
    methods: {
      getUserInfo(){
        settingUsersGet().then(res=>{
          this.need_review = res.data.need_review;
          this.can_modify = res.data.can_modify;
          this.editform = res.data.results;
          this.need_alert = res.data.need_alert;
        });
      },

      // 提交
      onSubmit: function () {
        this.$refs.editform.validate((valid) => {
          if (valid) {
            this.$confirm(this.$parent.lan.COMMON_BUTTON_CONFIRM_SUBMIT, this.$parent.lan.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.saveFormLoading = true;
              let para = Object.assign({}, this.editform);
              para.birthday = (!para.birthday || para.birthday == '') ? null : para.birthday;
              settingUsersUpdate(para).then((res) => {
                this.saveFormLoading = false;
                let status = res.data.status;
                if (status==1){
                  this.$message({message: this.$parent.lan.SETTING_USER_MESSAGE_1, type: 'success'});
                } else if (status==2){
                  this.$message({message: this.$parent.lan.SETTING_USER_MESSAGE_2, type: 'warning'});
                } else if (status==3){
                  this.$message({message: this.$parent.lan.COMMON_ALTER_SUCCESS, type: 'success'});
                }
                this.getUserInfo();
              }).catch(function (error) {
                console.log(error);
                this.saveFormLoading = false;
              });
            });
          }
        });
      },

    }
  }

</script>
<style>
  .demo-block-control-ext-top{
    /*border-top: 1px solid #eaeefb;*/
    /*border-bottom: 1px solid #eaeefb;*/
    box-sizing: border-box;
    /*background-color: #fff;*/
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    margin-top: 0px;
    color: #d3dce6;
    cursor: pointer;
    position: relative;
    text-align: center;
    font-size: 18px;
    font-weight: 500;
    margin-bottom: 13px;
  }
  .demo-block-control-ext-bottom{
    /*border-top: 1px solid #eaeefb;*/
    /*border-bottom: 1px solid #eaeefb;*/
    box-sizing: border-box;
    /*background-color: #fff;*/
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    margin-top: 1px;
    color: #d3dce6;
    cursor: pointer;
    position: relative;
    text-align: center;
    font-size: 18px;
    font-weight: 500;
    margin-bottom: 13px;
  }
  .demo-block-control-ext-bottom:hover{
    color: #409eff;
  }
  .demo-block-control-ext-top:hover{
    color: #409eff;
  }
  /*.el-form-item__label{*/
  /*font-weight: bold;*/
  /*}*/
</style>
