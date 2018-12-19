<template>
  <!--<article class="mlmain mltabview">-->
    <div class="mltabview-content">
      <div class="mltabview-panel">
      <div class="m-mlwelcome" data-view-cid="view-5" data-view-name="mail.welcome">
        <div class="container">
          <div class="header j-header">
            <div class="panel-sbj"><div class="tag skin-primary-bg"></div>您 好, {{username}}</div>
            <div class="panel-cnt">
              <div class="abstract">
                <div class="avatar">
                  <a href="javascript:void(0);" class="u-img u-img-round">

                    <img alt="avatar" class="j-avatar" v-if="gender =='male'"  src="@/assets/img/man.png">
                    <img alt="avatar" class="j-avatar" v-if="gender !='male'" src="@/assets/img/woman.png">
                  </a>
                </div>
                <div class="info">
                  <ul class="u-list u-list-horizontal j-link-trigger">
                    <li>
                      <span class="headings">我的邮箱:</span>
                      <a href="#" class="link" @click.prevent="viewMails" v-if="inboxUnread"><span class="mark">{{inboxUnread}}</span> 封未读邮件</a>
                      <span v-if="!inboxUnread">没有未读邮件</span>
                    </li>
                  </ul>
                  <ul class="u-list u-list-horizontal">
                    <li>
                      <span>邮箱容量: </span>
                      <div class="u-progress u-progress-success">
                        <div class="u-progress-bar" :style="{ width: userinfo.capacity_used_rate +'%'}"></div>
                      </div>
                      <span class="text-success">{{userinfo.capacity_used}} M / {{userinfo.capacity_total}} M</span>
                    </li>
                    <li style="display:none;">
                      <a href="javascript:void(0);" class="link" data-trigger="setting.folder.folder">管理</a>
                    </li>
                  </ul>
                  <ul class="u-list u-list-horizontal">
                    <li>最近登录: {{userinfo.last_login}}</li>
                    <li>{{userinfo.login_ip}} ({{userinfo.login_isp}})</li>
                    <li><a href="#" @click.prevent="search_details">详情</a></li>
                  </ul>

                </div>
              </div>

              <div class="weather" v-if="weatherinfo.has_weather">
                <div class="weadesc">
                  <div class="temp">{{weatherinfo.data.temLow}} ~ {{weatherinfo.data.temHigh}}℃</div>
                  <span>{{weatherinfo.data.stateDetailed}} / {{weatherinfo.data.windState}}</span>
                  <span class="place">{{weatherinfo.data.cityname}}</span>
                </div>
                <div class="weaimg" :style="{ backgroundPosition: weatherinfo.data.imgLocation1 }">
                  <!-- <img src="/coremail/XT5/89517/style/img/weather/zhongyu.png" alt="weather"> -->
                </div>
              </div>
            </div>
          </div>

          <div class="main j-main">
            <div class="bulletins" style="background: #fff;">
              <div class="panel-sbj" v-if="loginAfterData.system_name">
                <div class="tag skin-primary-bg"></div> {{loginAfterData.system_name}}
              </div>
              <div style="padding:20px;line-height:20px;" v-if="loginAfterData.system_name" v-html="loginAfterData.system_remark">

              </div>

              <el-tabs type="border-card" v-if="loginAfterData.welcome_links && loginAfterData.welcome_links.length>0">
                <el-tab-pane v-for="(l,k) in loginAfterData.welcome_links" :label="l.title" :key="k">
                  <el-row :gutter="10">
                    <el-col :xs="12" :sm="12" :md="8" :lg="6" :xl="6" v-for="(item,c) in l.links" :key="c" v-if="l.links && l.links.length>0">
                      <div style="border:1px solid #ECECEC;height:150px;overflow: auto;" class="clear">
                          <div style="float:left;width:48%;padding:1%;">
                            <a :href="item.url" target="_blank" v-if="item.url">
                              <img :src="origin + item.icon" style="width:100%;max-width:100%;">
                              <!--<img src="http://192.168.1.39:81/media/logo_f0XiV_20181218112627_990.jpg" style="width:100%;max-width:100%;">-->
                            </a>
                            <img :src="origin + item.icon" style="width:100%;max-width:100%;" v-if="!item.url">
                          </div>
                          <div style="float:left;width:48%;padding:1%;">
                            <p style="font-size:16px;">
                              <a :href="item.url" target="_blank" v-if="item.url" style="color:#333;text-decoration: none"><b> {{item.title}}</b></a></p>
                              <b v-if="!item.url"> {{item.title}}</b>
                            <p>
                              {{item.desc}}
                            </p>
                          </div>
                      </div>

                    </el-col>
                  </el-row>


                </el-tab-pane>
              </el-tabs>
              <div v-if="!loginAfterData.system_name && loginAfterData.welcome_links && loginAfterData.welcome_links.length == 0">
                <div class="panel-sbj">
                  <div class="tag skin-primary-bg"></div> 欢迎使用 Webmail
                </div>
                <div style="padding:20px 10px;">
                  <el-carousel trigger="click" >
                    <el-carousel-item v-for="banner in banners" :key="banner.id" >
                      <a href="http://www.comingchina.com" target="_blank">
                        <img :src="banner.url" :alt="banner.url" style="width:100%;">
                      </a>
                    </el-carousel-item>
                  </el-carousel>
                </div>

              </div>
              <div class="panel-sbj" v-if="false">
                <div class="tag skin-primary-bg"></div>
              </div>
              <div class="panel-cnt" v-if="false">
                <div class="content">


                </div>
              </div>

            </div>

            <div class="features j-features">
              <div class="panel-sbj">
                <div class="tag skin-primary-bg"></div>
                邮箱功能介绍
              </div>
              <div class="panel-cnt">
                <ul class="u-list u-list-img">
                  <li>
                    <div class="u-img icon-feature icon-check"></div>
                    <div class="u-img-text">
                      <a href="javascript:void(0);" class="u-img-title" @click="search_details">自助查询</a>
                      <div class="u-img-desc">邮箱使用记录查询，支持邮件召回、异地登录提醒</div>
                    </div>
                  </li>
                  <li>
                    <div class="u-img icon-feature icon-file"></div>
                    <div class="u-img-text">
                      <a href="javascript:void(0);" class="u-img-title" @click="view_file">文件中心</a>
                      <div class="u-img-desc">支持主流浏览器续传文件（支持Chrome，Safari）</div>
                    </div>
                  </li>
                  <li>
                    <div class="u-img icon-feature icon-schedule"></div>
                    <div class="u-img-text">
                      <a href="javascript:void(0);" class="u-img-title" @click="view_calendar">会议与日程</a>
                      <div class="u-img-desc">全新改版，高级版支持会议邀请和日程共享</div>
                    </div>
                  </li>
                  <li>
                    <div class="u-img icon-feature icon-client"></div>
                    <div class="u-img-text">
                      <!--<a href="http://software.icoremail.net/coremail-plugin/download.html" target="_blank" class="u-img-title">客户端插件</a>-->
                      <a href="#" @click.prevent="view_contact" class="u-img-title">通讯录</a>
                      <!--<div class="u-img-desc">可在Outlook，Foxmail中实现通讯录查询同步等功能</div>-->
                      <div class="u-img-desc">可在Outlook，Foxmail中实现通讯录查询同步等功能</div>
                    </div>
                  </li>
                  <li>
                    <div class="u-img icon-feature icon-lock"></div>
                    <div class="u-img-text">
                      <a href="javascript:void(0);" class="u-img-title" @click="view_setting">设置中心</a>
                      <div class="u-img-desc">个人资料、模板信、签名等设置</div>
                    </div>
                  </li>
                </ul>

                <div class="app">
                  <div>
                    <el-carousel trigger="click" indicator-position="outside" height="120px" v-if="loginAfterData.welcome_ads && loginAfterData.welcome_ads.length>0">
                      <el-carousel-item v-for="(item,k) in loginAfterData.welcome_ads" :key="k" v-if="loginAfterData.welcome_ads">
                        <a :href="item.link" target="_blank" v-if="item.link">
                          <img :src="origin + item.image" style="width:100%;max-width:100%;">
                        </a>
                        <img :src="origin + item.image" style="width:100%;max-width:100%;" v-if="!item.link">
                      </el-carousel-item>
                    </el-carousel>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div><!-- end container -->
        <div class="footer small text-gray">
          Copyright © <span>{{loginAfterData.name}}</span>
            <span v-if="loginAfterData.is_icp">
              <a :href="loginAfterData.icp_link" v-if="loginAfterData.icp_link"  target="_blank" style="color:#777;text-decoration:none;"> | {{loginAfterData.icp_no}}</a>
              <span v-if="!loginAfterData.icp_link"> | {{loginAfterData.icp_no}}</span>
            </span>
        </div>

      </div>
    </div>
    </div>

  <!--</article>-->
</template>

<script>
  import cookie from '@/assets/js/cookie';
  import {welcome} from '@/api/api'
  export default {
    name:'Home',
    data(){
      return {
        banners:[
          {id:1,url:require('../img/banner1.jpg')},
          {id:4,url:require('../img/banner4.jpg')},
          {id:2,url:require('../img/banner2.jpg')},
          {id:3,url:require('../img/banner3.jpg')},
        ],
        origin:window.location.origin, // window.location.origin 'http://192.168.1.39:81'
        userinfo: {
          "capacity_used": 1,
          "login_isp": "广东深圳电信",
          "capacity_used_rate": 0,
          "last_login": "2018年8月9日星期二下午15点49分46秒",
          "login_ip": "116.30.220.106",
          "unread": 10,
          "capacity_total": 1000
        },
        loginAfterData1:{
          "name":"77777umail",
          "title":"11111111111",
          "is_icp":true,
          "icp_no":"粤ICP备11061369号-1",
          "icp_link":"http://www.miitbeian.gov.cn/",
          "system_name":"aaaaaaaa",
          "system_remark":"aaaaaaaaaaaaa",
          "logout_url":null,
          "welcome_logo":"/media/logo_HXniZ_20181213113201_669.jpg",
          "welcome_links":[
            {"links":[
              {"url":"","title":"","icon":"/media/logo_0oyji_20181218094116_626.jpg","desc":"  "},
                {"url":"","title":"","icon":"/media/logo_Bzy1R_20181218094116_628.jpg","desc":"  "},
                {"url":"","title":"","icon":"/media/logo_EBe3i_20181218094116_628.jpg","desc":"  "},
                {"url":"","title":"","icon":"/media/logo_EBe3i_20181218094116_628.jpg","desc":"  "},
                {"url":"","title":"","icon":"/media/logo_AU9PJ_20181218094116_629.jpg","desc":""}
                ],
              "title":"首页链接"
            },
            {"links":[
              {"url":"","desc":"  ","icon":"/media/logo_CG5XS_20181218093036_594.jpg","title":""},
                {"url":"","desc":"  ","icon":"/media/logo_Q31Gg_20181218093036_596.jpg","title":""},
                {"url":"","desc":"  ","icon":"/media/logo_9AUO8_20181218093036_597.jpg","title":""},
                {"url":"","desc":"","icon":"/media/logo_Syjgv_20181218093036_597.jpg","title":""}
                ],
              "title":"首页链接"
            },
            {"links":[
              {"url":"","desc":"  ","icon":"/media/logo_dIcl4_20181218094534_579.jpg","title":""},
                {"url":"","desc":"  ","icon":"/media/logo_93ks7_20181218094534_580.jpg","title":""},
                {"url":"","desc":"  ","icon":"/media/logo_cVARr_20181218094534_580.jpg","title":""},
                {"url":"","desc":"","icon":"/media/logo_XYvCu_20181218094534_581.jpg","title":""}
                ],
              "title":"首页链接"
            },
            {"links":[
              {"url":"","desc":"  ","icon":"/media/logo_AVeob_20181218094547_727.jpg","title":""},
                {"url":"","desc":"  ","icon":"/media/logo_4M2i9_20181218094547_728.jpg","title":""},
                {"url":"","desc":"  ","icon":"/media/logo_Xc8Wr_20181218094547_729.jpg","title":""},
                {"url":"","desc":"","icon":"/media/logo_IHriA_20181218094547_729.jpg","title":""}
                ],
              "title":"首页链接"
            },
            {"links":[
              {"url":"","title":"","icon":"/media/logo_7LHtE_20181218094541_077.jpg","desc":"  "},
                {"url":"","title":"","icon":"/media/logo_lunr4_20181218094541_077.jpg","desc":"  "},
                {"url":"","title":"","icon":"/media/logo_yz7xE_20181218094541_077.jpg","desc":"  "},
                {"url":"","title":"","icon":"/media/logo_LEokC_20181218094541_077.jpg","desc":""}
                ],
              "title":"首页链接"
            }
          ],
          "welcome_ads":[
            {"image":"http://192.168.1.39:81/media/logo_G3sFK_20181213113312_339.jpg","link":"https://www.baidu.com/"}
          ]
        },
        weatherinfo:{
          has_weather:true,
          data:{
            cityname:"深圳",
            imgLocation1:'0 0',
            temLow:'0',
            temHigh:'0',
            stateDetailed:'晴',
            windState:'微风'
          }
        }
      }
    },
    methods:{
      view_setting(){
        this.$router.push('/setting/user')
      },
      view_contact(){
        this.$router.push('/contact/pab')
      },
      view_calendar(){
        this.$router.push('/calendar/index')
      },
      view_file(){
        this.$router.push('/file/pfile')
      },
      viewMails(){

        this.$router.push('/mailbox/innerbox/INBOX/')
        this.$nextTick(()=>{
          this.$parent.editableTabsValue2 = '1';
          let _this = this;
          setTimeout(function(){
            _this.$parent.$refs.innerbox[0].viewHandleCommand('unseen') ;
          },300)
        })


      },
      search_details(){
        this.$router.push('/search')
      },
      welcomefn(){
        welcome().then(res=>{
          this.userinfo = res.data.userinfo;
          this.weatherinfo = res.data.weatherinfo;
        })
      },
    },
    mounted: function(){

    },
    created:function(){
      // this.getLoginAfter();
      this.welcomefn()
    },
    computed: {
      gender(){
        return this.$store.getters.getSettingUser.gender;
      },
      username() { // 获取store中的数据
        return this.$store.getters.userInfo.name;
      },
      inboxUnread(){
        let c = this.$store.getters.getUnseenCount['INBOX'] || 0;
        return  c
        for(let i=0;i<this.$parent.folderList.length;i++){
          if(this.$parent.folderList[i]['id']=='INBOX'){
            return this.$parent.folderList[i].unseen;
          }
        }
      },
      loginAfterData(){
        return this.$store.getters.getLoginAfter
      }
    },
    watch: {
      username(nv,ov){
        this.welcomefn();
      },
    }
  }
</script>

<style>
  .lunkr_image{
    background:url('../../../assets/img/lunkr_banner.png')
  }
  .lunkr_download_links {
    margin-top: 12px;
    text-align: center;
  }
  .m-mlwelcome .icon-feature {
    background-image: url(../../../assets/img/features.png);
    width: 52px;
    height: 52px;
  }
  .weaimg{
    box-sizing: border-box;
    width:80px;
    height:80px;
    position:relative;
    left:10px;
    background:url(../../../assets/img/blue80.png) no-repeat;
    background-position:-80px -80px;
  }
</style>

