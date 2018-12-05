<template>
  <div class="j-module-content j-maillist mllist-list height100 ">

    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>密码修改</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>

    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">
      <el-form :model="passeordForm" label-width="100px" :rules="passeordFormRules" ref="passeordForm" size="mini" style="margin-left:13px;margin-right:13px;margin-top: 13px">
        <el-row>
          <el-col :span="24"><div class="demo-block-control"><p style="margin-bottom: 3px; margin-left: 13px"> 修改密码</p></div></el-col>
          <el-col :span="16"><el-form-item label="原始密码" prop="password" :error="password_error"><el-input type="password" v-model.trim="passeordForm.password" auto-complete="off"></el-input></el-form-item></el-col><br>
          <el-col :span="16"><el-form-item label="新密码" prop="new_password" :error="new_password_error"><el-input type="password" v-model.trim="passeordForm.new_password" auto-complete="off"></el-input></el-form-item></el-col><br>
          <el-col :span="16"><el-form-item label="确认密码" prop="confirm_password" :error="confirm_password_error"><el-input type="password" v-model.trim="passeordForm.confirm_password" auto-complete="off"></el-input></el-form-item></el-col>
        </el-row>
        <el-row><el-col :span="16"><pre style="margin-left: 100px"><strong style="color: red">注：</strong> 密码长度为8到20位，需要大写和小写字母数字组合或者特殊字符字母数字组合； 不能连续重复、递增、递减的数或字母，可包含特殊字符；<br>例：如密码为8位，则Abcd2357、1111test、1234test、4321test均不符合要求。</pre></el-col></el-row>
        <el-row><el-col :span="24"><el-form-item><el-button type="primary" @click.native="passeordFormSubmit()" :loading="passeordFormLoading">修改</el-button></el-form-item></el-col></el-row>
      </el-form>

      <el-form :model="securityForm" label-width="100px" :rules="securityFormRules" ref="securityForm" size="mini" style="margin-left:13px;margin-right:13px;margin-top: 13px">
        <el-row><el-col :span="24"><div class="demo-block-control"><p style="margin-bottom: 3px; margin-left: 13px"> 设置密保</p></div></el-col></el-row>
        <el-row>
          <el-col :span="16">
            <el-form-item label="密保问题1" prop="security_question1" :error="security_question1_error">
              <el-select v-model="securityForm.security_question1" placeholder="请选择密保问题" style="width: 100%">
                <el-option v-for="item in security_questions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
          </el-col><br>
          <el-col :span="16" v-if="securityForm.security_question1=='custom'"><el-form-item label="自定义问题" prop="security_custom1" :error="security_custom1_error"><el-input v-model.trim="securityForm.security_custom1" auto-complete="off"></el-input></el-form-item></el-col><br>
          <el-col :span="16"><el-form-item label="答案" prop="security_answer1" :error="security_answer1_error"><el-input v-model.trim="securityForm.security_answer1" auto-complete="off"></el-input></el-form-item></el-col><br>
        </el-row>

        <el-row>
          <el-col :span="16">
            <el-form-item label="密保问题2" prop="security_question2" :error="security_question2_error">
              <el-select v-model="securityForm.security_question2" placeholder="请选择密保问题" style="width: 100%">
                <el-option v-for="item in security_questions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
          </el-col><br>
          <el-col :span="16" v-if="securityForm.security_question2=='custom'"><el-form-item label="自定义问题" prop="security_custom2" :error="security_custom2_error"><el-input v-model.trim="securityForm.security_custom2" auto-complete="off"></el-input></el-form-item></el-col><br>
          <el-col :span="16"><el-form-item label="答案" prop="security_answer2" :error="security_answer2_error"><el-input v-model.trim="securityForm.security_answer2" auto-complete="off"></el-input></el-form-item></el-col><br>
        </el-row>

        <el-row>
          <el-col :span="16">
            <el-form-item label="密保问题3" prop="security_question3" :error="security_question3_error">
              <el-select v-model="securityForm.security_question3" placeholder="请选择密保问题" style="width: 100%">
                <el-option v-for="item in security_questions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
          </el-col><br>
          <el-col :span="16" v-if="securityForm.security_question3=='custom'"><el-form-item label="自定义问题" prop="security_custom3" :error="security_custom3_error"><el-input v-model.trim="securityForm.security_custom3" auto-complete="off"></el-input></el-form-item></el-col><br>
          <el-col :span="16"><el-form-item label="答案" prop="security_answer3" :error="security_answer3_error"><el-input v-model.trim="securityForm.security_answer3" auto-complete="off"></el-input></el-form-item></el-col><br>
        </el-row>


        <el-row>
          <el-col :span="24">
            <el-form-item>
              <el-button type="primary" @click.native="securityFormSubmit()" :loading="securityFormLoading">修改</el-button>
            </el-form-item>
          </el-col>
        </el-row>

      </el-form>

    </section>

  </div>
</template>

<script>
  import cookie from '@/assets/js/cookie';
  import { settingUsersSetpassword, settingUsersGetSecurity, settingUsersSetSecurity } from '@/api/api'
  export default {
    data() {
      return {
        passeordFormLoading: false,
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
            { required: true, message: '请填写原始密码', trigger: 'blur' },
            { min: 1, message: '长度必须大于 1 个字符', trigger: 'blur' }
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
          label: '我最爱的人的名字'
        }, {
          value: '2',
          label: '我最喜欢的物品的名称'
        }, {
          value: '3',
          label: '我最爱的电影名称'
        }, {
          value: '4',
          label: '中学的校名'
        }, {
          value: '5',
          label: '我最喜欢的歌曲'
        }, {
          value: '6',
          label: '我最喜欢的食物'
        }, {
          value: '7',
          label: '我的初恋日期'
        }, {
          value: '8',
          label: '我妈妈的生日'
        }, {
          value: 'custom',
          label: '自定义问题'
        }],


      }
    },
    mounted: function(){
      this.getSecurity();
    },
    methods: {

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
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.passeordFormLoading = true;
              let para = Object.assign({}, this.passeordForm);
              settingUsersSetpassword(para).then((res) => {
                cookie.setCookie('token',res.data.token, 7);
                this.$refs['passeordForm'].resetFields();
                this.passeordFormLoading = false;
                this.$message({message: '密码修改成功', type: 'success'});
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
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.securityFormLoading = true;
              let para = Object.assign({}, this.securityForm);
              settingUsersSetSecurity(para).then((res) => {
                // this.$refs['securityForm'].resetFields();
                this.securityFormLoading = false;
                this.$message({message: '密保修改成功', type: 'success'});
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
