<template>
  <div class="mltabview-content">
    <div  class="mltabview-panel">
      <div class="m-mllist" v-loading="fullscreenLoading" v-if="$store.getters.getSearchmailData.data.total>0">
        <div class="list-bg"></div>
        <div class="m-mllist-row">
          <div class="toolbar" style="background:#fff;"
               element-loading-spinner="el-icon-loading"
               element-loading-background="rgba(0, 0, 0, 0.6)" >
                            <span class=" f-fr j-setting">
                            <el-button  icon="el-icon-setting" circle></el-button></span>

            <!--<el-button size="mini" @click="selectAll" type="primary">-->
            <!--{{is_checked?'取消全选':'全选'}}-->
            <!--&lt;!&ndash;<el-checkbox @change="selectAll" :checked="is_checked" class="check_btn"></el-checkbox>&ndash;&gt;-->
            <!--</el-button>-->

            <!--排序-->
            <el-dropdown @command="orderHandleCommand" placement="bottom-start" trigger="click" v-if="false">
              <el-button  size="small" plain>
                <span>{{lan.MAILBOX_COM_INNERBOX_SORT}}</span>
                <i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item v-for="item in orderItems" :key="item.id" class="dropdown_item" :class="{ active: orderCheckIndex==item.id }"
                                  :divided="item.divided" :command="item">
                  <b><i class="el-icon-check vibility_hide" :class="{ vibility_show: orderCheckIndex==item.id }"></i> </b>
                  {{ item.text}}</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>

            <!--查看-->

            <el-dropdown @command="viewHandleCommand" trigger="click" v-if="false">
              <el-button  size="small" plain >
                <span>{{lan.MAILBOX_COM_INNERBOX_SEE}}</span>
                <i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item v-if="!item.children" v-for="(item,k) in viewItems" :key="k" class="dropdown_item"
                                  :command="item.id" :divided="item.divided" :class="{ active: viewCheckIndex===item.id }">
                  <b><i class="el-icon-check vibility_hide" v-if="!item.classN" :class="{ vibility_show: viewCheckIndex===item.id }"></i> </b><i :class="item.classN"></i>
                  {{ item.text}}
                </el-dropdown-item>
                <el-dropdown-item class="dropdown_item" v-else="item.children" :divided="item.divided">
                  <el-dropdown @command="viewHandleCommand"  placement="right-start">
                                      <span class="el-dropdown-link">
                                        <b><i class="el-icon-check vibility_hide" :class="item.classN"></i> </b>
                                      {{item.text}}<i class="el-icon-arrow-right el-icon--right"></i>
                                      </span>
                    <el-dropdown-menu slot="dropdown">
                      <el-dropdown-item  v-for="(c,k) in item.children" :key="k" class="dropdown_item" :command="c.id">
                        <i class="iconfont icon-iconflatcolor" :class="c.classN"></i> {{c.text}}
                      </el-dropdown-item>

                    </el-dropdown-menu>

                  </el-dropdown>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>

            <!-- 更多按钮 -->
            <div v-if="multipleSelection.length>0" class="inline_block">
              <el-button  size="small" plain @click="deleteMailById">
                {{lan.COMMON_BUTTON_DELETE}}
              </el-button>

              <el-dropdown @command="moveHandleCommand" trigger="click" v-if="boxId!='Drafts'">
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
                  <el-dropdown-item v-if="boxId!='Drafts'||item.id==6||item.id==7||item.id==8" v-for="item in moreItems" :key="item.id" class="dropdown_item" :class="{ active: moreCheckIndex===item.id }"
                                    :divided="item.divided" :command="item">
                    <b><i class="el-icon-check vibility_hide" :class="{ vibility_show: moreCheckIndex===item.id }"></i> </b>
                    {{ item.text}}</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>

            </div>

            <!--刷新-->
            <el-button  size="small" plain @click="refresh">
              {{lan.MAILBOX_COM_INNERBOX_REFRESH}}  <!-- <i class="el-icon-refresh el-icon--right"></i> -->
            </el-button>


          </div>

          <div class="mail-totals j-mail-totals" v-if="multipleSelection.length==0" style="line-height: 36px;height:38px;">

            <div class="totals-info">
              <!--<span style="color:green;font-size:14px;">{{$store.getters.getSearchmailData.searchtype=='keyword'?'关键字包含 "'+$store.getters.getSearchmailData.keyword:$store.getters.getSearchmailData.searchtype=='sender'?'发件人包含'+$store.getters.getSearchmailData.keyword:$store.getters.getSearchmailData.searchtype=='subject'?'主题包含'+$store.getters.getSearchmailData.keyword:$store.getters.getSearchmailData.searchtype=='attach'?'附件名包含'+$store.getters.getSearchmailData.keyword:'高级搜索'}}</span>-->
              <el-tooltip class="item" effect="light" :content="search_desc" placement="bottom-start">
                <el-button type="text">搜索条件</el-button>
              </el-tooltip>
              搜索结果：{{totalCount}} 封邮件

              <el-pagination style="float:right;text-align:right;padding:4px;height:32px;"
                             @size-change="handleSizeChange"
                             @current-change="handleCurrentChange"
                             background
                             v-if="totalCount>0"
                             :current-page="currentPage"
                             :page-sizes="[10, 20, 50,100]"
                             :page-size="pageSize"
                             layout="total, prev, slot, next, jumper"
                             :total="totalCount">
                  <span> {{currentPage+' / '+Math.ceil(totalCount/pageSize)}}</span>
              </el-pagination>

            </div>
          </div>
          <div class="j-select-count select-count" v-if="multipleSelection.length>0" style="line-height: 36px;height:38px">
            <span class="j-desc desc">{{lan.MAILBOX_COM_INNERBOX_HAVE_CHOSEN}} {{multipleSelection.length}} {{lan.MAILBOX_COM_INNERBOX_SEAL_SELECTED}}</span>
            <a class="j-cancel cancel" href="#" @click="noSelect">{{lan.COMMON_BUTTON_CANCELL}}</a>

            <el-pagination style="float:right;text-align:right;padding:4px;height:32px;"
                           @size-change="handleSizeChange"
                           @current-change="handleCurrentChange"
                           background
                           v-if="totalCount>0"
                           :current-page="currentPage"
                           :page-sizes="[10, 20, 50,100]"
                           :page-size="pageSize"
                           layout="total, prev, slot, next, jumper"
                           :total="totalCount">
                <span> {{currentPage+' / '+Math.ceil(totalCount/pageSize)}}</span>
            </el-pagination>
          </div>
        </div>
        <div class="m-mllist-row mllist-list-row">
          <div class="j-module-content j-maillist mllist-list u-scroll">
            <div class="table_box" style="height:100%">
              <el-table  :show-header="true" ref="innerTable" height="100%" :data="listData_new" style="width: 100%;height:100%;background:transparent" class="vertical_align_top maillist" v-loading="loading"
                         highlight-current-row  @cell-mouse-enter="hoverfn" @cell-mouse-leave="noHover" @row-click="rowClick" @cell-click="cellClick"
                         @select-all="selectAllTable"    @selection-change="handleSelectionChange"  :header-cell-style="{background:'#f0f1f3'}"
                         :span-method="arraySpanMethod"
              >
                <!--:span-method="arraySpanMethod"-->
                <el-table-column
                  type="selection"
                  width="46"
                  label=""
                  :selectable="selectablee"
                >
                </el-table-column>
                <el-table-column width="110" class-name="flag_btn">
                  <template slot-scope="scope">

                    <div class="mainMsg" :class="{hoverStyle:scope.row.uid==hoverIndex}" v-if="!scope.row.is_header">
                      <span class="read_bg" :class="scope.row.flagbg_class" :title="scope.row.flagStr"></span>
                      <i :title="lan.MAILBOX_COM_INNERBOX_ENCLOSURE" v-if="scope.row.flags && scope.row.flags.join().indexOf('umail-attach')>=0&&!scope.row.is_move" class="iconfont icon-attachment" style="color:#777;"></i>
                      <b class="is_red" :title="lan.MAILBOX_COM_INNERBOX_URGENT_MAIL" v-if="scope.row.flags && scope.row.flags.join().indexOf('umail-emergent')>=0&&!scope.row.is_move">!</b>
                      <el-dropdown trigger="click" @command="signHandleCommand_new($event,scope.row)" v-if="!scope.row.is_move">
                                      <span class="el-dropdown-link" :title="lan.MAILBOX_COM_INNERBOX_SET_FLAG">

                                        <i class="iconfont icon-iconflat" v-if="!scope.row.flagged" style="cursor:pointer;"></i><i class="iconfont icon-iconflatcolor" v-if="scope.row.flagged" style="color:#c00;cursor:pointer;" :class="scope.row.color"></i><i class="el-icon-arrow-down el-icon--right" style="cursor:pointer;"></i>
                                      </span>
                        <el-dropdown-menu slot="dropdown">
                          <el-dropdown-item  v-for="(c,k) in flagsData" :key="k" class="dropdown_item" :command="c">
                            <i class="iconfont icon-iconflatcolor" :class="[c.classN,{'icon-iconflat':k==flagsData.length-1}]" ></i> {{c.text}}
                          </el-dropdown-item>

                        </el-dropdown-menu>
                      </el-dropdown>

                    </div>
                    <div v-if="scope.row.is_header" style="cursor:pointer;">
                      <div style="font-weight:bold;font-size:14px;">
                        <span>{{scope.row.title}}</span>
                        <span>({{scope.row.count}})</span>
                      </div>
                    </div>
                  </template>
                </el-table-column>

                <!--<el-table-column width="80">-->
                <!--<template slot-scope="scope">-->
                <!--<b class="is_red" v-if="scope.row.flags && scope.row.flags.join().indexOf('umail-emergent')>=0">!</b>-->
                <!--<i v-if="scope.row.flags && scope.row.flags.join().indexOf('umail-attach')>=0" class="iconfont icon-attachment" style="color:#777;"></i>-->
                <!--<span class="read_bg" :class="{unseen:!scope.row.isread,answered:scope.row.flags.join().indexOf('Answered')>=0,forward:scope.row.flags.join().indexOf('umail-forword')>=0}" :title="scope.row.flagStr"></span>-->
                <!--</template>-->
                <!--</el-table-column>-->

                <el-table-column width="180" :label="lan.COMMON_SENDER">
                  <template slot-scope="scope">
                    <div class="info-summary" :class="scope.row.color">
                      <p class="summary-text">
                        <span class="fromto from" v-if="scope.row.mfrom" :class="{flagged:scope.row.flagged,unseen:!scope.row.isread,'line-through': scope.row.is_move}" :title="scope.row.mfrom[1]+' <'+scope.row.mfrom[0]+'>'" style="font-size:14px;">{{scope.row.mfrom[1]}} <{{scope.row.mfrom[0]}}></span>
                        <!--<span class="fromto">:</span>-->
                        <!--<span class="summary">-->
                        <!--sdajpofjsdfhup测试-->
                        <!--</span>-->
                      </p>
                    </div>
                  </template>
                </el-table-column>

                <el-table-column prop="subject"  :label="lan.COMMON_SUBJECT2" >
                  <template slot-scope="scope">
                    <div class="clear mainMsg" style="font-size:16px;" :class="[{flagged:scope.row.flagged,unseen:!scope.row.isread},scope.row.color]">
                                  <span class="fl_l subject_hover" style="width:96%;overflow: hidden;white-space: nowrap;text-overflow: ellipsis;" @click.stop.prevent="readMail(scope.row)" :title="scope.row.subject||''" :class="{'line-through':scope.row.is_move}">
                                    <!--<span v-if="scope.row.flags.join().indexOf('umail-burn')>=0">{{lan.MAILBOX_COM_COMPOSE_IS_BURN}}: </span>-->
                                    <span class="is_burn_img" :title="lan.MAILBOX_COM_COMPOSE_IS_BURN" v-if="scope.row.flags.join().indexOf('umail-burn')>=0"></span>
                                   <span style="">{{'['+scope.row.folder+'] '}}</span> {{scope.row.subject|| lan.MAILBOX_NO_SUBJECT}}</span>
                    </div>
                    <div class="info-summary" :class="scope.row.color" v-if="false">
                      <p class="summary-text">
                        <span class="fromto from" v-if="scope.row.mfrom">{{scope.row.mfrom[1]}} <{{scope.row.mfrom[0]}}></span>

                      </p>
                    </div>
                  </template>
                </el-table-column>

                <el-table-column class="plan_style" prop="date" :label="lan.COMMON_TIME"   :width="$store.getters.getIsSwtime?180:160"  >
                  <template slot-scope="scope">
                    <div class="plan_style" v-if="!scope.row.is_header">
                      {{(scope.row.date ||scope.row.internaldate).replace('T',' ')}}
                    </div>
                  </template>
                </el-table-column>
                <el-table-column class="plan_style" prop="size" :label="lan.COMMON_SIZE"   width="100">
                  <template slot-scope="scope">
                    <div class="plan_style">
                      {{scope.row.size | mailsize}}
                      <!--<p style="padding-left:10px" v-if="scope.row.flags && scope.row.flags.join().indexOf('umail-attach')>=0" >-->
                      <!--<i class="iconfont icon-attachment"></i>-->
                      <!--</p>-->
                    </div>
                  </template>
                </el-table-column>
              </el-table>

            </div>
          </div>

        </div>
      </div>
      <div v-if="$store.getters.getSearchmailData.data.total==0" style="margin:0 20px;font-size:14px;">
        <h3 style="margin:30px 0 10px 0;font-size:24px;font-weight:normal;">
          没有搜索到

          <span v-if="$store.getters.getSearchmailData.params.keyword && $store.getters.getSearchmailData.params.keyword != ''">【关键字包含 <span class="mark">"{{$store.getters.getSearchmailData.params.keyword}}"</span>】</span>
          <span v-if="$store.getters.getSearchmailData.params.subject && $store.getters.getSearchmailData.params.subject != ''">【主题包含 <span class="mark">"{{$store.getters.getSearchmailData.params.subject}}"</span>】</span>
          <span v-if="$store.getters.getSearchmailData.params.attach && $store.getters.getSearchmailData.params.attach != ''">【附件名包含 <span class="mark">"{{$store.getters.getSearchmailData.params.attach}}"</span>】</span>
          <span v-if="$store.getters.getSearchmailData.params.folder && $store.getters.getSearchmailData.params.folder != ''">【所在文件夹范围为 <span class="mark">"{{$store.getters.getSearchmailData.params.folder_desc}}"</span>】</span>
          <span v-if="$store.getters.getSearchmailData.params.sender && $store.getters.getSearchmailData.params.sender != ''">【发件人为 <span class="mark">"{{$store.getters.getSearchmailData.params.sender}}"</span>】</span>
          <span v-if="$store.getters.getSearchmailData.params.recipient && $store.getters.getSearchmailData.params.recipient != ''">【收件人为 <span class="mark">"{{$store.getters.getSearchmailData.params.recipient}}"</span>】</span>
          <span v-if="$store.getters.getSearchmailData.params.date && $store.getters.getSearchmailData.params.date != ''">【发信时间范围为 <span class="mark">"{{$store.getters.getSearchmailData.params.date_desc}}"</span>】</span>
          <span v-if="$store.getters.getSearchmailData.params.size && $store.getters.getSearchmailData.params.size != ''">【邮件大小为 <span class="mark">"{{$store.getters.getSearchmailData.params.size_desc}}" </span>】</span>
          的邮件
        </h3>
        <p>您可以：</p>
        <p>1. 更换关键字重新搜索</p>
        <p>2. 使用高级搜索，通过其他邮件特征进行搜索</p>

      </div>
    </div>

  </div>
</template>
<script>
  import lan from '@/assets/js/lan';
  import axios from 'axios';
  import {getMailMessage,moveMails,getFloder,getFloderMsg,deleteMail,messageFlag,readMail,rejectMessage,pruneMessage,zipMessage,messageExpunge,mailSearch} from "@/api/api";

  import router from '@/router'

  export default {
    name:'Innerbox',
    props:{
      floderResult:{
        type:Array,
        default: []
      }
    },

    data() {
      return {
        is_checked:false,
        listData:[],
        listData_new:[],
        flagsData:[
          {flags:'\\flagged',action:'add',text:' ',classN:'redcolor'},
          {flags:'umail-green',action:'add',text:' ',classN:'flag-green'},
          {flags:'umail-orange',action:'add',text:' ',classN:'flag-orange'},
          {flags:'umail-blue',action:'add',text:' ',classN:'flag-blue'},
          {flags:'umail-pink',action:'add',text:' ',classN:'flag-pink'},
          {flags:'umail-cyan',action:'add',text:' ',classN:'flag-cyan'},
          {flags:'umail-yellow',action:'add',text:' ',classN:'flag-yellow'},
          {flags:'umail-purple',action:'add',text:' ',classN:'flag-purple'},
          {flags:'umail-gray',action:'add',text:' ',classN:'flag-gray'},
          {flags:'\\flagged',text:'',action:'remove'},
        ],
        fullscreenLoading:false,
        reject_is_delete:false,
        boxId:'INBOX',
        curr_folder:'',
        searchForm: {
          from: '',
          subject: '',
          body: ''
        },
        loading: false,
        sort:'',
        search:'',
        hoverIndex:'',
        totalAllCount:0,
        multipleSelection:[],
        tableData: [],
        unreadCount:0,
        totalCount:0,
        currentPage:1,
        pageSize:20,
        checkIndex:'',
        checkAll:false,
        checkItems:[
          {id:0,text:'',divided:false},
          {id:1,text:'',divided:true},
          {id:2,text:'',divided:false},
          {id:3,text:'',divided:false},
          {id:4,text:'',divided:false},
          {id:5,text:'',divided:false},
        ],
        orderCheckIndex:'',
        orderItems:[
          {id:0,text:'',divided:false,sort:'REVERSE ARRIVAL'},
          {id:1,text:'',divided:false,sort:'ARRIVAL'},
          {id:3,text:'',divided:true,sort:'FROM'},
          {id:2,text:'',divided:false,sort:'REVERSE FROM'},
          {id:4,text:'',divided:true,sort:'REVERSE SUBJECT '},
          {id:5,text:'',divided:false,sort:'SUBJECT '},
          {id:8,text:'',divided:true,sort:'SIZE'},
          {id:9,text:'',divided:false,sort:'REVERSE SIZE'},
        ],

        viewCheckIndex:'',
        viewItems:[
          {id:'',text:'',divided:false},
          {id:'unseen',text:'',divided:false},
          {id:'seen',text:'',divided:false},
          {id:'flagged',text:'',divided:true,classN:'iconfont icon-iconflatcolor redcolor'},
          {id:'other',text:'',divided:false,children:[
              {id:'KEYWORD umail-green',text:'',classN:'flag-green'},
              {id:'KEYWORD umail-orange',text:'',classN:'flag-orange'},
              {id:'KEYWORD umail-blue',text:'',classN:'flag-blue'},
              {id:'KEYWORD umail-pink',text:'',classN:'flag-pink'},
              {id:'KEYWORD umail-cyan',text:'',classN:'flag-cyan'},
              {id:'KEYWORD umail-yellow',text:'',classN:'flag-yellow'},
              {id:'KEYWORD umail-purple',text:'',classN:'flag-purple'},
              {id:'KEYWORD umail-gray',text:'',classN:'flag-gray'}
            ]},
          {id:'unflagged',text:'',divided:false,classN:'iconfont icon-iconflat'},
          {id:'ANSWERED',text:'',divided:true,classN:'iconfont icon-iconback greencolor'},
          {id:'KEYWORD umail-forword',text:'',divided:false,classN:'iconfont icon-Forward greencolor'},
        ],
        moveCheckIndex:'',

        signItems:[
          {id:0,flags:'\\Seen',text:'',divided:false,action:'add'},
          {id:1,flags:'\\Seen',text:'',divided:false,action:'remove'},
          {id:2,flags:'\\flagged',text:'',divided:true,action:'add',classN:'iconfont icon-iconflatcolor redcolor'},
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
        moreCheckIndex:'',
        moreItems:[
          {id:0,text:'',divided:false,checkone:true},
          {id:1,text:'',divided:false,checkone:true},
          {id:2,text:'',divided:true,checkone:true},
          {id:3,text:'',divided:false,checkone:true},
          {id:4,text:'',divided:true,checkone:false},
          {id:5,text:'',divided:true,checkone:true},
          // {id:6,text:'',divided:false,checkone:false},
          {id:7,text:'',divided:true,checkone:false},
          // {id:8,text:'',divided:false,checkone:false},
        ],
        activeNames: [0],
        activeLi:[0,0],
        collapseItems:[
          {
            id:0,

            lists:[

            ]
          }
        ]

      }
    },
    methods:{
      selectablee(row,index){
        if(row.is_header || row.is_move){
          return false
        }else{
          return true;
        }
      },
      arraySpanMethod({ row, column, rowIndex, columnIndex }) {
        if(row.is_header){
          if (columnIndex === 1) {
            return [1, 6];
          } else  {
            return [0, 0];
          }
        }
      },
      selectAll(val){
        if(!this.is_checked){
          this.$refs.innerTable.forEach(val=>{
            val.clearSelection();
          })
          $('.table_box .el-table-column--selection').click();


        }else{
          this.$refs.innerTable.forEach(val=>{
            val.clearSelection();
          })
        }
      },
      selectAllTable(val){
      },
      changeShow(m){
        m.show = !m.show;
      },
      signHandleCommand_new:function(item,row){
        if(!item){
          return;
        }
        let param = {
          uids:[row.uid],
          // folder:this.$route.params.boxId,
          folder:row.raw_name,
          action:item.action,
          flags:[item.flags]
        }
        messageFlag(param).then((suc)=>{
          this.$message({
            type:'success',
            message: this.lan.MAILBOX_COM_INNERBOX_MAIL_MARKUP_SUCCESSFUL
          })
          // this.getMessageList();
          this.fullsearch();
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
      cellClick(row,col,cell){
        if(col.type=='default'){
          if(col.className!='flag_btn'){
            this.readMail(row)
          }
          if(row.is_header){
          }
        }else{
          // this.$refs.innerTable.toggleRowSelection(row)
          $(cell).find('label').click();
        }
      },
      refresh(){
        this.sort = '';
        this.orderCheckIndex = '';
        this.viewCheckIndex = '';
        this.search = '';
        this.searchForm = {
          from: '',
          subject: '',
          body: ''
        }
        this.$parent.$parent.$parent.getFloderfn()
        // this.getMessageList();
        this.fullsearch(1,20);
      },
      rowClick(row,e,col){

      },
      hoverfn(row, column, cell, event){
        if(row.uid){
          this.hoverIndex = row.uid;
        }
      },
      noHover(){
        this.hoverIndex = '';
      },
      readMail(row){
        if(row.is_move){
          this.$message({
            type:'error',
            message:'搜索邮件不存在或者已被删除!'
          })
          return;
        }
        if(!row.isread){
          let unseenArr = this.$store.getters.getUnseenCount;
          unseenArr[this.boxId] --;
          this.$store.dispatch('setUnseenCountA',unseenArr)
          console.log(row)
          if(row.flagbg_class == 'unseen'){
            row.flagStr = '已读';
            row.flagbg_class = ''
          }
        }
        row.isread = true;
        this.$parent.$parent.$parent.addTab('read',row.subject,row.uid,row.raw_name)
      },
      handleSelectionChange(val) {
        this.multipleSelection = [];
        this.multipleSelection = val
      },
      formatter(row, column) {
        return row.date.replace('T','  ');
      },
      handleCommand:function(index){
        this.checkIndex = index;
        if(index===0){
          this.checkAll=true;
        }else{
          this.checkAll=false;
        }
      },
      orderHandleCommand:function(item){
        this.orderCheckIndex = item.id;
        this.sort = item.sort;
        this.getMessageList();
      },
      viewHandleCommand:function(index){
        if(index == 'other'){
          return;
        }
        this.viewCheckIndex = index;
        this.search = index;
        this.currentPage = 1;
        this.getMessageList();
      },
      moveHandleCommand:function(index){
        this.fullscreenLoading = true;
        let abcd=[];
        let hashFloder = [];
        this.multipleSelection.forEach(val=>{
          if(hashFloder[val.raw_name]){
            abcd[val.raw_name].push(val.uid);
          }else{
            hashFloder[val.raw_name] = val.raw_name;
            abcd[val.raw_name] = [];
            abcd[val.raw_name].push(val.uid);
          }
        })
        let spreadArr = []
        for(var key in abcd){
          let params = {
            uids :abcd[key],
            src_folder:key,
            dst_folder:index
          }
          spreadArr.push(moveMails(params))
        }
        let _this = this;
        axios.all(spreadArr).then(axios.spread( function(){
          // 请求现在都执行完成
          _this.fullscreenLoading = false;
          _this.fullsearch(1,20)
        })).catch(err=>{
          console.log('err1:',err)
        })

        return;
        var params={
          uids:this.checkedMails,
          src_folder:this.boxId,
          dst_folder:index
        }
        moveMails(params).then((suc)=>{
          this.fullscreenLoading = false;
          if(suc.data.msg=='success'){
            this.$message({
              type:'success',
              message: this.lan.MAILBOX_COM_INNERBOX_MAIL_MOVE_SUCCESSFUL
            })
            this.getMessageList();
            this.$parent.$parent.$parent.getFloderfn();
          }
        },(err)=>{
          this.fullscreenLoading = false;
          console.log(err);
        }).catch(err=>{
          this.fullscreenLoading = false;
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({
            type:"error",
            message: this.lan.MAILBOX_COM_INNERBOX_MAIL_MOVE_FAILED +str
          })
        })
      },
      signHandleCommand:function(item){
        if(!item){
          return;
        }
        this.fullscreenLoading = true;
        let abcd=[];
        let hashFloder = [];
        this.multipleSelection.forEach(val=>{
          if(hashFloder[val.raw_name]){
            abcd[val.raw_name].push(val.uid);
          }else{
            hashFloder[val.raw_name] = val.raw_name;
            abcd[val.raw_name] = [];
            abcd[val.raw_name].push(val.uid);
          }
        })
        let spreadArr = []
        for(var key in abcd){
          let params = {
            uids :abcd[key],
            folder:key,
            action:item.action,
            flags:[item.flags]
          }
          spreadArr.push(messageFlag(params))
        }
        let _this = this;
        axios.all(spreadArr).then(axios.spread( function(){
          // 请求现在都执行完成
          _this.fullscreenLoading = false;
          _this.fullsearch(1,20)
        })).catch(err=>{
          console.log('err1:',err)
        })
        return;

        let param = {
          uids:this.checkedMails,
          folder:this.boxId,
          action:item.action,
          flags:[item.flags]
        }
        messageFlag(param).then((suc)=>{
          this.fullscreenLoading = false;
          this.getMessageList();
          this.$parent.$parent.$parent.getFloderfn();
        },(err)=>{
          this.fullscreenLoading = false;
        }).catch(err=>{
          this.fullscreenLoading = false;
        })
      },
      deleteMailById(){
        this.$confirm( this.lan.MAILBOX_COM_INNERBOX_DELETE_MAIL + this.lan.MAILBOX_COM_INNERBOX_CONTINUE, this.lan.COMMON_BUTTON_CONFIRM_NOTICE, {
          confirmButtonText: this.lan.COMMON_BUTTON_CONFIRM,
          cancelButtonText: this.lan.COMMON_BUTTON_CANCELL,
          type: 'warning'
        }).then(() => {
          this.fullscreenLoading = true;
          console.log(this.multipleSelection);

          let abcd=[];
          let hashFloder = [];
          this.multipleSelection.forEach(val=>{
            if(hashFloder[val.raw_name]){
              abcd[val.raw_name].push(val.uid);
            }else{
              hashFloder[val.raw_name] = val.raw_name;
              abcd[val.raw_name] = [];
              abcd[val.raw_name].push(val.uid);
            }
          })
          console.log(abcd)
          let spreadArr = []
          for(var key in abcd){
            let params = {
              uids :abcd[key],
              folder:key
            }
            spreadArr.push(deleteMail(params))
          }
          let _this = this;
          console.log('spreadArr')
          console.log(spreadArr)
          axios.all(spreadArr).then(axios.spread( function(){
            // 请求现在都执行完成
            _this.fullscreenLoading = false;
            _this.fullsearch(1,20)
          })).catch(err=>{
            console.log('err1:',err)
          })
          return;
          deleteMail(params).then((suc)=>{
            this.fullscreenLoading = false;
            if(suc.data.msg=='success'){
              this.$message({
                type:'success',
                message: this.lan.COMMON_DELETE_SUCCESS
              })
              if((this.currentPage-1)*this.pageSize >= this.totalCount-this.checkedMails.length){
                this.currentPage = 1;
              }
              this.getMessageList();
              this.$parent.$parent.$parent.getFloderfn()
            }
          },(err)=>{
            let str = '';
            if(err.detail){
              str = err.detail
            }
            this.fullscreenLoading = false
            this.$message({
              type:'error',
              message: this.lan.COMMON_DELETE_FAILED +str
            })
          })
        }).catch(() => {
          this.fullscreenLoading = false;
        });

      },
      moreHandleCommand:function(item){
        if(item.checkone && this.checkedMails.length > 1){
          this.$alert( this.lan.MAILBOX_COM_INNERBOX_ONLY_ONE+item.text+' !',this.lan.COMMON_BUTTON_CONFIRM_NOTICE);
          return;
        }
        let pp = this.$parent.$parent.$parent;
        let param = {
          uids:this.checkedMails,
          folder:this.multipleSelection[0].raw_name
          // folder:pp.activeMenubar.id || this.$route.params.boxId
        }
        if(item.id==0 || item.id==1 || item.id==2 || item.id==3 || item.id==5){
          this.fullscreenLoading = true;
          let fid = pp.activeMenubar.id || this.$route.params.boxId;
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
          }
          readMail(this.multipleSelection[0].uid,{"folder":fid,"view":view}).then(res=>{
            this.fullscreenLoading = false;
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
            // pp.ruleForm2 = res.data;
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
              pp.content = data.plain_text;
            }
            // if(item.id == 0 || item.id ==1 || item.id==5){
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
            // }
            pp.addTab('compose'+view+' ',data.subject,data.uid,fid)
            let row = this.multipleSelection[0];
            if(!row.isread){
              this.$parent.$parent.$parent.unseencount --;
              this.$parent.$parent.$parent.$refs.treeMenuBar.getCurrentNode().unseen--;
              let unseenArr = this.$store.getters.getUnseenCount;
              unseenArr[this.boxId] --;
              this.$store.dispatch('setUnseenCountA',unseenArr)
            }
            row.isread = true;


          }).catch(err=>{
            this.fullscreenLoading = false;
            console.log(err)
          })

        }else if(item.id==4){ //拒收邮件

          this.$confirm('<p>'+this.lan.MAILBOX_COM_INNERBOX_REJECT_MAIL_1+'</p><p style="margin-bottom:20px;">'+this.lan.MAILBOX_COM_INNERBOX_REJECT_MAIL_2+'</p> <input type="checkbox" id="is_delete"> '+this.lan.MAILBOX_COM_INNERBOX_REJECT_MAIL_3, this.lan.COMMON_BUTTON_CONFIRM_NOTICE, {
            confirmButtonText: this.lan.COMMON_BUTTON_CONFIRM,
            cancelButtonText: this.lan.COMMON_BUTTON_CANCELL,
            dangerouslyUseHTMLString: true,

          }).then(() => {
            this.fullscreenLoading = true;
            let abcd=[];
            let hashFloder = [];
            this.multipleSelection.forEach(val=>{
              if(hashFloder[val.raw_name]){
                abcd[val.raw_name].push(val.uid);
              }else{
                hashFloder[val.raw_name] = val.raw_name;
                abcd[val.raw_name] = [];
                abcd[val.raw_name].push(val.uid);
              }
            })
            let spreadArr = []
            for(var key in abcd){
              let params = {
                uids :abcd[key],
                folder:key,
              }
              if($('#is_delete').prop('checked')) {
                params.is_delete = true
              }
              spreadArr.push(rejectMessage(params))
            }
            let _this = this;
            axios.all(spreadArr).then(axios.spread( function(){
              // 请求现在都执行完成
              _this.fullscreenLoading = false;
              _this.fullsearch(1,20)
            })).catch(err=>{
              console.log('err1:',err)
            })
            return;

            if($('#is_delete').prop('checked')) {
              param.is_delete = true
            }
            rejectMessage(param).then(res=>{
              this.fullscreenLoading = false;
              this.$message(
                {type:'success',message:this.lan.COMMON_OPRATE_SUCCESS}
              )
              this.getMessageList();
            })
              .catch(err=>{
                let str = '';
                if(err.detail){
                  str = err.detail
                }
                this.fullscreenLoading = false;
                this.$message(
                  {type:'error',message: this.lan.COMMON_OPRATE_FAILED+str}
                )
              })
          }).catch(() => {

          });

        }else if(item.id == 7){//彻底删除
          this.$confirm(this.lan.MAILBOX_COM_INNERBOX_DELETE_MAIL + this.lan.MAILBOX_COM_INNERBOX_CONTINUE, this.lan.COMMON_BUTTON_CONFIRM_NOTICE, {
            confirmButtonText: this.lan.COMMON_BUTTON_CONFIRM,
            cancelButtonText: this.lan.COMMON_BUTTON_CANCELL,
            type: 'warning'
          }).then(() => {
            this.fullscreenLoading = true;
            let abcd=[];
            let hashFloder = [];
            this.multipleSelection.forEach(val=>{
              if(hashFloder[val.raw_name]){
                abcd[val.raw_name].push(val.uid);
              }else{
                hashFloder[val.raw_name] = val.raw_name;
                abcd[val.raw_name] = [];
                abcd[val.raw_name].push(val.uid);
              }
            })
            let spreadArr = []
            for(var key in abcd){
              let params = {
                uids :abcd[key],
                folder:key,
              }
              spreadArr.push(pruneMessage(params))
            }
            let _this = this;
            axios.all(spreadArr).then(axios.spread( function(){
              // 请求现在都执行完成
              _this.fullscreenLoading = false;
              _this.fullsearch(1,20)
            })).catch(err=>{
              console.log('err1:',err)
            })
            return;

            pruneMessage(param).then(res=>{
              this.fullscreenLoading = false;
              this.$message(
                {type:'success',message:this.lan.COMMON_DELETE_SUCCESS}
              )
              pp.getFloderfn();
              this.getMessageList();
            }).catch(err=>{
              this.fullscreenLoading = false;
              let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message({
                type:'error',
                message:this.lan.COMMON_DELETE_FAILED+str
              })
            })
          }).catch(() => {

          });

        }
      },
      noSelect(){
        this.$refs.innerTable.clearSelection();
        // this.$refs.innerTable.clearSelection();
        // this.$refs.innerTable.forEach(val=>{
        //   val.clearSelection();
        // })
      },
      getfullsearch(params){
        this.loading = true;
        mailSearch(params).then(res=>{
          this.loading = false;
          this.$store.dispatch('setSearchmailDataA',{params:params,data:res.data});
          this.getMessageList();

        }).catch(err=>{
          this.loading = false;
          console.log(err)
        })
      },
      fullsearch(page,page_size){
        let params = this.$store.getters.getSearchmailData.params;
        params.page = page;
        params.page_size = page_size;
        this.getfullsearch(params)
      },
      getMessageList(){
        this.getDateN();
      },
      getDateN(params){
        let res = {}
        console.log(1234321)
        res.data = this.$store.getters.getSearchmailData.data;
        console.log(res.data)
        this.totalCount = res.data.total;
          let items = res.data.results;
          for(let i=0;i<items.length;i++){
            items[i].flagged = (items[i].flags.join('').indexOf('Flagged')>=0);
            items[i].isread = (items[i].flags.join(' ').indexOf('Seen')>=0);
            if(items[i].flagged){
              if(items[i].flags.join('').indexOf('umail-yellow')>=0){
                items[i].color = {'flag-yellow':true};
              }else if(items[i].flags.join('').indexOf('umail-green')>=0){
                items[i].color = {'flag-green':true};
              }else if(items[i].flags.join('').indexOf('umail-orange')>=0){
                items[i].color = {'flag-orange':true};
              }else if(items[i].flags.join('').indexOf('umail-blue')>=0){
                items[i].color = {'flag-blue':true};
              }else if(items[i].flags.join('').indexOf('umail-pink')>=0){
                items[i].color = {'flag-pink':true};
              }else if(items[i].flags.join('').indexOf('umail-cyan')>=0){
                items[i].color = {'flag-cyan':true};
              }else if(items[i].flags.join('').indexOf('umail-purple')>=0){
                items[i].color = {'flag-purple':true};
              }else if(items[i].flags.join('').indexOf('umail-gray')>=0){
                items[i].color = {'flag-gray':true};
              }
            }
            items[i].plain = '';
            items[i].checked = false;
            if(this.$store.getters.getIsSwtime){
              if(items[i].date){
                let index = items[i].date.indexOf('T');
                items[i].date = items[i].date.slice(0,index) + this.set_12_time(items[i].date.slice(index+1))
              }else if(items[i].internaldate){
                let index = items[i].internaldate.indexOf('T');
                items[i].internaldate = items[i].internaldate.slice(0,index) + this.set_12_time(items[i].internaldate.slice(index+1))
              }

            }
            let flagbg_class = '';
            let flagStr = this.lan.MAILBOX_COM_INNERBOX_ALREADY_READ;
            if(!items[i].isread){
              flagStr = this.lan.MAILBOX_COM_INNERBOX_UNREAD;
              flagbg_class = 'unseen';
            }
            // if(items[i].flags.join('').indexOf('umail-deliver')>=0){
            //   flagStr = '投递成功';
            //   flagbg_class = 'sendsuc';
            // }
            if(items[i].flags.join('').indexOf('Answered')>=0 && items[i].flags.join('').indexOf('umail-forword')>= 0){
              flagStr = this.lan.MAILBOX_COM_INNERBOX_RECOVERED_AND_FORWARDED;
              flagbg_class = 'reandfw';
            }
            if(items[i].flags.join('').indexOf('umail-forword')>=0 && items[i].flags.join('').indexOf('Answered')==-1){
              flagStr = this.lan.MAILBOX_COM_INNERBOX_FORWARDED;
              flagbg_class = 'forward';
            }
            if(items[i].flags.join('').indexOf('Answered')>=0 && items[i].flags.join('').indexOf('umail-forword') == -1){
              flagStr = this.lan.MAILBOX_COM_INNERBOX_RECOVERED;
              flagbg_class = 'answered';
            }
            if(items[i].flags.join('').indexOf('umail-schedule')>=0){
              flagStr = this.lan.MAILBOX_COM_INNERBOX_REGULAR_MAIL;
              flagbg_class = 'schedule';
            }
            if(items[i].is_move){
              flagStr = '搜索邮件不存在';
              flagbg_class = 'is_move';
            }
            items[i].flagbg_class = flagbg_class
            items[i].flagStr = flagStr
          }
          this.collapseItems[0].lists = items;

          let result = [];
          let result_new = [];
          let today = {title:this.lan.MAILBOX_COM_INNERBOX_TODAY,arr:[],show:true},yestoday = {title:this.lan.MAILBOX_COM_INNERBOX_YESTODAY,arr:[],show:true},beforeYesdoday = {title:this.lan.MAILBOX_COM_INNERBOX_BEFOREYESTODAY,arr:[],show:true},earlier = {title:this.lan.MAILBOX_COM_INNERBOX_EARLIER,arr:[],show:true};
          items.forEach(val=>{
            if(val.date){
              let date = new Date(val.date.slice(0,10));
              let now = new Date();
              let count = now.getDate()-date.getDate()
              if(count == 0){
                today.arr.push(val)
              }else if(count == 1){
                yestoday.arr.push(val)
              }else if(count == 1){
                beforeYesdoday.arr.push(val)
              }else{
                earlier.arr.push(val)
              }
            }else if(val.internaldate){
              let date = new Date(val.internaldate.slice(0,10));
              let now = new Date();
              let count = now.getDate()-date.getDate()
              if(count == 0){
                today.arr.push(val)
              }else if(count == 1){
                yestoday.arr.push(val)
              }else if(count == 1){
                beforeYesdoday.arr.push(val)
              }else{
                earlier.arr.push(val)
              }
            }
          })
          if(today.arr.length>0){
            result.push(today)
            let obj = [].concat(today.arr[0])
            obj.title = this.lan.MAILBOX_COM_INNERBOX_TODAY
            obj.count = today.arr.length
            obj.is_header = true
            result_new.push(obj)
            result_new = result_new.concat(today.arr);
          }
          if(yestoday.arr.length>0){
            result.push(yestoday)
            let obj = [].concat(yestoday.arr[0])
            obj.title = this.lan.MAILBOX_COM_INNERBOX_YESTODAY
            obj.count = yestoday.arr.length
            obj.is_header = true
            result_new.push(obj)
            result_new = result_new.concat(yestoday.arr);
          }
          if(beforeYesdoday.arr.length>0){
            result.push(beforeYesdoday)
            let obj = [].concat(beforeYesdoday.arr[0])
            obj.title = this.lan.MAILBOX_COM_INNERBOX_BEFOREYESTODAY
            obj.count = beforeYesdoday.arr.length
            obj.is_header = true
            result_new.push(obj)
            result_new = result_new.concat(beforeYesdoday.arr);
          }
          if(earlier.arr.length>0){
            result.push(earlier)
            let obj = [].concat(earlier.arr[0])
            obj.title = this.lan.MAILBOX_COM_INNERBOX_EARLIER
            obj.count = earlier.arr.length
            obj.is_header = true
            result_new.push(obj)
            result_new = result_new.concat(earlier.arr);
          }
          this.listData = result;
          this.listData_new = result_new;

          this.loading = false;

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
      handleSizeChange(val) {
        this.pageSize = val;
        this.currentPage = 1;
        this.fullsearch(1,val)
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.fullsearch(val,this.pageSize)
      },


    },
    computed:{
      checkedMails:function(){
        let list=[];
        for(let i=0;i<this.multipleSelection.length;i++){
          list.push(this.multipleSelection[i].uid)
        }
        return list;
      },
      moveItems:function(){
        let folder = this.floderResult;
        let arr = [];
        for(let i=0;i<folder.length;i++){
          if(folder[i]['raw_name']!='Drafts'&&folder[i]['raw_name']!=this.boxId){
            let obj={};
            obj['text'] = folder[i]['name'];
            obj['id'] = folder[i]['raw_name'];
            obj['divided'] = false;
            arr.push(obj);
          }
        }
        return arr;
      },
      unseen_count_new:function(){
        return this.$store.getters.getUnseenCount[this.boxId]
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
        this.checkItems = [
          {id:0,text:lang.MAILBOX_COM_INNERBOX_ALL,divided:false},
          {id:1,text:lang.MAILBOX_COM_INNERBOX_CURRENT_PAGE,divided:true},
          {id:2,text:lang.MAILBOX_COM_INNERBOX_UNREAD,divided:false},
          {id:3,text:lang.MAILBOX_COM_INNERBOX_ALREADY_READ,divided:false},
          {id:4,text:lang.MAILBOX_COM_INNERBOX_REVERSE_ELECTION,divided:false},
          {id:5,text:lang.MAILBOX_COM_INNERBOX_NO_ELECTION,divided:false},
        ]
        this.orderItems = [
          {id:0,text:lang.MAILBOX_COM_INNERBOX_NEW_TO_OLD,divided:false,sort:'REVERSE ARRIVAL'},
          {id:1,text:lang.MAILBOX_COM_INNERBOX_OLD_TO_NEW,divided:false,sort:'ARRIVAL'},
          {id:3,text:lang.MAILBOX_COM_INNERBOX_UPGRADE_BY_SENDER,divided:true,sort:'FROM'},
          {id:2,text:lang.MAILBOX_COM_INNERBOX_DESCEND_BY_SENDER,divided:false,sort:'REVERSE FROM'},
          {id:4,text:lang.MAILBOX_COM_INNERBOX_DESCEND_BY_SUBJECT,divided:true,sort:'REVERSE SUBJECT '},
          {id:5,text:lang.MAILBOX_COM_INNERBOX_UPGRADE_BY_SUBJECT,divided:false,sort:'SUBJECT '},
          {id:8,text:lang.MAILBOX_COM_INNERBOX_SMALL_TO_BIG,divided:true,sort:'SIZE'},
          {id:9,text:lang.MAILBOX_COM_INNERBOX_BIG_TO_SMALL,divided:false,sort:'REVERSE SIZE'},
        ]
        this.viewItems = [
          {id:'',text:lang.MAILBOX_COM_INNERBOX_ALL_MAIL,divided:false},
          {id:'unseen',text:lang.MAILBOX_COM_INNERBOX_UNREAD_MAIL,divided:false},
          {id:'seen',text:lang.MAILBOX_COM_INNERBOX_READ_MAIL,divided:false},
          {id:'flagged',text:lang.MAILBOX_COM_INNERBOX_MARKED_MAIL,divided:true,classN:'iconfont icon-iconflatcolor redcolor'},
          {id:'other',text:lang.MAILBOX_COM_INNERBOX_OTHER_MARKERS,divided:false,children:[
              {id:'KEYWORD umail-green',text:lang.MAILBOX_COM_INNERBOX_GREEN_FLAG,classN:'flag-green'},
              {id:'KEYWORD umail-orange',text:lang.MAILBOX_COM_INNERBOX_ORANGE_FLAG,classN:'flag-orange'},
              {id:'KEYWORD umail-blue',text:lang.MAILBOX_COM_INNERBOX_BLUE_FLAG,classN:'flag-blue'},
              {id:'KEYWORD umail-pink',text:lang.MAILBOX_COM_INNERBOX_PINK_FLAG,classN:'flag-pink'},
              {id:'KEYWORD umail-cyan',text:lang.MAILBOX_COM_INNERBOX_CYAN_FLAG,classN:'flag-cyan'},
              {id:'KEYWORD umail-yellow',text:lang.MAILBOX_COM_INNERBOX_YELLOW_FLAG,classN:'flag-yellow'},
              {id:'KEYWORD umail-purple',text:lang.MAILBOX_COM_INNERBOX_PURPLE_FLAG,classN:'flag-purple'},
              {id:'KEYWORD umail-gray',text:lang.MAILBOX_COM_INNERBOX_GREY_FLAG,classN:'flag-gray'}
            ]},
          {id:'unflagged',text:lang.MAILBOX_COM_INNERBOX_UNMARKED_MAIL,divided:false,classN:'iconfont icon-iconflat'},
          {id:'ANSWERED',text:lang.MAILBOX_COM_INNERBOX_RECOVERED,divided:true,classN:'iconfont icon-iconback greencolor'},
          {id:'KEYWORD umail-forword',text:lang.MAILBOX_COM_INNERBOX_FORWARDED,divided:false,classN:'iconfont icon-Forward greencolor'},
        ]
        this.signItems = [
          {id:0,flags:'\\Seen',text:lang.MAILBOX_COM_INNERBOX_READ_MAIL,divided:false,action:'add'},
          {id:1,flags:'\\Seen',text:lang.MAILBOX_COM_INNERBOX_UNREAD_MAIL,divided:false,action:'remove'},
          {id:2,flags:'\\flagged',text:lang.MAILBOX_COM_INNERBOX_RED_FLAG,divided:true,action:'add',classN:'iconfont icon-iconflatcolor redcolor'},
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
          {id:0,text:lang.MAILBOX_COM_INNERBOX_RECOVER,divided:false,checkone:true},
          {id:1,text:lang.MAILBOX_COM_INNERBOX_RECOVER_ALL,divided:false,checkone:true},
          {id:2,text:lang.MAILBOX_COM_INNERBOX_FORWARD,divided:true,checkone:true},
          {id:3,text:lang.MAILBOX_COM_INNERBOX_ANNEX_FORWARDING,divided:false,checkone:true},
          {id:4,text:lang.MAILBOX_COM_INNERBOX_REJECTED_MAIL,divided:true,checkone:false},
          {id:5,text:lang.MAILBOX_COM_INNERBOX_SEND_AGAIN,divided:true,checkone:true},
          // {id:6,text:lang.MAILBOX_COM_INNERBOX_PACKAGE_DOWNLOAD,divided:false,checkone:false},
          {id:7,text:lang.MAILBOX_COM_INNERBOX_DELETE_THOROUGHLY,divided:true,checkone:false},
          // {id:8,text:lang.MAILBOX_COM_INNERBOX_EMPTY_FOLDER,divided:false,checkone:false},
        ]
        return lang
      },
      search_desc:function(){
          let str = '';
          if(this.$store.getters.getSearchmailData.params.keyword && this.$store.getters.getSearchmailData.params.keyword != ''){
            str += '【关键字包含 "'+this.$store.getters.getSearchmailData.params.keyword + '"】';
          }
          if(this.$store.getters.getSearchmailData.params.subject && this.$store.getters.getSearchmailData.params.subject != ''){
            str += '【主题包含 "'+this.$store.getters.getSearchmailData.params.subject + '"】';
          }
          if(this.$store.getters.getSearchmailData.params.attach && this.$store.getters.getSearchmailData.params.attach != ''){
            str += '【附件名包含 "'+this.$store.getters.getSearchmailData.params.attach + '"】';
          }
          if(this.$store.getters.getSearchmailData.params.folder && this.$store.getters.getSearchmailData.params.folder != ''){
            str += '【所在文件夹范围为 "'+this.$store.getters.getSearchmailData.params.folder_desc + '"】';
          }
          if(this.$store.getters.getSearchmailData.params.sender && this.$store.getters.getSearchmailData.params.sender != ''){
            str += '【发件人为 "'+this.$store.getters.getSearchmailData.params.sender + '"】';
          }
          if(this.$store.getters.getSearchmailData.params.recipient && this.$store.getters.getSearchmailData.params.recipient != ''){
            str += '【收件人为 "'+this.$store.getters.getSearchmailData.params.recipient + '"】';
          }
          if(this.$store.getters.getSearchmailData.params.date && this.$store.getters.getSearchmailData.params.date != ''){
            str += '【发信时间范围为 "'+this.$store.getters.getSearchmailData.params.date_desc + '"】';
          }
          if(this.$store.getters.getSearchmailData.params.size && this.$store.getters.getSearchmailData.params.size != ''){
            str += '【邮件大小为 "'+this.$store.getters.getSearchmailData.params.size_desc + '"】';
          }
        return str
      }
    },
    created(){
      // this.boxId = this.$route.params.boxId || 'INBOX'
      // this.curr_folder = sessionStorage['checkNodeLabel'] || this.lan.MAILBOX_INBOX

      this.getMessageList();
    },

  }
</script>

<style>
  .line-through{
    text-decoration: line-through;
  }
  .fromto.from{
    color:#222;
  }
  .fromto.unseen{
    font-weight:700;
  }
  .is_red{
    color:red;
  }
  .read_bg{
    display:inline-block;
    cursor: pointer;
    height: 18px;
    position:relative;
    top:2px;
    overflow: hidden;
    width: 18px;
    background:url(../../../assets/img/maillistbg.png) no-repeat scroll -48px -16px transparent
  }
  .read_bg.forward{
    background:url("../../../assets/img/maillistbg.png") no-repeat scroll -48px -48px transparent;
  }
  .read_bg.answered{
    background:url("../../../assets/img/maillistbg.png") no-repeat scroll -48px -32px transparent;
  }
  .read_bg.unseen{
    background:url("../../../assets/img/maillistbg.png") no-repeat scroll -48px 0 transparent;
  }
  .read_bg.reandfw{
    background:url("../../../assets/img/reandfw.jpg") no-repeat scroll transparent;
  }
  .read_bg.sendsuc{
    background:url("../../../assets/img/sendsuc.jpg") no-repeat scroll transparent;
  }
  .read_bg.schedule{
    background:url("../../../assets/img/schedule.jpg") no-repeat scroll transparent;
  }
  .read_bg.is_move{
    background:url("../../../assets/img/getfile.jpg") no-repeat scroll transparent;
  }
  .greencolor{
    color:rgb(46, 169, 98);
  }
  .redcolor,.redcolor .fromto.from{
    color:#c00;
  }
  .flagged,.flagged.fromto.from{
    color:#c00;
  }
  .flag-green,.flag-green .fromto{
    color: #349B08!important;
  }
  .flag-orange,.flag-orange .fromto{
    color: #ED501A!important;
  }
  .flag-yellow,.flag-yellow .fromto{
    color: #C79C17!important;
  }
  .flag-blue,.flag-blue .fromto{
    color: #1797DC!important;
  }
  .flag-pink,.flag-pink .fromto{
    color: #E33D97!important;
  }
  .flag-cyan,.flag-cyan .fromto{
    color: #0FB38E!important;
  }
  .flag-purple,.flag-purple .fromto{
    color: #AD50D8!important;
  }
  .flag-gray,.flag-gray .fromto{
    color: #818181!important;
  }

  .maillist.el-table td{
    padding:8px 0;
  }
  .mainMsg .icon-iconflat,.mainMsg .el-icon-arrow-down{
    display:none;
  }
  .mainMsg.hoverStyle .icon-iconflat,.mainMsg.hoverStyle .el-icon-arrow-down{
    display:inline;
  }
  .dropdown_item.active{
    color:#409EFF;
  }
  .width_100{
    width:100px;
  }
  #pagination{
    margin-right:10px;
  }
  .m-mllist .el-collapse-item__header{
    padding:0 14px;
    border-bottom: 1px solid #ebeef5;
    font-weight: bold;
  }
  .m-mllist .el-collapse-item__content{
    padding-bottom:0;
  }
  .flagged{
    color:#c00;
  }
  .unseen .fl_l{
    font-weight:700;
  }
  .fromto{
    color:#057ab8;
  }
  .subject_hover:hover{
    cursor:pointer;
  }
</style>

