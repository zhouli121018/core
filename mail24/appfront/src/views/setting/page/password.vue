<template>
  <div class="j-module-content j-maillist mllist-list height100 ">

    <el-row class="toolbar" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item>
          <el-breadcrumb-item>密码修改</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>


    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">
      <el-form :model="passeordForm" label-width="100px" :rules="passeordFormRules" ref="passeordForm" size="mini" style="margin-left:13px;margin-right:13px;margin-top: 13px">

        <el-row>
          <el-col :span="24">
            <div class="demo-block-control">
              <p style="margin-bottom: 3px; margin-left: 13px"> 修改密码</p>
            </div>
          </el-col>


          <el-col :span="16"><el-form-item label="原始密码" prop="password"><el-input type="password" v-model.trim="passeordForm.password" auto-complete="off"></el-input></el-form-item></el-col>

          <br>
          <el-col :span="16"><el-form-item label="新密码" prop="new_password"><el-input type="password" v-model.trim="passeordForm.new_password" auto-complete="off"></el-input></el-form-item></el-col>
          <br>

          <el-col :span="16"><el-form-item label="确认密码" prop="confirm_password"><el-input type="password" v-model.trim="passeordForm.confirm_password" auto-complete="off"></el-input></el-form-item></el-col>


        </el-row>

        <el-row>
          <el-col :span="24">
            <el-col :span="16">
            <pre style="margin-left: 100px"><strong style="color: red">注：</strong> 密码长度为8到20位，需要大写和小写字母数字组合或者特殊字符字母数字组合； 不能连续重复、递增、递减的数或字母，可包含特殊字符；
例：如密码为8位，则Abcd2357、1111test、1234test、4321test均不符合要求。</pre>
            </el-col>

          </el-col>
        </el-row>

        <el-row>
          <el-col :span="24">
            <el-form-item>
              <el-button type="primary" @click.native="passeordFormSubmit()" :loading="passeordFormLoading">修改</el-button>
            </el-form-item>
          </el-col>
        </el-row>

      </el-form>
    </section>

  </div>
</template>

<script>

  import { settingUsersSetpassword } from '@/api/api'
  export default {
    data() {
      return {
        passeordFormLoading: false,

        passeordForm: {
          password: '',
          new_password: '',
          confirm_password: '',
        },

        passeordFormRules: {
          password: [
            { required: true, message: '请填写原始密码', trigger: 'blur' },
            { min: 8, max: 20, message: '长度在 8 到 20 个字符', trigger: 'blur' }
          ],
          new_password: [
            { required: true, message: '请填写新密码', trigger: 'blur' },
            { min: 8, max: 20, message: '长度在 8 到 20 个字符', trigger: 'blur' }
          ],
          confirm_password: [
            { required: true, message: '请填写确认密码', trigger: 'blur' },
            { min: 8, max: 20, message: '长度在 8 到 20 个字符', trigger: 'blur' }
          ]
        },


      }
    },
    mounted: function(){

    },
    methods: {

      // 提交
      passeordFormSubmit: function () {
        this.$refs.passeordForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.passeordFormLoading = true;
              let para = Object.assign({}, this.passeordForm);
              console.log(para);
              settingUsersSetpassword(para).then((res) => {
                this.$refs['passeordForm'].resetFields();
                this.passeordFormLoading = false;
                this.$message({message: '修改成功', type: 'success'});
              }).catch(function (error) {
                console.log(error);
              });
            });
          }
        });
      },

    }
  }

</script>
