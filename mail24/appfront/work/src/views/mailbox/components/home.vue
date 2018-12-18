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
            <div class="bulletins">
              <div class="panel-sbj" v-if="loginAfterData.system_name">
                <div class="tag skin-primary-bg"></div> 系统公告： {{loginAfterData.system_name}}
              </div>
              <div style="padding:20px;line-height:20px;" v-if="loginAfterData.system_name" v-html="loginAfterData.system_remark">

              </div>

              <el-tabs type="border-card" v-if="loginAfterData.welcome_links && loginAfterData.welcome_links.length>0">
                <el-tab-pane v-for="(l,k) in loginAfterData.welcome_links" :label="l.title" :key="k">
                  <div style="width:80%;margin:0 auto;">
                      <el-carousel trigger="click" indicator-position="outside" height="200px">
                        <el-carousel-item v-for="(item,c) in l.links" :key="c" v-if="l.links && l.links.length>0">
                          <table style="width:100%;height:200px;border:none">
                            <tr>
                              <td style="width:60%;">
                                  <a :href="item.url" target="_blank" v-if="item.url">
                                    <img :src="origin + item.icon" style="width:100%;max-width:100%;">
                                    <!--<img src="http://192.168.1.39:81/media/logo_f0XiV_20181218112627_990.jpg" style="width:100%;max-width:100%;">-->
                                  </a>
                                  <img :src="origin + item.icon" style="width:100%;max-width:100%;" v-if="!item.url">
                                  <!--<img src="http://192.168.1.39:81/media/logo_f0XiV_20181218112627_990.jpg" style="width:100%;max-width:100%;" v-if="!item.url">-->
                              </td>
                              <td  style="background:#fff;vertical-align: top;padding-left:10px;border:none;">
                                <div>
                                  <p style="font-size:16px;">
                                    <a href="item.url" target="_blank" v-if="item.url" style="color:#333;text-decoration: none"><b> {{item.title}}</b></a></p>
                                    <b v-if="!item.url"> {{item.title}}</b>
                                  <p>
                                    {{item.desc}}
                                  </p>
                                </div>
                              </td>
                            </tr>

                          </table>

                        </el-carousel-item>
                      </el-carousel>
                  </div>

                </el-tab-pane>
              </el-tabs>
              <div class="panel-sbj" v-if="false">
                <div class="tag skin-primary-bg"></div>
              </div>
              <div class="panel-cnt" v-if="false">
                <div class="content">

                  <!--<p>-->
                    <!--<a href="http://www.lunkr.cn/" class="lunkr_image" target="_blank" title="了解Coremail论客" style="display: block;width: 100%;height: 266px;background-size: cover;background-repeat:no-repeat;">-->
                      <!--&lt;!&ndash; <img src="../assets/img/lunkr_banner.png" alt="" style="width: 100%; max-width: 100%;"> &ndash;&gt;-->
                    <!--</a>-->
                  <!--</p>-->
                  <!--<p class="lunkr_download_links">-->
                    <!--<a href="http://www.lunkr.cn/" target="_blank">-->
                      <!--<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF8AAABGCAYAAACqlUimAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA9FJREFUeNrsnF1y2jAQxx3KU2c69Q3KDeqeIHACwgkSTkD8zAPkIc+BE0BOUPcEOCeIewP3BKUvfetMd5PVsGigcQdZyPDfGQ22JJT4p9Xuog+3IsjRpAUEgA/4EMA/G2mfyoPc39/f0Mc1pcfxeLwEfD/QE/r4SqkjWU/QfD/gGfiKUqyyc9h8P7KwwJdkcgDfk7npWtkpoh0/YoO/I63PAL8eTe/uyF5T4sjmC4Gfcp099YKUiwaEjyNKicouKM0pZQR8LXX6lK6sr7/UCznsvAgUeizhowstZlM05I4K7Bnfh2p2Vo7ARzIiJgE+47tWgFo/tczMoWLMFH5kVZCRw7bY1PRCMzlBRjsSqcQOm0xDBR9iqOkyTFyHPsF2ylPKBX5kQc4SfgL4x5M49KmG0ODnjtubAP7xnCRPtC0Av4JITO66A26oA55l1Qvw35A6pgISaH41yWRawKkvoVFVAn410+Na+++g+dVlRql0qPU54P+f9g8dNOWqnfP6kSXaeuhuhGGItr4Rv3AJ3GxHB5hF8wGlnmh2tkvjQ9/NEPQCuhGJ0U2cXuyao5d13+RfdQJ7pg8R5HjwMaUMmw/4EMAHfAjgAz4E8AEfAviADwF8wIcAPuBDAB/wKwuvVvne2Cqn2M2R0618OdM7lTNitUi75ofjpb3n6PWQsjkz21FVlmqBm/MZfu6R/0P0ug7Mr4pZCmg+0/tNyvl/KRsJX4DrA2n8kGYDE3fMgsrngS10p572+fzxcRoxtjokVyODr3kXcabND33wCCnsTlEjJ7fa6fAIUuUzvYAubfJ5XPucltnDr/fys8nRf5a/U9SgmL9bnoZ2Vemr+hNjkwXgQspf2rTsNI+glYD/KB1qvteV+0Igr3Zpu7q+jDa7ILi9SSPNTgV/wKAfVTZrdCrlhWhrYTqBygZSjx0h+xKtxQOj7VJmZKTKcir7zH9b7tfWCOKO4jdVcTnXvYpqfHNV+wjQjeaxI3uyTMsvPdzVddfqpEhAJsYkWPt09DVr760yJR3RbIbeESf7Kdpszi2izUHsflTjJlvv8AlS71C/oTqqyoHptRVB5TKajO8w4WQsncBK8d34jzq3GzblHWuZREoa4iWDqwi/tCGKKfth1TWOm7cp/uQQuc6HagR8Ni0EhJ3srZiFaxWLvyVzE9JKR/TFryTR9hGk2PJF7E9GdF/bKwR8RDvpnmtbCsuBbt2LuSrF/s9lE+2+dlMrtB0qWz9X9jy3ohx2rivxRUNzLx0CcRxt6amN2KR99SAnJJjVBHzAhwA+4EMA/7TlrwADAH6KibcsLrLQAAAAAElFTkSuQmCC" alt="iphone">-->
                    <!--</a><a href="http://www.lunkr.cn/" target="_blank">-->
                    <!--<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF8AAABGCAYAAACqlUimAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA+lJREFUeNrsXE1y2jAYdSmrznTingB6gvgGhRMEThBzgg5rFoRF1sAJ4pwAOAHkBPURnBPU3XTXmeobnpqvGv+QYCd2+97MN7ZsWdhPn94nbEkdj3gzdEgBySf5BMkn+QTJJ/kEyfdub28HxvoleYKyPCT/ZUiMLQuI981mPpvNkjY8zLu2NVVD8I3ZXBgLYEJ4DJP9tSH/QPKrJz6E5/sF2VJjE1MBW8pOtR5/h2Sck816/wYV1WzyzU1+EGt6oBUtR1IkZZeTdYG4IFg2PfCK57+HNRlf1f5IVYSLjTFLuF+Qj7LzDIxe+bpXQbcNzJvg2bpeWSvJlz9JZrOHbCyg8fszipxAfkSOIlORE8pOsVTYrmQVmn2t4kCjekB8t0PyST5B8kk+QfJJPvEfkS+vglPsLyoo7957etkW8R9u8asEeS38Sf3jHZxZZGLK/EzPJ1pHfnrm9THJP0+GxtB/V7OjkuNjc33a1GdryytlCcJb6H+og6l8LM87TtkhSD7Jb0+QJvkZ2i86vkJyZXUd20gdj1vxQCZYfRSjCNDzST5B8kk+QfJJPkHyST5B8kk+QfJJPkHyST5RjG5bblSmds5ms6jOcjF7UT7EyOSMvv1egJntMmNGzl96x2/EceM9X25c5tDiAc7B9Qt/X9Zr2J9YbqhIHuD6795x4vUAeXZVfawRz/9VM/8jPGDivcFwPYxuSM4oIq5rHlfXFPyz5ue/MjZFBUTKI6VZJxj2IbbVHoWWEiIZOd5s5UHOH+Q6HAtxPLLjdbJaHGan93OcIcC2hzL9jCGLcRXjgTp1Sw60U8bdBA4RoUl/Q+UINs51cq4H/d04RS9xTM6lagajh2v26rcCVYlS9kb95lKR/Re53nGArYWehG1nNjY+4IrkHLC/RVp728IuUGFIuRAPQ5ALcU63FK3bPs4fFKFDu9QLPFts5TiDEJ1qGcmIB7EecGXOp1a+kJ5Xqfl1S84Dmu0j0pp83XR/qP0v5gHHZVrupLWuS4XeueRD3u7LAjvu98KUObVB1hwboUUkVZHTqVly7Ho4A2yDE3s9z+0Z+U5FpDlllJXbQ4u6wb32QfYWMWt+QuU1QvNHCKI31iBBp6yHEOslW06osFTngZfucrT8uqBC+k4LEvIfUZly3K9yDGi3ZslxZ5bs3F5PDtYImjawXZ6Yf+o9rTYyzJAqGWw7N7aEzF2WtIYrSM7ABmYVlxrt+Ws3MCG4rlX3UZ//k4b3DVVcmMAsphn6P1YyN1Rdwdip7CHijy1nqFrLQ0a3M0BljmHLNiyk1Do40hXg37lflI9oKfhWk+STfILkk3yC5P/b+C3AANzxh9SCcTwmAAAAAElFTkSuQmCC" alt="android">-->
                  <!--</a><a href="http://www.lunkr.cn/download.html?p=pc" target="_blank">-->
                    <!--<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF8AAABGCAYAAACqlUimAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAArlJREFUeNrsnEFu2kAUhgdE1nCD+AaQEwROQHOCKCcoWXsDC9akJ0g5QckJcG9AT1D3Bum6UtV59W9liuJCEApj833SaIztIPK98ZvBM8Y5AAAAAAA4hPl83vNlGONn6zRQ9sBXJrvvy0DFaCH/uKITyb1WPazT5+/USHQvFJym6dRX3+vceDo1TB9G1oQU2YlQ+sJXk3MYDLT9P9uN7DMNzmQUdtH29QUD0tM0/DYOTmgfBchHPjDOX/rydcc5ueoZ8o/LJpBbxXMTvmzFKH/hdt+jMekjX9ZveN/obqyR85GPfEA+8uFM5efIPxFpmt750tJQ8t6XVVMDEu1Mlg9ApvH8g73WNKKN/+1+fxf57xuMZ10Fq2D3lYLRDwKD/HcKiN2K2IT7tEYnXNGQIP+06WqA/NOlq4zRDiAf+YB85CMfkI98QD7yAfnIB+QjH5CPfEB+zWjUTJY9u2vzuprHzf12rv2JK+ZybTrx0peZZriQvyVwGrw0QZ9DUZqTted0r3V8pol0w5aX23ofk59J+qMrVjz8dMVkexaD+FL+r8j8j12xWMqpta69xJuyFbtiTX7miqdSLBALHa8SutRPBcTG71aELX/tZY2C1x8sCH7fg7bHtqqt6m8VlFtfvrlipZsFcxmepxUOdLgHXBWf9jhv6V7W8/QUjJJHOtz9rgJLOx99KVt6EuT3VwlbtTpeuwL6tl/9xQb51QyUPpxEzYJ8v2+H3Q3Szt+OW+ItbT0hv5pNmPO3j1ne98dX/2n5U7X4oXbl6qAnSlsjvmQdxpPS0D9je7Xq10g03s/KjjeWYWbt5EtibmnJ0ot+m+eLSdaPI23n87Fy/aQc+agfQX4F9zsCcOdenjz/4cuVOuHbrXzeVaAsOJf+nBu991qBgiOOjHrhtrVw1b2q8wAAAAAAGsofAQYAfXLtOs6wzyYAAAAASUVORK5CYII=" alt="pc">-->
                  <!--</a><a href="http://www.lunkr.cn/download.html?p=mac" target="_blank">-->
                    <!--<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF8AAABGCAYAAACqlUimAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABKZJREFUeNrsnDFMIkEUhkfjJXZscbEUbLTSw8LSiIl2JmJvAtYWHJZSqIW1Z2ENJNpLtNPkMJY2G0srsLM66DTX3PzLGxnW3T0WwR30/clkl93ZYfnemzezszOMClZkGmUEDJ/hsxg+w2cx/E+tsWG62cPDw4TcJCnpashkFwqF6jD9npEhAG7JTVqmnAd0L53LdDwMhhgxHHxWbo5ksnq4HPDz0gg2ww/v7UXy+PcKBvjF8LsH/7vLENOtStIAW9zb+XjwUFaWXTQOvrypmEH3UxwAeN0AadM8/5tBjeug4RSpdnHYcWmvl4tisVAV16LeE8N3eX2il2vj8Xgv4cdi+G1lwmReXFwUm5ubzv7T05NYWFgI+31pht/u4aTChBnAV+EG8GdmZsKGn3WG31IyrNdDl5eXr8fu7+/F6upqmGJSDD8kfMT3ubk58fj4KOr1egf8yclJMT09HabhZfhBIHZ2dsTu7u5rfFdef3Fx4YDGOaTx8XFxd3cn1tbWnH20ATiOzwHhLsXwAwSQOmx4N7y82Wx2hJnZ2VnnOPKvrKw4hkAey7JM/nlmj+dfXV2Jl5cXByS8//n5WVxfXzuNK2ArqTyAjnCE8HR7e+scC1CN4QvhO+QLmCrcADiAwgBI2Pcy1vb2tpP37Oyso11wq1Ao1DjsdOGBCDnKs/8nGAaamJjoyeBfCj697Gj4nUfvBl5+enr6CjZI8HgYCbUF1/qoyvDbOg+Crzy/G8FACDdofAMevCrc4LZ1jDEXrxPo6XQLXunh4UGcnJz49XZqprzfNcLzKfR4en9Y8Pp1Pg1u3pTenEn9/HxQ7O+TqtLQ5wzfu+s3SK+EYTdMeo4x6glXGqAkN1sDAr8sy28w/I81gAJv3PwdI8d2yADLfRgCQHyfMnXilLEDa9QdnJfpoIeG2CZv3zAt1JjYz/czAMDtI9G0D7yB8pooq55aAb1s8hTBDskf9V2wOOwwfBbDZ/gshs/wWQyf4bMYPsNnMXyGz2L4w6Kxz/rD6H8aMCSN+SMJNV2EFmNgSBrnf4gIh6BNWJmy714jhc84/s6isxrkFJX7R7QWxKUoTyXKsX94/t+I+e+Rh+pL9NN0fL/P32WbtBJ9TN5MM+J7QDjIuOBnhGs+pfTaJBkFhirprwdpoQNS1TUbTb3xilMYsjwWRdhRvWo0pcG1Ca6CXHOBTxN4BbaoncuK9tranBdcxHXtc85V6xJfvcEtE5Qt8vqy0BZF0ywzNdOsKgHrS0dz8vx8QJipaoZqUHmq8d2LOuZHLsCQIJT3puTnPMC4vB8erl6gW1otqQYUnaGaEEOZqpGlmmSLiFenmNTPr9A/g1Q8ekQ/5WZJtP47Z0q0FzfACH5tFpamH8j8aLSTFPNrVIMyVLPKDL+lEnUPSx7n1tFLcS/lofCx5FNewpUf8OvUuOK4FfVUcWMesgBKeueyz1qpGnm/Ld7+15pNNaZMPZ4azXh7Y0CqXSl1PfajNIAJnp93efKb49p+kvbntWvyGng0sCWK6Teu71GTrRBuNigdUVvC6vOTs6U/I9BTsxWUj/WFxKOaDJ/hsxg+w2cx/M+tfwIMAMzZ4vjxC6g+AAAAAElFTkSuQmCC" alt="mac">-->
                  <!--</a>-->
                  <!--</p>-->

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
                    <el-carousel trigger="click" indicator-position="outside" height="120px">
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

