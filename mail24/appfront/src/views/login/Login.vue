<template>
     <div  id="login_bg" ref="login_bg" :class="'bg'+bgIndex">
      <div class="main-bottom main-bottom-0"></div>
      <div class="main-middle main-middle-0"></div>


      <div class="main">
        <div class="content">
          <div>
            <a href="#" class="login_logo"  v-if="loginBeforeData.login_logo">
              <img :src="loginBeforeData.login_logo" alt=" U-Mail">
            </a>


          </div>
          <div class="version" style="width:60%;min-height:200px;margin:0 auto;" v-if="loginBeforeData.login_ads && loginBeforeData.login_ads.length>0">

            <el-carousel trigger="click" indicator-position="outside">
              <el-carousel-item v-for="(item,k) in loginBeforeData.login_ads" :key="k" v-if="loginBeforeData.login_ads">
                <a :href="item.link" target="_blank" v-if="item.link">
                  <img :src="item.image" style="width:100%;max-width:100%;">
                </a>
                <img :src="item.image" style="width:100%;max-width:100%;" v-if="!item.link">
              </el-carousel-item>
            </el-carousel>

          </div>
          <!--<div style="width:300px;padding-left:20px;margin-top:30px;">-->
            <!--<a :href="loginBeforeData.login_ads[0].link" target="_blank" >-->
              <!--<img :src="loginBeforeData.login_ads[0].image" style="width:100%;max-width:100%;">-->
            <!--</a>-->
          <!--</div>-->
          <div class="copyright">
            <label>
              Copyright © <span>{{loginBeforeData.name}}</span>
              <span v-if="loginBeforeData.is_icp">
                <a :href="loginBeforeData.icp_link" v-if="loginBeforeData.icp_link"  target="_blank" style="color:#fff;text-decoration:none;"> | {{loginBeforeData.icp_no}}</a>
                <span v-if="!loginBeforeData.icp_link"> | {{loginBeforeData.icp_no}}</span>
              </span>
            </label>
          </div>
        </div>
        <div class="aside-blur" style="min-width: 330px;z-index:10;">

        </div>
        <div class="aside" style="min-width: 330px;z-index:11;" ref="aside">
          <div class="text-center">
            <el-button type="text" style="color:#fff;">
              <!--<i class="el-icon-star-off" style="font-size:18px;"></i>-->
              <i class="el-icon-star-on" style="font-size:16px;"></i>收藏本页
            </el-button>
            <el-button type="text" @click="show_agreement_dialog" style="color:#fff">注 册</el-button>
            <el-button type="text" style="color:#fff">
              <i class="iconfont icon-iconhelp1" style="font-size:18px;"></i>
              帮助中心</el-button>
          </div>
          <div class="loginArea normalForm" curtype="normalForm">
            <div id="login_box" style="min-width:260px;width: 54%;margin:0 auto;">


              <h2 class="text-center">{{lan.user_login}}</h2>
              <el-form :label-position="labelPosition" class="loginForm" ref="loginForm" :rules="rules" label-width="80px" :model="formLabelAlign">
                <el-form-item :label="lan.user_name" prop="username" style="">
                  <label slot="label">
                    <template>
                      <el-select v-model="language" @change="changeLanguage" class="no_border" style="float:right;width:124px;">
                          <el-option label="中文（简体）" value="zh-hans"></el-option>
                          <el-option label="中文（繁體）" value="zh-tw"></el-option>
                          <el-option label="English" value="en"></el-option>
                          <!--<el-option label="Español" value="es" disabled></el-option>-->
                        </el-select>
                        <span>{{lan.user_name}}</span>

                    </template>
                  </label>
                  <!--<el-input v-model.trim="formLabelAlign.username"></el-input>-->
                  <el-input :placeholder="lan.placeholder_user_name" v-model.trim="formLabelAlign.username" class="input-with-select" name="username">
                    <template slot="append">@
                    <el-select v-model="loginBeforeData.domain"  :placeholder="lan.please_choose"  style="width:120px" @change="changeDomain">
                      <el-option v-for="(d,k) in loginBeforeData.domains" :key="k" :label="d[1]" :value="d[1]"></el-option>
                    </el-select>
                    </template>

                  </el-input>
                </el-form-item>
                <el-form-item :label="lan.password" prop="password">
                  <el-input type="password" name="password" v-model="formLabelAlign.password"></el-input>
                </el-form-item>
                <div style="height:30px;">
                  <el-checkbox style="float:left;" v-model="rememberUserInfo" :class="{'is-checked el-checkbox__input':rememberUserInfo}">{{lan.LOGIN_REMEMBER_USERNAME}}</el-checkbox>
                  <el-button type="text" style="float:right;padding:0;color:#e6a23c;" @click="forget">{{lan.forget_password}}</el-button>
                </div>

              </el-form>
              <div class="text-center">
                <el-button type="primary" @click="login" style="width:50%">{{lan.login}}</el-button>

              </div>

            </div>
          </div>

          <el-dialog :title="lan.reset_password" :visible.sync="formVisible" width="400px" :append-to-body="true" :close-on-click-modal="false">
            <el-form :model="form" size="small" :rules="formRule" ref="reset2Form">
              <el-input v-model="form.carbled" type="hidden" style="display:none;"></el-input>
              <el-form-item :label="lan.placeholder_validation_code +form.code_label" prop="code">
                <el-input v-model="form.code" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item :label="form.label_q1" prop="q1">
                <el-input v-model="form.q1" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item :label="form.label_q2" prop="q2">
                <el-input v-model="form.q2" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item :label="form.label_q3" prop="q3">
                <el-input v-model="form.q3" auto-complete="off"></el-input>
              </el-form-item>

            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="formVisible = false">{{lan.cancel}}</el-button>
              <el-button type="primary" @click="reset2_submit">{{lan.sure}}</el-button>
            </div>
          </el-dialog>

          <el-dialog :title="lan.reset_password" :visible.sync="form3Visible" width="400px" :append-to-body="true" :close-on-click-modal="false">
            <el-form :model="form3" size="small" :rules="form3Rule" ref="reset3Form">
              <el-input v-model="form3.carbled" type="hidden" style="display:none;"></el-input>
              <el-input v-model="form3.new_carbled" type="hidden" style="display:none;"></el-input>

              <el-form-item :label="lan.COMMON_NEW_PASSWORD" prop="new_password">
                <el-input v-model="form3.new_password" type="password" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item :label="lan.COMMON_CONFIRM_PASSWORD" prop="confirm_password">
                <el-input v-model="form3.confirm_password" type="password" auto-complete="off"></el-input>
              </el-form-item>
              <div>
                <div>
                  <strong style="color: red">{{lan.COMMON_PASSWORD_NOTICE}}</strong>
                  <ul style="margin-left: 26px;">
                    <li style="list-style-type:circle;"> {{lan.COMMON_PASSWORD_NOTICE_1}} {{passwordRules.passwd_size2}} {{lan.COMMON_PASSWORD_NOTICE_2}}</li>
                    <li v-if="passwordRules.passwd_type==2" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_3}}</li>
                    <li v-if="passwordRules.passwd_type==3" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_4}}</li>
                    <li v-if="passwordRules.passwd_type==4" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_5}}</li>
                    <li v-if="passwordRules.passwd_digital" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_6}}</li>
                    <li v-if="passwordRules.passwd_name" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_7}}</li>
                    <li v-if="passwordRules.passwd_name2" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_8}}</li>
                    <li v-if="passwordRules.passwd_letter" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_9}}</li>
                    <li v-if="passwordRules.passwd_letter2" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_10}}</li>
                  </ul>
                </div>
              </div>

            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="form3Visible = false">{{lan.cancel}}</el-button>
              <el-button type="primary" @click="reset3_submit">{{lan.sure}}</el-button>
            </div>
          </el-dialog>

          <el-dialog title="注册账号" :visible.sync="agreementVisible" width="80%" :append-to-body="true" >
            <div v-html="register_data.agreement"></div>
            <div slot="footer" class="dialog-footer">
              <el-button @click="agreementVisible = false">{{lan.cancel}}</el-button>
              <el-button type="primary" @click="show_register_dialog">同意</el-button>
            </div>
          </el-dialog>

          <el-dialog title="注册账号" :visible.sync="registerVisible" width="600px" :append-to-body="true" :close-on-click-modal="false">
            <el-form :model="register_form" size="small" :rules="register_form_rules" label-width="140px"  ref="register_form">
              <el-form-item label="邮件地址" prop="username">
                <el-input v-model="register_form.username" auto-complete="off" style="width:50%"></el-input>
                <span>@ <span>{{register_data.domain}}</span></span>
              </el-form-item>
              <el-form-item label="登录密码" prop="password">
                <el-input v-model="register_form.password" type="password" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item label="确认登录密码" prop="confirm_password">
                <el-input v-model="register_form.confirm_password" type="password" auto-complete="off"></el-input>
                <el-input  type="password" auto-complete="off" style="display:none"></el-input>
              </el-form-item>
              <el-form-item label="真实姓名" prop="realname">
                <el-input v-model="register_form.realname" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item label="英文名称" prop="engname">
                <el-input v-model="register_form.engname" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item label="工号" prop="eenumber">
                <el-input v-model="register_form.eenumber" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item label="手机号码" prop="mobile">
                <el-input v-model="register_form.mobile" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item label="所属部门" prop="department" >
                <el-cascader v-model="department_value" :props="props"
                  :options="register_data.departments"
                  change-on-select
                ></el-cascader>
              </el-form-item>
              <el-form-item label="备注" prop="remark">
                <el-input v-model="register_form.remark" type="textarea" :autosize="{ minRows: 2, maxRows: 5}"></el-input>
              </el-form-item>

              <div>
                <div>
                  <strong style="color: red">{{lan.COMMON_PASSWORD_NOTICE}}</strong>
                  <ul style="margin-left: 26px;">
                    <li style="list-style-type:circle;"> {{lan.COMMON_PASSWORD_NOTICE_1}} {{register_data.rules.passwd_size2}} {{lan.COMMON_PASSWORD_NOTICE_2}}</li>
                    <li v-if="register_data.rules.passwd_type==2" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_3}}</li>
                    <li v-if="register_data.rules.passwd_type==3" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_4}}</li>
                    <li v-if="register_data.rules.passwd_type==4" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_5}}</li>
                    <li v-if="register_data.rules.passwd_digital" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_6}}</li>
                    <li v-if="register_data.rules.passwd_name" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_7}}</li>
                    <li v-if="register_data.rules.passwd_name2" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_8}}</li>
                    <li v-if="register_data.rules.passwd_letter" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_9}}</li>
                    <li v-if="register_data.rules.passwd_letter2" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_10}}</li>
                  </ul>
                </div>
              </div>

            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="registerVisible = false">{{lan.cancel}}</el-button>
              <el-button type="primary" @click="do_register">注 册</el-button>
            </div>
          </el-dialog>

        </div>


      </div>

      <!--弹窗-->

    </div>

</template>
<script>
  import cookie from '@/assets/js/cookie';
  import lan from '@/assets/js/lan';
  import {login,resetSecret1,resetSecret2,resetSecret3,loginBefore,registerAgreement,register} from '@/api/api'
  const emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
  import router from '@/router'
  import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'
  export default {
    data() {
      let _this = this
      var validatePass = (rule, value, callback) => {
         // let reg =  /^(.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z]).*)|(.*(?=.{6,})(?=.*\d)(?=.*[A-Za-z])(?=.*[!@#$%^&*? ]).*)$/;
         let reg =  /^[\d]{6}$/;
        if (value === '') {
          callback(new Error(_this.lan.LAYOUT_INDEX_PASSWORD_RULE));
        } else{
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error(_this.lan.LAYOUT_INDEX_PASSWORD_RULE));
        } else if (value !== this.form3.new_password) {
          callback(new Error(_this.lan.LAYOUT_INDEX_TWO_INCONSISTENT_PASSWORDS));
        } else {
          callback();
        }
      };
      return {
        props:{
          value:'id',
          label: 'label',
          children: 'children',
        },
        domain_hash_id:[],
        department_value:[],
        register_data:{
          agreement:'',
          departments:[{
          value: 'zhinan',
          label: '指南',
          children: [
            {
              value: 'shejiyuanze',
              label: '设计原则',
              children: [{
                value: 'yizhi',
                label: '一致'
              }, {
                value: 'fankui',
                label: '反馈'
              }, {
                value: 'xiaolv',
                label: '效率'
              }, {
                value: 'kekong',
                label: '可控'
              }]
            }
          ],
        }],
          rules:{},
          domain:'',
        },
        show_agreement:false,
        agreementVisible:false,

        default_agreement:'<p><strong><span style="font-size:16px;">邮箱服务条款</span></strong></p>\n' +
          '<br />\n' +
          '<p>【注意】欢迎申请使用XXX公司提供的邮箱服务。请用户仔细阅读以下全部内容。如用户不同意本服务条款任意内容，请不要注册或使用邮箱服务。如用户通过进入注册程序并勾选“我同意”，即表示用户与XXX公司已达成协议，自愿接受本服务条款的所有内容。此后，用户不得以未阅读本服务条款内容作任何形式的抗辩。</p>\n' +
          '<p><strong>1、服务条款的确认和接纳</strong></p>\n' +
          '<p>邮箱服务相关软件的知识产权归XXX公司所有。XXX公司所提供的服务必须按照其发布的公司章程，服务条款和操作规则严格执行。本服务条款的效力范围及于XXX公司的一切产品和服务，用户在享受XXX公司任何单项服务时，应当受本服务条款的约束。</p>\n' +
          '<p>当用户使用XXX公司各单项服务时，用户的使用行为视为其对该单项服务的服务条款以及XXX公司在该单项服务中发出的各类公告的同意。</p>\n' +
          '<p><strong>2、邮箱服务简介</strong></p>\n' +
          '<p>XXX公司通过国际互联网络为用户提供各项服务。用户必须：</p>\n' +
          '<p>（1）提供设备，如个人电脑、手机或其他上网设备。</p>\n' +
          '<p>（2）个人上网和支付与此服务有关的费用。</p>\n' +
          '<p>考虑到邮箱服务的重要性，用户同意：</p>\n' +
          '<p>（1）提供及时、详尽及准确的个人资料。</p>\n' +
          '<p>（2）不断更新注册资料，符合及时、详尽准确的要求。所有原始键入的资料将引用为注册资料。</p>\n' +
          '<p>如果用户提供的资料不准确，不真实，不合法有效，XXX公司保留结束用户使用XXX公司各项服务的权利。用户同意，用户提供的真实准确的个人资料作为认定用户与帐号的关联性以及用户身份的唯一证据。</p>\n' +
          '<p><strong>3、服务条款的修改</strong></p>\n' +
          '<p>XXX公司有权在必要时通过在网页上发出公告等合理方式修改本服务条款以及各单项服务的相关条款。用户在享受各项服务时，应当及时查阅了解修改的内容，并自觉遵守本服务条款以及该单项服务的相关条款。用户如继续使用本服务条款涉及的服务，则视为对修改内容的同意；用户在不同意修改内容的情况下，有权停止使用本服务条款涉及的服务。</p>\n' +
          '<p><strong>4、服务的变更或中止</strong></p>\n' +
          '<p>XXX公司保留随时变更或中止服务的权利。用户同意XXX公司有权行使上述权利且不需对用户或第三方承担任何责任。</p>\n' +
          '<p><strong>5、用户隐私制度</strong></p>\n' +
          '<p>用户知悉并同意，为便于向用户提供更好的服务，XXX公司将在用户自愿选择服务或者提供信息的情况下收集用户的个人信息，并将这些信息进行整合。在用户使用XXX公司服务时，服务器会自动记录一些信息，包括但不限于URL、IP地址、浏览器类型、使用语言、访问日期和时间，等。为方便用户登录或使用XXX公司的服务，XXX公司在有需要时将使用cookies等技术，并将收集到的信息发送到对应的服务器。用户可以选择接受或者拒绝cookies。如用户选择拒绝cookies，则用户有可能无法登陆或使用依赖于cookies的服务或者功能。XXX公司收集的信息将成为XXX公司常规商业档案的一部分，且有可能因为转让、合并、收购、重组等原因而被转移到XXX公司的继任公司或者指定的一方。XXX公司同意善意使用收集的信息，且采取各项措施保证信息安全。</p>\n' +
          '<p>尊重用户个人隐私是XXX公司的一项基本政策。所以，作为对以上第2条个人注册资料分析的补充，XXX公司不会公开或透露用户的注册资料及保存在XXX公司各项服务中的非公开内容，除非XXX公司在诚信的基础上认为透露这些信息在以下几种情况是必要的：</p>\n' +
          '<p>（1）遵守有关法律规定，包括在国家有关机关查询时，提供用户的注册信息、用户在XXX公司的网页上发布的信息内容及其发布时间、互联网地址或者域名。</p>\n' +
          '<p>（2）保持维护XXX公司的知识产权和其他重要权利。</p>\n' +
          '<p>（3）在紧急情况下竭力维护用户个人和社会大众的隐私安全。</p>\n' +
          '<p>（4）根据本条款相关规定或者XXX公司认为必要的其他情况下。</p>\n' +
          '<p><strong>6、用户的帐号、密码和安全性</strong></p>\n' +
          '<p>用户一旦注册成功成为用户，用户将得到一个密码和帐号。如果用户未保管好自己的帐号和密码而对用户、XXX公司或第三方造成的损害，用户将负全部责任。另外，每个用户都要对其帐户中的所有活动和事件负全责。用户可随时改变用户的密码和图标，也可以结束旧的帐户重开一个新帐户。用户同意若发现任何非法使用用户帐号或安全漏洞的情况，有义务立即通告XXX公司。</p>\n' +
          '<p><strong>7、拒绝提供担保和免责声明</strong></p>\n' +
          '<p>用户明确同意使用XXX公司邮箱服务的风险由用户个人承担。XXX公司的邮箱帐号与服务以“现有”的状态提供给用户，XXX公司明确表示不提供任何类型的担保，不论是明确的或隐含的。XXX公司不担保服务一定能满足用户的要求，也不担保服务不会受中断，XXX公司对服务的及时性、安全性、真实性、出错发生都不作担保。XXX公司拒绝提供任何担保，包括信息能否准确、及时、顺利地传送。用户理解并接受下载或通过XXX公司产品服务取得的任何信息资料取决于用户自己，并由其承担系统受损、资料丢失以及其它任何风险。XXX公司对在服务网上得到的任何商品购物服务、交易进程、招聘信息，都不作担保。用户不会从XXX公司收到口头或书面的意见或信息，XXX公司也不会在这里作明确担保。</p>\n' +
          '<p><strong>8、免责条款</strong></p>\n' +
          '<p>XXX公司对直接、间接、偶然、特殊及继起的损害不负责任，这些损害来自：不正当使用产品服务，在网上购买商品或类似服务，在网上进行交易，非法使用服务或用户传送的信息有所变动。这些损害会导致XXX公司形象受损，所以XXX公司早已提出这种损害的可能性。</p>\n' +
          '<p>XXX公司对本项服务下涉及的境内外基础电信运营商的移动通信网络的故障、技术缺陷、覆盖范围限制、不可抗力、计算机病毒、黑客攻击、用户所在位置、用户关机或其他非XXX公司技术能力范围内的事因等造成的服务中断、用户发送的短信息的内容丢失、出现乱码、错误接收、无法接收、迟延接收不承担责任。</p>\n' +
          '<p><strong>9、禁止服务的商业化</strong></p>\n' +
          '<p>用户承诺，非经XXX公司同意，用户不能利用XXX公司各项服务进行销售或其他商业用途。如用户有需要将服务用于商业用途，应书面通知XXX公司并获得XXX公司的明确授权。</p>\n' +
          '<p><strong>10、用户管理</strong></p>\n' +
          '<p>用户独立承担其发布内容的责任。用户对服务的使用必须遵守所有适用于服务的地方法律、国家法律和国际法律。用户承诺：</p>\n' +
          '<p>（1）用户在XXX公司的网页上发布信息或者利用XXX公司的服务时必须符合中国有关法规，不得在XXX公司的网页上或者利用XXX公司的服务制作、复制、发布、传播以下信息：</p>\n' +
          '<p>(a) 违反宪法确定的基本原则的；</p>\n' +
          '<p>(b) 危害国家安全，泄露国家秘密，颠覆国家政权，破坏国家统一的；</p>\n' +
          '<p>(c) 损害国家荣誉和利益的；</p>\n' +
          '<p>(d) 煽动民族仇恨、民族歧视，破坏民族团结的；</p>\n' +
          '<p>(e) 破坏国家宗教政策，宣扬邪教和封建迷信的；</p>\n' +
          '<p>(f) 散布谣言，扰乱社会秩序，破坏社会稳定的；</p>\n' +
          '<p>(g) 散布淫秽、色情、赌博、暴力、恐怖或者教唆犯罪的；</p>\n' +
          '<p>(h) 侮辱或者诽谤他人，侵害他人合法权益的；</p>\n' +
          '<p>(i) 煽动非法集会、结社、游行、示威、聚众扰乱社会秩序的；</p>\n' +
          '<p>(j) 以非法民间组织名义活动的；</p>\n' +
          '<p>(k) 含有法律、行政法规禁止的其他内容的。</p>\n' +
          '<p>（2）用户在XXX公司的网页上发布信息或者利用XXX公司的服务时还必须符合其他有关国家和地区的法律规定以及国际法的有关规定。</p>\n' +
          '<p>（3）用户不得利用XXX公司的服务从事以下活动：</p>\n' +
          '<p>(a) 未经允许，进入计算机信息网络或者使用计算机信息网络资源的；</p>\n' +
          '<p>(b) 未经允许，对计算机信息网络功能进行删除、修改或者增加的；</p>\n' +
          '<p>(c) 未经允许，对进入计算机信息网络中存储、处理或者传输的数据和应用程序进行删除、修改或者增加的；</p>\n' +
          '<p>(d) 故意制作、传播计算机病毒等破坏性程序的；</p>\n' +
          '<p>(e) 其他危害计算机信息网络安全的行为。</p>\n' +
          '<p>（4）用户不得以任何方式干扰XXX公司的服务。</p>\n' +
          '<p>（5）用户不得滥用XXX公司邮箱服务，包括但不限于：利用XXX公司提供的邮箱服务发送垃圾邮件，利用XXX公司邮箱服务进行侵害他人知识产权或者合法利益的其他行为。</p>\n' +
          '<p>（6）用户应遵守XXX公司的所有其他规定和程序。</p>\n' +
          '<p>用户须对自己在使用XXX公司邮箱服务过程中的行为承担法律责任。用户承担法律责任的形式包括但不限于：对受到侵害者进行赔偿，以及在XXX公司首先承担了因用户行为导致的行政处罚或侵权损害赔偿责任后，用户应给予XXX公司等额的赔偿。用户理解，如果XXX公司发现其网站传输的信息明显属于上段第(1)条所列内容之一，依据中国法律，XXX公司有义务立即停止传输，保存有关记录，向国家有关机关报告，并且删除含有该内容的地址、目录或关闭服务器。</p>\n' +
          '<p>用户使用XXX公司电子公告服务，包括电子布告牌、电子白板、电子论坛、网络聊天室和留言板等以交互形式为上网用户提供信息发布条件的行为，也须遵守本条的规定以及XXX公司将专门发布的电子公告服务规则，上段中描述的法律后果和法律责任同样适用于电子公告服务的用户。若用户的行为不符合以上提到的服务条款，XXX公司将作出独立判断立即取消用户服务帐号。</p>\n' +
          '<p><strong>11、保障</strong></p>\n' +
          '<p>用户同意保障和维护XXX公司全体成员的利益，负责支付由用户使用超出服务范围引起的律师费用，违反服务条款的损害补偿费用，其它人使用用户的电脑、帐号而产生的费用。用户或者使用用户帐号的其他人在进行游戏过程中侵犯第三方知识产权及其他权利而导致被侵权人索赔的，由用户承担责任。</p>\n' +
          '<p><strong>12、结束服务</strong></p>\n' +
          '<p>用户或XXX公司可随时根据实际情况终止服务。XXX公司有权单方不经通知终止向用户提供某一项或多项服务；用户有权单方不经通知单方终止接受XXX公司的服务。</p>\n' +
          '<p>结束用户服务后，用户使用XXX公司邮箱服务的权利立即终止。从那时起，XXX公司不再对用户承担任何义务。</p>\n' +
          '<p>用户知道并同意，服务变更、中止与结束属于XXX公司商业决策之内容。用户不得因服务的变更、中止或者结束而要求XXX公司继续提供服务或者承担任何形式的赔偿责任，等。</p>\n' +
          '<p><strong>13、通知</strong></p>\n' +
          '<p>所有发给用户的通知都可通过电子邮件、常规的信件或在网站显著位置公告的方式进行传送。XXX公司将通过上述方法之一将消息传递给用户，告知他们服务条款的修改、服务变更、或其它重要事情。</p>\n' +
          '<p><strong>14、参与广告策划</strong></p>\n' +
          '<p>在XXX公司许可下用户可在他们发表的信息中加入宣传资料或参与广告策划，在XXX公司各项服务上展示他们的产品。任何这类促销方法，包括运输货物、付款、服务、商业条件、担保及与广告有关的描述都只是在相应的用户和广告销售商之间发生。XXX公司不承担任何责任，XXX公司没有义务为这类广告销售负任何一部分的责任。</p>\n' +
          '<p><strong>15、内容的所有权</strong></p>\n' +
          '<p>内容的定义包括：文字、软件、声音、相片、视频、图表；在广告中的全部内容；电子邮件系统的全部内容；XXX公司虚拟社区服务为用户提供的商业信息。所有这些内容均属于XXX公司，并受版权、商标、专利和其它财产所有权法律的保护。所以，用户只能在XXX公司和广告商授权下才能使用这些内容，而不能擅自复制、再造这些内容、或创造与内容有关的派生产品。</p>\n' +
          '<p><strong>16、法律</strong></p>\n' +
          '<p>本条款适用中华人民共和国的法律，并且排除一切冲突法规定的适用。</p>\n' +
          '<p>如出现纠纷，用户和XXX公司一致同意将纠纷交由广州市天河区人民法院管辖。</p>\n' +
          '<p><strong>17、信息储存及相关知识产权</strong></p>\n' +
          '<p>XXX公司对邮箱上所有服务将尽力维护其安全性及方便性，但对服务中出现的信息（包括但不限于用户发布的信息）删除或储存失败不承担任何责任。另外XXX公司保留判定用户的行为是否符合本服务条款的要求的权利，如果用户违背了本服务条款的规定，XXX公司有权中止或者终止对其XXX公司邮箱帐号的服务。</p>\n' +
          '<p>在XXX公司邮箱所含服务中，无论是用户原创或是用户得到著作权人授权转载的作品，用户上载的行为即意味着用户或用户代理的著作权人授权XXX公司对上载作品享有免费的不可撤销的永久的使用权和收益权，但用户或原著作权人仍保有上载作品的著作权。</p>\n' +
          '<p><strong>18、青少年用户特别提示</strong></p>\n' +
          '<p>青少年用户必须遵守全国青少年网络文明公约：</p>\n' +
          '<p>要善于网上学习，不浏览不良信息；要诚实友好交流，不侮辱欺诈他人；要增强自护意识，不随意约会网友；要维护网络安全，不破坏网络秩序；要有益身心健康，不沉溺虚拟时空。</p>\n' +
          '<p><strong>19、XXX公司邮箱帐号的有效期</strong></p>\n' +
          '<p>用户清楚知悉XXX公司邮箱帐号存在有效期，并同意不定时登录使用XXX公司邮箱帐号以延续其有效期。</p>\n' +
          '<p>(1)如果用户的XXX公司邮箱帐号下不存在XXX公司充值一卡通点数，而该帐号连续90天没有登录，则XXX公司有权终止用户使用该帐号下的邮箱并将邮箱中的内容删除，同时XXX公司有权删除该XXX公司邮箱帐号；</p>\n' +
          '<p>(2)如果用户的XXX公司邮箱帐号下存在XXX公司充值一卡通点数，而该帐号连续90天没有登录，则XXX公司有权终止用户使用该帐号下的邮箱并将邮箱中的内容删除；如该帐号连续540天没有登录，则该帐号下的XXX公司充值一卡通点数自该帐号最后一次登录之日起的第 540天24时到期作废，XXX公司有权删除该XXX公司邮箱帐号。</p>\n' +
          '<p>当帐号被删除后，该XXX公司邮箱帐号的所有资料以及与该XXX公司邮箱帐号相关的全部服务资料和数据（包括但不限于邮箱信息、XXX公司充值一卡通点数信息、游戏帐号信息，等）将同时删除，且不可恢复。该帐号名有可能会被新的用户注册。</p>\n' +
          '<p>登录XXX公司邮箱是指通过XXX公司邮箱帐号密码认证，包括但不限于如下方式：</p>\n' +
          '<p>(1)通过Web方式登录XXX公司邮箱；</p>\n' +
          '<p>(2)通过pop3方式收取该XXX公司邮箱下的邮箱中的信件；</p>\n' +
          '<p><strong>20、权利声明</strong></p>\n' +
          '<p>XXX公司不行使、未能及时行使或者未充分行使本条款或者按照法律规定所享有的权利，不应被视为放弃该权利，也不影响XXX公司在将来行使该权利。</p>\n' +
          '<p>在法律允许的最大范围内，XXX公司保留对本服务条款的最终解释权。</p>\n' +
          '<p>如用户对本条款内容有任何疑问，可拨打客服电话（010-00000000）进行查询。</p>\n',
        register_form:{
          username :'',
          password :'',
          confirm_password :'',
          realname :'',
          engname :'',
          eenumber :'',
          mobile :'',
          department :'',
          remark :'',
        },
        register_form_rules: {
          username: [
            { required: true, message: '请输入邮件地址', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入登录密码', trigger: 'blur' }
          ],
          confirm_password: [
            { required: true, message: '请确认密码', trigger: 'blur' }
          ],
          realname: [
            { required: true, message: '请输入真实姓名', trigger: 'blur' }
          ],
          department: [
            { required: true, message: '请选择所属部门', trigger: 'blur' }
          ],
        },
        registerVisible:false,
        rememberUserInfo:true,
        language:'zh',
        bgIndex:0,
        passwordRules:{},
        loginBeforeData:{
          "domain":"test.com",
          "name":"77777umail",
          "title":"11111111111",
          "is_domain":true,
          "domains":[[1,"test.com"],[33,"zsh1.com"],[31,"zsh.com"],[24,"domain2.com"],[25,"test.cn.com"],[26,"test1.cn.com"]],
          "is_icp":true,
          "icp_no":"dsfdsa",
          "icp_link":"dsa",
          "is_ssl":false,
          "login_logo":"/media/logo_5CrSq_20181213113208_763.jpg",
          "login_ads":[
            // {"image":"http://192.168.1.39:81/media/logo_FbIHh_20181213113253_180.jpg","link":"12"},
            // {"image":"http://192.168.1.39:81/media/logo_FbIHh_20181213113253_180.jpg","link":"1234"},
            // {"image":"http://192.168.1.39:81/media/logo_FbIHh_20181213113253_180.jpg","link":"12"}
            ]
        },
        reset1_show:false,
        form3Visible:false,
        form3:{
          carbled:'',
          new_carbled:'',
          new_password:'',
          confirm_password:'',
        },
        form3Rule:{
          new_password: [
            { validator:validatePass, trigger: 'blur' },
            // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
          confirm_password: [
            { validator:validatePass2, trigger: 'blur' },
            // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
        },
        formVisible:false,
        form:{
          code:'',
          code_label:'',
          carbled:'',
          q1:'',
          q2:'',
          q3:'',
          label_q1:'',
          label_q2:'',
          label_q3:'',
        }

        ,
        formRule:{
          code: [
            { required: true, message: '', trigger: 'blur' }
          ],
          q1: [
            { required: true, message: '', trigger: 'blur' }
          ],
          q2: [
            { required: true, message: '', trigger: 'blur' }
          ],
          q3: [
            { required: true, message: '', trigger: 'blur' }
          ]
        },
        rules:{
          username: [
            { required: true, message: '', trigger: 'blur' },
            // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '', trigger: 'blur' }
          ],
        },
        labelPosition: 'top',
        formLabelAlign: {
          username: '',
          password: ''
        },
        randB: ['url(../../assets/img/mainBg0.jpg)', 'url(../../assets/img/aside0.png)']
      };
    },
    methods: {
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
      do_register(){
        this.register_form.department = this.department_value[this.department_value.length-1]
        this.$refs['register_form'].validate(valid=>{
          if(valid){
            let obj = {
              username :'',
              password :this.register_form.password,
              confirm_password :this.register_form.confirm_password,
              realname :this.register_form.realname,
              engname :this.register_form.engname,
              eenumber :this.register_form.eenumber,
              mobile :this.register_form.mobile,
              department :this.register_form.department,
              remark :this.register_form.remark,
            };
            obj.username = this.register_form.username + '@'+this.register_data.domain
            register(obj).then(res=>{
              console.log(res)
              this.$message({
                type:'success',
                message:'账号 '+obj.username+' 注册成功！请耐心等待审核通过，即可使用申请账号登录!'
              })
               this.registerVisible = false;
              this.$refs['register_form'].resetFields()
            }).catch(err=>{
              console.log(err)
              let str = '';
              if(err.non_field_errors){
                str = err.non_field_errors[0]
              }
              this.$message({
                type:'error',
                message: str
              })
            })
          }else{
            return false;
          }
        })
      },
      show_agreement_dialog(){
        let param = {
          domain_id:  this.domain_hash_id[this.loginBeforeData.domain]
        }
        registerAgreement(param).then(res=>{
          console.log(res)
          if(!res.data.agreement || res.data.agreement == -1){
            this.register_data.agreement = this.default_agreement;
          }else{
            this.register_data.agreement = this.htmlDecodeByRegExp(res.data.agreement);
          }
          this.register_data.rules = res.data.rules;
          this.register_data.departments = res.data.departments;
          this.register_data.domain = res.data.domain;
          this.agreementVisible = true;
        }).catch(err=>{
          console.log(err);
        })
      },
      show_register_dialog(){
        this.agreementVisible = false;
        this.registerVisible = true;
      },
      changeLanguage(val){
        cookie.setCookie('webvue_language',val,365*10)
        this.$store.dispatch('setLanguageA',val)
        router.go(0)
      },
      changeDomain(val){
        console.log(val)
        let param = {
          domain:val
        }
        this.getLoginBefore(param)
      },
      getLoginBefore(param){
        loginBefore(param).then(res=>{
          let origin = window.location.origin  //window.location.origin  'http://192.168.1.39:81'
          this.loginBeforeData = res.data;
          this.loginBeforeData.login_logo = origin + this.loginBeforeData.login_logo;
          if(this.loginBeforeData.login_ads && this.loginBeforeData.login_ads[0]){
            this.loginBeforeData.login_ads[0].image = origin + this.loginBeforeData.login_ads[0].image;
          }
          if(!res.data.is_domain){
            this.loginBeforeData.domains = [[res.data.domain_id,res.data.domain]]
          }
          this.domain_hash_id = [];
          for(let i=0;i<this.loginBeforeData.domains.length;i++){
            this.domain_hash_id[this.loginBeforeData.domains[i][1]] = this.loginBeforeData.domains[i][0];
          }

          this.$store.dispatch('setLoginBeforeA',this.loginBeforeData);

          $('title').text(res.data.title)
        }).catch(err=>{
          console.log(err)
        })
      },
      reset3_submit(){
        this.$refs['reset3Form'].validate(valid=>{
          if(valid){
            let param = {
              carbled:this.form3.carbled,
              new_carbled:this.form3.new_carbled,
              new_password:this.form3.new_password,
              confirm_password:this.form3.confirm_password,
            }
            resetSecret3(this.form3).then(res=>{
              this.$message({
                type:'success',
                message:this.lan.COMMON_OPRATE_SUCCESS
              })
              this.form3Visible = false;
              this.$refs.reset3Form.resetFields();
            }).catch(err=>{
              let str = this.lan.COMMON_OPRATE_FAILED
              if(err.non_field_errors){
                str += err.non_field_errors[0]
              }
              this.$message({
                type:'error',
                message: str
              })
              console.log('第三步出错！',err)
            })
          }else{
            return false;
          }
        })
      },
      reset2_submit(){
        this.$refs['reset2Form'].validate(valid=>{
          if(valid){
            let param = {
              code:this.form.code,
              carbled:this.form.carbled,
              security_answer1:this.form.q1,
              security_answer2:this.form.q2,
              security_answer3:this.form.q3,
            }
            resetSecret2(param).then(res=>{
              this.formVisible = false;
              this.$refs.reset2Form.resetFields();
              this.form3.carbled = res.data.carbled;
              this.form3.new_carbled = res.data.new_carbled;
              this.passwordRules = res.data.rules
              this.form3Visible = true;
            }).catch(err=>{
              this.$message({
                type:'error',
                message:err.non_field_errors[0]
              })
            })
          }else{
            return false;
          }
        })
      },
      getLabel(c,b){
        let str = ''
        if(c==1){
         str = this.lan.CONMON_PASSWORD_SECURITY_QD1
        }else if(c==2){
          str = this.lan.CONMON_PASSWORD_SECURITY_QD2
        }else if(c==3){
          str = this.lan.CONMON_PASSWORD_SECURITY_QD3
        }else if(c==4){
          str = this.lan.CONMON_PASSWORD_SECURITY_QD4
        }else if(c==5){
          str = this.lan.CONMON_PASSWORD_SECURITY_QD5
        }else if(c==6){
          str = this.lan.CONMON_PASSWORD_SECURITY_QD6
        }else if(c==7){
          str = this.lan.CONMON_PASSWORD_SECURITY_QD7
        }else if(c==8){
          str = this.lan.CONMON_PASSWORD_SECURITY_QD8
        }else if(c=='custom'){
          str = b
        }
        return str;
      },
      forget(){
        this.reset1_show = true;
        this.$prompt(this.lan.MAILBOX_COM_COMPOSE_INPUT_EMAIL, this.lan.reset_password, {
          confirmButtonText: this.lan.sure,
          // dangerouslyUseHTMLString: true,
          cancelButtonText: this.lan.COMMON_BUTTON_CANCELL,
          inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
          inputErrorMessage: this.lan.CALENDAR_PAGE_SET_MAIL_TYPE
        }).then(({ value }) => {
          this.reset1_show = false;
          resetSecret1({username:value}).then(res=>{
            this.form.carbled = res.data.carbled;
            this.form.code_label = res.data.code;
            this.form.label_q1 = this.getLabel(res.data.security_question1,res.data.security_custom1);
            this.form.label_q2 = this.getLabel(res.data.security_question2,res.data.security_custom2);
            this.form.label_q3 = this.getLabel(res.data.security_question3,res.data.security_custom3);
            this.formVisible = true;
          }).catch(err=>{
            this.$message({
              type:'error',
              message:err.non_field_errors[0]
            })
          })
        }).catch(() => {

          this.reset1_show = false;
        });
      },
      login: function () {
        var that = this;
        this.$refs['loginForm'].validate((valid) => {
          if (valid) {
            let str = this.formLabelAlign.username;
            if(!emailReg.test(this.formLabelAlign.username)){
              str +='@'+ this.loginBeforeData.domain;
            }
            login({"username": str, "password": this.formLabelAlign.password})
            .then((response) => {
              if(response.data.token){
                cookie.setCookie('name', str, 7);
                cookie.setCookie('token', response.data.token, 7);
                cookie.delCookie('locked')
                // 设置联系人的初始值
                window.sessionStorage.clear();
                that.$store.dispatch('setInfo');
                if(this.rememberUserInfo){
                  localStorage['userName'] = str
                }else{
                  localStorage['userName'] = ''
                }
                that.$router.push('/mailbox')
              }
              if(response.data.uuid_string){
                this.$router.push({
                  path:'/twofactor_login',
                  query:{
                    uuid_string:response.data.uuid_string,
                    mail:str,
                    totp:response.data.has_totp,
                    phone:response.data.has_phone,
                    bi:this.bgIndex,
                    rememberUserInfo:this.rememberUserInfo
                  }
                })
                // this.twofactorList = response.data;
              }

            }).catch(err=>{
              let str = '';
              if(err.non_field_errors){
                str = err.non_field_errors[0]
              }
              that.$message({message:this.lan.LOGIN_ERROR+str,type:'error'});
            });
          } else {
            return false;
          }
        });

      },
      open(str) {
        this.$alert(str, this.lan.COMMON_BUTTON_CONFIRM_NOTICE, {
          confirmButtonText: this.lan.COMMON_BUTTON_CONFIRM,
          // callback: action => {
          //     this.$message({
          //     type: 'info',
          //     message: `action: ${ action }`
          //     });
          // }
        })
      },
      test: function () {
        var apiUrl = 'http://192.168.1.24:9090/ajax_get_captcha';
        this.$http.post('/api/login/', {
          "username": "system@test.com",
          "password": "1QAZ2wsx"
        }).then((data) => {}, (data) => console.log(data));
      }
    },
    mounted: function () {

      // this.test();
      // 去掉记住用户名和密码
      // this.formLabelAlign.username = cookie.getCookie('rememberName');
      // this.formLabelAlign.password = cookie.getCookie('rememberPwd');

      // this.$nextTick(()=>{
      //   this.table_width = this.$refs.login_bg.getBoundingClientRect().width-this.$refs.aside.getBoundingClientRect().width-40
      //   // this.read_height = (this.$refs.box_height.getBoundingClientRect().height-83 )+'px'
      // })

    },
    computed: {
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
        this.formRule = {
          code: [
            { required: true, message: lang.placeholder_validation_code, trigger: 'blur' }
          ],
          q1: [
            { required: true, message: lang.LOGIN_RULE1, trigger: 'blur' }
          ],
          q2: [
            { required: true, message: lang.LOGIN_RULE1, trigger: 'blur' }
          ],
          q3: [
            { required: true, message: lang.LOGIN_RULE1, trigger: 'blur' }
          ]
        }
        this.rules = {
          username: [
            { required: true, message: lang.placeholder_user_name, trigger: 'blur' },
            // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
          password: [
            { required: true, message: lang.LAYOUT_INDEX_PASSWORD_RULE, trigger: 'blur' }
          ],
        }
        return lang

      }
      // rememberUserInfo: {
      //   get: function () {
      //     return this.$store.state.rememberUserInfo
      //   },
      //   set: function () {
      //     this.$store.dispatch('setMember');
      //   }
      // }
    },
    created: function () {
      // setInterval(()=>{
      //   this.bgIndex ++;
      //   if(this.bgIndex >=4){
      //     this.bgIndex = 0
      //   }
      // },2000)
      console.log()
      if(localStorage['userName']=='' || !localStorage['userName']){
        this.rememberUserInfo = false;
      }else{
        this.rememberUserInfo = true;
        this.formLabelAlign.username = localStorage['userName']
      }

      var lang = cookie.getCookie('webvue_language')
      if(lang){
        cookie.setCookie('webvue_language',lang,365*10)
      }else{
        let JsSrc =(navigator.language || navigator.browserLanguage).toLowerCase();
        if(JsSrc.indexOf('zh')>=0)
        {
           // 假如浏览器语言是中文
          cookie.setCookie('webvue_language','zh-hans',365*10)
          if(JsSrc=='zh-tw'){
            cookie.setCookie('webvue_language','zh-tw',365*10)
          }
        }
        else if(JsSrc.indexOf('en')>=0)
        {
            // 假如浏览器语言是英文
          cookie.setCookie('webvue_language','en',365*10)
        }
        else
        {
           // 假如浏览器语言是其它语言
          cookie.setCookie('webvue_language','zh-hans',365*10)
        }
      }
      this.$store.dispatch('setLanguageA',cookie.getCookie('webvue_language'))
      this.language = cookie.getCookie('webvue_language');


      this.bgIndex = Math.floor(Math.random()*4)
      this.getLoginBefore()
      var lett = this;
      if(lett.$route.name && lett.$route.name == 'login'){
        document.onkeydown = function (e) {

          var key = e.keyCode;
          if (key == 13) {
            if( lett.reset1_show || lett.formVisible || lett.form3Visible ){

            }else{
              lett.login();
            }
          }
        }
      }
    }
  }
</script>
<style>
  #login_bg .el-form-item__label{
    width:100%;
  }
  #login_bg>.main{
    position: absolute;
    width: 100%;
    height: 100%;
  }
  #login_bg .main>.content {
    position: absolute;
    top: 0;
    right: 36%;
    left: 0;
    bottom: 0;
    overflow: hidden;
  }
  .login_logo{
    padding:20px;
    display:inline-block
  }
  .loginForm{
    margin-bottom:20px;
  }
  #login_bg{
    width:100%;

    height:100%;
    background-image: url(../../assets/img/mainBg0.jpg);
    /* background-image: url(../assets/img/login_right.png); */
    background-size: cover;
    background-position:right bottom;
  }
  #login_bg.bg1{
    background-image: url(../../assets/img/mainBg1.jpg);
  }
  #login_bg.bg2{
    background-image: url(../../assets/img/mainBg2.jpg);
  }
  #login_bg.bg3{
    background-image: url(../../assets/img/mainBg3.jpg);
  }
  body{
    width:100%;
    height:100%;
    /* background:url(../assets/img/mainbg0.jpg); */
    background-size: cover;
  }
  .text-center{
    text-align:center;
  }
  #login_box{
    background:rgba(255,255,255,1);
    /* margin:150px auto; */
    /* width:400px; */
    border:1px solid #007ACC;
    padding:20px;
    box-shadow: 0 0 10px #007ACC;
    border-radius: 5px;
    /* display: none; */
  }
  .aside-blur {
    position: absolute;
    top: 0;
    right: 0;
    width: 36%;
    bottom: 0;
    overflow: hidden;
    transition: width 0.3s ease-out;
    -webkit-background-size: cover;
    -moz-background-size: cover;
    -o-background-size: cover;
    background-size: cover;
    background-position: right bottom;
    /*background-image: url(../../assets/img/aside0.png);*/
    background:rgba(0,0,0,0.15);
    background-repeat: no-repeat;
    background-attachment: fixed;
  }
  .aside {
    position: absolute;
    top: 0;
    right: 0;
    width: 36%;
    bottom: 0;
    transition: width 0.3s ease-out;
  }
  .loginArea {
    position: absolute;
    top: 20%;
    /*left: 23%;*/
    /*width: 54%;*/
    left:0;
    right:0;
  }
  .loginArea .loginType {
    display: table;
    width: 100%;
    line-height: 40px;
    margin-bottom: 8px;
  }
  .content-wrapper {
    position: relative;
  }
  .viceLogo {
    position: absolute;
    width: 74%;
    left: 13%;
    top: 13%;
    text-align: center;
    display: none;
  }
  .weather {
    position: absolute;
    /* left: 23%; */
    top: 40px;
    /* width: 54%; */
    font-size: 13px;
    line-height: 36px;
    display: table;
  }
  .f-fl {
    float: left;
  }
  .f-fr {
    float: right;
  }
  .loginType a:last-child {
    margin-right: 0;
  }
  .normalForm [logintype="normalForm"], .ssl [logintype="ssl"] {
    color: #fff;
    font-weight: bold;
  }

  .loginType a {
    font-size: 14px;
    margin-right: 16px;
  }
  .loginArea .locale {
    position: relative;
    cursor: pointer;
    font-size: 14px;
  }
  .loginArea .locale {
    position: relative;
    cursor: pointer;
    font-size: 14px;
  }
  .u-menu-hidden {
    display: none;
  }

  .u-menu {
    position: absolute;
    z-index: 100;
    top: 100%;
    left: -30px;
    line-height: 1.5;
    margin: -5px 0 0;
    padding: 4px 0;
    border: 1px solid #ddd;
    border-radius: 2px;
    max-height: 300px;
    overflow: auto;
    background: #fff;
    list-style: none;
    text-align: left;
    opacity: 0;
    transition: opacity .1s ease-out,margin-top .1s ease-out;
  }
  .u-menu li {
    position: relative;
  }
  .loginType a:last-child {
    margin-right: 0;
  }

  @media (min-height: 1080px){
    .locale li a {
      padding-left: 30px;
    }
  }

  @media (min-height: 1080px)
  {
    .u-menu li a {
      padding: 13px 30px 13px 43px;
    }
  }
  .locale li a {
    padding-left: 30px;
  }
  .u-menu li a {
    display: block;
    margin: -1px 0;
    overflow: hidden;
    word-wrap: normal;
    white-space: nowrap;
    text-overflow: ellipsis;
    color: #333;
    text-decoration: none;
    padding: 12px 30px 12px 43px;
  }
  .u-menu a {
    font-size: 14px;
  }
  .copyright {
    position: absolute;
    bottom: 30px;
    left: 50px;
    color:#fff;
    font-style: normal;
  }
  .version {
    position: absolute;
    top: 20%;
    left: 0;
    right: 0;
    text-align: center;
    /* background: url(../assets/img/login_center.png) 50% 50%; */
  }

</style>

