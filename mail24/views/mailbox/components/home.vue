<template>
  <div class="mltabview-panel">
    <div class="m-mlwelcome" data-view-cid="view-5" data-view-name="mail.welcome">
      <div class="container">
        <div class="header j-header">
          <div class="panel-sbj"><div class="tag skin-primary-bg"></div>中午好, {{username}}</div>
          <div class="panel-cnt">
            <div class="abstract">
              <div class="avatar">
                <a href="javascript:void(0);" class="u-img u-img-round">
                  <img alt="avatar" class="j-avatar" src="@/assets/img/man.png">
                </a>
              </div>
              <div class="info">
                <ul class="u-list u-list-horizontal j-link-trigger">
                  <li>
                    <span class="headings">我的邮箱:</span>
                    <a href="#" class="link" ><span class="mark">{{userinfo.unread}}</span> 封未读邮件</a>
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
                  <li>
                    <a href="javascript:void(0);" class="link" data-trigger="setting.folder.folder">管理</a>
                  </li>
                </ul>
                <ul class="u-list u-list-horizontal">
                  <li>最近登录: {{userinfo.last_login}}</li>
                  <li>{{userinfo.login_ip}} ({{userinfo.login_isp}})</li>
                  <li><a href="#">详情</a></li>
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
          <div class="bulletins">

            <div class="panel-sbj"><div class="tag skin-primary-bg"></div>欢迎体验Coremail 论客</div>
            <div class="panel-cnt">
              <div class="content">

                <p>
                  <a href="http://www.lunkr.cn/" class="lunkr_image" target="_blank" title="了解Coremail论客" style="display: block;width: 100%;height: 266px;background-size: cover;background-repeat:no-repeat;">
                    <!-- <img src="../assets/img/lunkr_banner.png" alt="" style="width: 100%; max-width: 100%;"> -->
                  </a>
                </p>
                <p class="lunkr_download_links">
                  <a href="http://www.lunkr.cn/" target="_blank">
                    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF8AAABGCAYAAACqlUimAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA9FJREFUeNrsnF1y2jAQxx3KU2c69Q3KDeqeIHACwgkSTkD8zAPkIc+BE0BOUPcEOCeIewP3BKUvfetMd5PVsGigcQdZyPDfGQ22JJT4p9Xuog+3IsjRpAUEgA/4EMA/G2mfyoPc39/f0Mc1pcfxeLwEfD/QE/r4SqkjWU/QfD/gGfiKUqyyc9h8P7KwwJdkcgDfk7npWtkpoh0/YoO/I63PAL8eTe/uyF5T4sjmC4Gfcp099YKUiwaEjyNKicouKM0pZQR8LXX6lK6sr7/UCznsvAgUeizhowstZlM05I4K7Bnfh2p2Vo7ARzIiJgE+47tWgFo/tczMoWLMFH5kVZCRw7bY1PRCMzlBRjsSqcQOm0xDBR9iqOkyTFyHPsF2ylPKBX5kQc4SfgL4x5M49KmG0ODnjtubAP7xnCRPtC0Av4JITO66A26oA55l1Qvw35A6pgISaH41yWRawKkvoVFVAn410+Na+++g+dVlRql0qPU54P+f9g8dNOWqnfP6kSXaeuhuhGGItr4Rv3AJ3GxHB5hF8wGlnmh2tkvjQ9/NEPQCuhGJ0U2cXuyao5d13+RfdQJ7pg8R5HjwMaUMmw/4EMAHfAjgAz4E8AEfAviADwF8wIcAPuBDAB/wKwuvVvne2Cqn2M2R0618OdM7lTNitUi75ofjpb3n6PWQsjkz21FVlmqBm/MZfu6R/0P0ug7Mr4pZCmg+0/tNyvl/KRsJX4DrA2n8kGYDE3fMgsrngS10p572+fzxcRoxtjokVyODr3kXcabND33wCCnsTlEjJ7fa6fAIUuUzvYAubfJ5XPucltnDr/fys8nRf5a/U9SgmL9bnoZ2Vemr+hNjkwXgQspf2rTsNI+glYD/KB1qvteV+0Igr3Zpu7q+jDa7ILi9SSPNTgV/wKAfVTZrdCrlhWhrYTqBygZSjx0h+xKtxQOj7VJmZKTKcir7zH9b7tfWCOKO4jdVcTnXvYpqfHNV+wjQjeaxI3uyTMsvPdzVddfqpEhAJsYkWPt09DVr760yJR3RbIbeESf7Kdpszi2izUHsflTjJlvv8AlS71C/oTqqyoHptRVB5TKajO8w4WQsncBK8d34jzq3GzblHWuZREoa4iWDqwi/tCGKKfth1TWOm7cp/uQQuc6HagR8Ni0EhJ3srZiFaxWLvyVzE9JKR/TFryTR9hGk2PJF7E9GdF/bKwR8RDvpnmtbCsuBbt2LuSrF/s9lE+2+dlMrtB0qWz9X9jy3ohx2rivxRUNzLx0CcRxt6amN2KR99SAnJJjVBHzAhwA+4EMA/7TlrwADAH6KibcsLrLQAAAAAElFTkSuQmCC" alt="iphone">
                  </a><a href="http://www.lunkr.cn/" target="_blank">
                  <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF8AAABGCAYAAACqlUimAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA+lJREFUeNrsXE1y2jAYdSmrznTingB6gvgGhRMEThBzgg5rFoRF1sAJ4pwAOAHkBPURnBPU3XTXmeobnpqvGv+QYCd2+97MN7ZsWdhPn94nbEkdj3gzdEgBySf5BMkn+QTJJ/kEyfdub28HxvoleYKyPCT/ZUiMLQuI981mPpvNkjY8zLu2NVVD8I3ZXBgLYEJ4DJP9tSH/QPKrJz6E5/sF2VJjE1MBW8pOtR5/h2Sck816/wYV1WzyzU1+EGt6oBUtR1IkZZeTdYG4IFg2PfCK57+HNRlf1f5IVYSLjTFLuF+Qj7LzDIxe+bpXQbcNzJvg2bpeWSvJlz9JZrOHbCyg8fszipxAfkSOIlORE8pOsVTYrmQVmn2t4kCjekB8t0PyST5B8kk+QfJJPvEfkS+vglPsLyoo7957etkW8R9u8asEeS38Sf3jHZxZZGLK/EzPJ1pHfnrm9THJP0+GxtB/V7OjkuNjc33a1GdryytlCcJb6H+og6l8LM87TtkhSD7Jb0+QJvkZ2i86vkJyZXUd20gdj1vxQCZYfRSjCNDzST5B8kk+QfJJPkHyST5B8kk+QfJJPkHyST5RjG5bblSmds5ms6jOcjF7UT7EyOSMvv1egJntMmNGzl96x2/EceM9X25c5tDiAc7B9Qt/X9Zr2J9YbqhIHuD6795x4vUAeXZVfawRz/9VM/8jPGDivcFwPYxuSM4oIq5rHlfXFPyz5ue/MjZFBUTKI6VZJxj2IbbVHoWWEiIZOd5s5UHOH+Q6HAtxPLLjdbJaHGan93OcIcC2hzL9jCGLcRXjgTp1Sw60U8bdBA4RoUl/Q+UINs51cq4H/d04RS9xTM6lagajh2v26rcCVYlS9kb95lKR/Re53nGArYWehG1nNjY+4IrkHLC/RVp728IuUGFIuRAPQ5ALcU63FK3bPs4fFKFDu9QLPFts5TiDEJ1qGcmIB7EecGXOp1a+kJ5Xqfl1S84Dmu0j0pp83XR/qP0v5gHHZVrupLWuS4XeueRD3u7LAjvu98KUObVB1hwboUUkVZHTqVly7Ho4A2yDE3s9z+0Z+U5FpDlllJXbQ4u6wb32QfYWMWt+QuU1QvNHCKI31iBBp6yHEOslW06osFTngZfucrT8uqBC+k4LEvIfUZly3K9yDGi3ZslxZ5bs3F5PDtYImjawXZ6Yf+o9rTYyzJAqGWw7N7aEzF2WtIYrSM7ABmYVlxrt+Ws3MCG4rlX3UZ//k4b3DVVcmMAsphn6P1YyN1Rdwdip7CHijy1nqFrLQ0a3M0BljmHLNiyk1Do40hXg37lflI9oKfhWk+STfILkk3yC5P/b+C3AANzxh9SCcTwmAAAAAElFTkSuQmCC" alt="android">
                </a><a href="http://www.lunkr.cn/download.html?p=pc" target="_blank">
                  <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF8AAABGCAYAAACqlUimAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAArlJREFUeNrsnEFu2kAUhgdE1nCD+AaQEwROQHOCKCcoWXsDC9akJ0g5QckJcG9AT1D3Bum6UtV59W9liuJCEApj833SaIztIPK98ZvBM8Y5AAAAAAA4hPl83vNlGONn6zRQ9sBXJrvvy0DFaCH/uKITyb1WPazT5+/USHQvFJym6dRX3+vceDo1TB9G1oQU2YlQ+sJXk3MYDLT9P9uN7DMNzmQUdtH29QUD0tM0/DYOTmgfBchHPjDOX/rydcc5ueoZ8o/LJpBbxXMTvmzFKH/hdt+jMekjX9ZveN/obqyR85GPfEA+8uFM5efIPxFpmt750tJQ8t6XVVMDEu1Mlg9ApvH8g73WNKKN/+1+fxf57xuMZ10Fq2D3lYLRDwKD/HcKiN2K2IT7tEYnXNGQIP+06WqA/NOlq4zRDiAf+YB85CMfkI98QD7yAfnIB+QjH5CPfEB+zWjUTJY9u2vzuprHzf12rv2JK+ZybTrx0peZZriQvyVwGrw0QZ9DUZqTted0r3V8pol0w5aX23ofk59J+qMrVjz8dMVkexaD+FL+r8j8j12xWMqpta69xJuyFbtiTX7miqdSLBALHa8SutRPBcTG71aELX/tZY2C1x8sCH7fg7bHtqqt6m8VlFtfvrlipZsFcxmepxUOdLgHXBWf9jhv6V7W8/QUjJJHOtz9rgJLOx99KVt6EuT3VwlbtTpeuwL6tl/9xQb51QyUPpxEzYJ8v2+H3Q3Szt+OW+ItbT0hv5pNmPO3j1ne98dX/2n5U7X4oXbl6qAnSlsjvmQdxpPS0D9je7Xq10g03s/KjjeWYWbt5EtibmnJ0ot+m+eLSdaPI23n87Fy/aQc+agfQX4F9zsCcOdenjz/4cuVOuHbrXzeVaAsOJf+nBu991qBgiOOjHrhtrVw1b2q8wAAAAAAGsofAQYAfXLtOs6wzyYAAAAASUVORK5CYII=" alt="pc">
                </a><a href="http://www.lunkr.cn/download.html?p=mac" target="_blank">
                  <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF8AAABGCAYAAACqlUimAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABKZJREFUeNrsnDFMIkEUhkfjJXZscbEUbLTSw8LSiIl2JmJvAtYWHJZSqIW1Z2ENJNpLtNPkMJY2G0srsLM66DTX3PzLGxnW3T0WwR30/clkl93ZYfnemzezszOMClZkGmUEDJ/hsxg+w2cx/E+tsWG62cPDw4TcJCnpashkFwqF6jD9npEhAG7JTVqmnAd0L53LdDwMhhgxHHxWbo5ksnq4HPDz0gg2ww/v7UXy+PcKBvjF8LsH/7vLENOtStIAW9zb+XjwUFaWXTQOvrypmEH3UxwAeN0AadM8/5tBjeug4RSpdnHYcWmvl4tisVAV16LeE8N3eX2il2vj8Xgv4cdi+G1lwmReXFwUm5ubzv7T05NYWFgI+31pht/u4aTChBnAV+EG8GdmZsKGn3WG31IyrNdDl5eXr8fu7+/F6upqmGJSDD8kfMT3ubk58fj4KOr1egf8yclJMT09HabhZfhBIHZ2dsTu7u5rfFdef3Fx4YDGOaTx8XFxd3cn1tbWnH20ATiOzwHhLsXwAwSQOmx4N7y82Wx2hJnZ2VnnOPKvrKw4hkAey7JM/nlmj+dfXV2Jl5cXByS8//n5WVxfXzuNK2ArqTyAjnCE8HR7e+scC1CN4QvhO+QLmCrcADiAwgBI2Pcy1vb2tpP37Oyso11wq1Ao1DjsdOGBCDnKs/8nGAaamJjoyeBfCj697Gj4nUfvBl5+enr6CjZI8HgYCbUF1/qoyvDbOg+Crzy/G8FACDdofAMevCrc4LZ1jDEXrxPo6XQLXunh4UGcnJz49XZqprzfNcLzKfR4en9Y8Pp1Pg1u3pTenEn9/HxQ7O+TqtLQ5wzfu+s3SK+EYTdMeo4x6glXGqAkN1sDAr8sy28w/I81gAJv3PwdI8d2yADLfRgCQHyfMnXilLEDa9QdnJfpoIeG2CZv3zAt1JjYz/czAMDtI9G0D7yB8pooq55aAb1s8hTBDskf9V2wOOwwfBbDZ/gshs/wWQyf4bMYPsNnMXyGz2L4w6Kxz/rD6H8aMCSN+SMJNV2EFmNgSBrnf4gIh6BNWJmy714jhc84/s6isxrkFJX7R7QWxKUoTyXKsX94/t+I+e+Rh+pL9NN0fL/P32WbtBJ9TN5MM+J7QDjIuOBnhGs+pfTaJBkFhirprwdpoQNS1TUbTb3xilMYsjwWRdhRvWo0pcG1Ca6CXHOBTxN4BbaoncuK9tranBdcxHXtc85V6xJfvcEtE5Qt8vqy0BZF0ywzNdOsKgHrS0dz8vx8QJipaoZqUHmq8d2LOuZHLsCQIJT3puTnPMC4vB8erl6gW1otqQYUnaGaEEOZqpGlmmSLiFenmNTPr9A/g1Q8ekQ/5WZJtP47Z0q0FzfACH5tFpamH8j8aLSTFPNrVIMyVLPKDL+lEnUPSx7n1tFLcS/lofCx5FNewpUf8OvUuOK4FfVUcWMesgBKeueyz1qpGnm/Ld7+15pNNaZMPZ4azXh7Y0CqXSl1PfajNIAJnp93efKb49p+kvbntWvyGng0sCWK6Teu71GTrRBuNigdUVvC6vOTs6U/I9BTsxWUj/WFxKOaDJ/hsxg+w2cx/M+tfwIMAMzZ4vjxC6g+AAAAAElFTkSuQmCC" alt="mac">
                </a>
                </p></div>


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
                    <a href="javascript:void(0);" class="u-img-title" data-trigger="logs">自助查询</a>
                    <div class="u-img-desc">邮箱使用记录查询，支持邮件召回、异地登录提醒</div>
                  </div>
                </li>
                <li>
                  <div class="u-img icon-feature icon-file"></div>
                  <div class="u-img-text">
                    <a href="javascript:void(0);" class="u-img-title" data-trigger="file.transitcenter">文件中转站</a>
                    <div class="u-img-desc">支持主流浏览器续传文件（支持Chrome，Safari）</div>
                  </div>
                </li>
                <li>
                  <div class="u-img icon-feature icon-schedule"></div>
                  <div class="u-img-text">
                    <a href="javascript:void(0);" class="u-img-title" data-trigger="calendar">会议与日程</a>
                    <div class="u-img-desc">全新改版，高级版支持会议邀请和日程共享</div>
                  </div>
                </li>
                <li>
                  <div class="u-img icon-feature icon-client"></div>
                  <div class="u-img-text">
                    <a href="http://software.icoremail.net/coremail-plugin/download.html" target="_blank" class="u-img-title">客户端插件</a>
                    <div class="u-img-desc">可在Outlook，Foxmail中实现通讯录查询同步等功能</div>
                  </div>
                </li>
                <li>
                  <div class="u-img icon-feature icon-lock"></div>
                  <div class="u-img-text">
                    <a href="javascript:void(0);" class="u-img-title" data-trigger="setting.security.auth2lock">安全锁</a>
                    <div class="u-img-desc">为重要文件夹提供更多保护</div>
                  </div>
                </li>
              </ul>

              <div class="app">
                <p>移动邮件、即时沟通</p>
                <img src="@/assets/img/download.png" alt="qrcode">
                <div class="img-text">
                  <a href="http://www.lunkr.cn/download.html?p=pc" target="_blank">
                    <span class="iconfont icon-iconwindows"></span>
                    PC版
                  </a>
                  <a href="http://www.lunkr.cn/download.html?p=ios" target="_blank">
                    <span class="iconfont icon-icon-apple"></span>
                    iPhone版
                  </a>
                  <a href="http://www.lunkr.cn/download.html?p=android" target="_blank">
                    <span class="iconfont icon-iconanroid"></span>
                    Android版
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div><!-- end container -->
      <div class="footer small text-gray">Coremail. © Copyright 2000 - 2016 Mailtech.</div>

    </div>
  </div>
</template>

<script>
  import cookie from '@/assets/js/cookie';
  import {welcome} from '@/api/api'
  export default {
    data(){
      return {
        userinfo: {
          "capacity_used": 1,
          "login_isp": "广东深圳电信",
          "capacity_used_rate": 0,
          "last_login": "2018年8月9日星期二下午15点49分46秒",
          "login_ip": "116.30.220.106",
          "unread": 10,
          "capacity_total": 1000
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
    mounted: function(){
      welcome().then(res=>{
        console.log(res.data);
        this.userinfo = res.data.userinfo;
        this.weatherinfo = res.data.weatherinfo;
      })
    },
    computed: {
      username() { // 获取store中的数据
        return this.$store.state.userInfo.name;
      }
    },
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

