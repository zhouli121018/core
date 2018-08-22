<template>
    <div>
        <section class="m-mail">
            <MailAside @getData="getData"></MailAside>
            <article class="mlmain mltabview">
                    <div class="u-tab u-tab-seamless u-tab-highlight j-mltab" v-if="tabList.length">
                              <ul class="mltabview-nav">
                                <li class="mltabview-trigger" :class="{'z-current':activeTab==0}" :title="tab1.text"><span class="bar"></span><div class="trigger-wrap"><a href="#" trigger-title="" class="" :title="tab1.text" @click="changeTab1(tab1.url)">{{tab1.text}}</a></div></li>
                                <li v-for="(v,k) in tabList" :class="{'z-current':activeTab==k+1}"><span class="bar"></span><div class="trigger-wrap"><a href="#" @click="changeTabs(v.id,k)" :title="v.text">{{v.text}}</a><span class="iconfont icon-icontabclose30x30 close" @click.stop="delTabs(k)"></span></div></li>

                              </ul>
                              <div class="iconfont icon-iconcloseall closeall"></div>
                        </div>
                    <Home v-if="showTabIndex==0"></Home>
                    <Innerbox v-if="showTabIndex==1" :collapseItems="collapseItems" :curr_floder="curr_floder"></Innerbox>
                    <Read v-if="showTabIndex==2" @getRead="getRead"></Read>
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
export default {
    components:{
      MailAside,Innerbox,Home,Read
    },
    data:function(){
        return{
            showTabIndex:0,
            activeTab:0,
            curr_floder:'收件箱',
            tab1:{id:0,url:'home',text:'收件箱'},
            tabList:[
              {id:14724,text:'邮件主题1'},
              {id:14722,text:'邮件主题2'}
            ],
          collapseItems:[
            {
                  id:0,
                  title:"更早 （3）",
                  lists:[
                    {uid:0,isread:false,flagged:true,subject:'[召回邮件失败] MEMZ彩虹猫病毒/[Recall mail 失败] MEMZ彩虹猫病毒',internaldate:'08-09',mfrom:'postman',
                    plain:'发给751296883@qq.com的邮件召回失败,原因：不支持召回  email sent to 751296883@qq.com has been recalled unsucce',checked:false},
                    {uid:1,isread:true,flagged:false,subject:' MEMZ彩虹猫病毒/[Recall mail 失败] MEMZ彩虹猫病毒',internaldate:'08-08',mfrom:'postman',
                    plain:'发给751296883@qq.com的邮件召回失败,原因：不支持召回  email sent to 751296883@qq.com has been recalled unsucce',checked:false},
                    {uid:2,isread:true,flagged:false,subject:'欢迎进入XT5体验中心',internaldate:'08-06',mfrom:'postman',
                    plain:'',checked:false}
                    ]
              }
          ]

        }
    },
    methods:{
      jumpTo(path){
          router.push(path);
      },
      changeTab1(url){
        this.activeTab = 0;
        this.jumpTo('/mailbox/'+url);
      },
      changeTabs(vid,key){
        this.jumpTo('/read/');
        this.activeTab = key+1;
      },
      delTabs(id){
          this.tabList.splice(id,1);
          if(this.activeTab == id+1){
            this.changeTab1(this.tab1.url);
          }
      },
      getMessageList(param){
        getMailMessage(param).then((res)=>{
          var items = res.data;
          for(var i=0;i<items.length;i++){
            items[i].flagged = (items[i].flags.indexOf('Flagged')>=0);
            items[i].isread = (items[i].flags.indexOf('Seen')>=0);
            items[i].plain = '';
            items[i].checked = false;
          }
          this.collapseItems[0].lists = items;
        },(err)=>{
          console.log(err)
        })
      },
      getData(obj){
        this.curr_floder = obj.curr_floder;
        this.showTabIndex = obj.activeTab;
        this.getMessageList({folder:obj.id});
      },
      getRead(obj){
        console.log(obj)
        this.showTabIndex = obj.activeTab;
      }

    },
    beforeMount:function(){
      // this.test();
      this.getMessageList();

    },
}
</script>

<style>
/*.mltabview-content{*/
    /*top:0!important;*/
/*}*/
</style>
