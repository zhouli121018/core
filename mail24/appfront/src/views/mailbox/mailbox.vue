<template>
    <div>
        <section class="m-mail">
            <aside class="mlsidebar">
                <div class="mlsidebar-bg"></div>
                <div class="u-btns">
                    <button class="u-btn u-btn-default u-btn-large btn-compose j-mlsb" type="button" data-op="compose"><i class="iconfont icon-iconcreate"></i> <span class="title">写 信</span></button>
                    <button class="u-btn u-btn-default u-btn-large btn-inbox j-mlsb" type="button" data-op="inbox"><i class="iconfont icon-iconinbox"></i></button>
                </div>

                <div class="wrapper u-scroll">
                    <el-tree :data="data" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
                </div>
            </aside>
            <article class="mlmain mltabview">
                <div class="u-tab u-tab-seamless u-tab-highlight j-mltab" v-if="tabList.length">
                    <ul class="mltabview-nav">
                      <li class="mltabview-trigger" :class="{'z-current':activeTab==0}" :title="tab1.text"><span class="bar"></span><div class="trigger-wrap"><a href="#" trigger-title="" class="" :title="tab1.text" @click="changeTab1(tab1.url)">{{tab1.text}}</a></div></li>
                      <li v-for="(v,k) in tabList" :class="{'z-current':activeTab==k+1}"><span class="bar"></span><div class="trigger-wrap"><a href="#" @click="changeTabs(v.id,k)" :title="v.text">{{v.text}}</a><span class="iconfont icon-icontabclose30x30 close" @click.stop="delTabs(k)"></span></div></li>

                    </ul>
                  <div class="iconfont icon-iconcloseall closeall"></div>
                </div>  
                <router-view></router-view>
            </article>
        </section>
    </div>
</template>
<script>
import router from '@/router'
export default {
    data:function(){
        return{
            activeTab:0,
            tab1:{id:0,url:'home',text:'收件箱'},
            tabList:[
              {id:14724,text:'邮件主题1'},
              {id:14722,text:'邮件主题2'}
            ],
          data: [
            {
              id: 1,
              url:'innerbox',
              label: '收件箱',

            }, {
              id: 2,
              url:'outbox',
              label: '代办邮件',

            }, {
              id: 3,
              url:'innerbox',
              label: '草稿箱',

            },{
              id:4,
              url:'outbox',
              label:'已发送'
            },{
              id:5,
              label:'其他文件夹',
              children:[
                {id:6,label:'病毒文件夹'}
              ]
            }],
          defaultProps: {
            children: 'children',
            label: 'label',
            title:'label'
          }
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
      handleNodeClick(data) {
          console.log(data);
          if(data.url){
            this.jumpTo('/mailbox/'+data.url);
          }

      }
    }
}
</script>

<style>
/*.mltabview-content{*/
    /*top:0!important;*/
/*}*/
</style>
