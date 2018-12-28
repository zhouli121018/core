<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>参数设置</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;">
      <el-form :model="sForm" label-width="180px" :rules="sFormRules" ref="sForm" size="mini" style="margin-left:13px;margin-right:13px;margin-top: 13px" :inline="true">
        <el-row><el-col :span="24"><div class="demo-block-control"><p style="margin-bottom: 3px; margin-left: 13px"> 参数设置</p></div></el-col></el-row>
        <!--<el-row><el-form-item label="邮件显示格式" prop="read_type"><el-select v-model="sForm.read_type" style="width: 200px"><el-option v-for="item in read_types" :key="item.value" :label="item.label" :value="item.value"></el-option></el-select></el-form-item></el-row>-->
        <el-row><el-form-item label="发送邮件编码" prop="send_charset"><el-select v-model="sForm.send_charset" style="width: 200px"><el-option v-for="item in send_charsets" :key="item.value" :label="item.label" :value="item.value"></el-option></el-select></el-form-item></el-row>
        <!--<el-row><el-form-item label="每页显示邮件数" prop="page_limit"><el-input-number v-model.trim="sForm.page_limit" auto-complete="off" :min="1" style="width: 200px"></el-input-number></el-form-item></el-row>-->
        <!--<el-row><el-form-item label="列表刷新间隔时间" prop="page_refresh"><el-checkbox-group><el-input-number v-model.trim="sForm.page_refresh" auto-complete="off" :min="1" style="width: 200px"></el-input-number><el-button size="mini">分钟</el-button></el-checkbox-group></el-form-item></el-row>-->
        <!--<el-row><el-form-item label="登录超时时间" prop="login_overtime"><el-checkbox-group><el-input-number v-model.trim="sForm.login_overtime" auto-complete="off" :min="1" style="width: 200px"></el-input-number><el-button size="mini">分钟</el-button></el-checkbox-group></el-form-item></el-row>-->
        <!--<el-row><el-form-item label="网络硬盘文件共享期限" prop="nd_share_period"><el-checkbox-group><el-input-number v-model.trim="sForm.nd_share_period" auto-complete="off" :min="1" style="width: 200px"></el-input-number><el-button size="mini">天</el-button></el-checkbox-group></el-form-item></el-row>-->
        <el-row><el-form-item label="保存Webmail已发送邮件"><el-radio-group v-model="sForm.save_webmail_sent"><el-radio v-for="item in disabled_options" :label="item.value" :key="item.value">{{item.label}}</el-radio></el-radio-group></el-form-item></el-row>
        <el-row><el-form-item label="保存客户端已发送邮件"><el-radio-group v-model="sForm.save_client_sent"><el-radio v-for="item in disabled_options" :label="item.value" :key="item.value">{{item.label}}</el-radio></el-radio-group></el-form-item></el-row>
        <el-row><el-form-item label="自动保存收件人到通讯录"><el-radio-group v-model="sForm.save_contact"><el-radio v-for="item in disabled_options" :label="item.value" :key="item.value">{{item.label}}</el-radio></el-radio-group></el-form-item></el-row>
        <el-row><el-form-item label="邮件自动回执"><el-radio-group v-model="sForm.auto_receipt"><el-radio v-for="item in disabled_options" :label="item.value" :key="item.value">{{item.label}}</el-radio></el-radio-group></el-form-item></el-row>
        <el-row><el-form-item label="邮件编辑时自动保存草稿"><el-radio-group v-model="sForm.auto_save_draft"><el-radio v-for="item in disabled_options" :label="item.value" :key="item.value">{{item.label}}</el-radio></el-radio-group></el-form-item></el-row>
        <el-row><el-form-item label=" "><el-button type="primary" @click.native="sFormSubmit()" :loading="sFormLoading">修改</el-button></el-form-item></el-row>
      </el-form>
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
          // read_type: 'html',
          send_charset: 'utf-8',
          // page_limit: '30',
          // page_refresh: '5',
          // login_overtime: '30',
          // nd_share_period: '60',

          save_webmail_sent: '1',
          save_client_sent: '-1',
          save_contact: '1',
          auto_receipt: '-1',
          auto_save_draft: '1',
        },
        sFormRules: {
          // read_type: [{ required: true, message: '请选择邮件显示格式', trigger: 'blur' },],
          send_charset: [{ required: true, message: '请选择发送邮件编码', trigger: 'blur' },],
          // page_limit: [{ required: true, message: '请输入每页显示邮件数', trigger: 'blur' },],
          // page_refresh: [{ required: true, message: '请输入列表刷新间隔时间', trigger: 'blur' },],
          // login_overtime: [{ required: true, message: '请输入登录超时时间', trigger: 'blur' },],
          // nd_share_period: [{ required: true, message: '请输入网络硬盘文件共享期限', trigger: 'blur' },],
          save_webmail_sent: [{ required: true, message: '请选择保存Webmail已发送邮件', trigger: 'blur' },],
          save_client_sent: [{ required: true, message: '请选择保存客户端已发送邮件', trigger: 'blur' },],
          save_contact: [{ required: true, message: '请选择自动保存收件人到通讯录', trigger: 'blur' },],
          auto_receipt: [{ required: true, message: '请选择邮件自动回执', trigger: 'blur' },],
          auto_save_draft: [{ required: true, message: '请选择邮件编辑时自动保存草稿', trigger: 'blur' },],
        },

        read_types: [{ value: 'html', label: 'HTML超文本'}, {value: 'text', label: '纯文本' }],
        send_charsets: [{ value: 'utf-8', label: 'UTF-8'}, {value: 'gb18030', label: 'GB18030' }],
        disabled_options: [{ value: '1', label: '是'}, {value: '-1', label: '否' }],
      }
    },
    mounted: function(){
      this.getParam();
    },
    methods: {

      getParam: function(){
        settingUsersGetParam().then(res=>{
          this.sForm = res.data.results;
        });
      },

      sFormSubmit: function () {
        this.$refs.sForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.sFormLoading = true;
              let para = Object.assign({}, this.sForm);
              settingUsersSetParam(para).then((res) => {
                // this.$refs['sForm'].resetFields();
                this.sFormLoading = false;
                this.$message({message: '参数修改成功', type: 'success'});
              }, (data)=>{
                console.log(data)
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
