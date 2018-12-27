<template>
    <div class="mltabview-content" :id="'compose'+rid">
      <div class="mltabview-panel compose_style">
        <section class="m-mlcompose m_box_height" v-if="!send_suc" v-loading="sendLoading">
          <div class="toolbar" style="background:#fff;">
            <div id="pagination" class="f-fr">
                <div class="" @click="show_contact = !show_contact">
                    <el-button size="small">通讯录</el-button>
                </div>
            </div>

            <el-button size="small" type="primary" @click="sentMail('sent')" :loading="sendLoading"

    >{{ruleForm2.is_schedule?"定时发送":"发送"}}</el-button>
            <el-button-group >
              <el-button size="small" @click="preview">预览</el-button>
              <el-button size="small" @click="sentMail('save_draft')">存草稿</el-button>
            </el-button-group>

             <el-button  size="small" plain @click="closeTab">
                关闭
            </el-button>
            <!--<el-button type="warning" size="small" @click="open_notify">消息提醒</el-button>-->
          </div>
          <div class="main" ref="iframe_height">
            <div class="mn-aside right_menu" :class="{show_contact:show_contact}" :style="{'min-height':main_min_height+'px'}">
              <el-tabs v-model="activeName" @tab-click="loadingContact">
                <!--个人通讯录-->
                <el-tab-pane label="个人通讯录" name="first" v-loading="contact_loading">
                  <!--<el-input  placeholder="搜索" prefix-icon="el-icon-search" v-model="filterText" size="small" style="margin:6px 0;">-->
                  <!--</el-input>-->
                  <el-input placeholder="请输入内容" v-model="right_search" class="input-with-select" @keyup.native="getRightContact">
                    <el-button slot="append" icon="el-icon-search" @click="getRightContact" style="border-right: 1px solid #dcdfe6;border-radius: 0;"></el-button>
                    <el-button slot="append" icon="el-icon-refresh" @click="refresh_right"></el-button>
                  </el-input>
                  <!--<el-pagination-->
                    <!--v-if="right_page_total>0"-->
                    <!--class="only_current_page"-->
                    <!--style="text-align:center; margin-top:10px;"-->
                    <!--@current-change="contact_page_change"-->
                    <!--background-->
                    <!--:current-page="right_cpage"-->
                    <!--layout="prev,pager,next"-->
                    <!--prev-text=" 上一页 "-->
                    <!--next-text=" 下一页 "-->
                    <!--:total="right_page_total">-->
                  <!--</el-pagination>-->
                  <!--<el-tree class="filter-tree" :data="contactList" :props="defaultProps" :filter-node-method="filterNode"-->
                   <!--@node-click="selectContact"  accordion :indent="2" ref="tree2" v-loading="contact_loading">-->
                    <!--<span class="custom-tree-node" slot-scope="{ node, data }">-->

                      <!--<span :title="node.label">{{ node.label }}</span> <span v-if="data.count && data.count>0">( {{data.count}} )</span>-->
                    <!--</span>-->
                  <!--</el-tree>-->

                  <div >
                    <div v-for="(m,k) in contactList" :key="k" style="line-height:32px;cursor:pointer">
                      <div class="right_con_list"  @click="changeShowIndex(k)" :title="m.label" v-show="!right_search || m.id==0" style="font-size:16px;">
                        <i class="el-icon-caret-right" v-if="!m.show" style="margin-right:6px;" :style="{visibility:m.count==0?'hidden':''}"></i>
                        <i class="el-icon-caret-bottom" v-if="m.show" style="margin-right:6px;" :style="{visibility:m.count==0?'hidden':''}"></i>
                        <span>{{m.label}}</span>
                        <span v-if="m.count && m.count>0">( {{m.count}} )</span>
                      </div>
                      <transition>

                      </transition>
                      <div v-if="m.show" style="overflow:auto;" v-loading="m.loading">
                        <div v-for="(c,kk) in m.children" class="right_con_list" @click="selectContact(c)" :key="kk" :title="c.email" style="padding-left:30px;white-space: nowrap;">
                          <span>{{c.label}}</span>
                        </div>
                      </div>
                      <div v-if="m.show && m.count>10" style="text-align: center;margin:10px 0;">
                        <el-button type="primary" size="mini" @click="plus(false,m)" title="上一页" :disabled="m.page<=1" circle><i class="el-icon-arrow-left"></i></el-button>
                        <!--<el-button  type="text" size="small"><b>{{m.page}}</b></el-button>-->
                        第 <el-input @change="changePage($event,m)" min="1" :max="Math.ceil(m.count/10)" type="number" v-model="m.page" style="width:50px;" class="no-padding" size="mini"></el-input>页
                        <el-button size="mini" title="下一页" @click="plus(true,m)" type="primary" :disabled="m.page>= Math.ceil(m.count/10)" circle><i class="el-icon-arrow-right"></i></el-button>
                      </div>

                    </div>
                  </div>




                  <!--<el-input v-model="member_search" placeholder="请输入关键字搜索" class="input-with-select" size="small" style="margin:6px 0;">-->

                    <!--<el-button slot="append" icon="el-icon-search" @click="search_member"></el-button>-->
                  <!--</el-input>-->

                  <!--<el-select v-model="selected_group_id" placeholder="请选择"  @change="change_group" style="margin:10px 0;">-->
                    <!--<el-option  v-for="item in contact_groups" :key="item.id" :label="item.groupname" :value="item.id">-->
                      <!--<span style="float: left">{{ item.groupname }}</span>-->
                      <!--<span style="float: right; color: #8492a6; font-size: 13px">({{ item.count }})</span>-->
                    <!--</el-option>-->
                  <!--</el-select>-->
                  <!--<div style="padding-bottom:20px;border-bottom:1px dashed #aaa;margin-bottom:10px;">-->
                    <!--<div v-for="(m,k) in memberList" :key="k" class="group_member" :title="m.username">-->
                      <!--<span>{{m.name}}</span><span>&nbsp;&lt;{{m.username}}&gt;</span>-->
                    <!--</div>-->
                  <!--</div>-->
                  <!--<el-pagination-->
                    <!--style="text-align:center;"-->
                    <!--@current-change="contact_page_change"-->
                    <!--background-->
                    <!--layout="prev,next"-->
                    <!--prev-text=" 上一页 "-->
                    <!--next-text=" 下一页 "-->
                    <!--:total="100">-->
                  <!--</el-pagination>-->
                </el-tab-pane>

                <!--信纸-->
                <el-tab-pane label="信纸" name="second" class="page">
                  <ul >
                    <li><a href="#" @click="checkBgFn('noBg')">
                      <img src="../img/none_zh.png" alt="">
                      <span class="bg"></span>
                    </a></li>
                    <li v-for="(m,k) in stationeryList" :key="k" >
                      <a href="#" :class="{'active':checkBg === m.id}" @click.prevent="checkBgFn(m)">
                        <img :src="m.src" alt="">
                      </a>
                    </li>

                    <!--<li><a href="#">-->
                      <!--<img src="../img/Lotus_m.jpg" alt="">-->
                      <!--<span class="bg"></span>-->
                    <!--</a></li>-->
                  </ul>
                </el-tab-pane>
                <el-tab-pane label="模板信" name="third">
                  <div class="template_box" style="padding-top:4px;">
                    <ul class="template_ul">
                      <li class="f-csp" style="text-align: center" :class="{selected:selectId===''}" @click="deleteTemplate">
                        <img src="../img/none_zh.png" alt="">
                        <i class="el-icon-success choose"></i>
                      </li>
                      <li class="f-csp" :class="{selected:selectId===t.id}" v-for="(t,k) in templateList" :key="k" @click="selectTemplate(t)">
                        <span class="wrapper">{{t.caption}} <i class="el-icon-success choose"></i></span>
                      </li>
                      <li @click="getTemplateListfn" style="border:none;text-align:center;" v-if="showLoadMore"><el-button size="mini" plain type="success">加载更多模板</el-button></li>
                      <li @click="setTemplate" title="设置模板信" class="f-csp" style="text-align: center;font-size:32px;font-weight:bold;color:#868686"><span class="el-icon-plus"></span></li>

                    </ul>
                  </div>
                </el-tab-pane>
              </el-tabs>
            </div>
            <form class="u-form mn-form box_height"  :class="{right0:show_contact}" :style="{'min-height':main_min_height+'px'}">
              <div class="form-tt compose_title title_height">
                <el-form size="mini" inline-message :model="ruleForm2" status-icon ref="ruleForm2" label-width="90px" class="demo-ruleForm" style="font-size:16px;">
                  <el-form-item label="发件人:">
                    <el-col :span="12">
                      <el-input type="text" :value="this.$parent.$parent.$parent.username" readonly auto-complete="off"></el-input>
                    </el-col>
                    <el-col :span="12" style="text-align:right;">
                      <el-button v-show="!ruleForm2.is_partsend" type="text"  @click="changeCc">{{ruleForm2.is_cc?"取消抄送":"抄送"}} &nbsp;&nbsp;|</el-button>
                      <el-button v-show="!ruleForm2.is_partsend" type="text"  @click="changeBcc">{{ruleForm2.is_bcc?"取消密送":"显示密送"}} &nbsp;&nbsp;|</el-button>
                      <el-button type="text" @click="ruleForm2.is_partsend = !ruleForm2.is_partsend">{{ruleForm2.is_partsend?"取消群发单显":"群发单显"}} |</el-button>
                      <el-button type="text" @click="changeReply">{{show_replay_to?"取消指定回复人":"指定回复人"}}</el-button>
                    </el-col>

                  </el-form-item>

                  <el-form-item label="收件人:" >
                    <label slot="label">
                      <template>
                        <span @click="show_contact_fn('to')" class="show_contact_style">{{ruleForm2.is_partsend?"群发单显":"收件人"}}:</span>
                      </template>
                    </label>
                    <div class="padding_15">
                        <!--<el-popover-->
                           <!--v-for="(v,k) in maillist" :key="v.email"-->
                          <!--placement="bottom"-->
                          <!--width="400"-->
                          <!--trigger="click">-->
                          <!--<el-form label-width="80px" :rules="dbFormRules" ref="dbForm">-->
                            <!--<el-form-item label="姓名" prop="fullname" >-->
                              <!--<el-input v-model="v.fullname"></el-input>-->
                            <!--</el-form-item>-->
                            <!--<el-form-item label="邮箱" prop="email" >-->
                              <!--<el-input v-model="v.email"></el-input>-->
                            <!--</el-form-item>-->
                          <!--</el-form>-->

                          <!--<el-button slot="reference">-->
                            <!--<div class="mailbox_s" v-if="!ruleForm2.is_partsend" :class="{error:!v.status}" :title="v.email" @dblclick="dbEdit(v,'to',k)"><b>{{ v.fullname?(v.fullname+'<'+v.email+'>'):('<'+v.email+'>') }}</b><i class="el-icon-close" @click.stop="deleteMailboxForKey(k,v)"></i></div>-->
                          <!--</el-button>-->
                        <!--</el-popover>-->

                        <div class="mailbox_s" v-if="!ruleForm2.is_partsend" :class="{error:!v.status}" v-for="(v,k) in maillist" :key="k" :title="v.email" @dblclick="dbEdit(v,'to',k)"><b>{{ v.fullname?(v.fullname+' <'+v.email+'>'):('<'+v.email+'>') }}</b><i class="el-icon-close" @click.stop="deleteMailboxForKey(k,v)"></i></div>
                        <div class="mailbox_s" v-if="ruleForm2.is_partsend" :class="{error:!v.status}" v-for="(v,k) in partSendList" :key="k" :title="v.email" @dblclick="dbEdit(v,'partsend',k)"><b>{{ v.fullname?(v.fullname+' <'+v.email+'>'):('<'+v.email+'>') }}</b><i class="el-icon-close" @click="deleteMailboxForKey(k,v,1)"></i></div>
                        <el-autocomplete  class="no_padding"  v-model.trim="state1" :fetch-suggestions="querySearch" @keydown.8.native="deleteMailbox"
                        @blur="addMailbox" @focus="insertMailbox=1" placeholder="" @select="handleSelect" :trigger-on-focus="false" style="float:left">

                          <!--<template slot-scope="{ item }" :trigger-on-focus="false">-->
                            <!--<div class="name" style="width:300px;">{{ item.value }}</div>-->
                          <!--</template>-->
                        </el-autocomplete>

                    </div>

                  </el-form-item>
                  <el-form-item label="抄   送:" prop="cc" v-if="ruleForm2.is_cc" v-show="!ruleForm2.is_partsend">
                    <label slot="label">
                      <template>
                        <span @click="show_contact_fn('cc')" class="show_contact_style">抄送人:</span>
                      </template>
                    </label>
                    <div class="padding_15">
                      <div class="mailbox_s" :class="{error:!v.status}" v-for="(v,k) in maillist_copyer" :key="k" :title="v.email" @dblclick="dbEdit(v,'cc',k)" ><b>{{ v.fullname?(v.fullname+' <'+v.email+'>'):('<'+v.email+'>') }}</b><i class="el-icon-close" @click="deleteMailboxForKey_copyer(k,v)"></i></div>
                      <el-autocomplete  class="no_padding" v-model.trim="state_copyer" :fetch-suggestions="querySearch" @keydown.8.native="deleteMailbox_copyer"
                        @blur="addMailbox_copyer" @focus="insertMailbox=2" placeholder=""  @select="handleSelect_copyer" :trigger-on-focus="false" style="float:left"></el-autocomplete>
                    </div>
                  </el-form-item>
                  <el-form-item label="密   送:" prop="bcc" v-if="ruleForm2.is_bcc" v-show="!ruleForm2.is_partsend">
                    <label slot="label">
                      <template>
                        <span @click="show_contact_fn('bcc')" class="show_contact_style">密送人:</span>
                      </template>
                    </label>
                    <div class="padding_15">
                      <div class="mailbox_s" :class="{error:!v.status}" v-for="(v,k) in maillist_bcc" :key="k" :title="v.email" @dblclick="dbEdit(v,'bcc',k)" ><b>{{ v.fullname?(v.fullname+' <'+v.email+'>'):('<'+v.email+'>') }}</b><i class="el-icon-close" @click="deleteMailboxForKey_bcc(k,v)"></i></div>
                      <el-autocomplete  class="no_padding" v-model.trim="state_bcc" :fetch-suggestions="querySearch" @keydown.8.native="deleteMailbox_bcc"
                        @blur="addMailbox_bcc" @focus="insertMailbox=3" placeholder=""  @select="handleSelect_bcc" :trigger-on-focus="false" style="float:left"></el-autocomplete>
                    </div>
                  </el-form-item>
                  <el-form-item label="主  题:" prop="subject">
                    <el-input v-model="ruleForm2.subject"></el-input>
                  </el-form-item>

                  <el-form-item label="指定回复人:" prop="reply_to" v-show="show_replay_to">
                    <el-input v-model.trim="ruleForm2.reply_to" type="email" :placeholder="this.$parent.$parent.$parent.username"></el-input>
                  </el-form-item>
                  <el-form-item label="密  级:" prop="secret" v-if="false">
                    <el-input v-model.number="ruleForm2.secret" readonly></el-input>
                  </el-form-item>

                  <el-form-item v-show="fileList.length>0" label="附  件:" prop="attach">
                    <el-row style="line-height: 30px;padding: 2px 12px;margin: 10px 0;border: 1px solid #d4d7d9;background: #f0f1f3;border-radius: 3px;">
                      <el-col :span="14">
                        {{fileList.length}} 个文件，共 {{totalAttach | mailsize}}
                      </el-col>
                      <el-col :span="10" style="text-align:right;">
                        <el-button type="text" @click="remove_all_attach" style="color:rgb(245, 108, 108)">删除所有附件</el-button> |<el-button type="text" @click="show_all_attach = !show_all_attach">{{show_all_attach?'隐藏附件':'展开附件'}}</el-button>
                      </el-col>
                    </el-row>
                    <div  class="attach_list_style" v-if="show_all_attach">
                      <div  v-for="(f,k) in fileList" :key="f.id" class="attach_box" @mouseenter="attach_hoverfn(f.id)" @mouseleave="remove_attach_hover" :class="{attach_hover:attachIndex == f.id}">
                        <span>{{k+1}}. </span>
                        <i class="el-icon-document"></i>
                        <span >[非密] {{f.filename||f.name}}</span>
                        <i class="el-icon-check" style="margin:0 5px;color:#26af1e;font-weight:bold;"></i>
                        <span class="plan_style" v-if="f.size">{{f.size | mailsize }}</span>
                        <span class="plan_style" v-if="!f.size">{{f.file_size | mailsize }}</span>
                        <span class="attach_actions">
                          <el-button size="mini" type="text" plain @click="delete_attach(f.id,k)">删除</el-button>
                          <!--<el-button size="mini" type="text" plain>下载</el-button>-->
                        </span>
                      </div>
                    </div>

                  </el-form-item>
                  <el-row>
                    <el-col :span="18">

                      <!--<el-input type="file" id="file"></el-input>-->
                      <el-button size="small" type="text" @click="showBigDialog" id="addAttachBtn"><i class="el-icon-upload"></i> 添加附件</el-button>

                      <el-upload v-if="false"
                          class="upload-demo"
                          action=""
                          :http-request="uploadFile"
                          :show-file-list="false"
                          multiple :on-progress="uploadProgress" :on-success="sucUpload">
                          <el-button size="small" type="text" id="addAttachBtn"><i class="el-icon-upload"></i> 添加附件</el-button>
                          <div slot="tip" class="el-upload__tip"></div>
                      </el-upload>
                      <el-dropdown  placement="bottom" @command="selectUpload" style="margin-right:20px;" trigger="click">
                          <i class="el-icon-caret-bottom"></i>
                        <el-dropdown-menu slot="dropdown">
                          <el-dropdown-item  command="filecore">从文件中心添加</el-dropdown-item>
                          <el-dropdown-item  command="upload">上传到文件中转站</el-dropdown-item>
                        </el-dropdown-menu>
                      </el-dropdown>

                      <el-dropdown trigger="click" placement="bottom-start" @command="checkSignatrue">
                        <el-button type="text" size="small">
                          签名<i class="el-icon-caret-bottom el-icon--right"></i>
                        </el-button>
                        <el-dropdown-menu slot="dropdown">
                          <el-dropdown-item command="removeSign">不使用签名档</el-dropdown-item>
                          <el-dropdown-item v-for="(s,k) in signatureList" :key="k" :divided="k==0" :command="s" :class="{ blue_color: signCheck===s.id }">
                            <b><i class="el-icon-check vibility_hide" :class="{ vibility_show: signCheck===s.id }"></i> </b>
                            {{ s.caption}}</el-dropdown-item>
                          <el-dropdown-item divided command="editSign">编辑签名档</el-dropdown-item>
                        </el-dropdown-menu>
                      </el-dropdown>

                      <!--<el-upload-->
                          <!--action=""-->
                          <!--:http-request="imgChange"-->
                          <!--:show-file-list="false"-->
                          <!--multiple  style="display:inline-block;">-->
                          <!--<el-button size="small" type="primary"> 插入图片</el-button>-->
                      <!--</el-upload>-->
                    </el-col>
                    <el-col :span="6" style="text-align: right;">
                      <el-button type="text" @click="changeIsHtml" size="">{{ruleForm2.is_html?"纯文本":"多媒体文本"}}</el-button>
                    </el-col>
                  </el-row>



                </el-form>
              </div>
              <div class="form-edr compose_editor" ref="editor_box" style="min-height:280px;" :style="{height:editor_height+'px'}">

                <!--<div v-html="content"></div>-->
                <div>
                  <textarea name="aa" v-model="content" :id="editor_id" :ref="editor_id"  rows="10" style="width:100%" :style="{height:editor_height+'px'}"></textarea>
                </div>



                <!--<editor :id="editor_id+'1'" :ref="editor_id" :height="editor_height+'px'" width="100%" :content="content" :filterMode="false"-->
                    <!--pluginsPath="/static/kindeditor/plugins/" :resizeType="0" indentChar=""-->
                    <!--:loadStyleMode="false" :items="toolbarItems" :uploadJson="uploadJson"-->
                    <!--@on-content-change="onContentChange"  :autoHeightMode="false" :afterCreate="afterChange" @afterFocus="editorfocus">-->

                <!--</editor>-->



              </div>
              <!-- form-toolbar compose_footer -->
              <div class=" footer_height" style="padding-left: 10px;">
                <div class="bt-hd-wrap">
                  <el-checkbox v-model="ruleForm2.is_save_sent">保存到"已发送"</el-checkbox>
                  <el-checkbox v-model="ruleForm2.is_priority">设为"紧急"</el-checkbox>
                  <el-checkbox v-model="ruleForm2.is_confirm_read">已读回执</el-checkbox>
                  <el-checkbox v-model="ruleForm2.is_password" :disabled="ruleForm2.is_schedule||ruleForm2.is_burn" @change="changeBottom">邮件加密</el-checkbox>
                  <el-checkbox v-model="ruleForm2.is_schedule" :disabled="ruleForm2.is_password||ruleForm2.is_burn" @change="changeBottom('sch')">定时发送</el-checkbox>
                  <el-checkbox v-model="ruleForm2.is_burn" :disabled="ruleForm2.is_password||ruleForm2.is_schedule" @change="changeBottom('burn')">阅后即焚</el-checkbox>

                </div>
                <div >
                  <div class="bt-cnt" v-show="ruleForm2.is_password||ruleForm2.is_schedule||ruleForm2.is_burn">
                  <div v-show="ruleForm2.is_password">
                    <p ><b>邮件加密 </b> 收信人需要密码才能查看邮件</p>
                    <div style="border-top:1px dashed #e3e4e5;padding:12px 0;">
                      设置查看密码：<el-input style="width:auto;" size="mini" v-model.trim="ruleForm2.password" auto-complete="off"></el-input> <span style="font-size:12px;color:#aaa;">(请输入6个字符，数字或英文字母，字母区分大小写，首尾不能有空格)</span>
                    </div>
                  </div>

                  <div v-show="ruleForm2.is_schedule">
                    <div style="border-top:1px dashed #e3e4e5;padding:12px 0;">
                     <el-date-picker
                        v-model="ruleForm2.schedule_day"
                        type="datetime" size="small"
                        value-format="yyyy-MM-dd HH:mm" format="yyyy-MM-dd HH:mm"
                        :picker-options="pickerBeginDateBefore"
                        placeholder="选择定时发送的时间">
                      </el-date-picker>
                      <p style="margin-top:10px;" v-if="ruleForm2.schedule_day"><b>本邮件将在 {{ruleForm2.schedule_day.toLocaleString()}} 投递到对方邮箱</b></p>
                    </div>
                  </div>

                  <div v-show="ruleForm2.is_burn">
                    <p><b>阅后即焚 </b> 超过阅读次数或限定时间后，该邮件将自动销毁</p>
                    <div style="border-top:1px dashed #e3e4e5;padding:12px 0;">
                      <div>
                        限定阅读次数：<el-input style="width:auto;" size="mini" type="number" v-model="ruleForm2.burn_limit"></el-input> <span style="font-size:12px;color:#aaa;">（可统一向每个收件人设置1~99次，超出阅读次数后读信链接将自动失效）</span>
                      </div>
                      <div style="padding-top:12px;">
                        邮件销毁时间：
                        <el-date-picker
                          v-model="ruleForm2.burn_day"
                          format="yyyy-MM-dd" value-format="yyyy-MM-dd"
                          :picker-options="pickerBeginDateBefore"
                          type="date" style="display:inline-block"
                          placeholder="选择日期" size="mini">
                        </el-date-picker>
                        <span style="font-size:12px;color:#aaa;">（邮件在所设日期当天24时自动销毁）</span>
                      </div>
                    </div>
                  </div>

                </div>
                </div>

              </div>
            </form>
          </div>
        </section>
        <section class="m-mlcompose" v-if="send_suc" v-loading="recallLoading">
          <div class="suc-main u-scroll">
            <div class="suc-title j-suc-title">
                <div class="h2">
                  <i class="el-icon-success" style="color:#26af1e"></i>
                    {{sendResult.type=='schedule'?"邮件将于 "+sendResult.schedule_day+" 发送，暂时保存到草稿箱":"邮件已发送"}}
                </div>
                <el-button type="text" @click="change_show_result" v-if="sendResult.type=='send'">{{show_result?'[隐藏发送状态]':'[显示发送状态]'}}</el-button>
                <el-button type="text" @click="getMessageStatus" v-if="sendResult.type=='send' && show_result">[刷新]</el-button>
                <el-button type="text" @click="recall" v-if="sendResult.type=='send'">[召回邮件]</el-button>
                <el-button type="text" @click="goEdit" v-if="sendResult.type=='schedule'">[继续编辑邮件]</el-button>
            </div>
            <div class="suc-content">
              <div style="margin-bottom:10px;">
                <el-alert v-if="sendResult.is_password"
                  :title="'邮件已加密，密码为：'+sendResult.password"
                  type="warning"
                  description="需要密码才能查看，您可以通过其他方式告知对方。"
                          show-icon
                  >
                </el-alert>
                <el-alert v-if="sendResult.is_burn"
                  title="这是一封阅后即焚的邮件"
                  type="warning"
                  description=""
                          show-icon
                  >
                </el-alert>
              </div>
              <div class="j-status-detail" v-show="show_result&& sendResult.type!='schedule'">
                <el-table
                  type="expand"
                  :header-cell-style="{background:'#f0f1f3'}"
                  :data="mail_results"
                  style="width: 100%">
                  <el-table-column
                    prop="recipient"
                    label="收件人"
                    >
                  </el-table-column>

                  <el-table-column
                    prop="status"
                    label="发送状态">
                    <template slot-scope="scope">
                      {{scope.row.status_info}}
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="recall_status"
                    label="召回状态" >
                    <template slot-scope="scope">
                      {{scope.row.recall_status_info}}
                    </template>
                  </el-table-column>
                  <el-table-column label="详情">
                    <template slot-scope="scope">
                      <span style="color: #f56c6c;" v-if="scope.row.is_red">{{scope.row.inform}}</span>
                      <span v-if="!scope.row.is_red">{{scope.row.inform}}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-button type="text" size="small" v-if="!scope.row.is_zhaohui" @click="recall_single(scope.row)">召回邮件</el-button>
                    </template>
                  </el-table-column>
                </el-table>

              </div>
              <div class="desc  j-autosave-desc" v-if="!is_save_contact">

                <p class="autosave">
                  如要自动保存联系人，您可以 设置 <el-button type="text" @click="autoSave">自动保存</el-button>
                </p>
              </div>
            </div>
            <div class="suc-content">
                <div class="more-action u-btns j-more-action">
                  <el-button type="info" plain size="small" @click="backToBox(0)">返回邮箱</el-button>
                  <el-button type="primary" size="small" @click="backToBox(1)">继续写信</el-button>
                </div>
            </div>
        </div>
        </section>
      </div>


      <el-dialog title="添加发送地址" :visible.sync="transform_dialog" :append-to-body="true" width="80%" :close-on-click-modal="false" @close="">
        <!--<tree-transfer :title="tree_title" :from_data='fromData' :to_data='toData' :defaultProps="{label:'label'}" @addBtn='add' @removeBtn='remove' :mode='mode' height='540px' filter openAll>-->
    <!--</tree-transfer>-->
        <el-row :gutter="10" style="margin-bottom:10px;">
          <el-col :span="6">
            <span style="visibility: hidden"> 1</span>
          </el-col>
          <el-col :span="4">
            <div v-if="webmail_soab_show && expand_soab">
              <input type="hidden" v-model="soab_domain_cid"/>
              域名：
              <el-select v-model="soab_domain_cid" placeholder="请选择" @change="soabChangeDomain" size="mini">
                <el-option v-for="item in soab_domain_options" :key="item.id" :label="item.label" :value="item.id"></el-option>
              </el-select>
            </div>
          </el-col>
          <el-col :span="4">
            <el-input placeholder="请输入内容" v-model="contact_search" class="input-with-select" size="small">
              <el-button slot="append" icon="el-icon-search"  @click="search_dept"></el-button>
            </el-input>
          </el-col>
        </el-row>
        <el-row  :gutter="10">
          <el-col :span="6" >

            <div style="height:520px;overflow: auto;width:100%;border:1px solid #dcdfe6">
               <!--:default-expanded-keys="default_expanded"-->
                <!--:default-checked-keys="default_checked"-->
                <!--:expand-on-click-node="false"-->
              <el-tree

                node-key="keyId"
                :data="transform_menu"
                :default-expanded-keys="default_expanded"
                @node-expand="nodeExpand"
                @node-collapse="nodeCollapse"
                accordion
                ref="contactTreeRef"
                :highlight-current="true"
                :props="defaultPropsCon"
                @node-click="contact_tree_click">
                <span  slot-scope="{ node, data }" :title="node.label">

                  <!--<i v-if="data.children && data.children.length==0" class="iconfont icon-icongroup"></i>-->
                  <span>{{ node.label }}</span>


                </span>
              </el-tree>
            </div>

          </el-col>
          <el-col :span="12" style="height:420px;border-left:2px dotted #dcdfe6;border-right:2px dotted #dcdfe6;">
            <el-table
              height="520"
              :data="contactData"
              tooltip-effect="dark"
              style="width: 100%"
              @row-click="rowClick" @selection-change="select_change"
              @select="selectionChange_contact" @select-all="selectionChange_contact"  ref="contactTable" :header-cell-style="{background:'#f0f1f3'}">
              <el-table-column
                type="selection"
                width="55">
              </el-table-column>
              <el-table-column prop="fullname" label="姓名">
                <template slot-scope="scope">
                  <i v-if="scope.row.is_dept" style="color:red;" title="部门" class="iconfont icon-icongroup"></i>
                  <i v-if="!scope.row.is_dept" style="color:#2976A8;" class="iconfont icon-icon-gender-man"></i>
                  <span>{{ scope.row.fullname|| scope.row.name}}</span>
                </template>
              </el-table-column>
              <el-table-column  label="邮件地址">
                <template slot-scope="scope">
                  <span>{{scope.row.email || scope.row.pref_email || scope.row.username}}</span>
                  <span v-if="scope.row.is_dept" style="color:red;">(部门邮箱)</span>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
          <el-col :span="6" style="height:420px;">
            收件人：(<b>{{toList.length}}</b>)
            <div class="address_box" :class="{active:active_box=='to'}" @click="switch_to('to',toList)">
              <el-row v-for="(t,k) in toList" :key="k" class="hover_show_box">
                <el-col :span="22" style="overflow: hidden;white-space: nowrap" :title="t.username||t.email">{{t.name||t.fullname}} &lt;{{t.username||t.email}} &gt;</el-col>
                <el-col :span="2" style="text-align: right">
                  <i class="el-icon-error delete_hover" @click="deleteList('to',t.username,k)"></i>
                </el-col>
              </el-row>
            </div>
            抄送人：(<b>{{ccList.length}}</b>)
            <div class="address_box" :class="{active:active_box=='cc'}" @click="switch_to('cc',ccList)">
              <el-row v-for="(t,k) in ccList" :key="k" class="hover_show_box">
                <el-col :span="22" style="overflow: hidden;white-space: nowrap" :title="t.username||t.email">{{t.name||t.fullname}} &lt;{{t.username||t.email}} &gt;</el-col>
                <el-col :span="2" style="text-align: right">
                  <i class="el-icon-error delete_hover" @click="deleteList('cc',t.username,k)"></i>
                </el-col>
              </el-row>
            </div>

            密送人：(<b>{{bccList.length}}</b>)
            <div class="address_box" :class="{active:active_box=='bcc'}" @click="switch_to('bcc',bccList)">
              <el-row v-for="(t,k) in bccList" :key="k" class="hover_show_box">
                <el-col :span="22" style="overflow: hidden;white-space: nowrap" :title="t.username||t.email">{{t.name||t.fullname}} &lt;{{t.username||t.email}} &gt;</el-col>
                <el-col :span="2" style="text-align: right">
                  <i class="el-icon-error delete_hover" @click="deleteList('bcc',t.username,k)"></i>
                </el-col>
              </el-row>
            </div>
          </el-col>

        </el-row>
        <el-row :gutter="10" style="margin-bottom:10px;">
          <el-col :span="18" :offset="6">
            <el-pagination
              @size-change="handleSizeChange_contact"
              @current-change="handleCurrentChange_contact"
              :current-page="currentPage"
              :page-sizes="[10, 20,50,100]"
              :page-size="pageSize"
              layout="total,prev, pager, next,sizes"
              :total="totalCount">
            </el-pagination>
          </el-col>
        </el-row>
        <div slot="footer" class="dialog-footer" >
          <el-button @click="cancelAddress">取 消</el-button>
          <el-button type="primary" @click="sureAddress">确 定</el-button>
        </div>
      </el-dialog>

      <el-dialog title="文件中心" :visible.sync="coreFileDialog" :modal-append-to-body="false">
        <el-tabs v-model="activeName_file" @tab-click="switch_file" style="min-height:200px;">
          <el-tab-pane label="文件中转站" name="first">
            <el-pagination class="margin-bottom-5"
              @size-change="attachSizeChange"
              @current-change="attachCurrentChange"
              :current-page="attachCurrentPage"
              :page-sizes="[10,20,50,100]"
              :page-size="attachPageSize" background
              layout="total, prev, pager, next, sizes"
              :total="attachTotal" small>
            </el-pagination>

            <el-table @selection-change="fileSelectionChange" @row-click="rowClick_afile"
              ref="afileTable" :data="coreFileList" tooltip-effect="dark" style="width: 100%"
              >
              <el-table-column type="selection"  width="55"></el-table-column>
              <el-table-column prop="filename" label="文件名" ></el-table-column>
              <el-table-column prop="size" label="文件大小" width="100" >
                <template slot-scope="scope">
                    <span  class="plan_style">{{scope.row.size | mailsize}}</span>
                </template>
              </el-table-column>
            </el-table>

          </el-tab-pane>
          <el-tab-pane label="个人网盘" name="second">
            <div style="padding:0 0 8px 4px;">
              路径：<span v-for="(fn,k) in folder_names" :key="k"><b style="cursor: pointer;color:blue;" @click="getNetfile(fn.id)">{{fn.name}}</b> / </span>
            </div>
            <el-pagination class="margin-bottom-5"
              @size-change="attachSizeChange_net"
              @current-change="attachCurrentChange_net"
              :current-page="attachCurrentPage_net"
              :page-sizes="[10,20,50,100]"
              :page-size="attachPageSize_net" background
              layout="total, prev, pager, next, sizes"
              :total="attachTotal_net" small>
            </el-pagination>
            <el-table @selection-change="fileSelectionChange" @row-click="rowClick_nfile"
              ref="nfileTable" :data="nfileList" tooltip-effect="dark" style="width: 100%"

              >
              <el-table-column type="selection"  width="55" :selectable="selectablee"></el-table-column>
              <el-table-column prop="name" label="文件名" >
                <template slot-scope="scope">
                    <div v-if="scope.row.nettype=='folder'"><span @click="getNetfile(scope.row.id)" style="color:blue;text-decoration: underline;font-weight:bold;cursor:pointer;">{{scope.row.name}}</span></div>
                    <div v-if="scope.row.nettype!='folder'"><span>{{scope.row.name}}</span></div>
                </template>
              </el-table-column>
              <el-table-column prop="file_size" label="文件大小" width="100" >
                <template slot-scope="scope">
                    <span  class="plan_style">{{scope.row.file_size |mailsize}}</span>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="企业网盘" name="third">
            <div style="padding:0 0 8px 4px;">
              路径：<span v-for="(fn,k) in folder_names_company" :key="k"><b style="cursor: pointer;color:blue;" @click="getNetfile_company(fn.id)">{{fn.name}}</b> / </span>
            </div>
            <el-pagination class="margin-bottom-5"
              @size-change="attachSizeChange_company"
              @current-change="attachCurrentChange_company"
              :current-page="attachCurrentPage_company"
              :page-sizes="[10,20,50,100]"
              :page-size="attachPageSize_company" background
              layout="total, prev, pager, next, sizes"
              :total="attachTotal_company" small>
            </el-pagination>
            <el-table @selection-change="fileSelectionChange" @row-click="rowClick_nfile_company"
              ref="nfileTable_company" :data="nfileList_company" tooltip-effect="dark" style="width: 100%"

              >
              <el-table-column type="selection"  width="55" :selectable="selectablee"></el-table-column>
              <el-table-column prop="name" label="文件名" >
                <template slot-scope="scope">
                    <div v-if="scope.row.nettype=='folder'"><span @click="getNetfile_company(scope.row.id)" style="color:blue;text-decoration: underline;font-weight:bold;cursor:pointer;">{{scope.row.name}}</span></div>
                    <div v-if="scope.row.nettype!='folder'"><span>{{scope.row.name}}</span></div>
                </template>
              </el-table-column>
              <el-table-column prop="file_size" label="文件大小" width="100" >
                <template slot-scope="scope">
                    <span  class="plan_style">{{scope.row.file_size |mailsize}}</span>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
        <div slot="footer" class="dialog-footer">
          <el-button @click="coreFileDialog = false" size="small">取 消</el-button>
          <el-button type="primary" @click="addAttachfn" size="small">确 定</el-button>
        </div>
      </el-dialog>

      <el-dialog title="邮件召回" :visible.sync="recallTableVisible" :append-to-body="true">
        <el-table :data="recallData">
          <el-table-column property="recipient" label="收件人"></el-table-column>
          <el-table-column property="inform" label="详情">
            <template slot-scope="scope">
              <span style="color: #f56c6c;" v-if="scope.row.is_red">{{scope.row.inform}}</span>
              <span v-if="!scope.row.is_red">{{scope.row.inform}}</span>
            </template>
          </el-table-column>
        </el-table>
      </el-dialog>

      <el-dialog title="附件上传" :visible.sync="bigUploadVisible" :append-to-body="true" class="bigUpload" @close="bigClose" :close-on-click-modal="false">
        <div style="min-height:300px;">
          <!--:autoStart="false"-->
          <uploader :options="options" class="uploader-example" :autoStart="false" :fileStatusText="fileStatusText"
             @file-success="fileSuccess"
             @file-added="fileAdded"
                    @file-removed="fileRemoved"
              @files-added="filesAdded">
            <uploader-unsupport></uploader-unsupport>
            <uploader-drop>
              <!--<p>Drop files here to upload or</p>-->
              <uploader-btn>上传文件</uploader-btn>
            </uploader-drop>
            <uploader-list v-loading="loading2"
    element-loading-text="正在扫描文件..."
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(0, 0, 0, 0.6)">

            </uploader-list>

          </uploader>
          <!--multiple-->
          <!--:auto-upload="false"-->
          <el-upload v-if="false"
            class="upload-demo"
            ref="bigUpload"
            action=""
            :http-request="bigUpload"
            :file-list="bigList"
            :on-remove="handleRemove"
            :on-change="bigListSucess"
            :before-upload="beforeUpload"
            >
            <el-button slot="trigger" size="small" type="primary" :loading="bigLoading" :disabled="bigLoading">上传文件</el-button>
            <!--<el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>-->
            <div slot="tip" class="el-upload__tip" style="color:#f56c6c">{{tip}}</div>
          </el-upload>

        </div>
        <div slot="footer" class="dialog-footer">
          <el-button @click="bigUploadVisible = false" >取 消</el-button>
          <!--<el-button @click="submitUpload" type="primary">上 传</el-button>-->
          <el-button @click="addBigAttach" type="primary" :loading="bigLoading">确 定</el-button>
        </div>
      </el-dialog>

      <el-dialog title="修改邮箱"  :visible.sync="dbFormVisible"  :append-to-body="true" width="420px">
        <el-form :model="dbForm" label-width="80px" :rules="dbFormRules" ref="dbForm">

          <el-form-item label="姓名" prop="fullname" >
            <el-input v-model="dbForm.fullname"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email" >
            <el-input v-model="dbForm.email"></el-input>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="dbFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editEmail" >确定</el-button>
        </div>
      </el-dialog>
    </div>
</template>

<script>
  import axios from 'axios';
  import cookie from '@/assets/js/cookie';
  import SparkMD5 from 'spark-md5'
  // import treeTransfer from 'el-tree-transfer'
  import { contactPabGroupsGet,contactPabMapsGet,contactPabMembersGet,postAttach,deleteAttach,getAttach,contactOabDepartsGet,
  mailSent,netdiskGet,contactCabGroupsGet,contactSoabDomainsGet, contactSoabGroupsGet,contactOabMembersGet,contactCabMembersGet,contactSoabMembersGet,getParamBool,sendRecall,getMessageStatus,settingSignatureGet,getTemplateList,getTemplateById,getDeptMail,readMail,getContactInfo,getContactLab,uploadCheck,uploadChunk,uploadSuccess,netdiskCapacityGet,companyDiskGet,logRecall,singleSignatures} from '@/api/api'
  const emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
  export default {
    props:{
      type:'',
      compose_type:'',
      iframe_height:'',
      rid:'',
      parent_ruleForm2: {
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
      parent_content:'',
      parent_maillist:  {
        type:Array,
        default:[]
      },
      parent_maillist_copyer: {
        type:Array,
        default:[]
      },
      parent_maillist_bcc: {
        type:Array,
        default:[]
      },
      parent_fileList: {
        type:Array,
        default:[]
      },
      parent_show_reply_to:false
    },

    data(){
      const isEmail = function(rule,value,callback){
        if(emailReg.test(value) == false){
          callback(new Error("请输入正确的邮箱"));
        }else{
          callback();
        }
      };
      let _this = this;
      return {
        editoraaa:'',
        expand_soab:false,
        right_search:'',
        right_cpage:1,
        right_page_total:0,
        recallLoading:false,
        show_all_attach:true,
        nfileList_company:[],
        attachCurrentPage_company:1,
        attachPageSize_company:10,
        attachTotal_company:0,
        show_replay_to:false,
        dbIndex:0,
        activeDb:'to',
        dbFormVisible:false,
        dbForm:{fullname:'',email:''},
        dbFormRules:{
          email: [
            { required: true, message: '请输入邮箱地址', trigger: 'blur' },
            { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
          ]
        },
        folder_capacity:{},
        loading2:false,
        files:[],
        cfile:'',
        fileList_big:[],
        bigLoading:false,
        tip:'',
        bigList:[],
        bigUploadVisible:false,
        uploadFileData:{
          chunk:0,
          isLastChunk:false, //是否最后一片文件
          fileName:'filename'  //文件名称
        },
        fileStatusText:{
           success: '成功',
            error: '失败',
            uploading: '上传中...',
            paused: '暂停',
            waiting: '等待'
        },
        options: {
          // https://github.com/simple-uploader/Uploader/tree/develop/samples/Node.js
          // target: '/api/netdisk/upload/chunk/',
          target: '/api/netdisk/uploadnew/',
          testChunks: true,
          headers:{
            Authorization :`JWT ${cookie.getCookie('token')}`
          },
          query: {
            'fileMd5' : ''
          },
          testMethod:'GET',
          forceChunkSize:true,
          allowDuplicateUploads:true,
          fileParameterName:'chunkFile',
          singleFile:false,
          chunkSize:1024*1024*2,
          simultaneousUploads:3,
          // permanentErrors:[ 415, 500, 501],
          preprocess:function(chunk){

            chunk.preprocessFinished();
          },
          processParams:function(param){
            console.log('param')
            param = {
              chunkNumber:param.chunkNumber,
              fileMd5:param.identifier
            }
            return param;
          },
          generateUniqueIdentifier(file){
            // console.log('identifier')
            // let b;
            // _this.cfile = file;
            // _this.calcMD56(file,(a)=>{
            //   // _this.options.query['fileMd5'] = a
            //   b = a;
            // })
            // return _this.calcMD567(file);
          },
          parseTimeRemaining: function (timeRemaining, parsedTimeRemaining) {
            return parsedTimeRemaining
              .replace(/\syears?/, '年')
              .replace(/\days?/, '天')
              .replace(/\shours?/, '小时')
              .replace(/\sminutes?/, '分钟')
              .replace(/\sseconds?/, '秒')
          },
        },
        webmail_cab_show: false,
        webmail_soab_show: false,
        error_list:[],
        member_search:'',
        member_page:1,
        member_group_id:0,
        selected_group_id:0,
        contact_groups:[
          {id:1,groupname:'组名1',count:10,is_sysname:false},
          {id:2,groupname:'组名2',count:12,is_sysname:false},
          {id:3,groupname:'组名3',count:15,is_sysname:false}
        ],
        memberList:[
          {username:'512167072@qq.com512167072',name:'周莉'},
          {username:'512167072@qq.com',name:'周莉'},
          {username:'512167072@qq.com',name:'周莉'},
          {username:'512167072@qq.com',name:'周莉'},
          {username:'512167072@qq.com',name:'周莉'},
          {username:'512167072@qq.com',name:'周莉'},
          {username:'512167072@qq.com',name:'周莉'},
          {username:'512167072@qq.com',name:'周莉'},
          {username:'512167072@qq.com',name:'周莉'},
        ],
        sendLoading:false,
        oabchildren:[],
        contactSelection:[],
        showLoadMore:true,
        selectId:'',
        tpage:1,
        templateList:[

        ],
        checkBg:'',
        stationeryList:[
          {id:0,src:require('../img/0.png'),background:'url(/static/img/a_04.jpg) repeat-x #cdede2'},
          {id:1,src:require('../img/1.png'),background:'url(/static/img/a_01.jpg) no-repeat #f6ffec'},
          {id:2,src:require('../img/2.png'),background:'url(/static/img/a_12.jpg) repeat-x left bottom #e3ebf4'},

          {id:5,src:require('../img/5.png'),background:'url(/static/img/a_07.jpg) repeat-x #e4ebf5'},
          {id:6,src:require('../img/6.png'),background:'url(/static/img/b_02.jpg)'},
          {id:7,src:require('../img/7.png'),background:'url(/static/img/b_01.jpg)'},
          {id:8,src:require('../img/8.png'),background:'url(/static/img/a_02.jpg) no-repeat #fffaf6'},
          {id:9,src:require('../img/9.png'),background:'url(/static/img/a_03.jpg) no-repeat #fbf7f4'},
          {id:10,src:require('../img/10.png'),background:'url(/static/img/a_05.jpg) no-repeat #a7dcd2'},
          {id:11,src:require('../img/11.png'),background:'url(/static/img/a_08.jpg) no-repeat #f3f3eb'},
          {id:12,src:require('../img/12.png'),background:'url(/static/img/a_09.jpg) repeat-x #0e9dbb'},
          {id:13,src:require('../img/13.png'),background:'url(/static/img/a_10.jpg) repeat-x #bfdfec'},
          {id:14,src:require('../img/14.png'),background:'url(/static/img/a_11.jpg) no-repeat #fff2d8'},
          {id:3,src:require('../img/3.png'),background:'url(/static/img/a_06.jpg) repeat-x #221f18'},
        ],
        signCheck:'',
        signatureList:[],
        is_save_contact:false,
        maillist:[],
        maillist_copyer:[],
        maillist_bcc:[],
        fileList:[],
        ruleForm2:{
          reply_to:'',
          is_priority:false,
          is_html:true,
          is_cc:true,
          is_bcc:false,
          maillist_bcc:[],
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
        content:'',
        main_min_height:800,
        sendResult:{},
        mail_results:[],
        recallTableVisible:false,
        recallData:[],
        isRecall:false,
        message_id:'',
        recipient:'',
        show_result:true,
        send_suc:false,
        editor_height:300,
        active_box:'to',
        checkedList:[
          {
            department:"万国城店C组",
            id:1246,
            mailbox:1246,
            mobile:'',
            name:'王巧月',
            position:'买卖顾问',
            tel_group:null,
            tell_work:'None / None',
            username:"wangqiaoyue@test.com"
          }
        ],
        allSeclect: [],
        toList:[],
        hashTo:[],
        ccList:[],
        hashCc:[],
        bccList:[],
        hashBcc:[],
        contact_search:'',
        pid:'',
        default_expanded:[],
        default_checked:['0ab272'],
        soab_domain_cid:'',
        soab_domain_options:[],
        contactData:[],
        folder_names:[],
        folder_names_company:[],
        nfileList:[],
        activeName_file:'first',
        contact_loading:false,
        transform_menu: [],
        defaultPropsCon: {
          id:'id',
          label: 'label',
          children: 'children',
        },
        currentPage:1,
        pageSize:10,
        totalCount:0,
        attachCurrentPage:1,
        attachPageSize:10,
        attachTotal:0,
        attachCurrentPage_net:1,
        attachPageSize_net:10,
        attachTotal_net:0,
        coreFileList:[],
        hashFile:[],
        fileSelection:[],
        coreFileDialog:false,
        show_contact:false,
        attachIndex:'',
        imgSrc:'',
        transform_dialog:false,
        filterText:'',
        hashMail:[],
        insertMailbox:1,
        hashMail_copyer:[],
        hashMail_bcc:[],
        restaurants:[],
        state1:'',
        state_copyer:'',
        state_bcc:'',
        toolbarItems:
        ['source', '|','formatblock', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold',
        'italic', 'underline',  'lineheight', '|',  'justifyleft', 'justifycenter', 'justifyright',
        'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', '|','subscript',
        'superscript', 'link', 'unlink','image',  'table','hr','|', 'undo', 'redo', 'preview',
           'fullscreen',
         ],
        activeName: 'first',
        number_sign:false,
        safe_secret:true,

        contactList: [],
        defaultProps: {
          children: 'children',
          label: 'label',
          count:'count'
        },
        pickerBeginDateBefore: {
          disabledDate(time) {
            let beginDateVal = new Date();
            beginDateVal.setDate(beginDateVal.getDate()-1);
            if (beginDateVal) {
              return time.getTime() < beginDateVal;
            }
          }
        },

      };
    },
    methods:{
      createEditor(){
        let options = {
          items:this.toolbarItems,
          uploadJson:this.uploadJson,
          filterMode:false,
          resizeType:0,
          indentChar:"",
          loadStyleMode:false,
          autoHeightMode:false,
          afterCreate:this.afterChange
        }
       this.editoraaa = KindEditor.create('#'+this.editor_id,options);
      },
      afterChange:function(val){
        setTimeout(()=>{
          this.setEditorHeight();
        },10)

      },
      recall_single(row){
        this.$confirm('<p>确定召回此邮件吗？</p>', '召回邮件', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          dangerouslyUseHTMLString: true,
          type: 'warning'
        }).then(() => {
          let message_id = this.message_id;
          let param = {
            message_id: message_id,
            recipient: row.recipient
          }
          this.recallLoading = true;
          logRecall(param).then(res=>{
            this.getMessageStatus();
            this.recallLoading = false;
            this.recallData = res.data.results;
            this.recallTableVisible = true;
          }).catch(err=>{
            this.recallLoading = false;
            console.log(err)
            let str = '';
            if(err.detail){
              str = err.detail
            }
            this.$message({
              message: '邮件召回失败！'+str,
              type: 'error'
            })
          })


        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消召回'
          });
        });
      },
      htmlDecodeByRegExp:function (str){
        var s = "";
        if(str.length == 0) return "";
        s = str.replace(/&amp;/g,"&");
        s = s.replace(/&lt;/g,"<");
        s = s.replace(/&gt;/g,">");
        s = s.replace(/&nbsp;/g," ");
        s = s.replace(/&#39;/g,"\'");
        s = s.replace(/&quot;/g,"\"");
        return s;
      },
      remove_all_attach(){
        this.$confirm('<p>取消所有已添加的附件?</p>', '系统信息', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          dangerouslyUseHTMLString: true,
          type: 'warning'
        }).then(() => {
          this.fileList = [];
          this.hashFile = [];
        }).catch(() => {

        });

      },
      fileRemoved(file){

        for(let i=0;i<this.fileList_big.length;i++){
          if(file.id == this.fileList_big[i].fileId){
            this.fileList_big.splice(i,1)
            break;
          }
        }
      },
      changeReply(){
        if(this.show_replay_to && this.ruleForm2.reply_to){
          this.$confirm('<p>取消并清空指定回复人地址?</p>', '系统信息', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            dangerouslyUseHTMLString: true,
            type: 'warning'
          }).then(() => {
            this.ruleForm2.reply_to = '';
            this.show_replay_to = !this.show_replay_to
          }).catch(() => {

          });
        }else{
          this.show_replay_to = !this.show_replay_to
        }
      },
      editEmail(){
        this.$refs.dbForm.validate((valid) => {
          if (valid) {
            if(this.activeDb =='to'){
              this.hashMail[this.maillist[this.dbIndex].email] = false;
              this.maillist[this.dbIndex].fullname = this.dbForm.fullname;
              this.maillist[this.dbIndex].email = this.dbForm.email;
              this.maillist[this.dbIndex].status = true;
              this.hashMail[this.dbForm.email] = true;
            }else if(this.activeDb =='cc'){
              this.hashMail_copyer[this.maillist_copyer[this.dbIndex].email] = false;
              this.maillist_copyer[this.dbIndex].fullname = this.dbForm.fullname;
              this.maillist_copyer[this.dbIndex].email = this.dbForm.email;
              this.maillist_copyer[this.dbIndex].status = true;
              this.hashMail_copyer[this.dbForm.email] = true;
            }else if(this.activeDb =='bcc'){
              this.hashMail_bcc[this.maillist_bcc[this.dbIndex].email] = false;
              this.maillist_bcc[this.dbIndex].fullname = this.dbForm.fullname;
              this.maillist_bcc[this.dbIndex].email = this.dbForm.email;
              this.maillist_bcc[this.dbIndex].status = true;
              this.hashMail_bcc[this.dbForm.email] = true;
            }else if(this.activeDb == 'partsend'){
              if(this.partSendList[this.dbIndex].type == 'to'){
                this.hashMail[this.maillist[this.partSendList[this.dbIndex].k].email] = false;
                this.maillist[this.partSendList[this.dbIndex].k].fullname = this.dbForm.fullname;
                this.maillist[this.partSendList[this.dbIndex].k].email = this.dbForm.email;
                this.maillist[this.partSendList[this.dbIndex].k].status = true;
                this.hashMail[this.dbForm.email] = true;
              }else if(this.partSendList[this.dbIndex].type == 'cc'){
                this.hashMail_copyer[this.maillist_copyer[this.partSendList[this.dbIndex].k].email] = false;
                this.maillist_copyer[this.partSendList[this.dbIndex].k].fullname = this.dbForm.fullname;
                this.maillist_copyer[this.partSendList[this.dbIndex].k].email = this.dbForm.email;
                this.maillist_copyer[this.partSendList[this.dbIndex].k].status = true;
                this.hashMail_copyer[this.dbForm.email] = true;
              }else if(this.partSendList[this.dbIndex].type == 'bcc'){
                this.hashMail_bcc[this.maillist_bcc[this.partSendList[this.dbIndex].k].email] = false;
                this.maillist_bcc[this.partSendList[this.dbIndex].k].fullname = this.dbForm.fullname;
                this.maillist_bcc[this.partSendList[this.dbIndex].k].email = this.dbForm.email;
                this.maillist_bcc[this.partSendList[this.dbIndex].k].status = true;
                this.hashMail_bcc[this.dbForm.email] = true;
              }
            }

            this.dbFormVisible = false;
          }
        });
      },
      dbEdit(v,type,k){
        this.dbForm.email = v.email;
        this.dbForm.fullname = v.fullname;
        this.activeDb = type;
        this.dbIndex = k;
        this.dbFormVisible = true;
      },
      loadingContact(tab){
        console.log(tab)
        if(tab.name == 'first'){
          if(this.contactList.length==0){
            this.getRightContact();
          }
        }
      },
      getCapacity: function(){
        netdiskCapacityGet().then(res=>{
          this.folder_capacity = res.data;
        });
      },
      fileSuccess(rootFile, file, message, chunk){
        console.log('successsss')
        console.log(file)
        console.log(message)
        console.log(chunk.xhr.status)
        let md5 = file.uniqueIdentifier
        console.log(md5)

        let result = this.bigUploadSuccess(file.file,md5,file.id);
        console.log('progress:'+file.progress);
        console.log(result)
      },
      beforeUpload(file){
        console.log('before')
        console.log(file)
        console.log(this.bigList)
        let result = true;
        for(let i=0;i<this.bigList.length-1;i++){
          if(file.name == this.bigList[i].name){
            result = false;
          }
        }
        console.log(result)
        if(!result){
          return result;
        }
      },
      bigListSucess( file, fileList){
        this.bigList = fileList;

      },
      setSubject(val,type){
        if(this.ruleForm2.subject){
          return;
        }else{
          if(type && type=='template'){
            this.ruleForm2.subject = val
          }else{
            if(this.fileList.length>0){
              let str = this.fileList[0].filename || this.fileList[0].name;
              str = str.slice(0,str.lastIndexOf('.'));
              this.ruleForm2.subject = str;
            }
          }
        }
      },
      addBigAttach(){
        this.fileList_big.forEach(val=>{
          if(!this.hashFile[val.id]){
            this.fileList.push(val)
            this.hashFile[val.id] = true;
            this.setSubject();
          }
        })
        this.bigUploadVisible = false
      },
      bigClose(){
        // this.fileList_big = [];
        this.bigList = [];
        this.files = [];
      },
      showBigDialog(){
        this.bigUploadVisible = true;
        this.getCapacity();
      },
      handleRemove(file){
        // this.$message({
        //   type:'info',
        //   message:'已删除'
        // })
        for(let i=0;i<this.fileList_big.length;i++){
          if(file.name == this.fileList_big[i].name){
            this.fileList_big.splice(i,1);
            break;
          }
        }
      },
      submitUpload(){
         this.$refs.bigUpload.submit();
      },
      bigUploadSuccess(file,fileMd5,fileId){
        console.log(file)
        let param ={
          'fileMd5':fileMd5,
          'upload_type':'mail',
          'file_name':file.name,
          'file_type':file.type||'application/octet-stream',
          'file_size':file.size,
          'folder_id':-1,
        }
        uploadSuccess(param).then(res=>{
          // this.$message({
          //   type:'success',
          //   message:'上传成功！'
          // })
          // this.hashFile[res.data.id]=true;
          res.data.fileId = fileId;
          this.fileList_big.push(res.data)
          this.bigLoading = false;
          this.tip = ''
        }).catch(err=>{
          this.tip = '服务器错误！'
          if(err.non_field_errors){
            this.tip = err.non_field_errors[0]
          }
          this.$message({
            type:"error",
            message:' '+file.name+"上传失败！"+this.tip
          });
          console.log('merge错误！',err)
          this.bigLoading = false;
        })
      },
      chunksFile(file,fileMd5,fileparam,arr){
          let _this = this;

          let chunkLength=0;//文件分片后的长度

           this.uploadFileData.fileName=file.name;

          //获取分片后的长度
           if(file.size>1024*1024*2){
                  //每片长度2MB.
                 chunkLength=Math.ceil(file.size/(1024*1024*2));

            }else{
                chunkLength=1
           }
           //判断是不是最后一片，通知后台
           this.uploadFileData.chunk===chunkLength?this.uploadFileData.isLastChunk=true:false;
               //用formData通过ajax2上传文件内容


               //通过ajax上传分片文件内容


          let abcd = [];
          let hash = [];
          if(arr){
            for(let i=0;i<arr.length;i++){
              hash[(arr[i]-1)+'_n'] = true;
            }
          }
          for(let i=0;i<chunkLength;i++){
            if(!hash[i+'_n']){
              let fm = new FormData();
                 fm.append('fileMd5',fileMd5);//spark-md5计算出来的md5值
                 fm.append('chunkNumber',i+1);
                 fm.append('chunkFile',file.slice(i*1024 * 1024 * 2, (i+1)*1024 * 1024 * 2) );

                abcd.push(uploadChunk(fm))
            }
          }
          let timer = setInterval(()=>{
            if(fileparam.file.percent >= 100){
              clearInterval(timer)
            }
            uploadCheck({fileMd5:fileMd5}).then(res=>{
              if(res.data.state == 2){
                fileparam.file.percent = 100
                fileparam.onProgress(fileparam.file);
                clearInterval(timer)
              }else{
                fileparam.file.percent = (res.data.chunks.length/chunkLength)*100
                fileparam.onProgress(fileparam.file);
              }
            })
          },600)
          if(abcd.length>0){
            if(abcd.length>3){
              let splits = []
              for(let i=0;i<abcd.length;i+=3){
                let n = i*3+3;
                if(n > abcd.length-3){
                  n = abcd.length;
                }
                splits[i] = abcd.slice(i*3,n)
              }
              let i = splits.length-1;
              let count = 0;
              function digui(count,i){
                axios.all(splits[count]).then(axios.spread(function () {
                  // 请求现在都执行完成
                  if(count<i){
                    count++;
                    digui(count,i)
                    fileparam.file.percent += (3/chunkLength)*100
                    if(fileparam.file.percent >100 ){fileparam.file.percent = 100}
                    fileparam.onProgress(fileparam.file);
                  }else{
                    _this.bigUploadSuccess(file,fileMd5);
                    fileparam.file.percent = 100
                    fileparam.onProgress(fileparam.file);
                  }
                })).catch(err=>{
                  console.log('err:',err)
                })
              }
              // digui(count,i)

            }else{
              axios.all(abcd).then(axios.spread(function () {
                // 请求现在都执行完成
                _this.bigUploadSuccess(file,fileMd5);
                fileparam.file.percent = 100
                fileparam.onProgress(fileparam.file);
              })).catch(err=>{
                  console.log('err1:',err)
                })
            }
          }else{
             _this.bigUploadSuccess(file,fileMd5);
          }
      },
      progressTimer(fileparam){
        let timer = setInterval(()=>{
          if(fileparam.file.percent >= 100){
            clearInterval(timer)
          }
          fileparam.onProgress(fileparam.file);
          fileparam.file.percent += 2
        },100)
      },
      bigUpload(fileparam){
        // let file =  document.getElementById("file").files[0];
        console.time('timestart');
        let file =  fileparam.file;
        fileparam.file.percent = 0;
        fileparam.onProgress(fileparam.file);
        if(file){
          this.bigLoading = true;
          let _this = this;
          let spark_md5;
          this.calcMD56(file,(a)=>{

        console.timeEnd('timestart');
            // _this.bigUploadSuccess(file,a);
            // return;
            spark_md5 = a
            let param = {
              fileMd5:a
            }
            uploadCheck(param).then(res=>{
              let data = res.data;
              if(data.state==0){//判断之前是否上传成功此文件 0未上传
                  _this.chunksFile(file,a,fileparam);//上传文件
              }else if(data.state==1){
                  // _this.uploadFileData.chunk=parseInt(data.maxChuck)+1;//将查询到的结果赋值给表单中的分片
                  _this.chunksFile(file,a,fileparam,res.data.chunks);
              }else if(data.state==2){
                  _this.bigUploadSuccess(file,a);
                  fileparam.file.percent = 100
                  fileparam.onProgress(fileparam.file);
                  this.bigLoading = false;
              }
            }).catch(err=>{
              console.log('网络异常，请稍后再试！',err)
              this.bigLoading = false;
            })
          });
        }else{
          this.$message({
            type:'error',
            message:'请选择文件！'
          })
        }

      },
      calcMD56(file,callback){
          // this.upstate="MD5计算中...";
          // this.percent=0;
          let chunkSize=2097152,
          chunks=Math.ceil(file.size/chunkSize),
          currentChunk=0,
          spark=new SparkMD5.ArrayBuffer(),
          fileReader=new FileReader();
          fileReader.onload=(e)=>{
              //对于读取的文件计算hash码。
              spark.append(e.target.result);
              currentChunk++;
              // this.percent=((currentChunk/chunks)*100).toFixed(2)-0;
              if(currentChunk<chunks){
                  loadNext();
              }else{
                let str = spark.end();
                callback(str)
                return str;
              }
          }
          //分次读取大文件的内容，
          function loadNext(){
              let start=currentChunk*chunkSize,
                  end=((start+chunkSize)>=file.size)?file.size:start+chunkSize;
                  fileReader.readAsArrayBuffer(file.slice(start,end));
          }
          loadNext();
      },
      calcMD5 (){
        var fileReader = new FileReader(),
              // box=document.getElementById('box'),
              blobSlice = File.prototype.mozSlice || File.prototype.webkitSlice || File.prototype.slice,
              file = document.getElementById("file").files[0],
              chunkSize = 2097152,
              // read in chunks of 2MB
              chunks = Math.ceil(file.size / chunkSize),
              currentChunk = 0,
              spark = new SparkMD5();

          fileReader.onload = function(e) {
              spark.appendBinary(e.target.result); // append binary string
              currentChunk++;

              if (currentChunk < chunks) {
                  loadNext();
              }
              else {
                  let str = spark.end();
                  return str;
                  // box.innerHTML='MD5 hash:'+spark.end();
              }
          };

          function loadNext() {
              var start = currentChunk * chunkSize,
                  end = start + chunkSize >= file.size ? file.size : start + chunkSize;

              fileReader.readAsBinaryString(blobSlice.call(file, start, end));
          };

          loadNext();
      },
      filesAdded(files, fileList, event){
        console.log('adds')
        // netdiskCapacityGet().then(res=>{
        //   this.folder_capacity = res.data;
        //   let count = 0;
        //   for(let i=0;i<files.length;i++){
        //     count += files[i].size;
        //   }
        //   console.log(count)
        //   console.log(res.data.rtotal-res.data.rused)
        //
        //   if(count>(res.data.rtotal-res.data.rused)){
        //     this.$message({
        //       type:'error',
        //       message:'所选文件容量超出网盘剩余容量！'
        //     })
        //     files.forEach(val=>{
        //       val.cancel();
        //     })
        //     return false;
        //   }
        // });
      },
      fileAdded(file){
        console.log('add')
        if(file.size==0){
          file.cancel();
          return false;
        }
        netdiskCapacityGet().then(res=>{
          this.folder_capacity = res.data;
          if(res.data.rtotal!=0 && file.size>(res.data.rtotal-res.data.rused)){
            let fname = file.name;
            this.$message({
              type:'error',
              message:fname+'上传失败！上传文件已超过个人网盘剩余容量！'
            })
            file.cancel();
            return false;
          }else{
            this.loading2 = true;
            this.calcMD56(file.file,(a)=>{
              this.loading2 = false;
              file.uniqueIdentifier = a;
              file.resume();
            })
          }
        });


      },
      nodeExpand(data,node,vc){

      },
      nodeCollapse(data){

      },
      goEdit(){
        this.closeTab();
        let row = this.sendResult;
        let pp = this.$parent.$parent.$parent;
          readMail(row.uid,{"folder":row.folder}).then(res=>{
            let data = res.data
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
            }
            // pp.ruleForm2 = res.data;
            pp.maillist = []
            pp.maillist_copyer = [];
            pp.fileList = data.attachments;
            pp.ruleForm2.subject = data.subject;
            pp.ruleForm2.draft_id = data.attrs.draft_id;
            pp.ruleForm2.is_burn = data.attrs.is_burn;
            pp.ruleForm2.is_password = data.attrs.is_password;
            pp.ruleForm2.is_schedule = data.attrs.is_schedule;
            // pp.ruleForm2.password = data.attrs.password;
            pp.ruleForm2.schedule_day = data.attrs.schedule_day;
            pp.ruleForm2.is_html = data.is_html;
            if(data.is_html){
              pp.content = data.html_text ;
            }else{
              pp.content = data.plain_text;
            }
            // pp.ruleForm2.flags = data.flags;
            for(let i=0;i<data.to.length;i++){
              pp.maillist.push({fullname:data.to[i][1]||'',email:data.to[i][0],status:true})

            }
            if(data.cc){
              for(let i=0;i<data.cc.length;i++){
                pp.maillist_copyer.push({fullname:data.cc[i][1]||'',email:data.cc[i][0],status:true})
              }
            }

            pp.addTab('composedrafts',data.subject,row.uid,this.boxId)

          }).catch(err=>{
            console.log(err)
          })
      },
      closeTab(){
        let tagName = this.$parent.$parent.$parent.editableTabsValue2;
        this.$parent.$parent.$parent.removeTab(tagName);
      },
      search_member(){
        this.member_page = 1;
        this.getMemberList();
      },
      contact_page_change(val){
        this.member_page = val;
        this.getMemberList();
      },
      change_group(val){
        this.member_group_id = val;
        this.member_page = 1;
        this.getMemberList();
      },
      getMemberList(){
        if(this.member_group_id==0){
          let param = {
            "page":this.member_page,
            "page_size":10,
            "group_id":this.member_group_id,
            "is_group":0,
            "search":this.member_search
          }
          contactPabMembersGet(param).then(res=>{
          }).catch(err=>{
            console.log('获取所有联系人错误',err);
          })
        }else{
          let param = {
            "page": this.member_page,
            "page_size":10,
            "group_id": this.member_group_id,
            "is_group": 1,
            "search":this.member_search
          };
          contactPabMapsGet(param).then(res=>{
          }).catch(err=>{
            console.log('获取组成员错误',err);
          })
        }
      },
      setTemplate(){
        this.$router.push('/setting/template/')
      },
      deleteTemplate(){
        if(this.selectId){
          this.selectId = '';
          this.content = '';
          this.$refs[this.editor_id].editor.html(this.content);
        }
      },
      getTemplateListfn(){
        let param = {
          page:this.tpage,
          page_size:5
        }
        getTemplateList(param).then(res=>{
          this.templateList = this.templateList.concat(res.data.results);
          if(res.data.results.length<=5){
            this.tpage ++;
          }else if(res.data.results.length==0){
            this.showLoadMore = false;
          }else{
            this.tpage = 1;
          }
        }).catch(err=>{
          console.log('模板列表获取异常！',err)
          if(err.detail == '无效页面。'){
            this.$message({
              type:'info',
              message:'已加载全部模板信！'
            })
            this.showLoadMore = false;
          }
        })
      },

      selectTemplate(t){
        if(this.editoraaa.html()){
          this.$confirm('切换模板后, 已输入内容将清空,继续切换或者存草稿？', '系统信息', {
          distinguishCancelAndClose: true,
          confirmButtonText: '存草稿再切换',
          cancelButtonText: '直接切换'
        })
          .then(() => {
            this.sentMail('save_draft')
            this.selectId = t.id;

            getTemplateById(t.id).then(res=>{
              this.content = res.data.content;
              if(this.ruleForm2.is_html){
                this.editoraaa.html(this.content);
              }else{
                // $('#editor_id'+this.rid).html(this.content);
                this.editoraaa.html(this.content);
                this.no_html();
              }
              this.setSubject(t.caption,'template')

            }).catch(err=>{
              console.log('获取单个模板信错误！',err)
            })
          })
          .catch(action => {
          if(action === 'cancel'){
            this.selectId = t.id;
            getTemplateById(t.id).then(res=>{
              this.content = res.data.content;
              if(this.ruleForm2.is_html){
                this.editoraaa.html(this.content);
              }else{
                // $('#editor_id'+this.rid).html(this.content);
                this.editoraaa.html(this.content);
                this.no_html();
              }
              this.setSubject(t.caption,'template')

            }).catch(err=>{
              console.log('获取单个模板信错误！',err)
            })
          }else{
          }
        });
        }else{
          this.selectId = t.id;
            getTemplateById(t.id).then(res=>{
              this.content = res.data.content;
              if(this.ruleForm2.is_html){
                this.editoraaa.html(this.content);
              }else{
                // $('#editor_id'+this.rid).html(this.content);
                this.editoraaa.html(this.content);
                this.no_html();
              }
              this.setSubject(t.caption,'template')
            }).catch(err=>{
              console.log('获取单个模板信错误！',err)
            })
        }



      },
      cancelAddress(){
        this.transform_dialog = false
      },
      sureAddress(){
        this.hashMail = [];
        this.hashMail_copyer = [];
        this.hashMail_bcc = [];
        let arr = [].concat(this.toList)
        arr.forEach((mail)=>{
          if(mail.username){
            mail.email = mail.username;
            mail.fullname = mail.name;
            mail.status = true;
            this.hashMail[mail.username] = true;
          }else{
            this.hashMail[mail.email] = true;
          }
        })
        let arrcc = [].concat(this.ccList)
        arrcc.forEach((mail)=>{
          if(mail.username){
            mail.email = mail.username;
            mail.fullname = mail.name;
            mail.status = true;
            this.hashMail_copyer[mail.username] = true;
          }else{
            this.hashMail_copyer[mail.email] = true;
          }
        })
        let arrbcc = [].concat(this.bccList)
        arrbcc.forEach((mail)=>{
          if(mail.username){
            mail.email = mail.username;
            mail.fullname = mail.name;
            mail.status = true;
            this.hashMail_bcc[mail.username] = true;
          }else{
            this.hashMail_bcc[mail.email] = true;
          }
        })
        this.maillist = arr;
        this.maillist_copyer = arrcc;
        this.maillist_bcc = arrbcc;
        if(this.maillist_copyer.length>0){
          this.ruleForm2.is_cc = true;
        }
        if(this.maillist_bcc.length>0){
          this.ruleForm2.is_bcc = true;
        }
        this.transform_dialog = false
      },

      checkBgFn(m){
        if(this.ruleForm2.is_html){
          let html = this.editoraaa.html();
          if($(html).find('#stationery').length>0){
            html = $(html).find('#stationery').html();
          }
          if(m == 'noBg'){
            this.checkBg = '';
            this.editoraaa.html(html)
          }else{
            this.checkBg = m.id;
            let newHtml = `<table style="width:99.8%;"><tr><td id="stationery"  style="background:${m.background};min-height: 550px;padding: 100px 55px 200px;">${html}</td></tr></table>`
            this.editoraaa.html(newHtml)
          }
        }else{
          this.$message({
            type:'error',
            message:'使用信纸请切换到多媒体文本编辑！'
          })
        }
        

      },
      checkSignatrue(sign){
        if(sign == 'removeSign'){
          $("#compose"+this.rid +' .ke-edit-iframe').contents().find('#sign').html('')
          this.signCheck = ''
        }else if(sign == 'editSign'){
          this.$router.push('/setting/signature')
        }else{
          if(sign)this.signCheck = sign.id;
          singleSignatures(sign.id).then(res=>{
            let sign_content = res.data.content;
            sign_content = this.htmlDecodeByRegExp(sign_content)
            if(this.ruleForm2.is_html){
              // let html = this.$refs[this.editor_id].editor.html();
              let html = $('#'+this.editor_id).val();
              let hasSign = $("#compose"+this.rid +' .ke-edit-iframe').contents().find('#sign').length>0;
              let hasBg = $(html).find('#stationery').length>0;

              if(hasSign){
                $("#compose"+this.rid +' .ke-edit-iframe').contents().find('#sign').html('<br><br>'+sign_content)
              }else if(hasBg && !hasSign){
                let ht = $("#compose"+this.rid +' .ke-edit-iframe').contents().find('#stationery').html();
                $("#compose"+this.rid +' .ke-edit-iframe').contents().find('#stationery').html(ht+'<p><br><br></p><div id="sign"><br><br>'+sign_content+'</div><br>')
              }else{
                // this.$refs[this.editor_id].editor.appendHtml('<p><br><br></p><div id="sign">'+'<br><br>'+sign_content+'</div><br>')
                this.editoraaa.appendHtml('<p><br><br></p><div id="sign">'+'<br><br>'+sign_content+'</div><br>')
              }
            }else{
              // 纯文本签名
              // let html = this.$refs[this.editor_id].editor.html();
              let html = $('#'+this.editor_id).val();
              // this.$refs[this.editor_id].editor.html('<p>'+html+'</p>')
              this.editoraaa.html('<p>'+html+'</p>')
              // this.$refs[this.editor_id].editor.appendHtml('<p><br><br></p><div id="sign">'+'<br><br>'+sign_content+'</div>')
              this.editoraaa.appendHtml('<p><br><br></p><div id="sign">'+'<br><br>'+sign_content+'</div>')
              // this.content = this.htmlToText(this.$refs[this.editor_id].editor.text());
              this.content = this.htmlToText(this.editoraaa.text());
              this.editoraaa.text(this.content);
              // this.$refs[this.editor_id].editor.text(this.content);
              // $('#editor_id'+this.rid).val(html)

            }

          }).catch(err=>{
            console.log(err)
          })
        }

      },
      getSignatrue(){
        settingSignatureGet().then(res=>{
          this.signatureList = res.data.results;
          if(this.type == 'compose' ||this.type == 'compose_to_list' || this.type == 'compose_net_atta'){
            let sign_content = res.data.defaults.default_content;
            sign_content = this.htmlDecodeByRegExp(sign_content)
            if(this.ruleForm2.is_html){
              this.signCheck = res.data.defaults.default;
              // let html = this.$refs[this.editor_id].editor.html();
              let html = $('#'+this.editor_id).val();
              // this.$refs[this.editor_id].editor.html('<p><br><br></p><div id="sign">'+'<br><br>'+ sign_content +'</div><br>' + html)
              this.editoraaa.html('<p><br><br></p><div id="sign">'+'<br><br>'+ sign_content +'</div><br>' + html)
            }
          }else if(this.type == 'compose3 '||this.type == 'compose4 '|| this.type == 'compose5 '||this.type == 'compose6 '||this.type == 'compose_net_atta_event'){
            let sign_content = res.data.defaults.refw_default_content;
            sign_content = this.htmlDecodeByRegExp(sign_content)
            if(this.ruleForm2.is_html){
              this.signCheck = res.data.defaults.refw_default;
              // let html = this.$refs[this.editor_id].editor.html();
              let html = $('#'+this.editor_id).val();
              // this.$refs[this.editor_id].editor.html('<p><br><br></p><div id="sign">'+'<br><br>'+ sign_content +'</div><br>' + html)
              this.editoraaa.html('<p><br><br></p><div id="sign">'+'<br><br>'+ sign_content +'</div><br>' + html)
            }
          }
        });
      },
      change_show_result(){
        if(!this.show_result && this.mail_results.length<1){
          this.getMessageStatus();
        }
        this.show_result = !this.show_result;
      },
      autoSave(){
        this.$router.push('/setting/param')
      },
      editorfocus(){
        this.setEditorHeight();
      },
      htmlToText(html){
        // return html.replace(/<(style|script|iframe)[^>]*?>[\s\S]+?<\/\1\s*>/gi,'').replace(/<[^>]+?>/g,'').replace(/\s+/g,' ').replace(/ /g,' ').replace(/>/g,' ')
        // var htmlTagReg = /<(\/)?[^>].*?>/g;
        // var htmlTagReg = /<(?!\/?br\/?.+?>|\/?img.+?>)[^<>]*>/g;
        var htmlTagReg = /<(?!\/?br\/?.+?>)[^<>]*>/g;
        var p = /<p(([\s\S])*?)<\/p>/g;
        var dd=html.replace(/<\/?.+?>/g,"");


        // html = html.replace(/<p>([\s\S]*?)<\/p>/ig, '$1<br/>')
        // html = html.replace(/<div>([\s\S]*?)<\/div>/ig, '$1<br/>')
        // html = html.replace(/<h1>([\s\S]*?)<\/h1>/ig, '$1<br/>')
        // html = html.replace(/<h2>([\s\S]*?)<\/h2>/ig, '$1<br/>')
        // html = html.replace(/<h3>([\s\S]*?)<\/h3>/ig, '$1<br/>')
        // html = html.replace(/<h4>([\s\S]*?)<\/h4>/ig, '$1<br/>')
        // html = html.replace(/<h5>([\s\S]*?)<\/h5>/ig, '$1<br/>')
        // html = html.replace(/<h6>([\s\S]*?)<\/h6>/ig, '$1<br/>')
        // html = html.replace(/<ul>([\s\S]*?)<\/ul>/ig, '$1<br/>')
        // html = html.replace(/<li>([\s\S]*?)<\/li>/ig, '$1<br/>')

        // return html.replace(htmlTagReg,'');
        return dd.replace(/ /g,"");

      },
      no_html(){
        // let text = this.htmlToText(this.content)
        // this.content = text;
        // $('#compose'+this.rid+' .ke-outline').addClass('ke-disabled')
        // $('#compose'+this.rid+' .ke-outline').css({'opacity':0.5})

        // $('#compose'+this.rid+' .ke-outline[data-name="preview"]').removeClass('ke-disabled')
        // $('#compose'+this.rid+' .ke-outline[data-name="fullscreen"]').css({'opacity':1})


        // $('#compose'+this.rid+' .ke-toolbar').hide()
        this.signCheck = '';
        // this.content = this.htmlToText(this.editoraaa.text());
        this.content = this.htmlToText(this.editoraaa.text());
        console.log(this.editoraaa)
        console.log(this.editoraaa.html())
        $('#'+this.editor_id).val(this.content);
        $('#compose'+this.rid+' .ke-container.ke-container-default').hide()
        $('#editor_id'+this.rid).show()
        this.ruleForm2.is_html = false;
      },
      changeIsHtml(){
        if(this.ruleForm2.is_html){
          if(this.editoraaa.html()){
            this.$confirm('切换到纯文本编辑方式将丢失当前文本的格式，确定？', '系统信息', {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              dangerouslyUseHTMLString: true,
              type: 'warning'
            }).then(() => {
              this.no_html();
            }).catch(() => {

            });
          }else{
            this.no_html();
          }

        }else{
          if(!$('#compose'+this.rid+' .ke-outline[data-name="source"]').hasClass('ke-selected')){
            // $('#compose'+this.rid+' .ke-outline').removeClass('ke-disabled')
            // $('#compose'+this.rid+' .ke-outline').css({'opacity':1})
          }
          // $('#compose'+this.rid+' .ke-toolbar').show()
          this.content = '<p>'+$('#editor_id'+this.rid).val()+'</p>';
          this.editoraaa.html(this.content);
          $('#compose'+this.rid+' .ke-container.ke-container-default').show()
          $('#editor_id'+this.rid).hide()

          this.ruleForm2.is_html = !this.ruleForm2.is_html;

        }
        this.setEditorHeight();


      },
      set_main_min_height(){
        this.main_min_height = $('#compose'+this.rid+' .title_height').outerHeight()+$('#compose'+this.rid+' .compose_editor').outerHeight()+
          $('#compose'+this.rid+' .footer_height').outerHeight()
      },
      changeCc(){
        if(this.ruleForm2.is_cc && this.maillist_copyer.length>0){
          this.$confirm('<p>要删除已经存在的所有抄送地址?</p>', '系统信息', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            dangerouslyUseHTMLString: true,
            type: 'warning'
          }).then(() => {
            if(this.insertMailbox == 2){
              this.insertMailbox = 1;
            }
            this.maillist_copyer = [];
            this.hashMail_copyer = [];
            this.ruleForm2.is_cc = !this.ruleForm2.is_cc
          }).catch(() => {

          });
        }else{
          this.ruleForm2.is_cc = !this.ruleForm2.is_cc
        }


      },
      changeBcc(){
        if(this.ruleForm2.is_bcc && this.maillist_bcc.length>0){
          this.$confirm('<p>要删除已经存在的所有密送地址?</p>', '系统信息', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            dangerouslyUseHTMLString: true,
            type: 'warning'
          }).then(() => {
            if(this.insertMailbox == 3){
              this.insertMailbox = 1;
            }
            this.maillist_bcc = [];
            this.hashMail_bcc = [];
            this.ruleForm2.is_bcc = !this.ruleForm2.is_bcc
          }).catch(() => {

          });
        }else{
          this.ruleForm2.is_bcc = !this.ruleForm2.is_bcc
        }


      },
      backToBox(compose){
        this.$parent.$parent.$parent.removeTab(this.$parent.$parent.$parent.editableTabsValue2);
        if(compose){
          this.$parent.$parent.$parent.addTab('compose','写信')
        }else{
          this.$parent.$parent.$parent.editableTabsValue2 = '1';
        }
      },
      recall(){
        if(this.isRecall){
          this.recallTableVisible = true;
        }else {
          this.$confirm('<p>确定召回此邮件吗？</p>确定召回，系统将邮件通知您召回结果。', '召回邮件', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            dangerouslyUseHTMLString: true,
            type: 'warning'
          }).then(() => {
            let param = {
              message_id: this.message_id,
              // recipient: this.recipient
            }
            this.recallLoading = true;
            sendRecall(param).then(res => {
              this.getMessageStatus();
              this.recallLoading = false;
              if(res.data.results[0].recall_status=='recall_succ'){this.isRecall = true;}
              this.recallData = res.data.results;
              this.recallTableVisible = true;


            }, err => {
              console.log(err)
              this.recallLoading = false;
              let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message({
                message: '邮件召回失败！'+str,
                type: 'error'
              })
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消召回'
            });
          });
        }
      },
      getMessageStatus(){
        let param = {
          message_id: this.message_id,
          // recipient: this.recipient
        }
        getMessageStatus(param).then(res=>{
          this.mail_results = res.data.results;
          this.mail_results.forEach(val1=>{
            this.error_list.forEach(val2=>{
              if(val1.email == val2.email){
                val1.error_message = val2.error_message;
              }
            })
          })
        },err=>{
          console.log(err);
        })
      },
      changeBottom(a){
        let _this = this
        setTimeout(_this.setEditorHeight,50)
        setTimeout(_this.set_main_min_height,50)
        if(a=='sch' && !this.ruleForm2.schedule_day){
          let now = new Date();
          now.setHours(now.getHours()+1)
          this.ruleForm2.schedule_day = now.Format('yyyy-MM-dd hh:mm');
        }else if(a=='burn' && !this.ruleForm2.burn_day){
          let now= new Date();
          now.setDate(now.getDate()+3);
          this.ruleForm2.burn_day = now.Format('yyyy-MM-dd');
        }
      },
      setEditorHeight(){
        this.editor_height = $('#compose'+this.rid+'.mltabview-content').height()-$('#compose'+this.rid+' .title_height').outerHeight()-$('#compose'+this.rid+' .footer_height').outerHeight()-50;
        let th = this.editor_height - $('#compose'+this.rid+' .ke-toolbar').outerHeight()-30;
        if(th>0){
          $('#compose'+this.rid+' .ke-edit').css({'height': th+'px','minHeight':'200px'})
          $('#compose'+this.rid+' .ke-edit-iframe').css({'height': th+'px','minHeight':'200px'})
          $('#editor_id'+this.rid).css({'height': this.editor_height-20+'px','minHeight':'260px'})
        }
      },
      deleteList(a,id,k){
        if(a=='to'){
          this.hashTo[id] = false;
          this.toList.splice(k,1)
          if(this.active_box == 'to'){
            this.bang(this.toList)
          }
        }else if(a == 'cc'){
          this.hashCc[id] = false;
          this.ccList.splice(k,1)
          if(this.active_box == 'cc'){
            this.bang(this.ccList)
          }
        }else if(a == 'bcc'){
          this.hashBcc[id] = false;
          this.bccList.splice(k,1)
          if(this.active_box == 'bcc'){
            this.bang(this.ccList)
          }
        }
      },
      getParams(){
        getParamBool().then(res=>{
          this.ruleForm2.is_save_sent = res.data.results.is_save_sent;
          this.ruleForm2.is_confirm_read = res.data.results.is_confirm_read;
          this.is_save_contact = res.data.results.is_save_contact;
          this.timer();
        },err=>{
          console.log(err)
        })
      },
      timer(){
        if(this.compose_type=='compose'&&this.is_save_contact){
          if(this.$store.getters.getTimer){clearInterval(this.$store.getters.getTimer)}
          let _this = this;
          this.$store.dispatch('setTimer',
            setInterval(()=>{
              _this.sentMail('save_draft')
            },5*60*1000)
          )
        }
      },
      switch_to(a,arr){
        this.active_box=a;
        this.bang(arr);
      },
      select_change(selection){
        this.contactSelection = selection;
      },
      selectionChange_contact(v,row){
        if(this.active_box=='to'){
          if(!row){
            let rows = this.contactData;
            if(v.length>0){
              for(let key in rows){
                if(!this.hashTo[rows[key].username]){
                  this.hashTo[rows[key].username] = true;
                  this.toList.push(rows[key]);
                }
              }
            }else{
              for(let i=0;i<rows.length;i++){
                if(this.hashTo[rows[i].username]){
                  this.hashTo[rows[i].username] = false;
                  for(let j=0;j<this.toList.length;j++){
                    if(this.toList[j].username == rows[i].username){
                      this.toList.splice(j,1);
                      break;
                    }
                  }
                }
              }
            }
          }else{
            if(this.hashTo[row.username]){
              this.hashTo[row.username] = false;
              for(let i=0;i<this.toList.length;i++){
                if(row.username == this.toList[i].username){
                  this.toList.splice(i,1);
                  break;
                }
              }
            }else{
              this.hashTo[row.username] = true;
              this.toList.push(row);
            }
          }

        }else if(this.active_box == 'cc'){
          if(!row){
            let rows = this.contactData;
            if(v.length>0){
              for(let key in rows){
                if(!this.hashCc[rows[key].username]){
                  this.hashCc[rows[key].username] = true;
                  this.ccList.push(rows[key]);
                }
              }
            }else{
              for(let i=0;i<rows.length;i++){
                if(this.hashCc[rows[i].username]){
                  this.hashCc[rows[i].username] = false;
                  for(let j=0;j<this.ccList.length;j++){
                    if(this.ccList[j].username == rows[i].username){
                      this.ccList.splice(j,1);
                      break;
                    }
                  }
                }
              }
            }
          }else{
            if(this.hashCc[row.username]){
              this.hashCc[row.username] = false;
              for(let i=0;i<this.ccList.length;i++){
                if(row.username == this.ccList[i].username){
                  this.ccList.splice(i,1);
                  break;
                }
              }
            }else{
              this.hashCc[row.username] = true;
              this.ccList.push(row);
            }
          }
        }else if(this.active_box == 'bcc'){
          if(!row){
            let rows = this.contactData;
            if(v.length>0){
              for(let key in rows){
                if(!this.hashBcc[rows[key].username]){
                  this.hashBcc[rows[key].username] = true;
                  this.bccList.push(rows[key]);
                }
              }
            }else{
              for(let i=0;i<rows.length;i++){
                if(this.hashBcc[rows[i].username]){
                  this.hashBcc[rows[i].username] = false;
                  for(let j=0;j<this.bccList.length;j++){
                    if(this.bccList[j].username == rows[i].username){
                      this.bccList.splice(j,1);
                      break;
                    }
                  }
                }
              }
            }
          }else{
            if(this.hashBcc[row.username]){
              this.hashBcc[row.username] = false;
              for(let i=0;i<this.bccList.length;i++){
                if(row.username == this.bccList[i].username){
                  this.bccList.splice(i,1);
                  break;
                }
              }
            }else{
              this.hashBcc[row.username] = true;
              this.bccList.push(row);
            }
          }
        }
      },
      bang(arr){
        if(this.$refs.contactTable)this.$refs.contactTable.clearSelection()
        for(let i=0;i<arr.length;i++){
          for(let k=0;k<this.contactData.length;k++){
            if(arr[i].username == this.contactData[k].username){
              this.$refs.contactTable.toggleRowSelection(this.contactData[k],true);
              break;
            }
          }
        }
      },
      show_contact_fn(a){
        if(this.transform_menu.length==0){
          this.get_transform_menu();
        }
        this.active_box = a
        this.transform_dialog = true;
        this.toList = [].concat(this.maillist)
        this.ccList = [].concat(this.maillist_copyer);
        this.bccList = [].concat(this.maillist_bcc);
        this.hashTo = [];
        this.hashCc = [];
        this.hashBcc = [];
        this.toList.forEach((val)=>{
          val.username = val.email;
          this.hashTo[val.username] = true;
        })
        this.ccList.forEach(val => {
          val.username = val.email;
          this.hashCc[val.username] = true;
        });
        this.bccList.forEach(val => {
          val.username = val.email;
          this.hashBcc[val.username] = true;
        });
        if(this.active_box == 'to'){
          this.bang(this.toList);
        }else if(this.active_box == 'cc'){
          this.bang(this.ccList);
        }else if(this.active_box == 'bcc'){
          this.bang(this.bccList);
        }
      },
      getPabMembers() {
        var param = {
          "page": this.currentPage,
          "page_size": this.pageSize,
          "search": this.contact_search,
          "group_id": this.pid,
          "is_group": '',
        };
        if (this.pid >0){
          contactPabMapsGet(param).then((res) => {
            this.totalCount = res.data.count;
            this.contactData = res.data.results;
            this.contactData.forEach(val=>{
              val.username = val.email
              val.name = val.fullname
            })
            setTimeout(() => {
              this.bang(this.allSeclect)
            }, 50)
          });
        } else {
          contactPabMembersGet(param).then((res) => {
            this.totalCount = res.data.count;
            this.contactData = res.data.results;
            this.contactData.forEach(val=>{
              val.username = val.email
              val.name = val.fullname
            })
            setTimeout(() => {
              this.bang(this.allSeclect)
            }, 50)
          });
        }

      },
      getOabMembers() {
        let keys = new Array();
        // keys.push(Number(this.oab_cid));
        // this.default_expanded_keys = keys;
        // this.default_checked_keys = keys;

        var param = {
          "page": this.currentPage,
          "page_size": this.pageSize,
          "search": this.contact_search,
          "dept_id": this.pid,
        };
        contactOabMembersGet(param).then((res) => {
          this.totalCount = res.data.count;
          this.contactData = res.data.results;
          if(this.currentPage == 1){
            this.contactData = this.oabchildren.concat(this.contactData)
          }
          setTimeout(() => {
            this.bang(this.allSeclect)
          }, 50)
        });
      },
      getCabMembers() {
        var param = {
          "page": this.currentPage,
          "page_size": this.pageSize,
          "search": this.contact_search,
          "cate_id": this.pid,
        };
        contactCabMembersGet(param).then((res) => {
          this.totalCount = res.data.count;
          this.contactData = res.data.results;
          this.contactData.forEach(val=>{
            val.username = val.pref_email
            val.name = val.fullname
          })
          setTimeout(() => {
              this.bang(this.allSeclect)
            }, 50)
        }).catch(err=>{
          console.log(err)
        });
      },
      getSoabMembers() {
        var param = {
          "page": this.currentPage,
          "page_size": this.pageSize,
          "search": this.contact_search,
          "dept_id": this.pid,
          "domain_id": this.soab_domain_cid,
        };
        contactSoabMembersGet(param).then((res) => {
          this.totalCount = res.data.count;
          this.contactData = res.data.results;
          setTimeout(() => {
            this.bang(this.allSeclect)
          }, 50)
        }).catch(err=>{
          console.log(err)
        });
      },
      soabChangeDomain(selected){
        this.soab_domain_cid = selected;
        this.get_transform_menu();
      },
      getSoabDomains(){
        contactSoabDomainsGet().then(res=>{
          let data = res.data.results;
          if ( data.length>=1 ){
            this.soab_domain_options = data;
            this.soab_domain_cid = data[0].id
          }
        });
      },
      getLabs(){
        this.expand_soab = false;
        sessionStorage['openGroup'] = 'lab'
        let param = {
            page:this.currentPage,
            page_size:this.pageSize,
            "search": this.contact_search
          }
          getContactLab(param).then(res=>{
            this.totalCount = res.data.count;
            this.contactData = res.data.results;
            this.contactData.forEach(val=>{
              val.username = val.address
              val.name = val.listname
              if(val.listtype && val.listtype == 'dept'){
                val.is_dept = true;
              }
            })
            setTimeout(() => {
              this.bang(this.allSeclect)
            }, 50)
          }).catch(err=>{
            console.log('获取邮件列表异常！'+err)
          })
      },
      contact_tree_click(data,node,vc){
        let _this = this;
        if(data.keyId.indexOf('oab')==0){
          sessionStorage['curKey'] = 'oab';
        }else if(data.keyId.indexOf('pab')==0){
          sessionStorage['curKey'] = 'pab';
        }else if(data.keyId.indexOf('cab')==0){
          sessionStorage['curKey'] = 'cab';
        }else if(data.keyId.indexOf('soab')==0){
          sessionStorage['curKey'] = 'soab';
        }else if(data.keyId.indexOf('lab')==0){
          sessionStorage['curKey'] = 'lab';
        }
        console.log(sessionStorage['curKey'])
        sessionStorage['openGroup'] = sessionStorage['curKey'];
        if(sessionStorage['curKey'] == 'soab'){
          this.expand_soab = true
        }else{
          this.expand_soab = false
        }
        if(data.id=='lab'){
          sessionStorage['openGroup'] = data.id;
          this.currentPage = 1;
          this.get_transform_menu();
          this.getLabs();
          return;
        }
        if(data.id=='oab'||data.id=='pab'||data.id=='cab'||data.id=='soab'){
          // sessionStorage['openGroup'] = data.id;
          return;
        }
        this.pid = data.id;
        this.$refs.contactTreeRef.setCurrentNode(data);
        this.currentPage = 1;
        if(sessionStorage['openGroup'] == 'pab'){
          this.getPabMembers();
        }else if(sessionStorage['openGroup']=='oab'){
          let str = this.$store.getters.userInfo.name;
          let index = str.lastIndexOf('@');
          let domain = str.slice(index+1)
          this.oabchildren = [];
          if(data.id==0||data.id=='-1'){
            data.username = 'everyone@'+domain;
          }else{
            data.username = 'dept_'+data.id+'@'+domain;
          }
          data.name = data.label;
          data.is_dept = true;
          this.oabchildren.push(data)
          if(data.children.length>0){
            let paramArr = [];
            for(let i=0;i<data.children.length;i++){
              data.children[i].username = 'dept_'+data.children[i].id+'@'+domain;
              data.children[i].name = data.children[i].label;
              data.children[i].is_dept = true;
              paramArr.push(data.children[i]);
            }
            _this.oabchildren = _this.oabchildren.concat(paramArr);
            _this.getOabMembers();
          }else{
            this.getOabMembers();
          }

        }else if(sessionStorage['openGroup']=='cab'){
          console.log('cab')
          this.getCabMembers();
        }else if(sessionStorage['openGroup']=='soab'){
          console.log('soab')
          this.getSoabMembers();
        }
        return;
        if(sessionStorage['openGroup']=='pab'){
          this.getPabMembers();
        }else if(sessionStorage['openGroup']=='oab'){
          this.getOabMembers();
        }else if(sessionStorage['openGroup']=='cab'){
          this.getCabMembers();
        }else if(sessionStorage['openGroup']=='soab'){
          this.getSoabMembers();
        }

      },
      selectablee(row,index){
        if(row.nettype=='folder'){
          return false
        }else{
          return true;
        }
      },
      rowClick(row){
        this.$refs.contactTable.toggleRowSelection(row)
        this.selectionChange_contact(this.contactSelection,row);
      },
      rowClick_afile(row,e,col){
        this.$refs.afileTable.toggleRowSelection(row)
      },
      rowClick_nfile(row,e,col){
        if(row.nettype=='folder'){
          return
        }
        this.$refs.nfileTable.toggleRowSelection(row)
      },
      rowClick_nfile_company(row){
        if(row.nettype=='folder'){
          return
        }
        this.$refs.nfileTable_company.toggleRowSelection(row)
      },
      switch_file(tab,event){
        if(tab.name == 'second'){
          this.getNetfile(-1);
        }else if(tab.name == 'first'){
          this.getAttachList();
        }else if(tab.name == 'third'){
          this.getNetfile_company(-1)
        }
      },
      format (fromArr,toArr){
        for(let i=0;i<fromArr.length;i++){
          toArr.push([fromArr[i].email,fromArr[i].fullname||""]);
        }
      },
      getNetfile(n){
        var param = {
          "page": this.attachCurrentPage_net,
          "page_size": this.attachPageSize_net,
          "folder_id": n,
        };
        netdiskGet(param).then(res=>{
          this.attachTotal_net = res.data.count;
          this.nfileList = res.data.results;
          this.folder_names = res.data.folder_names;
        });
      },
      getNetfile_company(n){
        var param = {
          "page": this.attachCurrentPage_company,
          "page_size": this.attachPageSize_company,
          "folder_id": n,
        };
        companyDiskGet(param).then(res=>{
          this.attachTotal_company = res.data.count;
          this.nfileList_company = res.data.results;
          this.nfileList_company.forEach(val=>{
            val.is_company = true;
          })
          this.folder_names_company = res.data.folder_names;
        });
      },
      sentMail(type){
        this.ruleForm2.to = [];
        this.ruleForm2.cc = [];
        this.ruleForm2.bcc = [];
        this.ruleForm2.attachments = [];
        this.ruleForm2.net_attachments = [];
        this.ruleForm2.company_attachments = [];
        if(this.ruleForm2.is_partsend){
          this.format(this.partSendList,this.ruleForm2.to)
        }else{
          this.format(this.maillist,this.ruleForm2.to)
          this.format(this.maillist_copyer,this.ruleForm2.cc)
          this.format(this.maillist_bcc,this.ruleForm2.bcc)
        }
        if(type=='sent'&&this.ruleForm2.to.length<=0){
          this.$alert('请输入收件人！');
          return;
        }
        if(type=='sent' && !this.ruleForm2.subject){
          this.$alert('请填写邮件主题！');
          return;
        }
        if(type=='sent' && !this.ruleForm2.subject&& this.fileList.length>0){
          let str = this.fileList[0].filename || this.fileList[0].name;
          str = str.slice(0,str.lastIndexOf('.'));
          this.ruleForm2.subject = str;
        }
        let a = this.editoraaa.html();
        if(type=='sent' && !a){
          this.$alert('请填写邮件内容！');
          return;
        }
        if(type=='sent'&& this.ruleForm2.is_password){
          let reg = /^[0-9a-zA-Z]{6}$/;
          if(!reg.test(this.ruleForm2.password)){
            this.$alert('密码格式不正确！请重新填写');
            return;
          }
        }
        if(type=='sent'&& this.ruleForm2.reply_to && !emailReg.test(this.ruleForm2.reply_to)){
          this.$alert('指定回复人格式不正确！请重新填写！（不填则回复给发件人）');
          return;
        }
        if(this.ruleForm2.is_html){
          this.ruleForm2.html_text = a;
          this.ruleForm2.plain_text = '';
        }else{
          this.ruleForm2.html_text = '';
          this.ruleForm2.plain_text = a;
        }

        for(let i=0;i<this.fileList.length;i++){
          if(this.fileList[i].filename){
            this.ruleForm2.attachments.push(this.fileList[i].id)
          }else{
            if(this.fileList[i].is_company){
              this.ruleForm2.company_attachments.push(this.fileList[i].id)
            }else{
              this.ruleForm2.net_attachments.push(this.fileList[i].id)
            }
          }
        }
        let param = this.ruleForm2;
        param.action=type;// save_draft
        if(type!='sent'&&!a){
          return;
        }
        this.sendLoading = true;
        mailSent(param).then(res=>{
          this.sendLoading = false;
          if(this.$store.getters.getTimer){clearInterval(this.$store.getters.getTimer)}
          let info = type=='sent'?"发送成功！":"保存草稿成功！";
          this.$message({
             message:info,
             type:'success'
          })
          this.message_id = res.data.message_id;
          this.recipient = res.data.recipient;
          this.sendResult = res.data;
          this.$parent.$parent.$parent.getFloderfn()
          if( type != 'sent'){
            this.$parent.$parent.$children[1].$children[0].getMessageList()
          }
          if(res.data.draft_id){
            this.ruleForm2.draft_id = res.data.draft_id
          }
          if(res.data.success && res.data.success){
            this.send_suc = true;
            if(res.data.error_lists){
              this.error_list = res.data.error_lists
            }else{
              this.error_list = [];
            }

            this.getMessageStatus();
          }
        },err=>{
          this.sendLoading = false;
          let str = '';
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          if(err.error_message){
            str = err.error_message;
          }
          if(err.detail){
            str = err.detail
          }
          this.$message({
             message:"操作失败！"+str,
             type:'error'
          })
        }).catch(err=>{
          this.sendLoading = false;
          let str = '';
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          if(err.error_message){
            str = err.error_message;
          }
          if(err.detail){
            str = err.detail
          }
          this.$message({
             message:"操作失败！"+str,
             type:'error'
          })
        })
      },
      get_transform_menu(){
        let arr = [];
        let _this = this;
        let abcd = [];
        abcd.push(contactPabGroupsGet())
        abcd.push(contactOabDepartsGet())
        if(this.webmail_cab_show){
          abcd.push(contactCabGroupsGet())
        }
        if(this.webmail_soab_show){
          abcd.push(contactSoabGroupsGet(this.soab_domain_cid))
        }
        function keyId(arr,a){
          arr.forEach(val=>{
            val.keyId = a + val.id;
            if(val.children && val.children.length>0){
              keyId(val.children,a)
            }
          })
        }
        axios.all(abcd).then(axios.spread(function () {
          // 请求现在都执行完成
          arguments[0].data.results.forEach(val=>{
            val.label = val.groupname
            val.keyId = 'pab'+val.id
          })
          arr.push({
            id:'pab',
            label:'个人通讯录',
            keyId:'pab',
            children:arguments[0].data.results
          })

          keyId(arguments[1].data.results,'oab')
          arr.push({
            id:'oab',
            keyId:'oab',
            label:'组织通讯录',
            children:arguments[1].data.results
          })
          if(_this.webmail_cab_show){
            keyId(arguments[2].data.results,'cab')
            arr.push({
              id:'cab',
              keyId:'cab',
              label:'公共通讯录',
              children:arguments[2].data.results
            })
          }
          if(_this.webmail_soab_show){
            keyId(arguments[arguments.length-1].data.results,'soab')
            arr.push({
              id:'soab',
              keyId:'soab',
              label:'其他域通讯录',
              children:arguments[arguments.length-1].data.results
            })
          }
          arr.push({
            id:'lab',
            keyId:'lab',
            label:'邮件列表',
            children:[]
          })
          _this.transform_menu = arr;
          console.log(_this.transform_menu)
          _this.$nextTick(()=>{
            if(sessionStorage['curKey']){
              _this.default_expanded = [];
              _this.default_expanded.push(sessionStorage['curKey'])
              _this.default_expanded.push(sessionStorage['curKey']+'0')
              _this.$refs.contactTreeRef.setCurrentKey(sessionStorage['curKey']+'0');
            }else{
              _this.default_expanded = [];
              _this.default_expanded.push('pab')
              _this.default_expanded.push('pab0')
              _this.$refs.contactTreeRef.setCurrentKey('pab0');
            }
            // _this.$refs.contactTreeRef.setCurrentNode(arr[arr.length-1]);
            _this.currentPage = 1;
            // _this.getLabs();
            _this.pid = 0;
            if(sessionStorage['openGroup']){
              if(sessionStorage['openGroup'] == 'pab'){
                _this.getPabMembers();
              }else if(sessionStorage['openGroup']=='oab'){
                let data = _this.transform_menu[1].children[0];
                console.log(_this.transform_menu[1].children[0])
                let str = _this.$store.getters.userInfo.name;
                let index = str.lastIndexOf('@');
                let domain = str.slice(index+1)
                _this.oabchildren = [];
                if(data.id==0||data.id=='-1'){
                  data.username = 'everyone@'+domain;
                }else{
                  data.username = 'dept_'+data.id+'@'+domain;
                }
                data.name = data.label;
                data.is_dept = true;
                _this.oabchildren.push(data)
                if(data.children.length>0){
                  let paramArr = [];
                  for(let i=0;i<data.children.length;i++){
                    data.children[i].username = 'dept_'+data.children[i].id+'@'+domain;
                    data.children[i].name = data.children[i].label;
                    data.children[i].is_dept = true;
                    paramArr.push(data.children[i]);
                  }
                  _this.oabchildren = _this.oabchildren.concat(paramArr);
                  _this.getOabMembers();
                }else{
                  _this.getOabMembers();
                }

              }else if(sessionStorage['openGroup']=='cab'){
                console.log('cab')
                _this.getCabMembers();
              }else if(sessionStorage['openGroup']=='soab'){
                console.log('soab')
                _this.getSoabMembers();
              }
            }else{
              sessionStorage['openGroup'] = 'pab'
              _this.getPabMembers();
            }

          })
        }))
      },
      handleChange(value, direction, movedKeys) {

      },
      attachSizeChange(val){
        this.attachPageSize = val;
        this.getAttachList();
      },
      attachCurrentChange(val){
        this.attachCurrentPage = val;
        this.getAttachList();
      },
      attachSizeChange_net(val){
        this.attachPageSize_net = val;
        this.getNetfile(-1);
      },
      attachCurrentChange_net(val){
        this.attachCurrentPage_net = val;
        this.getNetfile(-1);
      },
      attachSizeChange_company(val){
        this.attachPageSize_company = val;
        this.getNetfile_company(-1);
      },
      attachCurrentChange_company(val){
        this.attachCurrentPage_company = val;
        this.getNetfile_company(-1);
      },
      handleSizeChange_contact(val){
        this.currentPage = 1
        this.pageSize = val;
        if(sessionStorage['openGroup']=='pab'){
          this.getPabMembers();
        }else if(sessionStorage['openGroup']=='oab'){
          this.getOabMembers();
        }else if(sessionStorage['openGroup']=='cab'){
          this.getCabMembers();
        }else if(sessionStorage['openGroup']=='soab'){
          this.getSoabMembers();
        }else if(sessionStorage['openGroup']=='lab'){
          this.getLabs();
        }
      },
      handleCurrentChange_contact(val){
        this.currentPage = val
        if(sessionStorage['openGroup']=='pab'){
          this.getPabMembers();
        }else if(sessionStorage['openGroup']=='oab'){
          this.getOabMembers();
        }else if(sessionStorage['openGroup']=='cab'){
          this.getCabMembers();
        }else if(sessionStorage['openGroup']=='soab'){
          this.getSoabMembers();
        }else if(sessionStorage['openGroup']=='lab'){
          this.getLabs();
        }
      },
      search_dept(){
        this.currentPage = 1
        if(sessionStorage['openGroup']=='pab'){
          this.getPabMembers();
        }else if(sessionStorage['openGroup']=='oab'){
          this.getOabMembers();
        }else if(sessionStorage['openGroup']=='cab'){
          this.getCabMembers();
        }else if(sessionStorage['openGroup']=='soab'){
          this.getSoabMembers();
        }else if(sessionStorage['openGroup']=='lab'){
          this.getLabs();
        }
      },

      addAttachfn(){
        for(let i=0;i<this.fileSelection.length;i++){
          if(!(this.hashFile[this.fileSelection[i].id])){
            this.hashFile[this.fileSelection[i].id] = true
            this.fileList.push(this.fileSelection[i]);
            this.setSubject();
          }
        }
        this.coreFileDialog = false;
        this.fileSelection = [];
      },
      fileSelectionChange(val) {
        this.fileSelection = val;
      },
      selectUpload(command){
        if(command == 'filecore'){
          this.coreFileDialog = true;
          if(this.attachTotal == 0){
            this.getAttachList();
          }
          this.activeName_file = 'first';

        }else if(command == 'upload'){
          document.getElementById('addAttachBtn').click()
        }
      },
      getAttachList(){
        let param={
          limit:this.attachPageSize,
          offset:(this.attachCurrentPage-1)*this.attachPageSize
        };
        getAttach(param).then((suc)=>{
          this.attachTotal = suc.data.count;
          this.coreFileList = suc.data.results;
        },(err)=>{
          console.log(err);
        })
      },
      delete_attach(id,k){
        this.hashFile[this.fileList[k].id]=false;
        this.fileList.splice(k,1);
      },
      attach_hoverfn(key){
        this.attachIndex = key;
      },
      remove_attach_hover(){
        this.attachIndex = '';
      },
      uploadFile(param){
        var file = param.file;
        var formData=new FormData();
        formData.append('filepath', file)
        postAttach(formData).then((res)=>{
          var obj = res.data;
          this.hashFile[res.data.id]=true;
          this.fileList.push(res.data)
          this.setSubject();
         this.$message({
             message:"上传成功",
             type:'success'
         })
        },(err)=>{
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({
               message:"上传失败! "+str,
               type:'error'
          })
        })
        return true;
      },
      uploadProgress(event, file, fileList){

      },
      sucUpload(response, file, fileList){
        this.fileList.push(file);
        this.setSubject();
      },
      imgChange(param){
        var file= param.file;
        // this.imageFileName.push(file.name);
            const isJPG = file.type === 'image/jpeg';
            const isGIF = file.type === 'image/gif';
            const isPNG = file.type === 'image/png';
            const isBMP = file.type === 'image/bmp';
            const isLt2M = file.size / 1024 / 1024 < 10;

            if (!isJPG && !isGIF && !isPNG && !isBMP) {
                this.$alert('上传图片必须是JPG/GIF/PNG/BMP 格式!', '提示：', {
                  confirmButtonText: '确定'
                });
                return;
            }
            if (!isLt2M) {
                this.$alert('上传图片大小不能超过 10MB!', '提示：', {
                  confirmButtonText: '确定'
                });
                return;
            }

        var _this = this;
        // var o = document.getElementById('img_upload');

        var reader=new FileReader();
        reader.readAsDataURL(file);
        reader.onload=function (e) {//上传成功，执行上传成功之后的事件
        var str=e.target.result;
        //将上传成功后的图片显示在特定位置
        this.imgSrc = str;
          _this.$refs[this.editor_id].editor.insertHtml(`<img src=${str} />`)


        }
      },
      onContentChange (val) {

        // console.log(this.$refs[this.editor_id].$data.outContent)
        this.content = this.$refs[this.editor_id].$data.outContent;
        // this.$refs[this.editor_id].editor.html(this.content);
        // $('#editor_id'+this.rid).val()

      },


      preview(){
        //ke-toolbar-icon ke-toolbar-icon-url ke-icon-preview
        let btn = document.querySelector('#compose'+this.rid+' .ke-toolbar-icon.ke-toolbar-icon-url.ke-icon-preview');
        btn.click();
      },
      addMailbox(){
        setTimeout(()=>{this.handleSelect()},300)
      },
      deleteMailbox(){
        if(!this.state1&&this.maillist.length>0){
          this.hashMail[this.maillist[this.maillist.length-1].email] = false;
          this.maillist.pop();
        }
      },
      deleteMailboxForKey(k,v,p){
        if(p=='1'){
          let c = 0;
          for(let i=0;i<this.maillist.length;i++){
            if(this.maillist[i].email == v.email){
              this.hashMail[v.email] =false;
              this.maillist.splice(i,1);
              c--;
              break;
            }
            c ++;
          }
          if(c>=this.maillist.length){
            for(let j=0;j<this.maillist_copyer.length;j++){
              if(this.maillist_copyer[j].email == v.email){
                this.hashMail_copyer[v.email] =false;
                this.maillist_copyer.splice(j,1);
                break;
              }
            }
          }
        }else{
          this.hashMail[v.email] = false;
          this.maillist.splice(k,1)
        }
      },
      handleSelect(item) {
        if(item){
          if(this.state1){
            if(this.hashMail[item.email]){

            }else{
              this.hashMail[item.email] = true;
              this.maillist.push(item);
              this.state1 = '';
            }
          }
          this.state1 = '';
        }else{
          if(this.state1){
            if(this.hashMail[this.state1]){

            }else{
              this.hashMail[this.state1] = true;
              let obj = {};
              obj.value = this.state1;
              obj.email = this.state1;
              obj.fullname = '';
              if(emailReg.test(this.state1)){
                obj.status = true;
              }else{
                obj.status = false;
              }
              this.maillist.push(obj);
              this.state1 = '';
            }
          }
          this.state1 = '';
        }

      },
      addMailbox_copyer(){
        setTimeout(()=>{this.handleSelect_copyer()},300)
      },
      addMailbox_bcc(){
        setTimeout(()=>{this.handleSelect_bcc()},300)
      },
      deleteMailbox_copyer(){
        if(!this.state_copyer&&this.maillist_copyer.length>0){
          this.hashMail_copyer[this.maillist_copyer[this.maillist_copyer.length-1].email] = false;
          this.maillist_copyer.pop();
        }
      },
      deleteMailbox_bcc(){
        if(!this.state_bcc&&this.maillist_bcc.length>0){
          this.hashMail_bcc[this.maillist_bcc[this.maillist_bcc.length-1].email] = false;
          this.maillist_bcc.pop();
        }
      },
      deleteMailboxForKey_copyer(k,v){
        this.hashMail_copyer[v.email] = false;
        this.maillist_copyer.splice(k,1)
      },
      deleteMailboxForKey_bcc(k,v){
        this.hashMail_bcc[v.email] = false;
        this.maillist_bcc.splice(k,1)
      },
      handleSelect_copyer(item) {
        if(item){
          if(this.state_copyer){
            if(this.hashMail_copyer[item.email]){

            }else{
              this.hashMail_copyer[item.email] = true;
              this.maillist_copyer.push(item);
              this.state_copyer = '';
            }
          }
          this.state_copyer = '';
        }else{
          if(this.state_copyer){
            if(this.hashMail_copyer[this.state_copyer]){

            }else{
              this.hashMail_copyer[this.state_copyer] = true;
              let obj = {};
              obj.value = this.state_copyer;
              obj.email = this.state_copyer;
              obj.fullname = '';
              if(emailReg.test(this.state_copyer)){
                obj.status = true;
              }else{
                obj.status = false;
              }
              this.maillist_copyer.push(obj);
              this.state_copyer = '';
            }
          }
          this.state_copyer = '';
        }
      },
      handleSelect_bcc(item) {
        if(item){
          if(this.state_bcc){
            if(this.hashMail_bcc[item.email]){

            }else{
              this.hashMail_bcc[item.email] = true;
              this.maillist_bcc.push(item);
              this.state_bcc = '';
            }
          }
          this.state_bcc = '';
        }else{
          if(this.state_bcc){
            if(this.hashMail_bcc[this.state_bcc]){

            }else{
              this.hashMail_bcc[this.state_bcc] = true;
              let obj = {};
              obj.value = this.state_bcc;
              obj.email = this.state_bcc;
              obj.fullname = '';
              if(emailReg.test(this.state_bcc)){
                obj.status = true;
              }else{
                obj.status = false;
              }
              this.maillist_bcc.push(obj);
              this.state_bcc = '';
            }
          }
          this.state_bcc = '';
        }
      },
      querySearch(queryString, cb) {
        var restaurants = this.restaurants;
        var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (restaurant) => {
          return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) >= 0);
        };
      },
      filterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      selectContact(data){
        if(!data.children){
          if(this.insertMailbox==1){
            if(!this.hashMail[data.email]){
              this.hashMail[data.email]=true;
              this.maillist.push({value:data.label,status:true,email:data.email,fullname:data.fullname});
            }
          }else if(this.insertMailbox == 2){
            if(!this.hashMail_copyer[data.email]){
              this.hashMail_copyer[data.email]=true;
              this.maillist_copyer.push({value:data.label,status:true,email:data.email,fullname:data.fullname});
            }
          }else if(this.insertMailbox == 3){
            if(!this.hashMail_bcc[data.email]){
              this.hashMail_bcc[data.email]=true;
              this.maillist_bcc.push({value:data.label,status:true,email:data.email,fullname:data.fullname});
            }
          }
        }else{
          this.right_cpage = 1;
          this.right_page_total = data.count;
        }
      },
      //获取个人通讯录组数据
      getPabGroups(){
        let _this = this;

        let count = 1;
        let arr = [];
        function getResult(page){
          console.log('page')
          console.log(page)
          let param = {
            "page": page,
            "page_size": 10,
            "search": '',
            "group_id": 0,
          };
          contactPabMembersGet(param).then(suc=>{
            for(let i=0;i<suc.data.results.length;i++){
              let o = suc.data.results[i];
              let obj = {};
              obj.id = o.contact_id;
              let str = o.fullname + '<'+o.email+'>';
              obj.value = str;
              obj.fullname = o.fullname;
              obj.email = o.email;
              obj.status = true;
              arr.push(obj);
            }
            console.log(count<Math.ceil(suc.data.count/10))
            if(count<Math.ceil(suc.data.count/10)){
              count ++;
              getResult(count);
            }else{
              _this.restaurants = arr;
              _this.$store.dispatch('setFilterContactA',arr);
            }
          }).catch(err=>{
            console.log(err);
          })
        }
        if(this.$store.getters.getFilterContact.length==0){
          // getResult(count);
          let param = {
            "group_id":0,
            "page_size":10000,
            "page":1
          }
          contactPabMembersGet(param).then((suc)=>{
            let arr = [];
            for(let i=0;i<suc.data.results.length;i++){
              let o = suc.data.results[i];
              let obj = {};
              obj.id = o.contact_id;
              let str = o.fullname + '<'+o.email+'>';
              obj.value = str;
              obj.fullname = o.fullname;
              obj.email = o.email;
              obj.status = true;
              arr.push(obj);
            }
            this.restaurants = arr;
            this.$store.dispatch('setFilterContactA',arr);
          },(err)=>{
            console.log(err);
          })
        }else{
          this.restaurants = this.$store.getters.getFilterContact
        }


      },
      getRightContact1(){
        this.contact_loading = true;
        contactPabGroupsGet().then(res=>{
          let _this = this;
          let resultArr = [];
          let total = res.data.results[res.data.results.length-1].count;
          let axiosArr = [];
          for(let i=0;i<res.data.pab_contact_groups.length;i++){
            let ob = res.data.pab_contact_groups[i];
            let param = {
              "page": 1,
              "page_size":total,
              "search": '',
              "group_id": ob.id,
              "is_group": 1,
            };
            axiosArr.push(contactPabMapsGet(param))
            resultArr.push({label:ob.label,id:ob.id,children:[]})
          }
          axiosArr.push(contactPabMembersGet({"page":1,"page_size":total,"group_id":0,"is_group":0,"search":''}))
          resultArr.push({label:'未分组联系人',id:0,children:[]})

          axios.all(axiosArr).then(axios.spread(function () {
            // 所有请求现在都执行完成
            for(let k = 0;k<arguments.length;k++){
              let ko = arguments[k];
              resultArr[k]['label'] += ' （'+ko.data.count+'）'
              for(let j=0;j<ko.data.results.length;j++){
                let obj = {};
                obj.id = ko.data.results[j].contact_id;
                obj.email = ko.data.results[j].email;
                obj.fullname = ko.data.results[j].fullname;
                obj.label = ko.data.results[j].fullname + '<'+ko.data.results[j].email+'>';
                resultArr[k]['children'].push(obj)
              }
            }
            _this.contactList = resultArr
            _this.contact_loading = false;
          }))
        }).catch(err=>{
          this.contact_loading = false;
        })
      },
      getRightContact(){
        this.contact_loading = true;
        contactPabGroupsGet().then(res=>{
          let _this = this;
          let resultArr = [];
          let total = res.data.results[res.data.results.length-1].count;
          let axiosArr = [];
          for(let i=0;i<res.data.results.length;i++) {
            let ob = res.data.results[i];
            let param = {
              "page": 1,
              "page_size": 10,
              "search": this.right_search,
              "group_id": ob.id,
            };
            if (ob.id > 0) {
              axiosArr.push(contactPabMapsGet(param))
            } else {
              axiosArr.push(contactPabMembersGet(param))
            }
            let show = false;
            if(ob.id == 0 ){
              show = true;
            }
            resultArr.push({label:ob.groupname,id:ob.id,children:[],count:ob.count,show:show,page:1,loading:false})
          }
          axios.all(axiosArr).then(axios.spread(function () {
            // 所有请求现在都执行完成
            for(let k = 0;k<arguments.length;k++){
              let ko = arguments[k];
              // resultArr[k]['label'] += ' （'+ko.data.count+'）'
              for(let j=0;j<ko.data.results.length;j++){
                let obj = {};
                obj.id = ko.data.results[j].contact_id;
                obj.email = ko.data.results[j].email;
                obj.fullname = ko.data.results[j].fullname;
                obj.label = ko.data.results[j].fullname + '<'+ko.data.results[j].email+'>';
                resultArr[k]['children'].push(obj)

              }
              resultArr[k]['count'] = ko.data.count
            }
            _this.contactList = resultArr
            _this.contact_loading = false;
          }))




        }).catch(err=>{
          this.contact_loading = false;
        })
      },
      plus(b,m){
        if(b){
          m.page++;
          this.getOneByPage(m)
        }else{
          m.page--;
          this.getOneByPage(m)
        }
      },
      changePage(val,m){
        if(val<=1){val = 1}
        if(val>= Math.ceil(m.count/10)){val = Math.ceil(m.count/10)}
        m.page = val;
        this.getOneByPage(m);
      },
      getOneByPage(m){
        let param = {
            "page": m.page,
            "page_size": 10,
            "search": this.right_search,
            "group_id": m.id
          };

          m.loading = true;
          if (m.id > 0) {
            contactPabMapsGet(param).then(res=>{
              let arr = [];
              for(let j=0;j<res.data.results.length;j++){
                let obj = {};
                obj.id = res.data.results[j].contact_id;
                obj.email = res.data.results[j].email;
                obj.fullname = res.data.results[j].fullname;
                obj.label = res.data.results[j].fullname + '<'+res.data.results[j].email+'>';
                arr.push(obj)
              }
              m.loading = false;
              m.children = arr;
            }).catch(err=>{
              m.loading = false;
              console.log('出错了error:'+error)
            })
          } else {
            contactPabMembersGet(param).then(res=>{
              let arr = [];
              for(let j=0;j<res.data.results.length;j++){
                let obj = {};
                obj.id = res.data.results[j].contact_id;
                obj.email = res.data.results[j].email;
                obj.fullname = res.data.results[j].fullname;
                obj.label = res.data.results[j].fullname + '<'+res.data.results[j].email+'>';
                arr.push(obj)
              }
              m.loading = false;
              m.children = arr;
            }).catch(err=>{
              m.loading = false;
              console.log('出错了error:'+error)
            })
          }
      },
      changeShowIndex(k){
        console.log(k)
        console.log(this.contactList[k].show)
        if(this.contactList[k].show){
          this.contactList[k].show = false;
          console.log('123')
        }else{
          console.log('1sdfa23')
          for(let i=0;i<this.contactList.length;i++){
            if(i==k){
              this.contactList[i].show = true;
            }else{
              this.contactList[i].show = false;
            }
          }
        }

      },
      refresh_right(){
        this.right_search = '';
        this.getRightContact();
      },

    },
    mounted() {
      console.log(this.type)
       this.$nextTick(() => {
        // window.uploader = this.$refs.uploader.uploader

      })
      this.content = this.parent_content;
      this.maillist = this.parent_maillist;
      this.maillist_copyer = this.parent_maillist_copyer;
      this.maillist_bcc = this.parent_maillist_bcc;
      this.ruleForm2 = this.parent_ruleForm2;
      this.fileList = this.parent_fileList;
      this.show_replay_to = this.parent_show_reply_to;
      this.hashMail = [];
      this.hashMail_copyer = [];
      this.hashMail_bcc = [];
      if(this.maillist_copyer.length>0){
        this.ruleForm2.is_cc = true;
      }
      if(this.maillist_bcc.length>0){
        this.ruleForm2.is_bcc = true;
      }else{
        this.ruleForm2.is_bcc = false;
      }
      if(this.ruleForm2.reply_to){
        this.show_replay_to = true;
      }
      for(let i=0;i<this.maillist.length;i++){
        this.hashMail[this.maillist[i].email] = true;
      }
      for(let i=0;i<this.maillist_copyer.length;i++){
        this.hashMail_copyer[this.maillist_copyer[i].email] = true;
      }
      for(let i=0;i<this.maillist_bcc.length;i++){
        this.hashMail_bcc[this.maillist_bcc[i].email] = true;
      }
      $('#editor_id'+this.rid).val(this.content);

       $('#editor_id'+this.rid).css({'width': '100%','border':'none','boxSizing':'border-box','padding':'10px 10px 0'})
      if(!this.ruleForm2.is_html){
        // this.$refs[this.editor_id].editor.text(this.content)
        $('#editor_id'+this.rid).val(this.content);
        this.no_html();
        // this.onContentChange();
      }
      this.createEditor();
      this.getParams();
      // sessionStorage['openGroup'] = 'pab';
      if(sessionStorage['curKey'] && sessionStorage['curKey'] == 'soab'){
        this.expand_soab = true;
      }else{
        this.expand_soab = false;
      }
      this.setEditorHeight();
      this.set_main_min_height();
      // this.$refs[this.editor_id].editor.insertHtml(' ');
      $('#compose'+this.rid+' .ke-edit-iframe').focus();
      let _this = this
       window.addEventListener("resize", function () {
            // 得到屏幕尺寸 (内部/外部宽度，内部/外部高度)
            _this.setEditorHeight();
            _this.set_main_min_height();
       }, false);

      //   setTimeout(_this.setEditorHeight,50)
      this.getSignatrue();
    },
    beforeMount() {

    },
    created(){

      this.getTemplateListfn();
      this.getPabGroups();
      this.getRightContact();
      // this.get_transform_menu();
      // this.getMemberList(); new通讯录
      getContactInfo().then((res) => {
        sessionStorage['soab_domain_cid'] = res.data.soab_domain_cid;
        this.soab_domain_cid = res.data.soab_domain_cid
        this.webmail_cab_show = res.data.webmail_cab_show;
        this.webmail_soab_show = res.data.webmail_soab_show;
        if(this.webmail_soab_show){
          this.getSoabDomains();
        }
      });
    },
    computed:{
      uploadJson:function(){
        return this.$store.state.uploadJson;
      },
      editor_id:function(){
        return 'editor_id'+this.rid;
      },
      partSendList:function(){
        let arr = [];
        for(let i=0;i<this.maillist.length;i++){
          this.maillist[i].type = 'to'
          this.maillist[i].k = i
          arr.push(this.maillist[i])
        }
        for(let i=0;i<this.maillist_copyer.length;i++){
          for(var j=0;j<this.maillist.length;j++){
            if(this.maillist_copyer[i].email == this.maillist[j].email){
              break;
            }
          }
          if( j ==this.maillist.length){
            this.maillist_copyer[i].type = 'cc'
            this.maillist_copyer[i].k = i
            arr.push(this.maillist_copyer[i])
          }
        }
        let p = [].concat(arr)
        for(let i=0;i<this.maillist_bcc.length;i++){
          for(var j=0;j<p.length;j++){
            if(this.maillist_bcc[i].email == p[j].email){
              break;
            }
          }
          if( j ==p.length){
            this.maillist_bcc[i].type = 'bcc'
            this.maillist_bcc[i].k = i
            arr.push(this.maillist_bcc[i])
          }
        }
        return arr;
      },
      totalAttach:function(){
        let total = 0;
        for(let i=0;i<this.fileList.length;i++){
          let o = this.fileList[i];
          if(o.size){
            total += o.size;
          }else{
            total += o.file_size
          }
        }
        return total;
      },



    },
    watch: {
      filterText(val) {
        this.$refs.tree2.filter(val);
      },
      toList(val){
        if(this.active_box == 'to'){
          this.allSeclect = val;
        }
      },
      ccList(val){
        if(this.active_box == 'cc'){
          this.allSeclect = val;
        }
      },
      bccList(val){
        if(this.active_box == 'bcc'){
          this.allSeclect = val;
        }
      },
      active_box(val){
        if(this.active_box == 'cc'){
          this.allSeclect = this.ccList;
        }else if(this.active_box == 'to'){
          this.allSeclect = this.toList;
        }else if(this.active_box == 'bcc'){
          this.allSeclect = this.bccList;
        }
      },
      fileList(){
        let _this = this;
        setTimeout(_this.setEditorHeight,0);
        setTimeout(_this.set_main_min_height,0);

      },
      "ruleForm2.is_cc"(nv){
        let _this = this;
        setTimeout(_this.setEditorHeight,0);
        setTimeout(_this.set_main_min_height,0);
      },
      "ruleForm2.is_partsend"(nv){
        let _this = this;
        setTimeout(_this.setEditorHeight,0);
        setTimeout(_this.set_main_min_height,0);
      },
      "ruleForm2.is_bcc"(nv){
        let _this = this;
        setTimeout(_this.setEditorHeight,0);
        setTimeout(_this.set_main_min_height,0);
      },
      show_replay_to(){
        let _this = this;
        setTimeout(_this.setEditorHeight,0);
        setTimeout(_this.set_main_min_height,0);
      },
      maillist(){
        let _this = this;
        setTimeout(_this.setEditorHeight,0);
        setTimeout(_this.set_main_min_height,0);
      },
      maillist_copyer(){
        let _this = this;
        setTimeout(_this.setEditorHeight,0);
        setTimeout(_this.set_main_min_height,0);
      },
      maillist_bcc(){
        let _this = this;
        setTimeout(_this.setEditorHeight,0);
        setTimeout(_this.set_main_min_height,0);
      },
      show_all_attach(){
        let _this = this;
        setTimeout(_this.setEditorHeight,0);
        setTimeout(_this.set_main_min_height,0);
      },
    },
    // components:{ treeTransfer } // 注册

  }
</script>
<style>
  .blue_color{
    background-color: #ecf5ff;
    color: #66b1ff;
  }
  .no-padding>.el-input__inner{
    padding:0 2px;
    text-align: center;
  }
  .right_con_list:hover{
    background:#e6e6e6;
  }
  .only_current_page .el-pager>li.number{
    display:none;
  }
  .only_current_page .el-pager>li.number.active{
    display:inline-block;
  }
  .bigUpload .el-progress-bar__outer{
    height: 10px !important;
  }
  .bigUpload .el-upload-list{
    border: 1px solid #cbcbcb;
    margin-top: 10px;
    min-height: 300px;
    padding:0 4px 10px;
  }
  .bigUpload .el-upload-list__item{
    /*border-bottom: 1px solid #cdcdcd;*/
        margin-top: 20px;
  }
  #app .right_menu .el-tabs__item{
    padding:0 14px;
  }
  #app .attach_list_style{
    /*max-height: 142px;*/
    overflow: auto;
  }
  .group_member{
    height:36px;
    line-height:36px;
    padding-left:16px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  .group_member:hover{
    background-color: #f0f1f3;
    cursor: pointer;
  }
  #app .compose_style .f-csp:hover,#app .compose_style .f-csp.selected{
    border-color:#2ea962 !important;
    box-shadow: 0 0 0 1px #2ea962;
  }
  #app .compose_style .template_box ul.template_ul>li{
    position: relative;
    font-size: 12px;
    height: 72px;
    width:100%;
    box-sizing: border-box;
    color: #444;
    padding: 12px;
    margin-bottom: 14px;
    border-radius: 2px;
    border: 1px solid #ddd;
    text-align: left;
  }
  #app .compose_style .template_box ul.template_ul>li.selected i.choose{
    display:inline-block;
  }
   #app .compose_style .template_box ul.template_ul>li i.choose{
     display:none;
     font-size:14px;
     color:#2ea962;
     position: absolute;
     right: 6px;
    bottom: 6px;
   }

  #app .compose_style .m-mlcompose{
    overflow: auto;
  }
  #app .compose_style .label_style{
    display:inline-block;
    width:100px;
    text-align:right;
  }
  .address_box .delete_hover{
    color:red;
    display:none;
  }
  .hover_show_box:hover .delete_hover{
    display:inline-block;
  }
   .address_box{
    border:1px solid #dcdfe6;height:140px;margin-bottom:20px;overflow-y: auto;padding:4px;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
  }
  .address_box:hover,#app .compose_style .address_box.active{
    border-color:#409EFF
  }
  .address_box.active{
    border-color:#409EFF;
    box-shadow: 0 0 5px #409eff;
  }
   .show_contact_style{
    color:#409EFF;
    text-decoration: underline;
  }
  #app .compose_style .show_contact_style:hover{
    background:#409EFF;
    color:#fff;
    padding:4px 0;
    border-radius: 3px;
  }
  #app .compose_style .tree {
  overflow-y: auto;
  overflow-x: auto;
  /* width: 80px; */
  height: 500px;
  background-color: #ffffff;
}
#app .compose_style .el-tree {
  min-width: 100%;
  font-size: 14px;
  display: inline-block !important;
}
  #app .compose_style .bico {
    display: inline-block;
    width: 32px;
    height: 32px;
    background-image: url(../../../assets/img/icons.png);
  }
  #app .compose_style .margin-bottom-5{
    margin-bottom:5px;
  }
  #app .compose_style .show_contact{
    opacity: 0;
    filter: alpha(opacity=0);
  }
  #app .compose_style .m-mlcompose .mn-form.right0{
    right:0;

  }
  #app .compose_style .m-mlcompose .upload-demo{
    display:inline-block;
  }
  #app .compose_style .attach_actions{
    display:none;
  }
  #app .compose_style .attach_hover .attach_actions{
    display:inline-block;
  }
  #app .compose_style .attach_box .el-button--mini{
    border:none;
    color:#409EFF;
    padding: 7px 10px;
  }
  #app .compose_style .right_menu .el-tabs__nav-scroll{
    padding-left:10px;
  }
  #app .compose_style .right_menu .el-tabs__content{
    padding:0 10px;
  }
  #app .compose_style .mn-aside.right_menu{
    padding:0;
    width:240px;
    box-sizing:border-box;
  }
 #app .compose_style  .right_menu .page ul li{
    width:50%;
    float:left;
    text-align:center;
    margin-bottom:20px;
  }
  #app .compose_style .right_menu ul li a{
    border:2px solid #e3e4e5;
    display:inline-block;
    position:relative;
    width: 80px;
    height: 80px;

  }
  #app .compose_style .right_menu ul li a.active{
    border:2px solid #449115;
    box-shadow:0 0  10px #449115;
  }
  #app .compose_style .right_menu ul li a.active .bg{
    background: url(../img/selected.gif) no-repeat;
    width: 78px;
    height: 78px;
    display: block;
    position: absolute;
    z-index: 9;
    top: 0;
    left: 0;
  }
  #app .compose_style .compose_title input{
    border:none;
    /*border-bottom:1px solid #dcdfe6;*/
    border-radius:0;
  }
  #app .compose_style .compose_title .el-form-item{
    border-bottom:1px solid #dcdfe6;
    margin-bottom:6px;
  }
  #app .compose_style .compose_title .el-select{
    width:100%;
  }
  #app .compose_style .compose_title .el-input--mini{
    font-size:15px;
  }
  #app .compose_style .compose_footer>div{
    padding:0 14px;
  }
  #app .compose_style .m-mlcompose .mn-form .form-edr.compose_editor{
    /*position:absolute;*/
    /*top:224px;*/
    /*bottom:72px;*/
    /*height:auto;*/
  }
 #app .compose_style  .compose_editor [data-name="preview"]{
    display:none;
  }
  #app .compose_style .mailbox_s{
    float:left;white-space:nowrap;
    cursor:pointer;
    border:1px solid #a3d9d2;
    background-color: #e4f7f5;
    margin-right:6px;
    padding:0 4px;
    border-radius:12px;
    font-size: 12px;
    margin-bottom: 4px;
  }
  #app .compose_style .mailbox_s.error{
    background-color: #f2dede;
    border-color: #ebccd1;
    color: #a94442;
  }
  #app .compose_style .mailbox_s>b{
    margin-right:4px;
  }
  #app .compose_style .compose_title .no_padding .el-input__inner{
    padding:0;
  }
  #app .compose_style .padding_15{
    padding-left:15px;
  }
</style>

