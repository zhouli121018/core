<template>
  <!--<article class="mlmain mltabview">-->
  <div class="mltabview-content">
    <div class="mltabview-panel">
      <section class="m-read" v-show="!notFond" v-loading="loading">
        <div class="toolbar" style="background:#fff"
        >

          <div id="pagination" class="f-fr">
          <div class="">
          <el-button-group>
          <el-button  size="small" icon="el-icon-arrow-left" :title="lan.MAILBOX_COM_READ_PREV" plain round @click="prevMail" :disabled="curr_mail_index==0 && curr_page==1"></el-button>
          <el-button  size="small" plain round icon="el-icon-arrow-right" :title="lan.MAILBOX_COM_READ_NEXT" @click="nextMail" :disabled="curr_mail_index==uids.length-1 && curr_page == total_page"></el-button>
          </el-button-group>
          </div>
          </div>

          <el-button size="small" @click="recallMessage" v-if="msg.attrs" v-show="msg.attrs.is_canrecall" :disabled="msg.attrs.is_recall">{{msg.attrs.is_recall? lan.MAILBOX_COM_READ_RECALLED: lan.COMMON_BUTTON_ZHAOHUI}}</el-button>
          <el-button-group >
            <el-button size="small" @click="actionView(3)">{{lan.MAILBOX_COM_INNERBOX_RECOVER}}</el-button>
            <el-button size="small"  @click="actionView(4)">{{lan.MAILBOX_COM_INNERBOX_RECOVER_ALL}}</el-button>
            <el-button size="small"  @click="actionView(5)">{{lan.MAILBOX_COM_INNERBOX_FORWARD}}</el-button>
          </el-button-group>



          <el-button size="small"  @click="print">{{lan.MAILBOX_COM_READ_PRINT}}</el-button>



          <el-dropdown @command="moveHandleCommand" trigger="click">
            <el-button  size="small" plain>
              <span>{{lan.MAILBOX_COM_INNERBOX_MOVE_TO}}</span>
              <i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item v-for="item in moveItems" :key="item.id" class="dropdown_item" :class="{ active: moveCheckIndex===item.id }"
                                :divided="item.divided" :command="item.id">
                <b><i class="el-icon-check vibility_hide" :class="{ vibility_show: moveCheckIndex===item.id }"></i> </b>
                {{ item.text}}</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>

          <el-dropdown @command="signHandleCommand" trigger="click">
            <el-button  size="small" plain >
              <span>{{lan.MAILBOX_COM_INNERBOX_MARKED_AS}}</span>
              <i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item v-if="!item.children" v-for="item in signItems" :key="item.id" class="dropdown_item"
                                :command="item" :divided="item.divided">
                <b><i class="el-icon-check vibility_hide" v-if="!item.classN"></i> </b><i :class="item.classN"></i>
                {{ item.text}}
              </el-dropdown-item>
              <el-dropdown-item class="dropdown_item" v-else="item.children" :divided="item.divided">
                <el-dropdown @command="signHandleCommand"  placement="right-start">
                    <span class="el-dropdown-link">
                      <b><i class="el-icon-check vibility_hide" v-if="!item.classN"></i> </b><i :class="item.classN"></i>
                    {{item.text}}<i class="el-icon-arrow-right el-icon--right"></i>
                    </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item  v-for="(c,k) in item.children" :key="k" class="dropdown_item" :command="c">
                      <i class="iconfont icon-iconflatcolor" :class="c.classN"></i> {{c.text}}
                    </el-dropdown-item>

                  </el-dropdown-menu>

                </el-dropdown>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>

          <el-dropdown @command="moreHandleCommand" trigger="click">
            <el-button  size="small" plain>
              <span>{{lan.MAILBOX_COM_INNERBOX_MORE}}</span>
              <i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item v-if="item.id!=12 || (item.id==12&&readFolderId=='Spam')" v-for="item in moreItems" :key="item.id" class="dropdown_item"
                                :divided="item.divided" :command="item" >
                <b><i class="el-icon-check vibility_hide" v-if="!item.classN"></i> </b><i :class="item.classN"></i>
                {{ item.text}}</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <el-button size="small"  @click="closeTab(tagName)">{{lan.COMMON_CLOSE}}</el-button>
          <el-button size="small" type="danger" plain @click="deleteMail">{{lan.COMMON_BUTTON_DELETE}}</el-button>


        </div>

        <div class="mail" :class="{is_reply:replying}" ref="iframe_height" :id="'mail_'+readId+'_'+readFolderId" >
          <div class="j-read-alert f-pr"></div>
          <div class="mail-top j-mail-top f-pr">
            <div class="top-bar">
              <div class="f-tar">
                <!--<span class="mail-flagged f-pr f-csp " :class="flag_color">-->
                <!--<i class="iconfont icon-iconflat" title="设置标记" v-if="!flagged"></i>-->
                <!--<i class="iconfont icon-iconflatcolor" v-if="flagged" :class="flag_color" title="设置标记"></i>-->

                <!--<i class="el-icon-arrow-down"></i>-->
                <!--<ul class="u-menu u-menu-hidden"><li value="mark:flagged"><i class="iconfont left icon-iconflatcolor flagged label0-0"></i><a href="javascript:void(0);" tabindex="-1">红旗</a></li><li class="divider"></li><li value="mark:noflagged"><a href="javascript:void(0);" tabindex="-1">取消标记</a></li></ul></span>-->
                <el-dropdown trigger="click" @command="signHandleCommand">
                        <span class="el-dropdown-link" :title="flagged?this.lan.MAILBOX_COM_READ_SET_FLAG:this.lan.MAILBOX_COM_READ_DELETE_FLAG">
                          <i class="iconfont icon-iconflat" v-if="!flagged"></i><i class="iconfont icon-iconflatcolor" v-if="flagged" style="color:#c00;" :class="flag_color"></i><i class="el-icon-arrow-down el-icon--right"></i>
                        </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item  v-for="(c,k) in flagsData" :key="k" class="dropdown_item" :command="c">
                      <i class="iconfont icon-iconflatcolor" :class="[c.classN,{'icon-iconflat':k==flagsData.length-1}]" ></i> {{c.text}}
                    </el-dropdown-item>

                  </el-dropdown-menu>
                </el-dropdown>

                <a class="iconfont icon-iconemailcontacts" href="javascript:void(0)" :title="lan.MAILBOX_COM_READ_CHECK_EXCHANGES" @click="mail_contact"></a>

                <a class="iconfont icon-iconnewtab" href="./detach.jsp?sid=BAcpKTaaYBZiTuHsrlaaUOhLUZiBhfEu#mail.read?mid=1:1tbiAQAJEFXEqdgAXgADsl&amp;fid=1&amp;mboxa=&amp;start=2" target="_blank" :title="lan.MAILBOX_COM_READ_NEW_WINDOW" v-if="false"></a>

                <a href="javascript:void(0)" :title="lan.MAILBOX_COM_READ_CONFERENCE" @click.prevent="mail_event">{{lan.MAILBOX_COM_READ_CONFERENCE}}</a>
              </div>
              <div class="f-tar">
                <span>{{time?time.replace('T',' '):''}}</span>
              </div>
            </div>
            <div class="mail-top-info" style="min-height: 42px;">
              <h3 class="mail-subject j-mail-subject " :class="[{redcolor:flagged},flag_color]" style="font-size:18px;">
                <!--<span class="icon"><i class="j-sourceIcon iconfont state-icon icon-SYSTEM" title="系统认证可信任来源"></i></span>-->
                <!--<span v-if="burn_flagged">{{lan.MAILBOX_COM_COMPOSE_IS_BURN}}: </span>-->
                <span class="is_burn_img" v-if="burn_flagged" :title="lan.MAILBOX_COM_COMPOSE_IS_BURN"></span>
                {{subject}}
              </h3>
              <div class="short-info f-ellipsis j-short-info" v-show="!showDetails" v-if="mfrom || to.length>0">
                <a class="j-u-email" href="javascript:void(0);" >{{mfrom}}</a>
                <span>{{lan.MAILBOX_COM_READ_SEND_TO}}</span>
                <a class="j-u-email" href="javascript:void(0)" v-for="(t,k) in to" :key="k">{{t}}; </a>

              </div>
              <div class="full-info j-full-info" v-show="showDetails">
                <table class="u-table u-table-row">
                  <tbody><tr v-if="mfrom">
                    <td class="info-item">{{lan.MAILBOX_COM_COMPOSE_SENDER}}</td>
                    <td>
                                     <span class="u-email j-u-email">
                                        <span class="name">{{mfrom}}</span>
                                        <span class="address"></span>
                                     </span>

                    </td>
                  </tr>
                  <tr v-if="to.length>0">
                    <td class="info-item">{{lan.MAILBOX_COM_COMPOSE_RECIVER}} </td>
                    <td>

                      <div class="j-contacts ">
                                        <span class="u-email j-u-email" v-for="(t,k) in to" :key="k" style="margin-right:2px;">
                                            <span class="name" >{{t}}</span>
                                            <span class="address"></span>
                                        </span>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="msg.cc">
                    <td class="info-item">{{lan.MAILBOX_COM_COMPOSE_CCER}}</td>
                    <td>

                      <div class="j-contacts ">
                                        <span class="u-email j-u-email" v-for="(t,k) in msg.cc" :key="k" style="margin-right:2px;">
                                            <span class="name" v-if="t" >{{t[1]+' <'+t[0]+ '>'}}</span>
                                            <span class="address"></span>
                                        </span>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="msg.attachments && msg.attachments.length>0">
                    <td class="info-item">{{lan.MAILBOX_COM_READ_ATTACH}}</td>
                    <td>
                      <b type="text">{{msg.attachments.length}}</b> {{lan.MAILBOX_COM_READ_COUNT}}(
                      <span>{{msg.attachments[0].name}}</span>
                      <span v-if="msg.attachments.length>1">{{lan.MAILBOX_COM_READ_AND_SO}}</span>)
                      <el-button type="text" @click="seeAttach" style="padding:0;margin-left:10px;"> {{lan.MAILBOX_COM_READ_SEE_ALL_ATTACH}}</el-button>
                    </td>
                  </tr>



                  </tbody>
                </table>
              </div>
            </div>
            <div class="mail-divider">
              <a href="javascript:void(0)" class="u-btn u-btn-default u-btn-round f-fr" @click="showDetails=!showDetails">
                <i :class="{'el-icon-arrow-down':!showDetails,'el-icon-arrow-up':showDetails}"></i>
              </a>
            </div>
          </div>
          <div class="mail-cipher-encrypted j-mailCipherEncrypted" v-if="is_password &&  password">
            <div class="decryption-success">
              <span class="iconfont icon-iconunlock"></span>
              {{lan.MAILBOX_COM_READ_ENCRYPTED_DESC}}
            </div>
          </div>
          <div class="u-alert u-alert-warning" v-if="msg.attrs && msg.attrs.is_notify" style="margin-bottom:0;padding: 2px 12px;">
            <div class="decryption-success">
              {{lan.MAILBOX_COM_READ_IS_NOTIFY_DESC}}
              <el-button type="text"  style="padding:0" @click="sendNotifyMessage">{{lan.MAILBOX_COM_READ_SENT}}</el-button>
              <el-button type="text"  style="padding:0" @click="msg.attrs.is_notify=false">{{lan.COMMON_BUTTON_CANCELL}}</el-button>
            </div>
          </div>
          <div class="mail-cipher-encrypted j-mailCipherEncrypted" v-if="msg.attrs && msg.attrs.is_burn && false">
            <div class="decryption-success" style="color:#e6a23c">
              <!--<span class="el-icon-warning"></span>-->
              <span class="is_burn_img" :title="lan.MAILBOX_COM_COMPOSE_IS_BURN"></span>
              {{lan.MAILBOX_COM_READ_IS_BURN_DESC}}
            </div>
          </div>
          <div class="mail-cipher-encrypted j-mailCipherEncrypted" v-if="msg.attrs && msg.attrs.is_calendar">
            <div class="decryption-success" style="color:#e6a23c">
              <span class="el-icon-warning"></span>
              {{lan.MAILBOX_COM_READ_IS_CALENDAR_DESC}}
            </div>
          </div>
          <div class="mail-cipher-encrypted j-mailCipherEncrypted" v-if="msg.attrs && msg.attrs.is_calendar_event && !msg.attrs.is_calendar_event_deleted ">
            <div class="decryption-success" style="color:#e6a23c">
              <span class="el-icon-warning"></span>
              {{lan.MAILBOX_COM_READ_IS_CALENDAR_EVENT_DESC}}
            </div>
            <div v-if="msg.attrs.calendar_event_id">
              <div class="decryption-success" style="font-size:14px;margin-top:10px;" v-if="msg.attrs.calendar_eventer_status!='start'">
                <span class="el-icon-star-on"></span>
                <b>{{msg.attrs.calendar_eventer_status=='pass'? lan.MAILBOX_COM_READ_PASS:msg.attrs.calendar_eventer_status=='reject'? this.lan.MAILBOX_COM_READ_REJECT: lan.MAILBOX_COM_READ_WAIT}}</b>
                <el-button type="text" style="margin-left:20px;" v-if="msg.attrs.calendar_eventer_status && msg.attrs.calendar_eventer_status!='start'" @click="show_change_btn = !show_change_btn">{{show_change_btn? lan.MAILBOX_COM_READ_HIDE: lan.COMMON_BUTTON_ALTER}}</el-button>
              </div>
              <div style="margin-top:10px;padding-left:18px;" v-show="show_change_btn">
                <span style="font-size:14px;color:#777;"><i class="el-icon-info"></i> <b>{{lan.MAILBOX_COM_READ_IS_RECIPT}}</b></span>
                <span>
                    <el-button type="success" @click="changeStatus('pass')" v-if="msg.attrs.calendar_eventer_status!='pass'" size="mini"> {{lan.MAILBOX_COM_READ_IS_PASS}} </el-button>
                    <el-button type="info" @click="changeStatus('wait')" v-if="msg.attrs.calendar_eventer_status!='wait'" size="mini"> {{lan.MAILBOX_COM_READ_IS_WAIT}} </el-button>
                    <el-button type="danger" @click="changeStatus('reject')" v-if="msg.attrs.calendar_eventer_status!='reject'" size="mini"> {{lan.MAILBOX_COM_READ_IS_REJECT}} </el-button>
                  </span>
              </div>
            </div>

          </div>
          <div class="mail-cipher-encrypted j-mailCipherEncrypted" v-if="msg.attrs && msg.attrs.is_calendar_event_deleted">
            <div class="decryption-success" style="color:#e6a23c">
              <span class="el-icon-warning"></span>
              {{lan.MAILBOX_COM_READ_IS_DELETE}}
            </div>
          </div>
          <div class="mail-sent-state j-sent-state" v-if="is_sender">
            <div class="" >
              <span :class="show_result?'el-icon-caret-bottom':'el-icon-caret-right'" style="font-size: 16px;cursor:pointer;" @click="show_result=!show_result"></span>
              {{send_desc }}
              <el-button type="text" style="padding:0;" @click="seeStatus" v-if="!show_result">[{{lan.MAILBOX_COM_READ_VIEW_DETAILS}}]</el-button>
              <el-button type="text" style="padding:0;" @click="show_result=false" v-if="show_result">[{{lan.MAILBOX_COM_READ_HIDE_DETAILS}}]</el-button>
              <el-button type="text" style="padding:0;" v-if="show_result" @click="refreshStatus">[{{lan.MAILBOX_COM_READ_REFRESH}}]</el-button>
              {{lan.MAILBOX_COM_READ_IS_SENDER_1}} {{mail_results.length}} {{lan.MAILBOX_COM_READ_IS_SENDER_2}}
              <span v-if="undeliverCount">{{undeliverCount}} {{lan.MAILBOX_COM_READ_IS_SENDER_3}}</span>
              <span v-if="reviewCount">{{reviewCount}} {{lan.MAILBOX_COM_READ_IS_SENDER_4}}</span>
              <span v-if="sequesterCount">{{sequesterCount}} {{lan.MAILBOX_COM_READ_IS_SENDER_5}}</span>
              <span v-if="deliverCount">{{deliverCount}} {{lan.MAILBOX_COM_READ_IS_SENDER_6}}</span>
              <span v-if="readedCount">{{readedCount}} {{lan.MAILBOX_COM_READ_IS_SENDER_7}}</span>
              <span v-if="deliver_failCount" style="color:red;">{{deliver_failCount}} {{lan.MAILBOX_COM_READ_IS_SENDER_8}}</span>
            </div>
            <div class="" v-show="show_result">
              <el-table
                type="expand"
                border
                size="mini"
                :header-cell-style="{background:'#f0f1f3'}"
                :data="mail_results"
                style="width: 100%;margin:10px 0;">
                <el-table-column
                  prop="email"
                  :label="lan.COMMON_RECAIVER"
                >
                  <template slot-scope="scope">
                    {{scope.row.recipient}}
                  </template>
                </el-table-column>

                <el-table-column
                  prop="status"
                  :label="lan.COMMON_STATUS" >
                  <template slot-scope="scope">
                    {{scope.row.status_info}}
                  </template>
                </el-table-column>
                <el-table-column
                  prop="recall_status"
                  :label="lan.CENTER_SEND_STATUS" >
                  <template slot-scope="scope">
                    {{scope.row.recall_status_info}}
                  </template>
                </el-table-column>
                <el-table-column
                  prop="inform"
                  :label="lan.MAILBOX_COM_HOME_DETAILS" >
                  <template slot-scope="scope">
                    <span :class="{red:scope.row.is_red}">{{scope.row.inform}}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  :label="lan.COMMON_OPRATE" >
                  <template slot-scope="scope">
                    <el-button type="text" size="small" v-if="!scope.row.is_zhaohui" @click="recall_single(scope.row)">{{lan.COMMON_BUTTON_ZHAOHUI}}</el-button>
                  </template>
                </el-table-column>

              </el-table>

            </div>
          </div>

          <div class="mail-cipher-encrypted j-mailCipherEncrypted" v-if="is_password && !password">
            <div class="no-decryption">
              <div class="lock-item" style="padding:20px;"><i class="lock_style"></i></div>
              <div class="action-item">
                <input type="text" :placeholder="lan.LAYOUT_INDEX_PASSWORD_RULE" class="u-input" v-model="de_password" maxlength="6">
              </div>
              <div class="decryption-msg">
                <span class="j-decryption-error decryption-error" v-show="decryption_error">{{lan.MAILBOX_COM_READ_PASSWORD_ERROR}}</span>
              </div>

              <div class="action-item">
                <span class="u-btn u-btn-primary j-decrypt-submit" @click="mailDecodeFn">{{lan.COMMON_BUTTON_CONFIRM}}</span>
              </div>
              <div class="label-item">{{lan.MAILBOX_COM_READ_THIS}} <span class="highlight ">{{mfrom}}</span> {{lan.MAILBOX_COM_READ_SECRET_MAIL}}</div>
              <div class="label-item">{{lan.MAILBOX_COM_READ_VIEW_DESC}}</div>
            </div>
          </div>
          <div class="mail-content" ref="companyStyle" >
            <!--<iframe width="100%" id="mail-1534902112297" class="j-mail-content" frameborder="0" allowtransparency="true" sandbox="allow-scripts allow-popups" src="jsp/viewMailHTML.jsp?mid=1%3A1tbiAQAJEFXEqdgAXgADsl&amp;mailCipherPassword=&amp;partId=&amp;isSearch=&amp;priority=&amp;supportSMIME=&amp;striptTrs=true&amp;mboxa=&amp;iframeId=1534902112297&amp;sspurl=false" style="width: 1642px; height: 198px;">-->
            <!--</iframe>-->

            <iframe   :id="'show-iframe'+readId+'_'+tagName" frameborder="0" scrolling="100%" height="auto" width="100%"></iframe>
            <el-collapse v-model="activeNames" v-if="attachments.length>0" class="attach_box">
              <el-collapse-item :title=" lan.MAILBOX_COM_READ_ATTACH+ ' ('+attachments.length+ lan.MAILBOX_COM_READ_COUNT +' )'" name="1">

                <div v-for="(a,k) in attachments" :key="k" >
                  <el-popover
                    placement="top-start"
                    width="160"
                    trigger="hover" popper-class="bg000">
                    <div>
                      <div style="margin-bottom:10px;width:100%;" class="f-ellipsis">{{a.name}}</div>
                      <el-row>
                        <el-col class="text-center cursorP" :span="8" :title="lan.FILE_P_DOWNLOAD"  @click.native="downloadAttach(a.sid,a.name)">
                          <i class="el-icon-download"></i>
                          <p>{{lan.FILE_P_DOWNLOAD}}</p>
                        </el-col>
                        <el-col v-if="/.(gif|jpg|jpeg|png|bmp|svg|pdf|html|txt|xls|xlsx|doc|docx|ppt|pptx|xml|csv|md|log)$/.test(a.name)" class="text-center cursorP" :span="8" :title="lan.COMMON_BUTTON_PREVIEW" @click.native="preview(a)">
                          <i class="el-icon-view"></i>
                          <p>{{lan.COMMON_BUTTON_PREVIEW}}</p>
                        </el-col>
                        <el-col class="text-center cursorP" :span="8" :title="lan.FILE_A_TOP" @click.native="save_attach(a)">
                          <i class="el-icon-star-off" ></i>
                          <p>{{lan.COMMON_BUTTON_SAVE}}</p>
                        </el-col>
                      </el-row>
                    </div>

                    <el-button   class="attach_item" slot="reference" style="padding-bottom:20px;border-radius:0;background:transparent;">
                      <div class="attach_type">
                        <span class="file-big-icon" :class="a.classObject"></span>
                      </div>
                      <div class="f-ellipsis">{{a.name}}</div>
                      <div class="attach_size">{{a.size | mailsize}}</div>
                    </el-button>
                  </el-popover>


                </div>


              </el-collapse-item>
            </el-collapse>
          </div>
        </div>
        <footer class="quick-reply j-quick-reply " style="padding-top:0" v-if="mfrom || to.length>0">
          <div class="quick-reply-default quick-reply-item j-reply-default" v-if="before_replying" @click="ready_reply">{{lan.MAILBOX_COM_READ_FAST_AN}}
          </div>

          <form class="quick-reply-form quick-reply-item j-reply-form tran" v-show="replying">

            <textarea  v-if="replying":id="'editor_id_fast_'+readId+readFolderId" :ref="'editor_id_fast_'+readId+readFolderId" style="width:100%;height:200px;" v-model="content"></textarea>
            <div style="height:4px"></div>
            <span class="u-btn u-btn-primary" @click="reply" >{{lan.MAILBOX_COM_READ_SENT}}</span>
            <span class="u-btn u-btn-default" @click="cancel_reply" >{{lan.COMMON_BUTTON_CANCELL}}</span>
            <span class="f-fr"><a href="javascript:void(0)" @click="actionView(4)">{{lan.MAILBOX_COM_READ_FULL_AN}}</a></span>
          </form>


          <div class="quick-reply-item  j-reply-sending" v-if="center_replying">
            <span class="reply-state reply-sending">{{lan.MAILBOX_COM_READ_SENDING}}</span>
          </div>
          <div class="quick-reply-item  j-reply-result" v-if="after_replying">
            <span class="reply-state reply-success j-reply-success">{{lan.MAILBOX_COM_READ_SEND_SUC}}</span>
            <span class="reply-state reply-fail j-reply-fail">{{lan.MAILBOX_COM_READ_SEND_FAIL}}</span>
            <a href="javascript:void(0)" data-type="open-quick-reply">{{lan.MAILBOX_COM_READ_SEND_AGAIN}}</a>
            <a class="f-dn" href="javascript:void(0)" data-type="compose">{{lan.MAILBOX_COM_READ_FULL_AN}}</a>
          </div>

          <div class="j-footer-btn j-toolbar-footer u-btns f-fr f-dn"></div>

        </footer>

      </section>
      <div v-show="notFond">
        <h3 style="margin:30px 0 0 20px;font-size:24px;font-weight:normal;">  {{lan.MAILBOX_COM_READ_NOT_FOND}}</h3>
      </div>
    </div>

  </div>

  <!--</article>-->
</template>

<script>
  import lan from '@/assets/js/lan';
  import {readMail,downloadAttach,mailDecode,moveMails,messageFlag,rejectMessage,zipMessage,pruneMessage,emlMessage,pabMessage,deleteMail,getMessageStatus,messageRecall,notifyRecall,notifyMessage,replayMessage,saveNetAttach,setStatus,getOpenoffice,logRecall,notSpam,getMailMessage,mailSearch} from '@/api/api';
  export default  {
    name:'Read',
    props:{
      tagName:'',
      parent_readId:'',
      parent_readFolderId: '',
      read_params:'',
      read_uids:'',
      currentPage:'',
      totalPage:'',
      read_type:''
    },
    data(){
      return {
        params:'',
        uids:[],
        curr_page:1,
        total_page:1,
        curr_mail_index:0,
        readId:'',
        readFolderId:'',
        createEditor:'',
        reviewCount:0,
        sequesterCount:0,
        passwordType:'text',
        show_change_btn:true,
        prev_src:'',
        toolbarItems:
          ['source', '|','formatblock', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold',
            'italic', 'underline',  'lineheight', '|',  'justifyleft', 'justifycenter', 'justifyright',
            'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', '|','subscript',
            'superscript', 'link', 'unlink','image',  'table','hr','|', 'undo', 'redo', 'preview',
            'fullscreen',
          ],
        after_replying:false,
        center_replying:false,
        before_replying:true,
        replying:false,
        content:'',
        actionLoading:false,
        is_sender:false,
        show_result:false,
        mail_results:[],
        send_desc:'',
        undeliverCount:0,
        deliverCount:0,
        readedCount:0,
        deliver_failCount:0,
        flagsData:[
          {flags:'\\flagged',action:'add',text:'',classN:'redcolor'},
          {flags:'umail-green',action:'add',text:'',classN:'flag-green'},
          {flags:'umail-orange',action:'add',text:'',classN:'flag-orange'},
          {flags:'umail-blue',action:'add',text:'',classN:'flag-blue'},
          {flags:'umail-pink',action:'add',text:'',classN:'flag-pink'},
          {flags:'umail-cyan',action:'add',text:'',classN:'flag-cyan'},
          {flags:'umail-yellow',action:'add',text:'',classN:'flag-yellow'},
          {flags:'umail-purple',action:'add',text:'',classN:'flag-purple'},
          {flags:'umail-gray',action:'add',text:'',classN:'flag-gray'},
          {flags:'\\flagged',text:'',action:'remove'},
        ],
        flagged:false,
        burn_flagged:false,
        flag_color:'',
        de_password:'',
        decryption_error:false,
        is_password:false,
        password:false,
        visible:false,
        loading:false,
        attachments:[],
        activeNames: ['1'],
        notFond:false,
        msg:'',
        showDetails:true,
        iframeState:false,
        subject:'',
        time:'',
        mfrom:'',
        to:'',
        moveCheckIndex:'',
        moreCheckIndex:'',
        moreItems:[
          {id:3,text:'',divided:false,checkone:true},
          {id:8,text:'',divided:false,classN:'iconfont icon-iconcontacts1'},
          {id:9,text:'',divided:false,classN:'el-icon-download'},
          {id:4,text:'',divided:true,checkone:false},
          {id:12,text:'',divided:false,checkone:false},
          {id:5,text:'',divided:true,checkone:true},
          // {id:6,text:'打包下载',divided:false,checkone:false},
          {id:7,text:'',divided:false,checkone:false},
          {id:10,text:'',divided:true,checkone:true},
          {id:11,text:'',divided:false,checkone:true},

        ],
        signItems:[
          // {id:1,flags:'\\Seen',text:'未读邮件',divided:false,action:'remove'},
          {id:2,flags:'\\flagged',text:'',divided:false,action:'add',classN:'iconfont icon-iconflatcolor redcolor'},
          {id:3,text:'',divided:false,children:[
              {flags:'umail-green',action:'add',text:'',classN:{'flag-green':true}},
              {flags:'umail-orange',action:'add',text:'',classN:{'flag-orange':true}},
              {flags:'umail-blue',action:'add',text:'',classN:{'flag-blue':true}},
              {flags:'umail-pink',action:'add',text:'',classN:{'flag-pink':true}},
              {flags:'umail-cyan',action:'add',text:'',classN:{'flag-cyan':true}},
              {flags:'umail-yellow',action:'add',text:'',classN:{'flag-yellow':true}},
              {flags:'umail-purple',action:'add',text:'',classN:{'flag-purple':true}},
              {flags:'umail-gray',action:'add',text:'',classN:{'flag-gray':true}}
            ]},
          {id:4,flags:'\\flagged',text:'',divided:false,action:'remove'},
        ],
        print_html:''
      }
    },
    methods:{
      prevMail(){
        if(this.curr_mail_index==0){
          this.curr_page --;
          this.loading = true;
          if(this.read_type=='innerbox_read'){
            this.params.offset = (this.curr_page-1)*this.params.limit;
            getMailMessage(this.params).then(res=>{
              this.total_page = Math.ceil(res.data.count/this.params.limit);
              this.uids = [];
              for(let i=0;i<res.data.results.length;i++){
                this.uids.push(res.data.results[i].uid)
              }
              this.loading = false;
              this.curr_mail_index = this.uids.length-1;
              this.readId = this.uids[this.curr_mail_index]

            }).catch(err=>{
              this.loading = false;
            })
          }else if(this.read_type == 'search_read'){
            this.params.page = this.curr_page;
            mailSearch(this.params).then(res=>{
              this.loading = false;
              this.total_page = Math.ceil(res.data.count/20);
              this.uids = [];
              for(let i=0;i<res.data.results.length;i++){
                this.uids.push([res.data.results[i].uid,res.data.results[i].raw_name])
              }
              this.loading = false;
              this.curr_mail_index = 0;
              this.readFolderId = this.uids[this.curr_mail_index][1]
              this.readId = this.uids[this.curr_mail_index][0]
            }).catch(err=>{
              this.loading = false;
              console.log(err);
            })
          }

        }else{
          this.curr_mail_index --;
          if(this.read_type=='innerbox_read'){
            this.readId = this.uids[this.curr_mail_index]
          }else if(this.read_type == 'search_read'){
            this.readFolderId = this.uids[this.curr_mail_index][1]
            this.readId = this.uids[this.curr_mail_index][0]
          }
        }

      },
      nextMail(){
        if(this.curr_mail_index==this.uids.length-1){
          this.curr_page ++;
          this.loading = true;
          if(this.read_type=='innerbox_read'){
            this.params.offset = (this.curr_page-1)*this.params.limit;
            getMailMessage(this.params).then(res=>{
              this.total_page = Math.ceil(res.data.count/this.params.limit);
              this.uids = [];
              for(let i=0;i<res.data.results.length;i++){
                this.uids.push(res.data.results[i].uid)
              }
              this.loading = false;
              this.curr_mail_index = 0;
              this.readId = this.uids[this.curr_mail_index]

            }).catch(err=>{
              this.loading = false;
            })
          }else if(this.read_type == 'search_read'){
            this.params.page = this.curr_page;
            mailSearch(this.params).then(res=>{
              this.loading = false;
              this.total_page = Math.ceil(res.data.count/20);
              this.uids = [];
              for(let i=0;i<res.data.results.length;i++){
                this.uids.push([res.data.results[i].uid,res.data.results[i].raw_name])
              }
              this.loading = false;
              this.curr_mail_index = 0;
              this.readFolderId = this.uids[this.curr_mail_index][1]
              this.readId = this.uids[this.curr_mail_index][0]
            }).catch(err=>{
              this.loading = false;
              console.log(err);
            })
          }

        }else{
          this.curr_mail_index ++;
          if(this.read_type=='innerbox_read'){
            this.readId = this.uids[this.curr_mail_index]
          }else if(this.read_type == 'search_read'){
            this.readFolderId = this.uids[this.curr_mail_index][1]
            this.readId = this.uids[this.curr_mail_index][0]
          }
        }
        console.log(this.uids)
        console.log(this.curr_mail_index)
      },
      createEditorFn(val){
        let language = 'zh_CN';
        if(this.$store.getters.getLanguage == 'en'){
          language = 'en';
        }else if(this.$store.getters.getLanguage == 'zh-tw'){
          language = 'zh_TW';
        }
        let options = {
          items:this.toolbarItems,
          uploadJson:this.uploadJson,
          filterMode:false,
          resizeType:1,
          indentChar:"",
          langType : language,
          loadStyleMode:false,
          autoHeightMode:false
        }
        this.createEditor = KindEditor.create('#editor_id_fast_'+this.readId+this.readFolderId,options);
        this.createEditor.html(val);
      },
      recall_single(row){
        this.$confirm('<p>'+this.lan.CENTER_SEND_MSG1+'</p>', this.lan.COMMON_BUTTON_ZHAOHUI, {
          confirmButtonText: this.lan.COMMON_BUTTON_CONFIRM,
          cancelButtonText: this.lan.COMMON_BUTTON_CANCELL,
          dangerouslyUseHTMLString: true,
          type: 'warning'
        }).then(() => {
          let message_id = this.msg.message_id;
          let param = {
            message_id: message_id,
            recipient: row.recipient
          }
          logRecall(param).then(res=>{
            this.getMessageStatus();
          }).catch(err=>{
            console.log(err)
            let str = '';
            if(err.detail){
              str = err.detail
            }
            this.$message({
              message: this.lan.COMMON_OPRATE_FAILED +str,
              type: 'error'
            })
            this.getMessageStatus();
          })
        }).catch(() => {

        });
      },
      changeType(){
        this.passwordType = 'password';
      },
      seeAttach(){
        $('#mail_'+this.readId+'_'+this.readFolderId).animate({scrollTop:$('#mail_'+this.readId+'_'+this.readFolderId).find('.attach_box').offset().top}, 600);
      },
      changeStatus(a){
        setStatus(this.msg.attrs.calendar_event_id,a).then(res=>{
          this.msg.attrs.calendar_eventer_status = a;
          this.show_change_btn = false;
          this.$message({message:this.lan.COMMON_OPRATE_SUCCESS,type:'success'});
        },err=>{
          let str = '';
          if(err.detail){
            str = err.detail
          }
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          this.$message({message:this.lan.COMMON_OPRATE_FAILED +str,type:'error'});
        })
      },
      mail_event(){
        let param = {
          event_jump:true,
          title:this.msg.subject,
          invitors:[]
        }
        let hash = [];
        if(this.msg.mfrom){
          param.invitors.push(this.msg.mfrom[0])
          hash[this.msg.mfrom[0]] = true;
        }
        if(this.msg.to){
          this.msg.to.forEach(val=>{
            if(!hash[val[0]]){
              param.invitors.push(val[0])
              hash[val[0]] = true
            }
          })
        }
        if(this.msg.cc){
          this.msg.cc.forEach(val=>{
            if(!hash[val[0]]){
              param.invitors.push(val[0])
              hash[val[0]] = true
            }
          })
        }


        this.$store.dispatch('setMailE',param)
        this.$router.push('/calendar/index')
      },
      mail_contact(){
        // $('#treeMenuBar .el-tree-node:eq(0)').click();
        this.$router.push('/mailbox/innerbox/INBOX')
        this.$nextTick(()=>{
          this.$parent.$parent.$parent.$refs.innerbox[0].moreSearch = true;
          this.$parent.$parent.$parent.$refs.innerbox[0].search = '';
          this.$parent.$parent.$parent.$refs.innerbox[0].sort = '';
          this.$parent.$parent.$parent.$refs.innerbox[0].currentPage = 1;
          this.$parent.$parent.$parent.$refs.innerbox[0].searchForm = {
            from:this.msg.mfrom[0],
            subject:'',
            body:''
          };
          this.$parent.$parent.$parent.$refs.innerbox[0].getMessageList();
          this.$parent.$parent.$parent.editableTabsValue2 = '1'
        })


      },
      save_attach(item){
        this.loading = true;
        let param = {
          folder:this.readFolderId,
          uid:this.readId,
          sid:item.sid,
          password:this.msg.attrs.is_password && this.msg.attrs.password,
        }
        saveNetAttach(param).then(res=>{
          this.$message({
            type:'success',
            message:this.lan.COMMON_SAVE_SUCCESS
          })
          this.loading = false;
        }).catch(err=>{
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({
            type:'error',
            message:this.lan.COMMON_SAVE_FAILED +str
          })
          this.loading = false;
        })
      },
      onContentChange (val) {
        this.content = val;
      },
      ready_reply(){
        this.before_replying = false;
        this.center_replying = false;
        this.replying=true;
        $('#createEditor').val(this.content)
        setTimeout(()=>{
          if(this.createEditor){
            this.content = this.createEditor.html();
            this.createEditor.remove('#editor_id_fast_'+this.readId+this.readFolderId)
          }
          this.createEditorFn(this.content);
        },10)
      },
      cancel_reply(){
        this.replying=false;
        this.center_replying=false;
        this.before_replying = true;
      },
      reply(){
        this.content = this.createEditor.html();
        if(!this.content){
          this.$message({
            type:'error',
            message:this.lan.MAILBOX_COM_READ_INPUT_CONTENT
          })
          return;
        }
        let param = {
          folder:this.readFolderId,
          uid:this.readId,
          html_text:this.content
        }
        this.replying=false;
        this.center_replying=true;
        replayMessage(param).then(res=>{
          this.$message({
            type:'success',
            message:this.lan.MAILBOX_COM_READ_SEND_SUC
          })
          this.center_replying = false;
          this.before_replying = true;
          this.content = '';
          this.createEditor.html('')
        }).catch(err=>{
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({
            type:'error',
            message: this.lan.MAILBOX_COM_READ_SEND_FAIL +str
          })
          this.center_replying = false;
          this.before_replying = true;
        })
      },
      closeTab(tagName){
        this.$parent.$parent.$parent.removeTab(tagName);
      },
      print(){
        let mfrom = '';
        let to = '';
        let cc = '';
        if(this.mfrom){
          mfrom += '<p>'+this.lan.COMMON_SENDER+'：'+this.mfrom+'</p>'
        }
        if(this.msg.to && this.msg.to.length>0){
          to += '<p>'+this.lan.COMMON_RECAIVER+'：'
          for(let i=0;i<this.msg.to.length;i++){
            to += this.msg.to[i][1] + '&lt;'+this.msg.to[i][0]+'&gt;;'
          }
          to += '</p>'
        }
        if(this.msg.cc&&this.msg.cc.length>0){
          cc += '<p>'+this.lan.MAILBOX_COM_COMPOSE_CCER+'：'
          for(let j=0;j<this.msg.cc.length;j++){
            let t = this.msg.cc[j];
            cc += `${t[1]+'&lt;'+t[0]+ '&gt; '}`
          }
          cc += '</p>'
        }
        let print_main = `
        <div>
        <p>${this.lan.MAILBOX_COM_READ_PRINT_TITLE}</p>
        <div style="border-top:1px solid #7CACDB;border-bottom:1px solid #7CACDB;padding:4px 0;margin-bottom:16px;font-size:12px;">
            <h3>${this.subject|| this.lan.MAILBOX_NO_SUBJECT }</h3>
            ${mfrom}
            <p>${this.lan.COMMON_TIME}：${this.time.replace('T',' ')}</p>
            ${to}
            ${cc}
        </div>
        <div style="position:relative;font-size:14px;padding:15px 15px 10px 15px;*padding:15px 15px 0 15px;overflow:visible;font-size: 14px;line-height:170%;min-height:100px;_height:100px;">
            <div class="border: 1px #f1f1f1 solid; margin-left: auto; margin-right: auto; width: 640px; padding: 0px 55px; background-color: #fff;">
                 ${this.print_html}
            </div>
        </div>
      </div>`;
        var printHtml = '<div style="background:#fff;margin:0;padding:10px;font-family:Verdana">'+print_main+'</div>';//这个元素的样式需要用内联方式，不然在新开打印对话框中没有样式



        var wind = window.open('',this.lan.MAILBOX_COM_READ_NEW_W);


        wind.document.head.innerHTML = '<title>'+this.lan.MAILBOX_COM_READ_PRINT_TITLE_PAGE+'</title>'
        wind.document.body.innerHTML = printHtml;
        wind.print();
      },
      sendNotifyMessage(){
        this.msg.attrs.is_notify = false;
        let param = {
          uid:this.readId,
          folder:this.readFolderId
        }
        notifyMessage(param).then(res=>{
          this.$message({
            type:'success',
            message:this.lan.MAILBOX_COM_READ_NOTICE_SEND_SUC
          })
        }).catch(err=>{
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({
            type:'error',
            message:this.lan.MAILBOX_COM_READ_NOTICE_SEND_FAIL +str
          })
        })
      },
      recallMessage(){
        this.loading = true;
        let param = {
          uid:this.readId,
          folder:this.readFolderId
        }
        messageRecall(param).then(res=>{
          this.loading = false;
          let str = res.data.results[0].inform || res.data.results[0].recall_status_info
          this.$message({
            type:'success',
            message: this.lan.COMMON_OPRATE_SUCCESS + str
          })
          this.getReadMail();
        }).catch(err=>{
          this.loading = false;
          let str = '';
          if(err.detail){
            str = err.detail
          }
          if(err.error){
            str = err.error
          }
          this.$message({
            type:'error',
            message:this.lan.COMMON_OPRATE_FAILED +str
          })
          this.getReadMail();
        })
      },
      seeStatus(){
        this.show_result = true;
      },
      refreshStatus(){
        this.getMessageStatus();
      },
      getMessageStatus(){
        let recp = [];
        let hashRecp = [];
        let cc = this.msg.cc;
        let to = this.msg.to;
        if(to){
          for(let i=0;i<to.length;i++){
            hashRecp[to[i][0]] = true;
            recp.push(to[i][0]);
          }
        }
        if(cc){
          for(let i=0;i<cc.length;i++){
            if(!hashRecp[cc[i][0]]){
              recp.push(cc[i][0]);
            }
          }
        }
        let param = {
          message_id: this.msg.message_id,
          // recipient: recp.join(',')
        }
        getMessageStatus(param).then(res=>{
          this.mail_results = res.data.results;
          let a=0,b=0,c=0,d=0,e=0,f=0;
          for(let i=0;i<this.mail_results.length;i++){
            let o = this.mail_results[i];
            if(o.status == 'undeliver'){
              a++;
            }else if(o.status == 'deliver'){
              b++;
            }else if(o.status == 'readed'){
              c++;
            }else if(o.status == 'deliver_fail'){
              d++;
            }else if(o.status == 'review'){
              e++;
            }else if(o.status == 'sequester'){
              f++;
            }
            if(d>0){
              this.send_desc = this.lan.MAILBOX_COM_READ_PART_SEND_FAIL
            }else{
              this.send_desc = this.lan.MAILBOX_COM_READ_SEND_SUC
            }
          }
          this.undeliverCount = a;
          this.deliverCount = b;
          this.readedCount = c;
          this.deliver_failCount = d;
          this.reviewCount = e;
          this.sequesterCount = f;
        },err=>{
          console.log(err);
        })
      },
      moreHandleCommand:function(item){

        let pp = this.$parent.$parent.$parent;
        let fid = this.readFolderId;
        let param = {
          uids:[this.readId],
          folder:this.readFolderId
        }
        let pa = {
          uid:this.readId,
          folder:this.readFolderId
        }
        if(item.id==0 || item.id==1 || item.id==2 || item.id==3 || item.id==5 || item.id==10 || item.id==11){
          let view = 3; //回复
          if(item.id == 0){
            view = 3;
          }else if(item.id == 1){
            view = 4;
          }else if(item.id == 2){
            view = 5;
          }else if(item.id == 3){
            view = 6;
          }else if(item.id == 5){
            view = 7;
          }else if(item.id == 10){
            view = 2;
          }else if(item.id == 11){
            view = 1;
          }
          if(item.id==10||item.id==11){
            let href = window.location.origin+'/#/messageInfo/'+this.readId+'?folder='+encodeURIComponent(this.readFolderId)+'&view='+view;
            window.open(href)
            return;
          }
          this.loading = true;
          readMail(this.readId,{"folder":fid,"view":view}).then(res=>{
            this.loading = false;
            pp.ruleForm2 = {
              reply_to:'',
              is_priority:false,
              is_html:true,
              is_cc:true,
              is_bcc:false,
              is_partsend:false,
              to: [],
              cc: [],
              subject: '',
              secret:'',
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
            }
            let data = res.data
            pp.maillist = []
            pp.maillist_copyer = [];
            pp.maillist_bcc = [];
            pp.show_replay_to = false;
            pp.fileList = data.attachments;
            pp.ruleForm2.subject = data.subject;
            pp.ruleForm2.is_html = data.is_html;
            if(data.is_html){
              pp.content = data.html_text ;
            }else{
              // pp.content = data.plain_text.replace(/(\r\n)|(\n)/g,'<br>');
              pp.content = data.plain_text;
            }
            if(data.reply_to){
              pp.ruleForm2.reply_to = data.reply_to;
              pp.show_reply_to = true;
            }
            if(data.uid)pp.ruleForm2.uid = data.uid;
            if(data.folder)pp.ruleForm2.folder = data.folder;
            if(data.refw_type)pp.ruleForm2.refw_type = data.refw_type
            if(data.to && data.to.length>0){
              for(let i=0;i<data.to.length;i++){
                pp.maillist.push({fullname:data.to[i][1]||'',email:data.to[i][0],status:true})
              }
            }
            if(data.cc && data.cc.length>0){
              for(let i=0;i<data.cc.length;i++){
                pp.maillist_copyer.push({fullname:data.cc[i][1]||'',email:data.cc[i][0],status:true})
              }
            }
            if(data.bcc && data.bcc.length>0){
              for(let i=0;i<data.bcc.length;i++){
                pp.maillist_bcc.push({fullname:data.bcc[i][1]||'',email:data.bcc[i][0],status:true})
              }
            }

            pp.addTab('compose'+view+' ',data.subject,this.readId,fid)

          }).catch(err=>{
            console.log(err)
            this.loading = false;
          })

        }else if(item.id==4){ //拒收邮件
          this.loading = true;
          rejectMessage(param).then(res=>{
            this.loading = false;
            this.$message(
              {type:'success',message: this.lan.MAILBOX_COM_READ_MAIL_REJECT_SUC}
            )
          })
            .catch(err=>{
              this.loading = false;
              let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message(
                {type:'error',message: this.lan.MAILBOX_COM_READ_MAIL_REJECT_FAIL+str}
              )
            })
        }else if(item.id == 7){//彻底删除
          this.$confirm( this.lan.MAILBOX_COM_READ_DELETE_THROU_CONTINUE, this.lan.MAILBOX_COM_READ_SYSTEM_NOTICE, {
            confirmButtonText: this.lan.COMMON_BUTTON_CONFIRM,
            cancelButtonText: this.lan.COMMON_BUTTON_CANCELL,
            type: 'warning'
          }).then(() => {
            this.loading = true;
            pruneMessage(param).then(res=>{
              this.loading = false;
              this.$message(
                {type:'success',message: this.lan.COMMON_DELETE_SUCCESS}
              )
              this.$parent.$parent.$parent.removeTab(this.$parent.$parent.$parent.editableTabsValue2);
              pp.getFloderfn();
              this.$parent.$parent.$children[1].$children[0].getMessageList()
            }).catch(err=>{
              this.loading = false;
              let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message({
                type:'error',
                message:this.lan.COMMON_DELETE_FAILED +str
              })
            })
          }).catch(() => {

          });

        }else if(item.id==8){//添加到通讯录
          this.loading = true;
          pabMessage(pa).then(res=>{
            this.loading = false;
            this.$message(
              {type:'success',message: this.lan.COMMON_OPRATE_SUCCESS}
            )
          }).catch(err=>{
            this.loading = false;
            let str = '';
            if(err.detail){
              str = err.detail
            }
            this.$message(
              {type:'error',message: this.lan.COMMON_OPRATE_FAILED +str}
            )
          })
        }else if(item.id==9){
          this.loading = true;
          emlMessage(pa).then(response=>{
            this.loading = false;
            let blob = new Blob([response.data], { type: response.headers["content-type"] })
            let objUrl = URL.createObjectURL(blob)
            let filenameHeader = response.headers['content-disposition']
            let filename = decodeURIComponent(filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1));
            if (window.navigator.msSaveOrOpenBlob) {
              // if browser is IE
              navigator.msSaveBlob(blob, filename);//filename文件名包括扩展名，下载路径为浏览器默认路径
            } else {
              // var encodedUri = encodeURI(csvContent);//encodeURI识别转义符
              var link = document.createElement("a");
              link.setAttribute("href", objUrl);
              link.setAttribute("download", filename);

              document.body.appendChild(link);
              link.click();
            }
            this.$message(
              {type:'success',message: this.lan.COMMON_DOWNLOAD_SUCCESS}
            )
          }).catch(err=>{
            this.loading = false;
            console.log(err)
            let str = '';
            if(err.detail){
              str = err.detail
            }
            this.$message(
              {type:'error',message: this.lan.COMMON_DOWNLOAD_FAILED +str}
            )
          })
        }else if(item.id == 12){//这不是垃圾邮件
          this.$confirm('<p>'+this.lan.MAILBOX_COM_INNERBOX_CONFIRM_1+'</p><input type="checkbox" id="to_white"> '+this.lan.MAILBOX_COM_INNERBOX_CONFIRM_2, this.lan.COMMON_BUTTON_CONFIRM_NOTICE, {
            confirmButtonText: this.lan.COMMON_BUTTON_CONFIRM,
            cancelButtonText: this.lan.COMMON_BUTTON_CANCELL,
            dangerouslyUseHTMLString: true,

          }).then(() => {
            this.loading = true;
            let param_not_spam = {
              uids:[this.readId],
            }
            if($('#to_white').prop('checked')) {
              param_not_spam.to_white = true
            }else{
              param_not_spam.to_white = false
            }
            notSpam(param_not_spam).then(res=>{
              this.loading = false;
              this.$message(
                {type:'success',message:this.lan.COMMON_OPRATE_SUCCESS}
              )
              pp.getFloderfn();
              // this.closeTab(this.tagName)
              this.readFolderId = 'INBOX';
              this.$parent.$parent.$children[1].$children[0].getMessageList()
            })
              .catch(err=>{
                this.loading = false;
                let str = '';
                if(err.detail){
                  str = err.detail
                }
                this.$message(
                  {type:'error',message: this.lan.COMMON_OPRATE_FAILED+str}
                )
              })
          }).catch(() => {

          });
        }
      },
      deleteMail(){
        var params={
          uids:[this.readId],
          folder:this.readFolderId,
        };
        this.$confirm(this.lan.MAILBOX_COM_READ_DELETE_CONTINUE, this.lan.COMMON_BUTTON_CONFIRM_NOTICE, {
          confirmButtonText: this.lan.COMMON_BUTTON_CONFIRM,
          cancelButtonText: this.lan.COMMON_BUTTON_CANCELL,
          type: 'warning'
        }).then(() => {
          this.loading = true;
          deleteMail(params).then((suc)=>{
            this.loading = false;
            if(suc.data.msg=='success'){
              this.$message({
                type:'success',
                message: this.lan.COMMON_DELETE_SUCCESS
              })
              this.$parent.$parent.$parent.removeTab(this.$parent.$parent.$parent.editableTabsValue2);
              this.$parent.$parent.$children[1].$children[0].getMessageList()
            }
          },(err)=>{
            this.loading = false;
            let str = '';
            if(err.detail){
              str = err.detail
            }
            this.$message({
              type:'error',
              message: this.lan.COMMON_DELETE_FAILED +str
            })
          })
        }).catch(() => {

        });

      },
      actionView(view){
        this.actionLoading = true;
        let pp = this.$parent.$parent.$parent;
        let fid = this.readFolderId;
        this.loading = true;
        readMail(this.readId,{"folder":fid,"view":view}).then(res=>{
          this.loading = false;
          this.actionLoading = false;
          pp.ruleForm2 = {
            reply_to:'',
            is_priority:false,
            is_html:true,
            is_cc:true,
            is_bcc:false,
            is_partsend:false,
            to: [["512167072@qq.com",'zhouli']],
            cc: [],
            subject: '',
            secret:'',
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
          }
          let data = res.data
          pp.maillist = []
          pp.maillist_copyer = [];
          pp.maillist_bcc = [];
          pp.show_replay_to = false;
          pp.fileList = data.attachments;
          pp.ruleForm2.subject = data.subject;
          if(data.reply_to){
            pp.ruleForm2.reply_to = data.reply_to;
            pp.show_reply_to = true;
          }
          if(data.uid)pp.ruleForm2.uid = data.uid;
          if(data.folder)pp.ruleForm2.folder = data.folder;
          if(data.refw_type)pp.ruleForm2.refw_type = data.refw_type
          pp.ruleForm2.is_html = data.is_html;
          if(data.is_html){
            pp.content = data.html_text ;
          }else{
            // pp.content = data.plain_text.replace(/(\r\n)|(\n)/g,'<br>');
            pp.content = data.plain_text;
          }
          if(data.to && data.to.length>0){
            for(let i=0;i<data.to.length;i++){
              pp.maillist.push({fullname:data.to[i][1]||'',email:data.to[i][0],status:true})
            }
          }
          if(data.cc && data.cc.length>0){
            for(let i=0;i<data.cc.length;i++){
              pp.maillist_copyer.push({fullname:data.cc[i][1]||'',email:data.cc[i][0],status:true})
            }
          }
          if(data.bcc && data.bcc.length>0){
            for(let i=0;i<data.bcc.length;i++){
              pp.maillist_bcc.push({fullname:data.bcc[i][1]||'',email:data.bcc[i][0],status:true})
            }
          }
          pp.addTab('compose'+view+' ',data.subject,data.uid,fid)

        }).catch(err=>{
          this.loading = false;
          this.actionLoading = false;
          console.log(err)
        })
      },
      mailDecodeFn(){
        this.passwordType = 'text'
        let param = {
          uid:this.readId,
          folder:this.readFolderId,
          password:this.de_password
        }
        this.loading = true;
        mailDecode(param).then(res=>{
          this.loading = false;
          this.getReadMail();
        },err=>{
          this.loading = false;
          this.decryption_error=true;
        })
      },
      downloadAttach(sid,sname){
        let param = {
          uid:this.readId,
          folder:this.readFolderId,
          sid:sid,
          download:true
        };
        if(this.password){
          param.password = 1;
        }
        this.loading = true;
        downloadAttach(param).then(response=>{
          this.loading = false;
          let blob = new Blob([response.data], { type: response.headers["content-type"] })
          let objUrl = URL.createObjectURL(blob);
          // let filenameHeader = response.headers['content-disposition']
          let filename = sname;
          if (window.navigator.msSaveOrOpenBlob) {
            // if browser is IE
            navigator.msSaveBlob(blob, filename);//filename文件名包括扩展名，下载路径为浏览器默认路径
          } else {
            // var encodedUri = encodeURI(csvContent);//encodeURI识别转义符
            let link = document.createElement("a");
            link.setAttribute("href", objUrl);
            link.setAttribute("download", filename);

            document.body.appendChild(link);
            link.click();
          }
          this.$message({ message: this.lan.COMMON_DOWNLOAD_SUCCESS, type: 'success' });
        },err=>{
          console.log(err);
          this.loading = false;
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({ message: this.lan.COMMON_DOWNLOAD_FAILED +str, type: 'error' });
        })

      },
      preview(a){
        if(a.size && a.size>10*1024*1024){
          this.$message({
            type:'error',
            duration:6000,
            showClose:true,
            message:this.lan.FILE_INDEX_MSG1
          })
          return;
        }
        let href = window.location.origin+'/#/preview/?id='+this.readId+'&fid='+this.readFolderId+'&sid='+a.sid+'&type=attach&size='+a.size+'&suffix='+a.name.slice(a.name.lastIndexOf('.')+1)+'&name='+a.name+'&subject='+this.msg.subject;
        window.open(href)


      },
      handleCommand:function(index){
        this.checkIndex = index;
        if(index===0){
          this.checkAll=true;
        }else{
          this.checkAll=false;
        }
      },
      moveHandleCommand:function(index){
        var params={
          uids:[this.readId],
          src_folder:this.readFolderId,
          dst_folder:index
        }
        this.loading = true;
        moveMails(params).then((suc)=>{
          this.loading = false;
          this.$message({
            type:'success',
            message: this.lan.MAILBOX_COM_INNERBOX_MAIL_MOVE_SUCCESSFUL
          })
          // this.closeTab(this.tagName);
          this.readFolderId = index;
          // this.$parent.$parent.$parent.getFloderfn();
        },(err)=>{
          this.loading = false;
          this.$message({
            type:'error',
            message: this.lan.MAILBOX_COM_INNERBOX_MAIL_MOVE_FAILED
          })
        }).catch(err=>{
          this.loading = false;
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({
            type:'error',
            message: this.lan.MAILBOX_COM_INNERBOX_MAIL_MOVE_FAILED +str
          })
        })
      },
      signHandleCommand:function(item){
        if(!item){
          return;
        }
        let param = {
          uids:[this.readId],
          folder:this.readFolderId,
          action:item.action,
          flags:[item.flags]
        }
        messageFlag(param).then((suc)=>{
          this.$message({
            type:'success',
            message: this.lan.MAILBOX_COM_INNERBOX_MAIL_MARKUP_SUCCESSFUL
          })
          if(item.action == 'add'){
            this.flagged = true;
            if(item.flags == 'umail-yellow'){
              this.flag_color = 'flag-yellow';
            }else if(item.flags == 'umail-green'){
              this.flag_color = 'flag-green';
            }else if(item.flags == 'umail-orange'){
              this.flag_color = 'flag-orange';
            }else if(item.flags == 'umail-blue'){
              this.flag_color = 'flag-blue';
            }else if(item.flags == 'umail-pink'){
              this.flag_color = 'flag-pink';
            }else if(item.flags == 'umail-cyan'){
              this.flag_color = 'flag-cyan';
            }else if(item.flags == 'umail-purple'){
              this.flag_color = 'flag-purple';
            }else if(item.flags == 'umail-gray'){
              this.flag_color = 'flag-gray';
            }else{
              this.flag_color = '';
            }
          }else{
            this.flagged = false;
            this.flag_color = ''
          }
          this.$parent.$parent.$parent.$refs.innerbox[0].getMessageList();
        },(err)=>{

        }).catch(err=>{
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({
            type:'error',
            message: this.lan.MAILBOX_COM_INNERBOX_MAIL_MARKUP_FAILED +str
          })
        })
      },
      set_12_time(time){
        let theHour = time.slice(0,2);
        let min_ss = time.slice(2);
        let flag = ''
        if(theHour>=12){
          flag = this.lan.MAILBOX_COM_INNERBOX_AFTERNOON
        }else{
          flag = this.lan.MAILBOX_COM_INNERBOX_MORNING
        }
        if (theHour > 12) {
          theHour = theHour-12
        }
        if (theHour == 0) {
          theHour = 12;
        }
        return flag+theHour+min_ss
      },
      getReadMail(){
        this.loading = true;
        let rid = this.readId;
        let tagName = this.tagName;
        readMail(this.readId,{"folder":this.readFolderId}).then((data)=>{
          this.notFond = false;
          this.msg = data.data
          if(this.msg.attrs.calendar_eventer_status && this.msg.attrs.calendar_eventer_status!='start'){
            this.show_change_btn = false;
          }
          if(this.msg.attrs.is_canrecall){
            this.is_sender = true;
            this.getMessageStatus();
          }else{
            this.is_sender = false;
          }
          this.is_password = data.data.attrs.is_password;
          this.password = data.data.attrs.password;
          this.subject = data.data.subject || this.lan.MAILBOX_NO_SUBJECT;
          this.$parent.$parent.$parent.changeTabRid(this.readId,this.readFolderId,this.tagName,data.data)
          this.time = data.data.date;
          if(this.$store.getters.getIsSwtime){
            let index = this.time.indexOf('T');
            this.time = this.time.slice(0,index) + this.set_12_time(this.time.slice(index+1))
          }
          if(data.data.mfrom){this.mfrom = data.data.mfrom[1]+' < '+data.data.mfrom[0]+' > ';}
          this.to = [];
          if(data.data.to && data.data.to.length>0){
            for(let i=0;i<data.data.to.length;i++){
              let o = data.data.to[i];
              let t = o[1]+' <'+o[0]+'>'
              this.to.push(t);
            }
          }
          this.flag_color = '';
          if(data.data.flags){
            this.flagged = (data.data.flags.join('').indexOf('Flagged')>=0);
            this.burn_flagged = (data.data.flags.join('').indexOf('umail-burn')>=0);
            if(this.flagged){
              if(data.data.flags.join('').indexOf('umail-yellow')>=0){
                this.flag_color = 'flag-yellow';
              }else if(data.data.flags.join('').indexOf('umail-green')>=0){
                this.flag_color = 'flag-green';
              }else if(data.data.flags.join('').indexOf('umail-orange')>=0){
                this.flag_color = 'flag-orange';
              }else if(data.data.flags.join('').indexOf('umail-blue')>=0){
                this.flag_color = 'flag-blue';
              }else if(data.data.flags.join('').indexOf('umail-pink')>=0){
                this.flag_color = 'flag-pink';
              }else if(data.data.flags.join('').indexOf('umail-cyan')>=0){
                this.flag_color = 'flag-cyan';
              }else if(data.data.flags.join('').indexOf('umail-purple')>=0){
                this.flag_color = 'flag-purple';
              }else if(data.data.flags.join('').indexOf('umail-gray')>=0){
                this.flag_color = 'flag-gray';
              }
            }
          }
          const oIframe = document.getElementById('show-iframe'+rid+'_'+tagName);
          //-30padding
          // const deviceWidth = this.$refs.companyStyle.getBoundingClientRect().width-30;

          oIframe.style.height = 'auto';
          oIframe.style.width = '100%';
          if(data.data.is_html){
            // oIframe.contentDocument.getElementsByTagName('html')[0].innerHTML = data.data.html_text||data.data.plain_text;
            // oIframe.contentDocument.getElementsByTagName('html')[0].innerHTML = data.data.html_text||data.data.plain_text;
            var aa = data.data.html_text||data.data.plain_text
            $('#show-iframe'+rid+'_'+tagName).contents().find("body").html(aa)
            this.print_html =  data.data.html_text
          }else{
            let bhtml = data.data.html_text||data.data.plain_text;
            // oIframe.contentDocument.getElementsByTagName('html')[0].innerHTML = '<pre>'+bhtml+'</pre>';
            $('#show-iframe'+rid+'_'+tagName).contents().find("body").html('<pre>'+bhtml+'</pre>')
            this.print_html =  '<pre>'+bhtml+'</pre>'
          }


          this.attachments = data.data.attachments;
          for(let i=0;i<this.attachments.length;i++){
            let aa = this.attachments[i];
            let aname = aa.name;
            let index = aname.lastIndexOf('.');
            let type = aname.slice(index+1);
            let className = "icon-big-"+type;
            aa.classObject = {};
            aa.classObject[className] = true;
          }
          setTimeout(function(){
            const deviceHeight = oIframe.contentWindow.document.body.offsetHeight ;
            const deviceWidth = oIframe.contentWindow.document.body.scrollWidth ;
            oIframe.style.width = deviceWidth + 'px';
            oIframe.style.height = deviceHeight + 46+'px';
          },100)




          this.loading = false;
        },(err)=>{
          this.notFond=true;
          this.$parent.$parent.$parent.getFloderfn();
          this.$parent.$parent.$parent.$refs.innerbox[0].getMessageList();
          this.loading = false;
        });
      },

    },
    created:function(){

      this.readFolderId = this.parent_readFolderId
      this.readId = this.parent_readId
      this.params = this.read_params
      this.uids = this.read_uids
      this.curr_page = this.currentPage
      this.total_page = this.totalPage
      if(this.read_type=='innerbox_read'){
        for(let i=0;i<this.uids.length;i++){
          if(this.uids[i] == this.readId){
            this.curr_mail_index = i;
            break;
          }
        }
      }else if(this.read_type=='search_read'){
        for(let i=0;i<this.uids.length;i++){
          if(this.uids[i][0] == this.readId){
            this.curr_mail_index = i;
            break;
          }
        }
      }
      this.getReadMail();
    },
    watch: {
      readId(newValue, oldValue) {
        this.getReadMail();
      }
    },
    computed:{
      moveItems:function(){
        let folder = this.$parent.$parent.$parent.floderResult;
        let arr = [];
        for(let i=0;i<folder.length;i++){
          if(folder[i]['raw_name']!='Drafts'&&folder[i]['raw_name']!=this.readFolderId){
            let obj={};
            obj['text'] = folder[i]['name'];
            obj['id'] = folder[i]['raw_name'];
            obj['divided'] = false;
            arr.push(obj);
          }
        }
        return arr;
      },
      uploadJson:function(){
        return this.$store.state.uploadJson;
      },
      lan:function(){
        let lang = lan.zh
        if(this.$store.getters.getLanguage=='zh-hans'){
          lang = lan.zh
        }else if(this.$store.getters.getLanguage=='zh-tw'){
          lang = lan.zh_tw
        }else if(this.$store.getters.getLanguage=='en'){
          lang = lan.en
        }else if(this.$store.getters.getLanguage=='es'){
          lang = lan.zh
        }else{
          lang = lan.zh
        }
        this.flagsData = [
          {flags:'\\flagged',action:'add',text:lang.MAILBOX_COM_INNERBOX_RED_FLAG,classN:'redcolor'},
          {flags:'umail-green',action:'add',text:lang.MAILBOX_COM_INNERBOX_GREEN_FLAG,classN:'flag-green'},
          {flags:'umail-orange',action:'add',text:lang.MAILBOX_COM_INNERBOX_ORANGE_FLAG,classN:'flag-orange'},
          {flags:'umail-blue',action:'add',text:lang.MAILBOX_COM_INNERBOX_BLUE_FLAG,classN:'flag-blue'},
          {flags:'umail-pink',action:'add',text:lang.MAILBOX_COM_INNERBOX_PINK_FLAG,classN:'flag-pink'},
          {flags:'umail-cyan',action:'add',text:lang.MAILBOX_COM_INNERBOX_CYAN_FLAG,classN:'flag-cyan'},
          {flags:'umail-yellow',action:'add',text:lang.MAILBOX_COM_INNERBOX_YELLOW_FLAG,classN:'flag-yellow'},
          {flags:'umail-purple',action:'add',text:lang.MAILBOX_COM_INNERBOX_PURPLE_FLAG,classN:'flag-purple'},
          {flags:'umail-gray',action:'add',text:lang.MAILBOX_COM_INNERBOX_GREY_FLAG,classN:'flag-gray'},
          {flags:'\\flagged',text:lang.MAILBOX_COM_INNERBOX_CANCEL_FLAG,action:'remove'},
        ]
        this.moreItems = [
          {id:3,text:lang.MAILBOX_COM_INNERBOX_ANNEX_FORWARDING,divided:false,checkone:true},
          {id:8,text:lang.CONTACT_OAB_TOPAB,divided:false,classN:'iconfont icon-iconcontacts1'},
          {id:9,text:lang.MAILBOX_COM_READ_MAIL_DOWNLOAD,divided:false,classN:'el-icon-download'},
          {id:4,text:lang.MAILBOX_COM_INNERBOX_REJECTED_MAIL,divided:true,checkone:false},
          {id:12,text:lang.MAILBOX_COM_INNERBOX_NOT_SPAM,divided:false,checkone:false},
          {id:5,text:lang.MAILBOX_COM_INNERBOX_SEND_AGAIN,divided:true,checkone:true},
          {id:7,text:lang.MAILBOX_COM_INNERBOX_DELETE_THOROUGHLY,divided:false,checkone:false},
          {id:10,text:lang.MAILBOX_COM_READ_LETTER_HEAD,divided:true,checkone:true},
          {id:11,text:lang.MAILBOX_COM_READ_ORIGINAL_TEXT,divided:false,checkone:true},

        ]
        this.signItems = [
          {id:2,flags:'\\flagged',text:lang.MAILBOX_COM_INNERBOX_RED_FLAG,divided:false,action:'add',classN:'iconfont icon-iconflatcolor redcolor'},
          {id:3,text:lang.MAILBOX_COM_INNERBOX_OTHER_FLAG,divided:false,children:[
              {flags:'umail-green',action:'add',text:lang.MAILBOX_COM_INNERBOX_GREEN_FLAG,classN:{'flag-green':true}},
              {flags:'umail-orange',action:'add',text:lang.MAILBOX_COM_INNERBOX_ORANGE_FLAG,classN:{'flag-orange':true}},
              {flags:'umail-blue',action:'add',text:lang.MAILBOX_COM_INNERBOX_BLUE_FLAG,classN:{'flag-blue':true}},
              {flags:'umail-pink',action:'add',text:lang.MAILBOX_COM_INNERBOX_PINK_FLAG,classN:{'flag-pink':true}},
              {flags:'umail-cyan',action:'add',text:lang.MAILBOX_COM_INNERBOX_CYAN_FLAG,classN:{'flag-cyan':true}},
              {flags:'umail-yellow',action:'add',text:lang.MAILBOX_COM_INNERBOX_YELLOW_FLAG,classN:{'flag-yellow':true}},
              {flags:'umail-purple',action:'add',text:lang.MAILBOX_COM_INNERBOX_PURPLE_FLAG,classN:{'flag-purple':true}},
              {flags:'umail-gray',action:'add',text:lang.MAILBOX_COM_INNERBOX_GREY_FLAG,classN:{'flag-gray':true}}
            ]},
          {id:4,flags:'\\flagged',text:lang.MAILBOX_COM_INNERBOX_CANCEL_FLAG,divided:false,action:'remove'},
        ]
        return lang
      },
    },
    mounted(){
      // this.$parent.$parent.$parent.$refs.innerbox[0].getMessageList();
    }
  }
</script>
<style>
  .is_burn_img{
    display:inline-block;
    width:18px;
    height:18px;
    background:url(../img/is_burn.jpg)
  }
  .attach_box .el-collapse-item__header,.attach_box .el-collapse-item__wrap{
    background:transparent;
  }
  .m-read .mail.is_reply{
    bottom:268px;
  }
  .red{
    color:red;
  }
  .lock_style{
    display:inline-block;
    width:62px;
    height:62px;
    background:url('../../../assets/img/iconlock.png') no-repeat;
  }
  .attach_box .el-collapse-item__header{
    font-weight:bold;
  }
  .cursorP{
    border:1px solid #000;
  }
  .cursorP:hover{
    cursor:pointer;
    border:1px solid #fff;
  }
  .cursorP>p{
    visibility:hidden;
  }
  .cursorP>i{
    font-size:18px;
  }
  .cursorP:hover>p{
    visibility:visible;
  }
  .bg000{
    background:#000;
    color:#fff;
  }
  .el-popper.bg000[x-placement^=top] .popper__arrow::after{
    border-top-color:#000;
  }
  .attach_box .f-ellipsis{
    text-align:center;
  }
  .attach_item{
    padding-bottom: 20px;
    width: 110px;
    padding: 0 2px;
    margin: 6px 16px 6px 6px;
    border: 1px solid transparent;
    float:left;
  }
  .attach_item:hover{
    border: 1px solid #e3e4e5;
    background-color: #f0f1f3;
  }
  .attach_type{

    text-align: center;
    padding: 3px 0;
    font-size: 12px;
  }
  .file-big-icon{
    background-image: url(../../../assets/img/file-sprite.png);
    display:inline-block;
  }
  .attach_size{
    text-align: center;
    padding: 3px 0;
    font-size: 12px;
  }
</style>
