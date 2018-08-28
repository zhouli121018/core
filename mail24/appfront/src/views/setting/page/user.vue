<template>
  <div class="j-module-content j-maillist mllist-list height100 ">

    <el-row class="toolbar" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item>
          <el-breadcrumb-item>个人资料</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>

    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">
      <el-form :model="editform" :rules="formRules" ref="editform" label-width="100px" style="margin-left:13px;margin-right:13px;margin-top: 13px" size="mini">

        <el-alert title="提示：修改申请已提交，请等待审核" type="warning" :closable="false" v-if="need_alert"></el-alert>

        <el-row>
          <el-col :span="24">
            <div class="demo-block-control">
              <p style="margin-bottom: 3px; margin-left: 13px"> 基本资料</p>
            </div>
          </el-col>
          <el-col :span="8"><el-form-item label="姓名：" prop="realname"><el-input v-model.trim="editform.realname" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="英文名："><el-input v-model.trim="editform.engname" auto-complete="off" :disabled="!can_modify" ></el-input></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="工号："><el-input v-model.trim="editform.eenumber" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="邮箱地址："><span>{{editform.email}}</span></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="部门："><span>{{editform.department}}</span></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="职位："><span>{{editform.position}}</span></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="移动电话："><el-input v-model.trim="editform.tel_mobile" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="生日："><el-date-picker type="date" placeholder="选择日期" v-model="editform.birthday" style="width: 100%;" value-format="yyyy-MM-dd" auto-complete="off" :disabled="!can_modify"></el-date-picker></el-form-item></el-col>
          <el-col :span="8">
            <el-form-item label="性别：">
              <el-radio-group v-model="editform.gender" :disabled="!can_modify">
                <el-radio label="male">男</el-radio>
                <el-radio label="female">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>


        <div class="demo-block-control-ext-top" @click="extendInfoShow=!extendInfoShow" v-if="!extendInfoShow">
          <i :class="[extendInfoShow ? 'el-icon-caret-top':'el-icon-caret-bottom']"></i>
          <span>{{extendInfoShow?'隐藏更多信息':'显示更多信息'}}</span>
          <button type="button" class="el-button control-button el-tooltip el-button--text el-button--small" style="display: none;" aria-describedby="el-tooltip-7026" tabindex="0"></button>
        </div>

        <div v-show="extendInfoShow">
          <el-row>
            <el-col :span="24">
              <div class="demo-block-control">
                <p style="margin-bottom: 3px; margin-left: 13px"> 电话/即时通讯ID</p>
              </div>
            </el-col>
            <el-col :span="8"><el-form-item label="工作电话："><el-input v-model.trim="editform.tel_work" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="分机号："><el-input v-model.trim="editform.tel_work_ext" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="集团号："><el-input v-model.trim="editform.tel_group" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="住宅电话："><el-input v-model.trim="editform.tel_home" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="QQ："><el-input v-model.trim="editform.im_qq" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="MSN："><el-input v-model.trim="editform.im_msn" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="16"><el-form-item label="主页："><el-input v-model.trim="editform.homepage" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
          </el-row>

          <el-row>
            <el-col :span="24">
              <div class="demo-block-control">
                <p style="margin-bottom: 3px; margin-left: 13px"> 联系地址</p>
              </div>
            </el-col>

            <el-col :span="8"><el-form-item label="国家："><el-input v-model.trim="editform.addr_country" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="省份/地区："><el-input v-model.trim="editform.addr_state" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="城市："><el-input v-model.trim="editform.addr_city" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="邮编："><el-input v-model.trim="editform.addr_zip" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
            <el-col :span="16"><el-form-item label="详细地址："><el-input v-model.trim="editform.addr_address" auto-complete="off" :disabled="!can_modify"></el-input></el-form-item></el-col>
          </el-row>

          <el-row>
            <el-col :span="24">
              <div class="demo-block-control">
                <p style="margin-bottom: 3px; margin-left: 13px">备注</p>
              </div>
            </el-col>
            <el-col :span="16"><el-form-item label="备注："><el-input type="textarea" v-model.trim="editform.remark" :disabled="!can_modify"></el-input></el-form-item></el-col>
          </el-row>
        </div>

        <div class="demo-block-control-ext-bottom" @click="extendInfoShow=!extendInfoShow"  v-if="extendInfoShow">
          <i :class="[extendInfoShow ? 'el-icon-caret-top':'el-icon-caret-bottom']"></i>
          <span>{{extendInfoShow?'隐藏更多信息':'显示更多信息'}}</span>
          <button type="button" class="el-button control-button el-tooltip el-button--text el-button--small" style="display: none;" aria-describedby="el-tooltip-7026" tabindex="0"></button>
        </div>

        <el-row>
          <el-col :span="24">
            <el-form-item>
              <el-button type="primary" @click.native="onSubmit()" :loading="saveFormLoading" v-if="can_modify">{{need_review?'提交审核':'保存'}}</el-button>
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
            { required: true, message: '请输入姓名', trigger: 'blur' },
            { min: 1, max: 35, message: '长度在 1 到 35 个字符', trigger: 'blur' }
          ]
        },

      }
    },
    mounted: function(){
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
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.saveFormLoading = true;
              let para = Object.assign({}, this.editform);
              para.birthday = (!para.birthday || para.birthday == '') ? null : para.birthday;
              settingUsersUpdate(para).then((res) => {
                this.saveFormLoading = false;
                let status = res.data.status;
                if (status==1){
                  this.$message({message: '修改申请已提交，请等待审核', type: 'success'});
                } else if (status==2){
                  this.$message({message: '个人资料未做任何修改', type: 'warning'});
                } else if (status==3){
                  this.$message({message: '修改成功', type: 'success'});
                }
                this.getUserInfo();
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
