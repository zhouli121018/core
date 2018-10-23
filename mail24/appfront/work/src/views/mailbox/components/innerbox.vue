<template>
        <div class="mltabview-content">
            <div v-if="totalAllCount>0" class="mltabview-panel">
                <div class="m-mllist">
                    <div class="list-bg"></div>
                    <div class="m-mllist-row">
                        <div class="toolbar" style="background:#fff;">
                            <span class=" f-fr j-setting">
                            <el-button  icon="el-icon-setting" circle></el-button></span>

                            <!--排序-->
                            <el-dropdown @command="orderHandleCommand" placement="bottom-start" trigger="click">
                                <el-button  size="small" plain>
                                    <span>排序</span>
                                    <i class="el-icon-arrow-down el-icon--right"></i>
                                </el-button>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item v-for="item in orderItems" :key="item.id" class="dropdown_item" :class="{ active: orderCheckIndex===item.id }"
                                    :divided="item.divided" :command="item">
                                    <b><i class="el-icon-check vibility_hide" :class="{ vibility_show: orderCheckIndex===item.id }"></i> </b>
                                    {{ item.text}}</el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>

                            <!--查看-->

                            <el-dropdown @command="viewHandleCommand" trigger="click">
                                <el-button  size="small" plain >
                                    <span>查看</span>
                                    <i class="el-icon-arrow-down el-icon--right"></i>
                                </el-button>
                                <el-dropdown-menu slot="dropdown">
                                  <el-dropdown-item v-if="!item.children" v-for="(item,k) in viewItems" :key="k" class="dropdown_item"
                                   :command="item.id" :divided="item.divided">
                                      <b><i class="el-icon-check vibility_hide" v-if="!item.classN"></i> </b><i :class="item.classN"></i>
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
                                    删除
                                </el-button>

                                <el-dropdown @command="moveHandleCommand" trigger="click" v-if="boxId!='Drafts'">
                                    <el-button  size="small" plain>
                                    <span>移动到</span>
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
                                        <span>标记为</span>
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
                                    <span>更多</span>
                                    <i class="el-icon-arrow-down el-icon--right"></i>
                                    </el-button>
                                    <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item v-if="boxId!='Drafts'||item.id==6||item.id==7" v-for="item in moreItems" :key="item.id" class="dropdown_item" :class="{ active: moreCheckIndex===item.id }"
                                    :divided="item.divided" :command="item">
                                        <b><i class="el-icon-check vibility_hide" :class="{ vibility_show: moreCheckIndex===item.id }"></i> </b>
                                        {{ item.text}}</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>

                            </div>

                            <!--刷新-->
                            <el-button  size="small" plain @click="refresh">
                                刷新  <!-- <i class="el-icon-refresh el-icon--right"></i> -->
                            </el-button>
                            <el-button v-show="!moreSearch" @click="moreSearch=true" size="small">更多搜索</el-button>

                            <div v-show="moreSearch">
                              <el-form :inline="true" :model="searchForm" ref="searchForm" class="demo-form-inline" size="small">
                                <el-form-item label="发件人">
                                  <el-input v-model="searchForm.from" placeholder="发件人"></el-input>
                                </el-form-item>
                                <el-form-item label="邮件主题">
                                  <el-input v-model="searchForm.subject" placeholder="邮件主题"></el-input>
                                </el-form-item>
                                <el-form-item label="邮件内容">
                                  <el-input v-model="searchForm.body" placeholder="邮件内容"></el-input>
                                </el-form-item>
                                <el-form-item>
                                  <el-button type="primary" @click="moreSearchfn">查询</el-button>
                                  <el-button v-show="moreSearch" @click="moreSearch=false" size="small">隐藏</el-button>
                                </el-form-item>
                              </el-form>
                            </div>

                        </div>

                    <div class="mail-totals j-mail-totals" v-if="multipleSelection.length==0">
                        <div class="totals-info">
                        {{curr_folder}}(
                        <span class="all-mail">共<span class="number">{{totalAllCount}}</span>封</span>
                        <span class="unread-mail"><span class="number">{{unreadCount}}</span>封</span>
                        <a href="#" >未读</a>
                        <a href="#" v-if="unreadCount" @click.prevent="readAll">，全部设为已读</a>
                        )

                        </div>
                    </div>
                    <div class="j-select-count select-count" v-if="multipleSelection.length>0">
                        <span class="j-desc desc">已选择 {{multipleSelection.length}} 封</span>
                        <a class="j-cancel cancel" href="#" @click="noSelect">取消</a>
                    </div>
                      <div style="text-align:right;padding:4px;height:32px;">
                        <el-pagination
                              @size-change="handleSizeChange"
                              @current-change="handleCurrentChange"
                              background
                              :current-page="currentPage"
                              :page-sizes="[10, 20, 50,100]"
                              :page-size="pageSize"
                              layout="total, sizes, prev, pager, next, jumper"
                              :total="totalCount">
                            </el-pagination>
                      </div>
                    </div>
                    <div class="m-mllist-row mllist-list-row">
                      <div class="j-module-content j-maillist mllist-list u-scroll">
                        <div>
                          <el-table ref="innerTable" :data="collapseItems[0].lists" style="width: 100%;" class="vertical_align_top maillist"
                              highlight-current-row  @cell-mouse-enter="hoverfn" @cell-mouse-leave="noHover" @row-click="rowClick" @cell-click="cellClick"
                                    @selection-change="handleSelectionChange"  v-loading="loading" :header-cell-style="{background:'#f0f1f3'}"
                            >
                            <el-table-column
                              type="selection"
                              width="36"

                            >全选/取消
                            </el-table-column>

                            <el-table-column prop="subject"  label="" @click="">
                              <template slot-scope="scope">
                                <div class="clear mainMsg" style="font-size:16px;" :class="[{flagged:scope.row.flagged,unseen:!scope.row.isread,hoverStyle:scope.row.uid==hoverIndex},scope.row.color]">
                                  <span class="fl_l subject_hover" style="width:80%;overflow: hidden;white-space: nowrap;text-overflow: ellipsis;" @click.stop.prevent="readMail(scope.row)" >{{scope.row.subject||'无主题'}}</span>
                                  <span class="fl_r">
                                    <i :title="scope.row.flagged?'点击取消旗帜':'设为红旗'" @click.stop="changeFlags(scope.row)" class="iconfont" :class="{'icon-iconflatcolor':scope.row.flagged||scope.row.color,'icon-iconflat':!scope.row.flagged&&!scope.row.color}" style="cursor:pointer;"></i>
                                  </span>
                                </div>
                                <div class="info-summary" :class="scope.row.color">
                                  <p class="summary-text">
                                    <span class="fromto">from</span>
                                    <span class="fromto">:</span>
                                    <span class="fromto from" v-if="scope.row.mfrom">{{scope.row.mfrom[1]}} <{{scope.row.mfrom[0]}}></span>
                                    <!--<span class="fromto">:</span>-->
                                    <!--<span class="summary">-->
                                      <!--sdajpofjsdfhup测试-->
                                    <!--</span>-->
                                  </p>
                                </div>
                              </template>
                            </el-table-column>



                            <el-table-column class="plan_style" prop="date" label="时间"   width="160"  >
                              <template slot-scope="scope">
                                <div class="plan_style">
                                  {{(scope.row.internaldate ||scope.row.date).replace('T',' ')}}
                                  <p style="text-align:center;" v-if="scope.row.has_attachment" >
                                    <i class="iconfont icon-attachment"></i>
                                  </p>
                                </div>

                              </template>
                            </el-table-column>
                            <el-table-column class="plan_style" prop="size" label="大小"   width="100">
                              <template slot-scope="scope">
                                <div class="plan_style">
                                  {{scope.row.size | mailsize}}
                                </div>
                              </template>
                            </el-table-column>
                          </el-table>
                        </div>
                      </div>

                    </div>
                </div>
            </div>
            <div v-if="totalAllCount==0" class="mltabview-panel">
               <h3 style="margin:30px 0 0 20px;font-size:24px;font-weight:normal;"> "{{curr_folder}}" 没有邮件</h3>
            </div>
        </div>
</template>
<script>
  import {getMailMessage,moveMails,getFloder,getFloderMsg,deleteMail,messageFlag,readMail,rejectMessage,pruneMessage,zipMessage} from "@/api/api";

  import router from '@/router'

  export default {
    name:'Innerbox',
    props:{
      boxId:'',
      curr_folder:{
        type:String,
        default:''
      },
      floderResult:{
        type:Array,
        default: []
      }
    },

    data() {
        return {
          moreSearch:false,
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
          pageSize:10,
          checkIndex:'',
          checkAll:false,
          checkItems:[
            {id:0,text:'所有',divided:false},
            {id:1,text:'当前页',divided:true},
            {id:2,text:'未读',divided:false},
            {id:3,text:'已读',divided:false},
            {id:4,text:'反选',divided:false},
            {id:5,text:'不选',divided:false},
          ],
          orderCheckIndex:'',
          orderItems:[
            {id:0,text:'按时间从新到旧',divided:false,sort:'REVERSE ARRIVAL'},
            {id:1,text:'按时间从旧到新',divided:false,sort:'ARRIVAL'},
            {id:3,text:'按发件人升序',divided:true,sort:'FROM'},
            {id:2,text:'按发件人降序',divided:false,sort:'REVERSE FROM'},
            {id:4,text:'按邮件主题降序',divided:true,sort:'REVERSE SUBJECT '},
            {id:5,text:'按邮件主题升序',divided:false,sort:'SUBJECT '},
            {id:8,text:'按邮件大小（从小到大）',divided:true,sort:'SIZE'},
            {id:9,text:'按邮件大小（从大到小）',divided:false,sort:'REVERSE SIZE'},
          ],

          viewCheckIndex:'',
          viewItems:[
            {id:'',text:'全部邮件',divided:false},
            {id:'unseen',text:'未读邮件',divided:false},
            {id:'seen',text:'已读邮件',divided:false},
            {id:'flagged',text:'已标记邮件',divided:true,classN:'iconfont icon-iconflatcolor redcolor'},
            {id:'other',text:'其他标记',divided:false,children:[
                {id:'KEYWORD umail-green',text:'绿旗',classN:'flag-green'},
                {id:'KEYWORD umail-orange',text:'橙旗',classN:'flag-orange'},
                {id:'KEYWORD umail-blue',text:'蓝旗',classN:'flag-blue'},
                {id:'KEYWORD umail-pink',text:'粉旗',classN:'flag-pink'},
                {id:'KEYWORD umail-cyan',text:'青旗',classN:'flag-cyan'},
                {id:'KEYWORD umail-yellow',text:'黄旗',classN:'flag-yellow'},
                {id:'KEYWORD umail-purple',text:'紫旗',classN:'flag-purple'},
                {id:'KEYWORD umail-gray',text:'灰旗',classN:'flag-gray'}
              ]},
            {id:'unflagged',text:'未标记邮件',divided:false,classN:'iconfont icon-iconflat'},
            {id:'ANSWERED',text:'已回复',divided:true,classN:'iconfont icon-iconback greencolor'},
            {id:'KEYWORD umail-forword',text:'已转发',divided:false,classN:'iconfont icon-Forward greencolor'},
          ],
          moveCheckIndex:'',

          signItems:[
            {id:0,flags:'\\Seen',text:'已读邮件',divided:false,action:'add'},
            {id:1,flags:'\\Seen',text:'未读邮件',divided:false,action:'remove'},
            {id:2,flags:'\\flagged',text:'红旗',divided:true,action:'add',classN:'iconfont icon-iconflatcolor redcolor'},
            {id:3,text:'其他旗帜',divided:false,children:[
                {flags:'umail-green',action:'add',text:'绿旗',classN:{'flag-green':true}},
                {flags:'umail-orange',action:'add',text:'橙旗',classN:{'flag-orange':true}},
                {flags:'umail-blue',action:'add',text:'蓝旗',classN:{'flag-blue':true}},
                {flags:'umail-pink',action:'add',text:'粉旗',classN:{'flag-pink':true}},
                {flags:'umail-cyan',action:'add',text:'青旗',classN:{'flag-cyan':true}},
                {flags:'umail-yellow',action:'add',text:'黄旗',classN:{'flag-yellow':true}},
                {flags:'umail-purple',action:'add',text:'紫旗',classN:{'flag-purple':true}},
                {flags:'umail-gray',action:'add',text:'灰旗',classN:{'flag-gray':true}}
              ]},
            {id:4,flags:'\\flagged',text:'取消旗帜',divided:false,action:'remove'},
          ],
          moreCheckIndex:'',
          moreItems:[
            {id:0,text:'回复',divided:false,checkone:true},
            {id:1,text:'回复全部',divided:false,checkone:true},
            {id:2,text:'转发',divided:true,checkone:true},
            {id:3,text:'附件方式转发',divided:false,checkone:true},
            {id:4,text:'拒收邮件',divided:true,checkone:false},
            {id:5,text:'再次发送',divided:true,checkone:true},
            {id:6,text:'打包下载',divided:false,checkone:false},
            {id:7,text:'彻底删除',divided:false,checkone:false}
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
      cellClick(row,col){
        if(col.type=='default'){
          this.readMail(row)
        }else{
          this.$refs.innerTable.toggleRowSelection(row)
        }
      },
      refresh(){
        this.sort = '';
        this.orderCheckIndex = '';
        this.search = '';
        this.getMessageList();
      },
      rowClick(row,e,col){

      },
      moreSearchfn(){
        this.loading = true;
        let params = {
          folder:this.boxId,
          limit:this.pageSize,
          offset:0,
        }
        let str='';
        if(this.searchForm.from){
          str += ' from "'+this.searchForm.from+'"';
        }
        if(this.searchForm.subject){
          str += ' subject "'+this.searchForm.subject+'"';
        }
        if(this.searchForm.body){
          str += ' body "'+this.searchForm.body+'"';
        }
        if(str){params['search'] = str;}
        getMailMessage(params).then((res)=>{
          this.totalCount = res.data.count;
          var items = res.data.results;
          for(var i=0;i<items.length;i++){
            items[i].flagged = (items[i].flags.join('').indexOf('Flagged')>=0);
            items[i].isread = (items[i].flags.join(' ').indexOf('Seen')>=0);
            items[i].plain = '';
            items[i].checked = false;
          }
          this.collapseItems[0].lists = items;
          this.loading = false;
        },(err)=>{
          console.log(err)
        })
      },
      hoverfn(row, column, cell, event){
        this.hoverIndex = row.uid;
      },
      noHover(){
        this.hoverIndex = '';
      },
      changeFlags(row){
        row.flagged=!row.flagged;
        if(row.color){
          row.color=null
        }
        console.log(row)
        let ac = row.flagged?'add':'remove';
        let param = {
          uids:[row.uid],
          folder:this.$parent.$parent.$parent.activeMenubar.id,
          action:ac,
          flags:['\\flagged']
        }
        messageFlag(param).then((suc)=>{

        },(err)=>{

        })
      },
      readAll(){
        let param = {
          uids:['all'],
          folder:this.$parent.$parent.$parent.activeMenubar.id,
          action:'add',
          flags:['\\Seen']
        }
        messageFlag(param).then((suc)=>{
          this.getMessageList();
          this.getFloderMsgById(this.boxId);
          this.$parent.$parent.$parent.getFloderfn();
        },(err)=>{

        })
      },
      readMail(row){
          row.isread = true;
          console.log(row)
        let param = {
          uids:[row.uid],
          folder:this.$parent.$parent.$parent.activeMenubar.id,
          action:'add',
          flags:['\\Seen']
        }
        messageFlag(param).then((suc)=>{
          // this.getMessageList();
          this.getFloderMsgById(this.boxId);
          this.$parent.$parent.$parent.getFloderfn();
        },(err)=>{

        })

        console.log(this.$parent.$parent.$parent);
        if(this.boxId=='Drafts'){
          let pp = this.$parent.$parent.$parent;
          readMail(row.uid,{"folder":this.boxId}).then(res=>{
            let data = res.data
            // pp.ruleForm2 = res.data;
            pp.ruleForm2 = res.data;
            pp.content = data.html_text || data.plain_text;
            pp.maillist = []
            pp.maillist_copyer = [];
            pp.fileList = data.attachments;
            pp.ruleForm2.is_html = true;
            for(let i=0;i<data.to.length;i++){
              pp.maillist.push({fullname:data.to[i][1]||'',email:data.to[i][0],status:true})

            }
            console.log('maillist')
            console.log(pp.maillist)
            if(data.cc){
              for(let i=0;i<data.cc.length;i++){
                pp.maillist_copyer.push({fullname:data.cc[i][1]||'',email:data.cc[i][0],status:true})
              }
            }

            pp.addTab('composedrafts',data.subject,row.uid,this.boxId)

          }).catch(err=>{
            console.log(err)
          })
        }else{
          this.$parent.$parent.$parent.addTab('read',row.subject,row.uid,this.boxId)
        }



      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
        console.log(this.multipleSelection)
      },
      formatter(row, column) {
        return row.date.replace('T','  ');
      },
      jumpTo(path,rid){
            router.push({
             name: path,
             params: {
              id: rid
             }
            });
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
        console.log(item)
        this.orderCheckIndex = item.id;
        this.sort = item.sort;
        this.getMessageList();
      },
      viewHandleCommand:function(index){
        console.log(index);
        if(index == 'other'){
          return;
        }
        this.search = index;
        this.currentPage = 1;
        this.getMessageList();
      },
      moveHandleCommand:function(index){
        var params={
          uids:this.checkedMails,
          src_folder:this.$parent.$parent.$parent.activeMenubar.id,
          dst_folder:index
        }
        moveMails(params).then((suc)=>{
          console.log(suc.data)
          console.log(suc.data.msg)
          if(suc.data.msg=='success'){
            this.$message({
              type:'success',
              message: '邮件移动成功!'
            })
            this.getMessageList();
            this.$parent.$parent.$parent.getFloderfn();
          }
        },(err)=>{
          console.log(err);
        })
      },
      signHandleCommand:function(item){
        console.log(item);
        if(!item){
          return;
        }
        let param = {
          uids:this.checkedMails,
          folder:this.$parent.$parent.$parent.activeMenubar.id,
          action:item.action,
          flags:[item.flags]
        }
        messageFlag(param).then((suc)=>{
          this.getMessageList();
          this.getFloderMsgById(this.boxId);
          this.$parent.$parent.$parent.getFloderfn();
        },(err)=>{

        })
      },
      deleteMailById(){
        var params={
          uids:this.checkedMails,
          folder:this.$parent.$parent.$parent.activeMenubar.id,
        };
        this.$confirm('删除此邮件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteMail(params).then((suc)=>{
            if(suc.data.msg=='success'){
              this.$message({
                type:'success',
                message: '邮件删除成功!'
              })
              this.getMessageList();
              this.$parent.$parent.$parent.refreshMenu()
            }
          },(err)=>{
            this.$message({
                type:'error',
                message: '删除失败！!'
              })
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });

      },
      moreHandleCommand:function(item){
        if(item.checkone && this.checkedMails.length > 1){
          this.$alert('您只能选择一封邮件进行 '+item.text+' !','提示');
          return;
        }
        console.log(this.checkedMails)
        console.log(this.multipleSelection)
        let pp = this.$parent.$parent.$parent;
        let param = {
          uids:this.checkedMails,
          folder:pp.activeMenubar.id
        }
        if(item.id==0 || item.id==1 || item.id==2 || item.id==3 || item.id==5){
          let fid = pp.activeMenubar.id;
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
            pp.ruleForm2 = {
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
            }
            let data = res.data
            // pp.ruleForm2 = res.data;
            pp.maillist = []
            pp.maillist_copyer = [];
            pp.content = data.html_text || data.plain_text;
            pp.fileList = data.attachments;
            pp.ruleForm2.subject = data.subject;
            if(data.uid)pp.ruleForm2.uid = data.uid;
            if(data.folder)pp.ruleForm2.folder = data.folder;
            if(data.refw_type)pp.ruleForm2.refw_type = data.refw_type
            pp.ruleForm2.is_html = true;
            // if(item.id == 0 || item.id ==1 || item.id==5){
              for(let i=0;i<data.to.length;i++){
                pp.maillist.push({fullname:data.to[i][1]||'',email:data.to[i][0],status:true})
              }
              if(data.cc){
                for(let i=0;i<data.cc.length;i++){
                  pp.maillist_copyer.push({fullname:data.cc[i][1]||'',email:data.cc[i][0],status:true})
                }
              }
            // }
            pp.addTab('compose'+view+' ',data.subject,data.uid,fid)

          }).catch(err=>{
            console.log(err)
          })

        }else if(item.id==4){ //拒收邮件
          rejectMessage(param).then(res=>{
            console.log(res)
            this.$message(
              {type:'success',message:'邮件拒收成功！'}
            )
          })
            .catch(err=>{
            console.log(err)
              this.$message(
              {type:'error',message:'邮件拒收失败！'}
            )
          })
        }else if(item.id==6){//打包下载
          zipMessage(param).then(response=>{
            let blob = new Blob([response.data], { type: response.headers["content-type"] })
            let objUrl = URL.createObjectURL(blob);
            this.blobUrl = objUrl;
            let filenameHeader = response.headers['content-disposition']
            let filename = filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1);
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
              {type:'success',message:'打包下载邮件成功！'}
            )
          }).catch(err=>{
            console.log(err)
            this.$message(
              {type:'error',message:'打包下载邮件失败！'}
            )
          })

        }else if(item.id == 7){//彻底删除
          this.$confirm('彻底删除此邮件, 是否继续?', '系统信息', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            pruneMessage(param).then(res=>{
              console.log(res)
              this.$message(
                {type:'success',message:'彻底删除邮件成功！'}
              )
              pp.getFloderfn();
              this.getMessageList();
            }).catch(err=>{
              console.log('彻底删除失败！',err);
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消彻底删除'
            });
          });

        }
      },
      handleChange(value) {
        console.log(value);
      },
      noSelect(){
          for(var i=0;i<this.collapseItems.length;i++){
              for(var k=0;k<this.collapseItems[i].lists.length;k++){
                  this.collapseItems[i].lists[k].checked = false;
              }
          }
      },
      getMessageList(){
        this.loading = true;
        let params = {
          folder:this.boxId,
          limit:this.pageSize,
          offset:(this.currentPage-1)*this.pageSize,

        }
        if(this.search){
          params['search'] = this.search;
        }
        let str=this.search||'';
        if(this.searchForm.from){
          str += ' from "'+this.searchForm.from+'"';
        }
        if(this.searchForm.subject){
          str += ' subject "'+this.searchForm.subject+'"';
        }
        if(this.searchForm.body){
          str += ' body "'+this.searchForm.body+'"';
        }
        if(str){
          params['search'] = str;
        }


        if(this.sort){
          params['sort'] = this.sort;
        }
        getMailMessage(params).then((res)=>{
          this.totalCount = res.data.count;
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
          }
          this.collapseItems[0].lists = items;
          this.loading = false;
        },(err)=>{
          console.log(err)
          this.loading = false;
        })
      },
      getFloderMsgById(param){
        getFloderMsg(param).then((suc)=>{
          this.totalAllCount = suc.data.count;
          this.unreadCount = suc.data.unseen_count;
        },(err)=>{
          console.log(err)
        })
      },
      handleSizeChange(val) {
        this.pageSize = val;
        this.getMessageList();
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.getMessageList();
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
          if(folder[i]['raw_name']!='Drafts'&&folder[i]['raw_name']!=this.$parent.$parent.$parent.activeMenubar.id){
            let obj={};
            obj['text'] = folder[i]['name'];
            obj['id'] = folder[i]['raw_name'];
            obj['divided'] = false;
            arr.push(obj);
          }
        }
        return arr;
      }
    },
    mounted(){
      this.getMessageList();
      this.getFloderMsgById(this.boxId)
    },
    watch: {
        boxId(newValue, oldValue) {
          this.currentPage = 1;
          this.search = '';
          this.viewCheckIndex = ''
          this.multipleSelection = [];
            this.getMessageList();
            this.getFloderMsgById(this.boxId)
        },
      checkedMails(v){
          // console.log(v)
      }
    }

}
</script>

<style>
  .greencolor{
    color:rgb(46, 169, 98);
  }
  .redcolor{
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
    padding:18px 0;
  }
  .mainMsg .icon-iconflat{
  display:none;
}
.mainMsg.hoverStyle .icon-iconflat{
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

