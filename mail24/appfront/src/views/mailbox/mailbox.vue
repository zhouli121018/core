<template>
    <div>
        <section class="m-mail">
            <MailAside></MailAside>
<article class="mlmain mltabview">
                <router-view></router-view>
</article>
        </section>

    </div>
</template>
<script>
import router from '@/router'
import MailAside from './components/MailAside'
export default {
    components:{
      MailAside
    },
    data:function(){
        return{
            activeTab:0,
            tab1:{id:0,url:'home',text:'收件箱'},
            tabList:[
              {id:14724,text:'邮件主题1'},
              {id:14722,text:'邮件主题2'}
            ],

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
        this.jumpTo('/mailbox/read/'+vid);
        this.activeTab = key+1;
        console.log(this.activeTab)
      },
      delTabs(id){
          this.tabList.splice(id,1);
          if(this.activeTab == id+1){
            this.changeTab1(this.tab1.url);
          }
      },

    }
}
</script>

<style>
/*.mltabview-content{*/
    /*top:0!important;*/
/*}*/
</style>
