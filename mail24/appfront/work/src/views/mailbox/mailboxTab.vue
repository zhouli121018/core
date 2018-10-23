<template>
    <div>
        <section class="m-mail">
            <MailAside @getData="getData" @getCompose="getCompose" ref="menubar"></MailAside>
            <article class="mlmain mltabview tab_box" :class="{position_top0:!tabList.length}" ref="editor_h">

                    <el-tabs v-model="editableTabsValue2" type="card" closable @tab-remove="removeTab" class="tab_style_tt" @tab-click="tabClick" :class="{hide_tab_top:editableTabs2.length<=1}" v-if="showTabIndex==1">
                      <el-tab-pane
                        v-for="(item, index) in editableTabs2"
                        :key="item.name"
                        :label="item.title"
                        :name="item.name"

                      >
                         <span slot="label" class="tab_title" :class="{no_close:item.name==1}" :title="item.title"><i class="" :class="{'el-icon-message':item.type=='read','el-icon-edit':item.type!='read'&&item.name!='1','el-icon-menu':item.name=='1'}"></i> {{item.title | hide_subject}}</span>
                        <!--<div :style="{height: tab_content_height}">-->

                        <!--</div>-->
                        <Innerbox v-if="item.name=='1'" :boxId="boxId" :curr_folder="curr_folder"  @getRead="getRead" :floderResult="floderResult" ref="innerbox"></Innerbox>
                        <Read :readId="item.rid" :readFolderId="item.fid" v-if="item.type=='read'"></Read>
                        <Compose  v-if="item.type!='read'&&item.name!='1'" :iframe_height="iframe_height" :rid="item.name" :parent_ruleForm2="ruleForm2" :parent_content="content" :parent_maillist="maillist" :parent_maillist_copyer="maillist_copyer" :parent_fileList="fileList"></Compose>

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
import {getMailMessage,getFloder} from "@/api/api"
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
        editableTabsValue2: '2',
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
        tab1:{id:0,url:'home',text:'收件箱'},
        tabList:[],
        titleHash:[],
        boxId:'INBOX'
      }
  },
  methods:{
    tabClick(tab,event){
      this.showTabIndex=1;
    },
    addTab(type,subject,rid,fid,info) {
      if(type=='compose'){
        this.ruleForm2['refw_type']=undefined;
        this.ruleForm2 = {
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
      console.log(targetName)
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
    refreshMenu(){
      this.getFloderfn();
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

    getData(obj){
      this.activeMenubar = obj;
      console.log(this.activeMenubar)
      this.showTabIndex = 1;
      this.activeTab = 0;
      this.curr_folder = obj.label;
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
      console.log(obj);
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
      },(err)=>{
        console.log(err)
      });
    },

  },
  beforeMount:function(){
    // this.test();
    // this.getMessageList();
    console.log('router')
    console.log(this.$route.path)
    if(this.$route.path == '/mailbox/innerbox'){
      this.showTabIndex = 1;
    }else{
      this.showTabIndex = 0;
    }
  },
  mounted(){
    this.getFloderfn();
    const fheight = this.$refs.editor_h.getBoundingClientRect().height-50-50-220-80;
    console.log(fheight)
    this.iframe_height = fheight+'px';
    console.log(this.$route.path)
    let v = this.$route;
    if(v.path == '/mailbox/welcome'){
        this.showTabIndex = 0;
      }else if(v.path == '/mailbox/innerbox'){
        this.showTabIndex = 1;
      }else if(v.path == '/mailbox/readmail'){
        this.showTabIndex = 2;
      }else if(v.path == '/mailbox/compose'){
        this.showTabIndex = 3;
      };
  },
  computed: {
    username() { // 获取store中的数据
      return this.$store.state.userInfo.name;
    }
  },
  watch:{
      $route(v,o){
        console.log(v.path)
        if(v.path == '/mailbox/welcome'){
          this.showTabIndex = 0;
        }else if(v.path == '/mailbox/innerbox'){
          this.showTabIndex = 1;
        }else if(v.path == '/mailbox/readmail'){
          this.showTabIndex = 2;
        }else if(v.path == '/mailbox/compose'){
          this.showTabIndex = 3;
        }
      },
      username(nv,ov){
        this.$refs.menubar.getFloderfn();
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
      this.$confirm('您正在写信中，是否离开写信页面？', '系统信息', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        dangerouslyUseHTMLString: true,
        type: 'warning'
      }).then(() => {
        next()
      }).catch(() => {
        next(false)
      });
    }else{
      next();
    }
  }

}
</script>

<style>
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
    top: 56px;
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
