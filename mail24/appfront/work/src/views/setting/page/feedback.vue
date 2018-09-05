<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>邮箱意见反馈</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>

    <el-alert title="非常感谢您一直以来对我们服务的肯定与支持，您的热心反馈是我们不断改良服务的源泉，希望占用您几分钟时间，对我们的服务进行反馈。" type="success" :closable="false"></el-alert>

    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">

      <el-form :model="createForm" :rules="createFormRules" ref="createForm" label-width="120px" style="margin-left:13px;margin-right:13px;margin-top: 13px" size="mini">

        <el-row>
          <el-col :span="12">
            <el-form-item label="我们怎么称呼您:" prop="name">
              <el-input v-model.trim="createForm.name" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item label="您的邮箱地址:" prop="email">
              <el-input v-model.trim="createForm.email" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item label="您的联系电话:" prop="mobile">
              <el-input v-model.trim="createForm.mobile" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item label="反馈信息:" prop="content">
              <el-input v-model.trim="createForm.content" auto-complete="off" type="textarea"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading" >提交</el-button>
        </el-form-item>
      </el-form>

    </section>
  </div>
</template>
<script>
  import {settingFeedbackSet} from '@/api/api'

  export default {
    data() {
      var isEmail = function(rule,value,callback){
        if( /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/.test(value) == true ){
          callback();
        }else{
          callback(new Error("请输入正确的邮箱"));
        }
      };
      return {
        createFormLoading: false,
        createForm: {name: '', email: '', mobile: '', content: ''},
        createFormRules: {
          email: [
            { required: true, message: '请填写邮箱', trigger: 'blur' },
            {validator: isEmail, trigger: 'blur'}
          ],
          content: [ { required: true, message: '请填写反馈信息', trigger: 'blur' } ]
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
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.createFormLoading = true;
              let para = Object.assign({}, this.createForm);

              this.$message({message: '反馈信息发送成功', type: 'success'});
              this.$refs['createForm'].resetFields();
              this.createFormLoading = false;
              this.createForm.email = this.$store.state.userInfo.name;

              settingFeedbackSet(para)
                .then((res) => {
                })
                .catch(function (error) {
                  console.log(error);
                });
            });
          }
        });
      }

    },

  }
</script>
