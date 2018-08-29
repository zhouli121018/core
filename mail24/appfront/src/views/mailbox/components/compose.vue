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
              <el-tabs v-model="activeName">
                <!--个人通讯录-->
                <el-tab-pane label="个人通讯录" name="first">
                  <el-input  placeholder="搜索" prefix-icon="el-icon-search" v-model="filterText">
                  </el-input>

                  <el-tree class="filter-tree" :data="contactList" :props="defaultProps" :filter-node-method="filterNode"
                   @node-click="selectContact"  accordion ref="tree2">
                  </el-tree>
                </el-tab-pane>

                <!--信纸-->
                <el-tab-pane label="信纸" name="second">
                  <ul c>
                    <li><a href="#" @click="">
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

                  <el-form-item label="收件人:">
                    <div class="padding_15">
                      <div class="mailbox_s" :class="{error:!v.status}" v-for="(v,k) in maillist" :key="k" :title="v.mailbox"><b>{{v.mailbox}}</b><i class="el-icon-close" @click="deleteMailboxForKey(k,v)"></i></div>
                      <el-autocomplete  class="no_padding"  v-model="state1" :fetch-suggestions="querySearch" @keydown.8.native="deleteMailbox"
                        @blur="addMailbox" @focus="insertMailbox=1" placeholder="" @select="handleSelect" :trigger-on-focus="false"></el-autocomplete>
                    </div>

                  </el-form-item>
                  <el-form-item label="抄   送:" prop="copyer">
                    <div class="padding_15">
                      <div class="mailbox_s" :class="{error:!v.status}" v-for="(v,k) in maillist_copyer" :key="k" :title="v.mailbox"><b>{{v.mailbox}}</b><i class="el-icon-close" @click="deleteMailboxForKey_copyer(k,v)"></i></div>
                      <el-autocomplete  class="no_padding" v-model="state_copyer" :fetch-suggestions="querySearch" @keydown.8.native="deleteMailbox_copyer"
                        @blur="addMailbox_copyer" @focus="insertMailbox=2" placeholder=""  @select="handleSelect_copyer" ></el-autocomplete>
                    </div>
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

                <editor id="editor_id" ref="editor_id" :height="iframe_height" width="100%" :content="content"
                    :afterChange="afterChange()"
                    pluginsPath="/static/kindeditor/plugins/"
                    :loadStyleMode="false"
                        :items="toolbarItems"
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
  import { contactPabGroupsGet,contactPabMapsGet,contactPabMembersGet } from '@/api/api'
  export default {
    props:{
      iframe_height:'',
    },
    data(){
      return {
        filterText:'',
        hashMail:[],
        insertMailbox:1,
        hashMail_copyer:[],
        maillist:[

        ],
        maillist_copyer:[],
        restaurants:[

        ],
        state1:'',
        state_copyer:'',
        toolbarItems:
        ['source', '|','formatblock', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold',
        'italic', 'underline',  'lineheight', '|',  'justifyleft', 'justifycenter', 'justifyright',
        'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', '|','subscript',
        'superscript', 'link', 'unlink','image',  'table','hr','|', 'undo', 'redo', 'preview',
           'fullscreen',
         ],
        content:'<div>内容</div>',
        activeName: 'first',
        number_sign:false,
        safe_secret:true,
        ruleForm2: {
          reciver: [],
          copyer: '',
          subject: '',
          secret:'非密'
        },
        contactList: [
          {
          id: 1,
          label: 'aaa组',
          children: [{
            id: 4,
            label: 'yc@test.com',
          }]},
          {
          id: 2,
          label: '未分组联系人',
          children: [{
            id: 5,
            label: 'lw@test.com'
          }, {
            id: 6,
            label: 'system@domain.com'
          }]},

          ],
        defaultProps: {
          children: 'children',
          label: 'label'
        }

      };
    },
    methods:{
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
      },
      addMailbox(){
        setTimeout(()=>{this.handleSelect()},300)
      },
      deleteMailbox(){
        if(!this.state1&&this.maillist.length>0){
          this.hashMail[this.maillist[this.maillist.length-1].mailbox] = false;
          this.maillist.pop();
        }
      },
      deleteMailboxForKey(k,v){
        this.hashMail[v.mailbox] = false;
        this.maillist.splice(k,1)
      },
      handleSelect(item) {
        // console.log(item);
        if(this.state1){
          if(this.hashMail[this.state1]){

          }else{
            this.hashMail[this.state1] = true;
            let obj = {};
            obj.mailbox = this.state1;
            obj.status = true;
            this.maillist.push(obj);
            this.state1 = '';
          }
        }
        this.state1 = '';
      },
      addMailbox_copyer(){
        setTimeout(()=>{this.handleSelect_copyer()},300)
      },
      deleteMailbox_copyer(){
        if(!this.state_copyer&&this.maillist_copyer.length>0){
          this.hashMail_copyer[this.maillist_copyer[this.maillist_copyer.length-1].mailbox] = false;
          this.maillist_copyer.pop();
        }
      },
      deleteMailboxForKey_copyer(k,v){
        this.hashMail_copyer[v.mailbox] = false;
        this.maillist_copyer.splice(k,1)
      },
      handleSelect_copyer(item) {
        // console.log(item);
        if(this.state_copyer){
          if(this.hashMail_copyer[this.state_copyer]){

          }else{
            this.hashMail_copyer[this.state_copyer] = true;
            let obj = {};
            obj.mailbox = this.state_copyer;
            obj.status = true;
            this.maillist_copyer.push(obj);
            this.state_copyer = '';
          }
        }
        this.state_copyer = '';
      },
      querySearch(queryString, cb) {
        var restaurants = this.restaurants;
        var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (restaurant) => {
          return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
      },
      loadAll() {
        return [
          { "value": "anna@test.com" },
          { "value": "lw@test.com" },
          { "value": "system@domain.com" },
        ];
      },
      filterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      selectContact(data){
        console.log(data)
        if(!data.children){
          if(this.insertMailbox==1){
          if(!this.hashMail[data.label]){
            this.hashMail[data.label]=true;
            this.maillist.push({mailbox:data.label,status:true});
          }
        }else if(this.insertMailbox == 2){
          if(!this.hashMail_copyer[data.label]){
            this.hashMail_copyer[data.label]=true;
            this.maillist_copyer.push({mailbox:data.label,status:true});
          }

        }
        }

      },
      //获取个人通讯录组数据
      getPabGroups(){
        contactPabMembersGet({"group_id": 0}).then((suc)=>{
          console.log(suc)
        },(err)=>{
          console.log(err);
        })
      },

    },
    mounted() {
      this.restaurants = this.loadAll();
      this.getPabGroups();
    },
    watch: {
      filterText(val) {
        this.$refs.tree2.filter(val);
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
  .compose_editor [data-name="preview"]{
    display:none;
  }
  .mailbox_s{
    float:left;white-space:nowrap;
    cursor:pointer;
    border:1px solid #a3d9d2;
    background-color: #e4f7f5;
    margin-right:6px;
    padding:0 4px;
    border-radius:12px;
  }
  .mailbox_s.error{
    background-color: #f2dede;
    border-color: #ebccd1;
    color: #a94442;
  }
  .mailbox_s>b{
    margin-right:4px;
  }
  .compose_title .no_padding .el-input__inner{
    padding:0;
  }
  .padding_15{
    padding-left:15px;
  }
</style>

