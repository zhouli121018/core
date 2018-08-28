<template>
    <div class="mltabview-content">
      <div class="mltabview-panel">
        <section class="m-mlcompose">
          <div class="toolbar" style="background:#fff;">
            <div id="pagination" class="f-fr">
                <div class="">
                    <el-button size="small">通讯录</el-button>
                </div>
            </div>

            <el-button size="small" type="primary">发送</el-button>
            <el-button-group >
              <el-button size="small" @click="preview">预览</el-button>
              <el-button size="small">存草稿</el-button>
            </el-button-group>

             <el-button  size="small" plain>
                取消
            </el-button>
          </div>


          <div class="main" ref="iframe_height">
            <div class="mn-aside right_menu">
              <el-tabs v-model="activeName" @tab-click="handleClick">
                <el-tab-pane label="个人通讯录" name="first">个人通讯录</el-tab-pane>
                <el-tab-pane label="信纸" name="second">
                  <ul c>
                    <li><a href="#">
                      <img src="../img/none_zh.png" alt="">
                      <span class="bg"></span>
                    </a></li>
                    <li><a href="#" class="active">
                      <img src="../img/Peace_m.jpg" alt="">
                      <span class="bg"></span>
                    </a></li>
                    <li><a href="#">
                      <img src="../img/Buckle_m.jpg" alt="">
                      <span class="bg"></span>
                    </a></li>
                    <li><a href="#">
                      <img src="../img/LeatherCowBoy_m.jpg" alt="">
                      <span class="bg"></span>
                    </a></li>
                    <li><a href="#">
                      <img src="../img/Lilium_martagan_m.jpg" alt="">
                      <span class="bg"></span>
                    </a></li>
                    <li><a href="#">
                      <img src="../img/Lotus_m.jpg" alt="">
                      <span class="bg"></span>
                    </a></li>
                  </ul>
                </el-tab-pane>
                <el-tab-pane label="模板信" name="third">模板信</el-tab-pane>
              </el-tabs>
            </div>
            <form class="u-form mn-form">
              <div class="form-tt compose_title">
                <el-form size="mini" inline-message :model="ruleForm2" status-icon ref="ruleForm2" label-width="80px" class="demo-ruleForm" style="font-size:16px;">
                  <el-form-item label="发件人:">
                    <el-input type="text" value="myself@test.com" readonly auto-complete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="收件人:" prop="checkReciver">
                    <el-select required
                      v-model="ruleForm2.reciver"
                      multiple
                      filterable
                      allow-create
                      placeholder="">
                      <el-option
                        v-for="item in options5"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                      </el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="抄   送:" prop="copyer">
                    <el-input v-model.number="ruleForm2.copyer"></el-input>
                  </el-form-item>
                  <el-form-item label="主  题:" prop="subject">
                    <el-input v-model="ruleForm2.subject"></el-input>
                  </el-form-item>
                  <el-form-item label="密  级:" prop="secret">
                    <el-input v-model.number="ruleForm2.secret" readonly></el-input>
                  </el-form-item>
                  <el-button type="primary" size="small" @click="submitForm('ruleForm2')">添加附件</el-button>
                </el-form>
              </div>
              <div class="form-edr compose_editor" ref="editor_box">

                <editor id="editor_id" ref="editor_id" :height="iframe_height" width="100%" :content="content" v-model="content"
                    :afterChange="afterChange()"
                    pluginsPath="/static/kindeditor/plugins/"
                    :loadStyleMode="false"
                    @on-content-change="onContentChange">

                </editor>

              </div>
              <div class="form-toolbar compose_footer">
                <div>
                  <el-checkbox v-model="number_sign">数字签名</el-checkbox>
                  <el-checkbox v-model="safe_secret">安全加密</el-checkbox>
                </div>
                <div class="bt-hd-wrap">
                  <el-checkbox v-model="number_sign">保存到"已发送"</el-checkbox>
                  <el-checkbox v-model="safe_secret">设为"紧急"</el-checkbox>
                  <el-checkbox v-model="number_sign">已读回执</el-checkbox>
                  <el-checkbox v-model="safe_secret">定时发送</el-checkbox>
                  <el-checkbox v-model="number_sign">阅后即焚</el-checkbox>
                  <el-checkbox v-model="safe_secret">邮件加密</el-checkbox>
                  <el-checkbox v-model="number_sign">禁止转发</el-checkbox>
                </div>
              </div>
            </form>
          </div>
        </section>
      </div>
    </div>

</template>
<script>
  import { quillEditor } from 'vue-quill-editor'
  export default {
    props:{
      iframe_height:'',
    },
    data(){
      return {
        content:'contentceshi',
        activeName: 'second',
        number_sign:false,
        safe_secret:true,
        ruleForm2: {
          reciver: [],
          copyer: '',
          subject: '',
          secret:'非密'
        },
        options5: [{
          value: '123',
          label: 'system@test.com'
        }, {
          value: '456',
          label: 'anna@test.com'
        }, {
          value: '789',
          label: 'lw@test.com'
        }],
      };
    },
    methods:{

      handleClick(tab, event) {
        console.log(tab, event);
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            console.log(this.ruleForm2.reciver)
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      onContentChange (val) {
        console.log(this.$refs.editor_id.$data.outContent)
      },
      afterChange (val) {

      },
      preview(){
        //ke-toolbar-icon ke-toolbar-icon-url ke-icon-preview
        let btn = document.querySelector('.ke-toolbar-icon.ke-toolbar-icon-url.ke-icon-preview');
        btn.click();
      }
    },

  }
</script>
<style>
  .right_menu .el-tabs__nav-scroll{
    padding-left:10px;
  }
  .right_menu .el-tabs__content{
    padding:0 10px;
  }
  .mn-aside.right_menu{
    padding:0;
    width:240px;
    box-sizing:border-box;
  }
  .right_menu ul li{
    width:50%;
    float:left;
    text-align:center;
    margin-bottom:20px;
  }
  .right_menu ul li a{
    border:1px solid #e3e4e5;
    display:inline-block;
    position:relative;
    width: 78px;
    height: 48px;

  }
  .right_menu ul li a.active{
    border:1px solid transparent;
  }
  .right_menu ul li a.active .bg{
    background: url(../img/selected.gif) no-repeat;
    width: 80px;
    height: 52px;
    display: block;
    position: absolute;
    z-index: 9;
    top: 0;
    left: 0;
  }
  .compose_title input{
    border:none;
    /*border-bottom:1px solid #dcdfe6;*/
    border-radius:0;
  }
  .compose_title .el-form-item{
    border-bottom:1px solid #dcdfe6;
    margin-bottom:6px;
  }
  .compose_title .el-select{
    width:100%;
  }
  .compose_title .el-input--mini{
    font-size:15px;
  }
  .compose_footer>div{
    padding:0 14px;
  }
  .m-mlcompose .mn-form .form-edr.compose_editor{
    position:absolute;
    top:224px;
    bottom:72px;
    height:auto;
  }
</style>

