<template>
    <div ref="tab_parent">
        <section class="m-mail">
            <!--<MailAside @getData="getData" @getCompose="getCompose" ref="menubar"></MailAside>-->
            <aside class="mlsidebar">
                <div class="mlsidebar-bg"></div>
                <div class="u-btns">
                    <button class="u-btn u-btn-default u-btn-large btn-compose j-mlsb" type="button" @click="goToCompose"><i class="iconfont icon-iconcreate"></i> <span class="title">写 信</span></button>
                    <button class="u-btn u-btn-default u-btn-large btn-inbox j-mlsb" type="button" @click="reloadMails"><i class="iconfont icon-iconinbox"></i></button>
                </div>

                <div class="wrapper u-scroll">
                    <el-tree
                      :data="folderList"
                      node-key="id"
                      :default-checked-keys="checkNodes"
                      :highlight-current="true"
                      @node-click="handleNodeClick" ref="treeMenuBar" id="treeMenuBar">
                      <span class="custom-tree-node" slot-scope="{ node, data }" :title="node.label">


                        <span>{{ node.label }} <el-badge v-if="data.unseen" class="mark" :value="data.unseen" /></span>

                        <span class="" style="position:absolute;right:2px;" class="hide_btn">
                          <el-button
                            type="text"
                            size="mini"
                            @click.stop.prevent="() => showDialog(data)" title="新建文件夹">
                            <i class="el-icon-plus"></i>
                          </el-button>
                          <el-button
                            type="text"
                            size="mini"
                            v-if="!data.is_default"
                            @click.stop="() => remove(node, data)" title="删除">
                            <i class="el-icon-delete"></i>
                          </el-button>
                        </span>
                      </span>
                    </el-tree>
                </div>

                      <el-dialog title="新建文件夹" :visible.sync="dialogFormVisible" :append-to-body="true">
                    <el-form :model="form" :rules="rules" ref="ruleForm">
                      <el-form-item label="文件夹名称" :label-width="formLabelWidth" prop="name">
                        <el-input v-model="form.name" auto-complete="off"></el-input>
                      </el-form-item>

                    </el-form>
                    <div slot="footer" class="dialog-footer">
                      <el-button @click="dialogFormVisible = false">取 消</el-button>
                      <el-button type="primary" @click="append">确 定</el-button>
                    </div>
                  </el-dialog>

            </aside>
            <article class="mlmain mltabview tab_box" :class="{position_top0:!tabList.length}" ref="editor_h">

                    <el-tabs v-model="editableTabsValue2" type="card" closable @tab-remove="removeTab" class="tab_style_tt" @tab-click="tabClick" :class="{hide_tab_top:editableTabs2.length<=1}" v-if="showTabIndex==1" ref="tabref">
                      <el-tab-pane
                        v-for="(item, index) in editableTabs2"
                        :key="item.name"
                        :label="item.title"
                        :name="item.name"

                      >
                         <span slot="label" class="tab_title" :class="{no_close:item.name==1}" :title="item.title"><i class="" :class="{'el-icon-message':item.type=='read','el-icon-edit':item.type!='read'&&item.name!='1','el-icon-menu':item.name=='1'}"></i> {{item.title | hide_subject}} </span>
                        <!--<div :style="{height: tab_content_height}">-->

                        <!--</div>-->
                        <Innerbox v-if="item.name=='1'" :boxId="boxId" :curr_folder="curr_folder"  @getRead="getRead" :unseencount="unseencount" :floderResult="floderResult" ref="innerbox"></Innerbox>
                        <Read :readId="item.rid" :readFolderId="item.fid" :tagName="item.name" v-if="item.type=='read'"></Read>
                        <Compose  v-if="item.type!='read'&&item.name!='1'" :ref="'ref_compose_'+item.name" :iframe_height="iframe_height" :rid="item.name" :parent_ruleForm2="ruleForm2" :parent_content="content" :parent_maillist="maillist" :parent_maillist_copyer="maillist_copyer" :parent_fileList="fileList" :compose_type="item.type"></Compose>

                      </el-tab-pane>
                    </el-tabs>
                    <Home v-if="showTabIndex==0"></Home>
                    <!--<Innerbox v-if="showTabIndex==1" :boxId="boxId" :curr_folder="curr_folder" @getRead="getRead" ref="innerbox"></Innerbox>-->
                    <!--<Read v-if="showTabIndex==2" :readId="readId" :readFolderId="readFolderId"></Read>-->
                    <!--<Compose v-if="showTabIndex==3" :iframe_height="iframe_height" ></Compose>-->
            </article>
        </section>

    </div>
</template>
<script>
import router from '@/router'
import MailAside from './components/MailAside'
import {getMailMessage,getFloder,creatFolder,deleteFolder } from "@/api/api"
import Innerbox from './components/innerbox'
import Home from './components/home'
import Read from './components/read'
import Compose from './components/compose'
export default {
  components:{
    MailAside,Innerbox,Home,Read,Compose
  },
  data:function(){
      return{
        content:'',
        maillist: [
          // {email:'anna@test.com',fullname:'章太炎',id:12280,status:true,value:'章太炎<anna@test.com>'}
        ],
        maillist_copyer: [],
        fileList: [],
        ruleForm2: {
          is_html:true,
          is_cc:true,
          is_partsend:false,
          to: [["512167072@qq.com",'zhouli']],
          cc: [],
          subject: '',
          secret:'非密',
          is_save_sent:true,
          is_confirm_read:true,
          is_schedule:false,
          schedule_day:'',
          is_password:false,
          password:'',
          is_burn:false,
          burn_limit:1,
          burn_day:'',
          html_text:'',
          plain_text:'',
          attachments:[],
          net_attachments:[]
        },
        hashTab:[],
        tab_content_height:'',
        editableTabsValue2: '1',
        editableTabs2: [{
          title: '收件箱',
          name: '1',
          fid:'INBOX'
        }],
        tabIndex: 1,
        floderResult:[],
        activeMenubar:{},
        iframe_height:'',
        showTabIndex:0,
        activeTab:0,
        readId:'',
        readFolderId:'',
        curr_folder:'收件箱',
        unseencount:0,
        tab1:{id:0,url:'home',text:'收件箱'},
        tabList:[],
        titleHash:[],
        boxId:'INBOX',

        checkNodes:[],

        defaultProps: {
          children: 'children',
          label: 'label',
        },
        dialogFormVisible: false,
        form: {
          title:'',
          name: '',
          region: '',
        },
        rules:{
          name:[{required:true,message:'请填写文件夹名称！',trigger:'blur'}]
        },
        formLabelWidth: '120px',
        rootFloder:''
      }
  },
  methods:{
    tabClick(tab,event){
      this.showTabIndex=1;
    },
    addTab(type,subject,rid,fid,info) {
      if(type=='compose'||type == 'compose_to_list'){
        this.ruleForm2['refw_type']=undefined;
        this.ruleForm2 = {
          is_priority:false,
          is_html:true,
          is_cc:true,
          is_partsend:false,
          to: [],
          cc: [],
          subject: '',
          secret:'非密',
          is_save_sent:true,
          is_confirm_read:true,
          is_schedule:false,
          schedule_day:'',
          is_password:false,
          password:'',
          is_burn:false,
          burn_limit:1,
          burn_day:'',
          html_text:'',
          plain_text:'',
          attachments:[],
          net_attachments:[]
        };
        this.content = '';
        this.maillist = [];
        this.maillist_copyer = [];
        this.fileList = [];
      }else if(type =='compose_net_atta'){
        this.ruleForm2['refw_type']=undefined;
        this.ruleForm2 = {
          is_priority:false,
          is_html:true,
          is_cc:true,
          is_partsend:false,
          to: [],
          cc: [],
          subject: '',
          secret:'非密',
          is_save_sent:true,
          is_confirm_read:true,
          is_schedule:false,
          schedule_day:'',
          is_password:false,
          password:'',
          is_burn:false,
          burn_limit:1,
          burn_day:'',
          html_text:'',
          plain_text:'',
          attachments:[],
          net_attachments:[]
        };
        this.content = '';
        this.maillist = [];
        this.maillist_copyer = [];
        this.fileList = this.$store.getters.getPfileNetAtta;
      }
      if(type == 'compose_to_list'){
        this.maillist = this.$store.getters.getToList;
      }
      if(rid && this.hashTab[type+rid+fid+'']){
        this.editableTabsValue2 = this.hashTab[type+rid+fid+''];
      }else{
        let newTabName = ++this.tabIndex + '';
        this.hashTab[type+rid+fid+''] = newTabName;
        this.editableTabs2.push({
          title: subject||'无主题',
          name: newTabName,
          content: 'New Tab content',
          rid:rid,
          fid:fid,
          type:type,
          info:info
        });
        this.editableTabsValue2 = newTabName;
      }

    },
    removeTab(targetName) {
      let tabs = this.editableTabs2;
      let activeName = this.editableTabsValue2;
      if (activeName === targetName) {
        tabs.forEach((tab, index) => {
          if (tab.name === targetName) {
            let nextTab = tabs[index + 1] || tabs[index - 1];
            if (nextTab) {
              activeName = nextTab.name;
            }
          }
        });
      }
      this.editableTabsValue2 = activeName;
      for(let i=0;i<tabs.length;i++){
        if(tabs[i].name == targetName){
          if(tabs[i].rid && tabs[i].fid){
            this.hashTab[tabs[i].type+tabs[i].rid+tabs[i].fid+''] = false;
          }
        }
      }
      this.editableTabs2 = tabs.filter(tab => tab.name !== targetName);
    },
    jumpTo(path){
        router.push(path);
    },
    changeTab1(){
      this.activeTab = 0;
      this.showTabIndex = 1;
      this.$router.push('/mailbox/innerbox')
    },
    changeTabs(v,key){
      if(v.id == 'compose'){
        this.showTabIndex = 3;
        this.$router.push('/mailbox/compose')
      }else{
        this.showTabIndex = 2;
        this.readId = v.id;
        this.readFolderId = v.folder;
        this.$router.push('/mailbox/readmail')
      }

      this.activeTab = v.id;
    },
    delTabs(id,vid){
        this.tabList.splice(id,1);
        this.titleHash[vid] = false;
        if(vid == 'compose'){
          this.$store.commit('setIsCompose',false)
        }
        if(this.activeTab == vid){
          this.changeTab1();
        }
    },
    closeAllTab(){
      this.tabList = [];
      this.titleHash = [];
      this.changeTab1();
    },

    setCurrentKey(boxId) {
      this.$nextTick(() =>{
        this.$refs.treeMenuBar.setCurrentKey(boxId||'INBOX');
        if(this.$refs.treeMenuBar.getCurrentNode()){
          this.unseencount = this.$refs.treeMenuBar.getCurrentNode().unseen;
          this.editableTabs2[0].title = this.$refs.treeMenuBar.getCurrentNode().label;
        }
        // let data = this.$refs.treeMenuBar.getCurrentNode();
        // this.pab_cname = data.groupname;
      })
    },
    getData(obj){
      this.activeMenubar = obj;
      this.showTabIndex = 1;
      this.activeTab = 0;
      this.curr_folder = obj.label;
      this.unseencount = obj.unseen;
      this.tab1.text = obj.label;
      this.boxId = obj.id;
      this.editableTabsValue2 = '1';
    },
    getCompose(obj){
      this.showTabIndex = obj.activeTab;
      if(this.titleHash['compose']){

      }else{
        this.titleHash['compose']=true;
        this.$store.commit('setIsCompose',true)
        this.tabList.push({id:'compose',text:'写信'})
      }
      this.activeTab = 'compose';
    },
    getRead(obj){
      if(this.titleHash[obj.id]){

      }else{
        this.titleHash[obj.id]=true;
        this.tabList.push({id:obj.id,text:obj.subject,folder:this.activeMenubar.id})
      }
      this.readId = obj.id;
      this.readFolderId = this.activeMenubar.id;
      this.activeTab = obj.id;
    },
    getFloderfn(){
      getFloder().then((res)=>{
        this.floderResult = res.data;
        if(sessionStorage['checkNodes']){
          this.checkNodes = [];
          this.checkNodes.push(sessionStorage['checkNodes'])
        }
        if(this.$route.params.boxId)this.setCurrentKey(this.$route.params.boxId);
      },(err)=>{
        console.log(err)
      });
    },

    showDialog(data) {
        this.dialogFormVisible = true;
        this.rootFloder = data;
        this.form.title = data.label;

      },
    append(){
      this.$refs['ruleForm'].validate((valid) => {
        if (valid) {
          let newName = this.form.name;
          if (!this.rootFloder.children) {
            this.$set(this.rootFloder, 'children', []);
          }
          creatFolder({"name":this.form.name}).then((suc)=>{
            this.getFloderfn();
            this.form.name='';
            this.$message({
              type: 'success',
              message: '添加成功!'
            });
          },(err)=>{
            this.$message({
              type: 'error',
              message: '添加失败！'
            });
            console.log(err);
          })

          this.dialogFormVisible = false;
        } else {
          return false;
        }
      });

    },

    remove(node, data) {
      const parent = node.parent;
      const children = parent.data.children || parent.data;
      const index = children.findIndex(d => d.id === data.id);
      this.$confirm('删除 "'+data.label+'" 文件夹, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteFolder(data.id).then((suc)=>{
          this.getFloderfn();
          if(this.$route.path!='/mailbox/welcome' && this.checkNodes[0] == data.id){
            this.$router.push('/mailbox/innerbox/INBOX')
            sessionStorage['checkNodeLabel'] = '收件箱'
          }
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
        },(err)=>{
          console.log(err)
          this.$message({
            type: 'error',
            message: '删除失败!'
          });
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });

    },
    handleNodeClick(data) {
      this.$router.push('/mailbox/innerbox/'+data.id)
      this.getData(data);
      this.checkNodes=[data.id];
      sessionStorage['checkNodes']=data.id;
      sessionStorage['checkNodeLabel']=data.label;
      this.editableTabs2[0].title = data.label;
      // this.$router.push('/mailbox/innerbox')
    },
    goToCompose(){
      // this.$emit('getCompose', {activeTab:3});
      // this.$router.push('/mailbox/compose')
      this.showTabIndex = 1;
      this.addTab('compose','写信')
    },
    reloadMails(){
      this.getFloderfn();
      if(this.$refs.innerbox[0]){
        this.$refs.innerbox[0].getMessageList()
      }

    },

  },
  mounted(){
    this.getFloderfn();
    const fheight = this.$refs.editor_h.getBoundingClientRect().height-50-50-220-80;
    this.iframe_height = fheight+'px';
  },
  computed: {
    username() { // 获取store中的数据
      return this.$store.state.userInfo.name;
    },
    folderList(){
        let folder = this.floderResult;
        let arr = [];
        for(let i=0;i<folder.length;i++){
          let obj={};
          obj['label'] = folder[i]['name'];
          obj['id'] = folder[i]['raw_name'];
          obj['flags'] = folder[i]['flags'];
          obj['unseen'] = folder[i]['unseen_count'];
          obj['is_default'] = folder[i]['is_default'];
          arr.push(obj);
        }
        return arr;
      },
  },
  created(){
    if(this.$route.name == 'innerbox'){
      this.showTabIndex = 1;
      // this.getData({id:'INBOX',label:'收件箱'})
      this.setCurrentKey(this.$route.params)
    }else{
      this.showTabIndex = 0;
      this.$nextTick(()=>{
        this.$refs.treeMenuBar.setCurrentKey('');
      })

    }

  },
  watch:{
      $route(v,o){
        if(v.path == '/mailbox/welcome'){
          this.showTabIndex = 0;
        }else if(v.path.indexOf('/mailbox/innerbox')>=0){
          this.showTabIndex = 1;
          this.setCurrentKey(v.params.boxId)
        }
      },
      username(nv,ov){
        this.getFloderfn();
      },
    editableTabsValue2(nv){

        let is_edit = false;
        for(let i=0;i<this.editableTabs2.length;i++){
          if(this.editableTabs2[i].name == nv && this.editableTabs2[i].type && this.editableTabs2[i].type.indexOf('compose')>=0){
            let a ='ref_compose_'+nv;
            if(this.$refs[a])this.$refs[a][0].timer()
            is_edit = true;
          }
        }
        if(!is_edit && this.$store.getters.getTimer){
          clearInterval(this.$store.getters.getTimer)
        }
    }

  },
  filters: {
    hide_subject: function (value) {
      if (!value) return ''
      value = value.toString()
      if(value.length>6){
        return value.slice(0,6)+'...'
      }else{
        return value
      }
    },
    plain_rn:function(value){
      if (!value) return '';
      var reg = new RegExp("\r\n", "g");//g,表示全部替换
      value = value.replace(reg, "<br/>");
      return value;
    }
  },
  beforeRouteLeave (to, from , next) {
    let hasCompose = false;
    for(let i=0;i<this.editableTabs2.length;i++){
      if(this.editableTabs2[i].type && this.editableTabs2[i].type.indexOf('compose')>=0){
        hasCompose = true;
      }
    }
    if(hasCompose){
      if(to.path=='/login'){
        if(this.$store.getters.getTimer){clearInterval(this.$store.getters.getTimer)}
        next();
        return;
      }
      if(to.path.indexOf('/mailbox/innerbox/')>=0){
        if(this.$store.getters.getTimer){clearInterval(this.$store.getters.getTimer)}
        next();
        return;
      }
      this.$confirm('您正在写信中，是否离开写信页面？', '系统信息', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        dangerouslyUseHTMLString: true,
        type: 'warning'
      }).then(() => {
        if(this.$store.getters.getTimer){clearInterval(this.$store.getters.getTimer)}
        next()
      }).catch(() => {
        next(false)
      });
    }else{
      if(this.$store.getters.getTimer){clearInterval(this.$store.getters.getTimer)}
      next();
    }
  }

}
</script>

<style>
  .fr{
    float:right;
  }
  .hide_btn{
    display:none;
  }
  .el-tree-node:hover .hide_btn{
    display:inline-block;
  }
  .tab_box .el-tabs__header{
    margin:0 0 5px;
  }
  /*.el-tabs__nav .el-tabs__item:nth-child(1) span.el-icon-close{*/
    /*display: none;*/
/*}*/
  .no_close+.el-icon-close{
    display:none;
  }
  .hide_tab_top .el-tabs__header.is-top{
    display:none;
  }
  .tab_title{
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  .tab_box>div.el-tabs.el-tabs--card{
    position:relative;
  }
  .tab_box>div.el-tabs.hide_tab_top.tab_style_tt>.el-tabs__content{
    top:0 !important;
  }
  .tab_box>div.el-tabs.tab_style_tt>.el-tabs__content{
    overflow:auto;
    box-sizing: border-box;
    padding-bottom:10px;
    /*min-height:600px;*/
    position: absolute;
    top: 41px;
    bottom: 0;
    left: 0;
    right: 0;
  }
  .tab_box .el-tabs.el-tabs--card.el-tabs--top{
    height:100%;
  }
.position_top0 .mltabview-content{
    top:0!important;
}
  .icon-icontabclose30x30.close{
    font-size:20px;
    padding-left:4px;
  }
</style>
