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
                            <el-dropdown @command="orderHandleCommand" placement="bottom-start">
                                <el-button  size="small" plain>
                                    <span>排序</span>
                                    <i class="el-icon-arrow-down el-icon--right"></i>
                                </el-button>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item v-for="item in orderItems" :key="item.id" class="dropdown_item" :class="{ active: orderCheckIndex===item.id }"
                                    :divided="item.divided" :command="item.id">
                                    <b><i class="el-icon-check vibility_hide" :class="{ vibility_show: orderCheckIndex===item.id }"></i> </b>
                                    {{ item.text}}</el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>

                            <!--查看-->
                            <el-dropdown @command="viewHandleCommand" placement="bottom-start">
                                <el-button  size="small" plain>
                                    <span>查看</span>
                                    <i class="el-icon-arrow-down el-icon--right"></i>
                                </el-button>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item v-for="item in viewItems" :key="item.id" class="dropdown_item" :class="{ active: viewCheckIndex===item.id }"
                                    :divided="item.divided" :command="item.id">
                                    <b><i class="el-icon-check vibility_hide" :class="{ vibility_show: viewCheckIndex===item.id }"></i> </b>
                                    {{ item.text}}</el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>

                            <!-- 更多按钮 -->
                            <div v-if="multipleSelection.length>0" class="inline_block">
                                <el-button  size="small" plain @click="deleteMailById">
                                    删除
                                </el-button>

                                <el-dropdown @command="moveHandleCommand">
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

                                <el-dropdown @command="signHandleCommand">
                                    <el-button  size="small" plain >
                                        <span>标记为</span>
                                        <i class="el-icon-arrow-down el-icon--right"></i>
                                    </el-button>
                                    <el-dropdown-menu slot="dropdown">
                                      <el-dropdown-item v-for="item in signItems" :key="item.id" class="dropdown_item"
                                       :command="item">
                                          <b><i class="el-icon-check vibility_hide"></i> </b>
                                          {{ item.text}}
                                      </el-dropdown-item>
                                    </el-dropdown-menu>

                                </el-dropdown>

                                <el-dropdown @command="moreHandleCommand">
                                    <el-button  size="small" plain>
                                    <span>更多</span>
                                    <i class="el-icon-arrow-down el-icon--right"></i>
                                    </el-button>
                                    <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item v-for="item in moreItems" :key="item.id" class="dropdown_item" :class="{ active: moreCheckIndex===item.id }"
                                    :divided="item.divided" :command="item.id">
                                        <b><i class="el-icon-check vibility_hide" :class="{ vibility_show: moreCheckIndex===item.id }"></i> </b>
                                        {{ item.text}}</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>

                            </div>

                            <!--刷新-->
                            <el-button  size="small" plain>
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
                        {{boxName}}(
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
                              :page-sizes="[5,10, 15, 20,30, 50,100,300,500]"
                              :page-size="pageSize"
                              layout="total, sizes, prev, pager, next, jumper"
                              :total="totalCount">
                            </el-pagination>
                      </div>
                    </div>
                    <div class="m-mllist-row mllist-list-row">
                      <div class="j-module-content j-maillist mllist-list u-scroll">
                        <div>
                          <el-table :data="collapseItems[0].lists" style="width: 100%;" class="vertical_align_top maillist"
                              highlight-current-row  @cell-mouse-enter="hoverfn" @cell-mouse-leave="noHover" @cell-click="readMail"
                                    @selection-change="handleSelectionChange"  v-loading="loading"
                            >
                            <el-table-column
                              type="selection"
                              width="36"

                            >全选/取消
                            </el-table-column>

                            <el-table-column prop="subject"  label="" @click="">
                              <template slot-scope="scope">
                                <div class="clear mainMsg" style="font-size:16px;" :class="{flagged:scope.row.flagged,unseen:!scope.row.isread,hoverStyle:scope.row.uid==hoverIndex}">
                                  <span class="fl_l" style="width:80%;overflow: hidden;white-space: nowrap;text-overflow: ellipsis;">{{scope.row.subject||'无主题'}}</span>
                                  <span class="fl_r">
                                    <i :title="scope.row.flagged?'点击取消旗帜':'设为红旗'" @click.stop="changeFlags(scope.row)" class="iconfont" :class="{'icon-iconflatcolor':scope.row.flagged,'icon-iconflat':!scope.row.flagged}" style="cursor:pointer;"></i>
                                  </span>
                                </div>
                                <div class="info-summary">
                                  <p class="summary-text">
                                    <span class="fromto from" v-if="scope.row.mfrom">{{scope.row.mfrom[1]}} <{{scope.row.mfrom[0]}}></span>
                                    <!--<span class="fromto">:</span>-->
                                    <!--<span class="summary">-->
                                      <!--sdajpofjsdfhup测试-->
                                    <!--</span>-->
                                  </p>
                                </div>
                              </template>
                            </el-table-column>



                            <el-table-column class="plan_style" prop="date" label="时间" sortable  width="160"  >
                              <template slot-scope="scope">
                                <div class="plan_style">
                                  {{scope.row.date.replace('T',' ')}}
                                </div>
                              </template>
                            </el-table-column>
                            <el-table-column class="plan_style" prop="size" label="大小" sortable  width="100" :formatter="formatterSize">
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
  import {getMailMessage,moveMails,getFloder,getFloderMsg,deleteMail,messageFlag} from "@/api/api";

  import router from '@/router'

  export default {
    name:'Innerbox',
    props:{
      boxId:'',
      curr_folder:{
        type:String,
        default:''
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
            {id:0,text:'按时间从新到旧',divided:false},
            {id:1,text:'按时间从旧到新',divided:false},
            {id:2,text:'按发件人降序',divided:true},
            {id:3,text:'按发件人升序',divided:false},
            {id:4,text:'按主题降序',divided:true},
            {id:5,text:'按主题升序',divided:false},
            {id:6,text:'按附件降序',divided:true},
            {id:7,text:'按附件升序',divided:false},
          ],
          viewCheckIndex:'',
          viewItems:[
            {id:'',text:'全部邮件',divided:false},
            {id:'unseen',text:'未读邮件',divided:false},
            {id:'seen',text:'已读邮件',divided:false},
            {id:'flagged',text:'已标记邮件',divided:true},
            {id:'unflagged',text:'未标记邮件',divided:false},
            // {id:5,text:'紧急',divided:true},
            // {id:6,text:'普通',divided:false},
            // {id:7,text:'缓慢',divided:false},
            // {id:8,text:'包含附件',divided:true},
            // {id:9,text:'不包含附件',divided:false},
            // {id:10,text:'已回复',divided:true},
            // {id:11,text:'已转发',divided:false},
          ],
          moveCheckIndex:'',
          moveItems:[
            {id:0,text:'已发送',divided:false},
            {id:1,text:'已删除',divided:false},
            {id:2,text:'垃圾邮件',divided:false},
            {id:3,text:'病毒文件夹',divided:false}
          ],
          signItems:[


            {id:0,flags:'\\Seen',text:'已读邮件',divided:false,action:'add'},
            {id:1,flags:'\\Seen',text:'未读邮件',divided:false,action:'remove'},
            {id:2,flags:'\\flagged',text:'红旗',divided:true,action:'add'},
            {id:3,flags:'\\flagged',text:'取消红旗',divided:true,action:'remove'},
          ],
          moreCheckIndex:'',
          moreItems:[
            {id:0,text:'回复',divided:false},
            {id:1,text:'回复全部',divided:false},
            {id:2,text:'转发',divided:true},
            {id:3,text:'附件方式转发',divided:false},
            {id:4,text:'举报',divided:true},
            {id:5,text:'拒收邮件',divided:false},
            {id:6,text:'来信分类',divided:false},
            {id:7,text:'再次发送',divided:true},
            {id:8,text:'打包下载',divided:false},
            {id:9,text:'彻底删除',divided:false}
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
      },
      readAll(){
        let param = {
          uids:['all'],
          folder:this.$parent.activeMenubar.id,
          action:'add',
          flags:['\\Seen']
        }
        messageFlag(param).then((suc)=>{
          this.getMessageList();
          this.getFloderMsgById(this.boxId);
          this.$parent.$refs.menubar.getFloderfn();
        },(err)=>{

        })
      },
      readMail(row, column, cell, event){
          row.isread = true;
          this.$parent.showTabIndex=2;
          console.log(row)
        let param = {
          uids:[row.uid],
          folder:this.$parent.activeMenubar.id,
          action:'add',
          flags:['\\Seen']
        }
        messageFlag(param).then((suc)=>{
          this.getMessageList();
          this.getFloderMsgById(this.boxId);
          this.$parent.$refs.menubar.getFloderfn();
        },(err)=>{

        })
        this.$parent.getRead({'id':row.uid,'subject':row.subject});

      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
        console.log(this.multipleSelection)
      },
      formatter(row, column) {
        return row.date.replace('T','  ');
      },
      formatterSize(row,col){
        var s = (row.size/1024).toFixed(2);
        if(s>1024){
          s = (s/1024).toFixed(2) + ' M'
        }else{
          s = s +' KB'
        }
        return s
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
      tabCheckAll:function(){
        if(this.checkAll){
          this.checkIndex=0;
          for(var i=0;i<this.collapseItems.length;i++){
              for(var k=0;k<this.collapseItems[i].lists.length;k++){
                  this.collapseItems[i].lists[k].checked = true;

              }
          }
        }else{
          this.checkIndex='';
          for(var i=0;i<this.collapseItems.length;i++){
              for(var k=0;k<this.collapseItems[i].lists.length;k++){
                  this.collapseItems[i].lists[k].checked = false;
              }
          }
        }
      },
      orderHandleCommand:function(index){
        this.orderCheckIndex = index;
      },
      viewHandleCommand:function(index){
        console.log(index);
        this.search = index;
        this.currentPage = 1;
        this.getMessageList();
        this.viewCheckIndex = index;
      },
      moveHandleCommand:function(index){
        var params={
          uids:this.checkedMails,
          src_folder:this.$parent.activeMenubar.id,
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
            this.$parent.refreshMenu()
          }
        },(err)=>{
          console.log(err);
        })
      },
      signHandleCommand:function(item){
        console.log(item);
        let param = {
          uids:this.checkedMails,
          folder:this.$parent.activeMenubar.id,
          action:item.action,
          flags:[item.flags]
        }
        messageFlag(param).then((suc)=>{
          this.getMessageList();
          this.getFloderMsgById(this.boxId);
          this.$parent.$refs.menubar.getFloderfn();
        },(err)=>{

        })
      },
      deleteMailById(){
        var params={
          uids:this.checkedMails,
          folder:this.$parent.activeMenubar.id,
        };
        deleteMail(params).then((suc)=>{
          if(suc.data.msg=='success'){
            this.$message({
              type:'success',
              message: '邮件删除成功!'
            })
            this.getMessageList();
            this.$parent.refreshMenu()
          }
        },(err)=>{
          this.$message({
              type:'error',
              message: '删除失败！!'
            })
        })
      },
      moreHandleCommand:function(index){
        this.moreCheckIndex = index;
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
      boxName:function(){
        return this.$parent.activeMenubar.label
      }
    },
    beforeMount(){
      this.getMessageList();
      this.getFloderMsgById(this.boxId)
      getFloder().then((res)=>{
        let folder = res.data
        let arr = [];
        for(let i=0;i<folder.length;i++){
          let obj={};
          obj['text'] = folder[i]['name'];
          obj['id'] = folder[i]['raw_name'];
          obj['divided'] = false;
          arr.push(obj);
        }
        this.moveItems = arr
      },(err)=>{
        console.log(err)
      });


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
</style>

