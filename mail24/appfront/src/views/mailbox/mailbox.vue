<template>
    <div>
        <section class="m-mail">
            <MailAside @getData="getData" @getCompose="getCompose" ref="menubar"></MailAside>
            <article class="mlmain mltabview" :class="{position_top0:!tabList.length}" ref="editor_h">
                    <div class="u-tab u-tab-seamless u-tab-highlight j-mltab" v-if="tabList.length">
                              <ul class="mltabview-nav">
                                <li class="mltabview-trigger" :class="{'z-current':activeTab==0}" @click="changeTab1" :title="tab1.text"><span class="bar"></span><div class="trigger-wrap"><a href="#" trigger-title="" class="" :title="tab1.text" >{{tab1.text}}</a></div></li>
                                <li v-for="(v,k) in tabList" :class="{'z-current':activeTab==v.id}"><span class="bar"></span><div class="trigger-wrap"><a href="#" @click="changeTabs(v,k)" :title="v.text">{{v.text}}</a><span class="iconfont icon-icontabclose30x30 close" @click.stop="delTabs(k,v.id)"></span></div></li>

                              </ul>
                              <div class="iconfont icon-iconcloseall closeall" @click="closeAllTab"></div>
                        </div>
                    <Home v-if="showTabIndex==0"></Home>
                    <Innerbox v-show="showTabIndex==1" :boxId="boxId" :curr_folder="curr_folder" @getRead="getRead"></Innerbox>
                    <Read v-if="showTabIndex==2" :readId="readId" :readFolderId="readFolderId"></Read>
                    <Compose v-if="showTabIndex==3" :iframe_height="iframe_height" ></Compose>
            </article>
        </section>

    </div>
</template>
<script>
import router from '@/router'
import MailAside from './components/MailAside'
import {getMailMessage} from "@/api/api"
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
          activeMenubar:{},
          iframe_height:'',
            showTabIndex:0,
            activeTab:0,
            readId:'',
            readFolderId:'',
            curr_folder:'收件箱',
            tab1:{id:0,url:'home',text:'收件箱'},
            tabList:[

            ],
          titleHash:[],
          boxId:'INBOX'


        }
    },
    methods:{
      jumpTo(path){
          router.push(path);
      },
      refreshMenu(){
        this.$refs['menubar'].getFloderfn();
      },
      changeTab1(){
        this.activeTab = 0;
        this.showTabIndex = 1;
      },
      changeTabs(v,key){
        if(v.id == 'compose'){this.showTabIndex = 3;}else{
          this.showTabIndex = 2;
          this.readId = v.id;
          this.readFolderId = v.folder;
        }

        this.activeTab = v.id;
      },
      delTabs(id,vid){
          this.tabList.splice(id,1);
          this.titleHash[vid] = false;
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
      },
      getCompose(obj){
        this.showTabIndex = obj.activeTab;
        if(this.titleHash['compose']){

        }else{
          this.titleHash['compose']=true;
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
        this.showTabIndex = obj.activeTab;
      }

    },
    beforeMount:function(){
      // this.test();
      // this.getMessageList();

    },
    mounted(){
      const fheight = this.$refs.editor_h.getBoundingClientRect().height-50-50-220-80;
      console.log(fheight)
      this.iframe_height = fheight+'px'
    }
}
</script>

<style>
.position_top0 .mltabview-content{
    top:0!important;
}
  .icon-icontabclose30x30.close{
    font-size:20px;
    padding-left:4px;
  }
</style>
