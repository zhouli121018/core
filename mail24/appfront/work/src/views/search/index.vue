<template>
  <div style="box-sizing: border-box" id="search">
    <el-tabs v-model="activeName" @tab-click="handleClick">

      <el-tab-pane label="登录查询" name="login" v-loading="loginData.loading">
        <el-row style="padding-bottom:10px;">
          <el-col :span="12">
            <el-date-picker type="date" placeholder="查询日期" v-model="loginfilterdate" value-format="yyyy-MM-dd" auto-complete="off" size="mini" style="width: 200px!important;" @change="searchLoginDate"></el-date-picker>
          </el-col>
          <el-col :span="12" style="text-align:right;">
            <el-pagination style="text-align: right;" @size-change="sizeChange($event,'login')" @current-change="currentChange($event,'login')" :current-page="loginData.page" :page-sizes="[10, 20, 50, 100]" :page-size="loginData.page_size" layout="total, sizes, prev, pager, next " :total="loginData.total"></el-pagination>
          </el-col>
        </el-row>
        <el-table :data="loginData.tableData" stripe :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}" size="mini" style="width: 100%">
          <el-table-column prop="created" label="登录时间" width="180">
            <template slot-scope="scope"><div>{{scope.row.created.replace('T',' ')}}</div></template>
          </el-table-column>
          <el-table-column prop="client_ip" label="IP地址" width="200"></el-table-column>
          <el-table-column prop="area" label="登录地区" width="300">
            <template slot-scope="scope" >
              <div class="nowrap" :title="scope.row.area">{{scope.row.area}}</div>
            </template>
          </el-table-column>
          <el-table-column prop="type" label="登录方式" width="100"></el-table-column>
          <el-table-column prop="remark" label="登录结果" width="150">
            <template slot-scope="scope"><div><span style="color:#45AB19;"> {{scope.row.remark }} </span></div></template>
          </el-table-column>
          <el-table-column prop="browser" label="浏览器类型">
            <template slot-scope="scope" >
              <div class="nowrap" :title="scope.row.browser">{{scope.row.browser}}</div>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="发信查询" name="send" v-loading="sendData.loading">
        <el-row style="padding-bottom:10px;">
          <el-col :span="12">
            <el-date-picker type="date" placeholder="查询日期" v-model="sendfilterdate" value-format="yyyy-MM-dd" auto-complete="off" size="mini" style="width: 200px!important;" @change="searchSendDate"></el-date-picker>
          </el-col>
          <el-col :span="12" style="text-align:right;">
            <el-pagination style="text-align: right;" @size-change="sizeChange($event,'send')" @current-change="currentChange($event,'send')" :current-page="sendData.page" :page-sizes="[10, 20, 50, 100]" :page-size="sendData.page_size" layout="total, sizes, prev, pager, next " :total="sendData.total"></el-pagination>
          </el-col>
        </el-row>
        <el-table ref="sendTable" id="sendTable" :data="sendData.tableData" stripe :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}" size="mini" style="width: 100%">
          <el-table-column type="expand" class="expand">
            <template slot-scope="props">
              <el-row v-for="(r,k) in props.row.details" v-if="props.row.details.length>1" :key="k" style="padding:4px 0;">
                <el-col :style="{marginLeft:expand_table.marginLeft+'px',width:expand_table.col1+'px'}" :title="r.recipient" style="box-sizing:border-box;overflow: hidden;white-space: nowrap;text-overflow: ellipsis;padding-left:10px;">
                  <span v-if="r.name">{{r.name +' '}} &lt;</span> <span> {{r.recipient}}</span> <span v-if="r.name">&gt;</span>
                </el-col>
                <el-col :style="{width:expand_table.col2+'px'}" style="overflow: hidden; white-space: nowrap;text-overflow: ellipsis;box-sizing:border-box;padding-left:10px;">
                  <span style="color:#45AB19;" :class="{is_red:r.is_red}"> {{r.inform||''}}</span>
                </el-col>
                <el-col :style="{width:expand_table.col3+'px'}" style="overflow: hidden;white-space: nowrap;text-overflow: ellipsis;box-sizing:border-box;padding-left:10px;">
                  <el-button type="text" size="mini" v-if="!r.is_zhaohui" @click="recall(props.row,'single',r.recipient)">召回邮件</el-button>
                </el-col>
              </el-row>
            </template>
          </el-table-column>
          <el-table-column prop="send_time" label="时 间" width="180">
            <template slot-scope="scope">
              <div>{{scope.row.send_time.replace('T',' ')}}</div>
            </template>
          </el-table-column>
          <el-table-column prop="subject" label="主 题">
            <template slot-scope="scope" >
              <div class="nowrap" :title="scope.row.subject">{{scope.row.subject}}</div>
            </template>
          </el-table-column>
          <el-table-column prop="" label="收件人">
            <template slot-scope="scope">
              <div v-if="scope.row.details.length>1">
                <el-button type="text" size="mini" icon="el-icon-arrow-up" @click="changeExpand(scope.row)"> 所有收件人{{'（'+scope.row.details.length+'）'}}</el-button>
              </div>
              <div v-if="scope.row.details.length==1">
                <span v-if="scope.row.details[0].name">{{scope.row.details[0].name+' '}} &lt;</span>
                <span>{{scope.row.details[0].recipient}}</span>
                <span v-if="scope.row.details[0].name">&gt;</span>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="details" label="状 态">
            <template slot-scope="scope" >
              <div v-if="scope.row.details.length==1">
                <span style="color:#45AB19;" :class="{is_red:scope.row.details[0].is_red}"> {{scope.row.details[0].inform||''}} </span>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="操 作" width="150">
            <template slot-scope="scope">
              <div>
                <el-button type="text" size="mini" v-if="scope.row.details.length == 1 && !scope.row.details[0].is_zhaohui" @click="recall(scope.row)">召回邮件</el-button>
                <el-button type="text" size="mini" v-if="show_recall_all(scope.row)" @click="recall(scope.row)">召回全部邮件</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="收信查询" name="mail" v-loading="mailData.loading">
        <el-row style="padding-bottom:10px;">
          <el-col :span="12">
            <el-button-group>
              <el-button class="status_btn" size="mini" :class="{active:mailData.status == ''}" @click="changeStatus('')">全部来信</el-button>
              <el-button class="status_btn" size="mini" :class="{active:mailData.status == 'success'}" @click="changeStatus('success')">收件箱和个人文件夹</el-button>
              <el-button class="status_btn" size="mini" :class="{active:mailData.status == 'spam-flag'}" @click="changeStatus('spam-flag')">垃圾邮件</el-button>
              <el-button class="status_btn" size="mini" :class="{active:mailData.status == 'virus'}" @click="changeStatus('virus')">病毒拦截</el-button>
              <el-button class="status_btn" size="mini" :class="{active:mailData.status == 'spam'}" @click="changeStatus('spam')">垃圾拦截</el-button>
            </el-button-group>
            <el-date-picker type="date" placeholder="查询日期" v-model="receivefilterdate" value-format="yyyy-MM-dd" auto-complete="off" size="mini" style="width: 200px!important;" @change="searchReceiveDate"></el-date-picker>
          </el-col>
          <el-col :span="12" style="text-align:right;">
            <el-pagination style="text-align: right;" @size-change="sizeChange($event,'mail')" @current-change="currentChange($event,'mail')" :current-page="mailData.page" :page-sizes="[10, 20, 50, 100]" :page-size="mailData.page_size" layout="total, sizes, prev, pager, next " :total="mailData.total"></el-pagination>
          </el-col>
        </el-row>
        <el-table :data="mailData.tableData" stripe :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}" size="mini" style="width: 100%">
          <el-table-column prop="logtime" label="时 间" width="180">
            <template slot-scope="scope">
              <div>{{scope.row.logtime.replace('T',' ')}}</div>
            </template>
          </el-table-column>
          <el-table-column prop="subject" label="主题">
            <template slot-scope="scope" >
              <div class="nowrap" :title="scope.row.subject">{{scope.row.subject}}</div>
            </template>
          </el-table-column>
          <el-table-column prop="send_mail" label="发件人" width="250">
            <template slot-scope="scope" >
              <div class="nowrap" :title="scope.row.send_mail">{{scope.row.send_mail}}</div>
            </template>
          </el-table-column>
          <el-table-column prop="folder" label="存储位置" width="250">
            <template slot-scope="scope">
              <div class="nowrap" :title="scope.row.folder">{{scope.row.folder }} </div>
            </template>
          </el-table-column>
          <el-table-column prop="remark" label="备注" width="300">
            <template slot-scope="scope">
              <div><span> {{scope.row.remark }} </span></div>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="删信查询" name="delete" v-loading="deleteData.loading">
        <el-row style="padding-bottom:10px;">
          <el-col :span="12">
            <el-button-group>
              <el-button class="status_btn" size="mini" :class="{active:deleteData.status == ''}" @click="changeType('')">全部删信</el-button>
              <el-button class="status_btn" size="mini" :class="{active:deleteData.status == 'web'}" @click="changeType('web')">网页删信</el-button>
              <el-button class="status_btn" size="mini" :class="{active:deleteData.status == 'system'}" @click="changeType('system')">自动清理</el-button>
              <el-button class="status_btn" size="mini" :class="{active:deleteData.status == 'client'}" @click="changeType('client')">客户端删信</el-button>
            </el-button-group>
            <el-date-picker type="date" placeholder="查询日期" v-model="deleletfilterdate" value-format="yyyy-MM-dd" auto-complete="off" size="mini" style="width: 200px!important;" @change="searchDeleteDate"></el-date-picker>
          </el-col>
          <el-col :span="12">
            <el-pagination style="text-align: right;" @size-change="sizeChange($event,'delete')" @current-change="currentChange($event,'delete')" :current-page="deleteData.page" :page-sizes="[10, 20, 50, 100]" :page-size="deleteData.page_size" layout="total, sizes, prev, pager, next " :total="deleteData.total"></el-pagination>
          </el-col>
        </el-row>
        <el-table :data="deleteData.tableData" stripe :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}" size="mini" style="width: 100%">
          <el-table-column prop="created" label="删除时间" width="180">
            <template slot-scope="scope">
              <div>{{scope.row.created.replace('T',' ')}}</div>
            </template>
          </el-table-column>
          <el-table-column prop="subject" label="主题">
            <template slot-scope="scope" >
              <div class="nowrap" :title="scope.row.subject">{{scope.row.subject}}</div>
            </template>
          </el-table-column>
          <el-table-column prop="send_mail" label="发件人 / 操作人" width="250">
            <template slot-scope="scope" >
              <div class="nowrap" :title="scope.row.send_mail">{{scope.row.send_mail}}</div>
            </template>
          </el-table-column>
          <el-table-column prop="type_show" label="删除信息" width="200">
            <template slot-scope="scope">
              <div><span> {{scope.row.type_show }} </span></div>
            </template>
          </el-table-column>
          <el-table-column prop="folder" label="删除位置" width="250">
            <template slot-scope="scope">
              <div class="nowrap" :title="scope.row.folder">{{scope.row.folder }} </div>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <el-dialog title="邮件召回" :visible.sync="recallTableVisible" :append-to-body="true" size="mini">
      <el-table :data="recallData">
        <el-table-column property="recipient" label="收件人"></el-table-column>
        <el-table-column property="recall_status_info" label="召回状态" width="200"></el-table-column>
        <el-table-column prop="" label="详情">
          <template slot-scope="scope">
            <span style="color:#45AB19;" v-if="!scope.row.is_red"> {{scope.row.inform||''}}</span>
            <span style="color:#45AB19;" v-if="scope.row.is_red" class="is_red"> {{scope.row.inform||''}}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>

  import {getLoginList,getSendlog,getMaillog,getDeletellog,sendRecall,logRecall} from '@/api/api'
  export default {
    data() {
      return {
        expand_table:{
          marginLeft:0,
          col1:100,
          col2:100,
          col3:100,
        },
        loginfilterdate: '',
        sendfilterdate: '',
        receivefilterdate: '',
        deleletfilterdate: '',
        recallTableVisible:false,
        recallData:[],
        activeName: 'login',
        loginData:{
          loading:false,
          page: 1,
          page_size:20,
          total:200,
          tableData: [
          ]
        },
        sendData:{
          loading:false,
          page: 1,
          page_size:20,
          total:200,
          tableData: [
          ]
        },
        mailData:{
          loading:false,
          page: 1,
          page_size:20,
          total:200,
          tableData: [
          ],
          status:''
        },
        deleteData:{
          loading:false,
          page: 1,
          page_size:20,
          total:200,
          tableData: [
          ],
          status:''
        }

      };
    },
    methods: {
      searchLoginDate(val){
        this.loginfilterdate = val;
        this.getLogin();
      },
      searchSendDate(val){
        this.sendfilterdate = val;
        this.getSend();
      },
      searchReceiveDate(val){
        this.deleletfilterdate = val;
        this.getMail();
      },
      searchDeleteDate(val){
        this.deleletfilterdate = val;
        this.getDelete();
      },
      show_recall_all(row){
        let len = row.details.length >1;
        let result =  false;
        for(let i=0;i<row.details.length;i++){
          if(!row.details[i].is_zhaohui){
            result = true;
            break;
          }
        }
        result = len && result;
        return result;
      },
      resetWidth(){
        this.$nextTick(()=>{
          this.expand_table.marginLeft = parseFloat($('#sendTable colgroup>col:eq(0)').attr('width'))+
            parseFloat($('#sendTable colgroup>col:eq(1)').attr('width'))+
            parseFloat($('#sendTable colgroup>col:eq(2)').attr('width'));
          this.expand_table.col1 = parseFloat($('#sendTable colgroup>col:eq(3)').attr('width'))
          this.expand_table.col2 = parseFloat($('#sendTable colgroup>col:eq(4)').attr('width'))
          this.expand_table.col3 = parseFloat($('#sendTable colgroup>col:eq(5)').attr('width'))-18;
        })
      },
      recall(row,type,r){
        this.$confirm('<p>确定召回此邮件吗？</p>', '召回邮件', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          dangerouslyUseHTMLString: true,
          type: 'warning'
        }).then(() => {
          let message_id = row.message_id;
          let str = '';
          let param = {
            message_id: message_id,
          }
          if(type && type =='single'){
            param.recipient = r;
            this.sendData.loading = true;
            logRecall(param).then(res=>{
              this.recallData = res.data.results;
              this.sendData.loading = false;
              this.recallTableVisible = true;
              this.getSend();
            }).catch(err=>{
              this.sendData.loading = false;
              let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message({
                message: '邮件召回失败！'+str,
                type: 'error'
              })
            })
          }else{
            // row.details.forEach(val=>{
            //   str += val.recipient+','
            // })
            // str = str.slice(0,str.length-1)
            this.sendData.loading = true;
            sendRecall(param).then(res => {
              this.recallData = res.data.results;
              this.sendData.loading = false;
              this.recallTableVisible = true;
              this.getSend();
            }).catch(err=>{
              this.sendData.loading = false;
              let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message({
                message: '邮件召回失败！'+str,
                type: 'error'
              })
            })
          }


        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消召回'
          });
        });
      },
      changeType(status){
        this.deleteData.page = 1;
        this.deleteData.status = status;
        sessionStorage['searchType'] = status;
        this.getDelete();
      },
      changeStatus(status){
        this.mailData.page = 1;
        this.mailData.status = status;
        sessionStorage['searchStatus'] = status;
        this.getMail();
      },
      changeExpand(row){
        this.$refs.sendTable.toggleRowExpansion(row)
      },
      handleClick(tab, event) {
        let index = tab.$data.index;
        sessionStorage['searchIndex'] = index;
        if(index==1){
          this.getSend();
        }else if(index == 2){
          this.getMail();
        }else if(index == 3){
          this.getDelete();
        }else if(index == 0){
          this.getLogin();
        }
      },
      sizeChange(val,type) {
        if(type=='login'){
          this.loginData.page_size = val;
          this.getLogin();
        }else if(type=='send'){
          this.sendData.page_size = val;
          this.getSend();
        }else if(type=='mail'){
          this.mailData.page_size = val;
          this.getMail()
        }else if(type=='delete'){
          this.deleteData.page_size = val;
          this.getDelete()
        }
      },
      currentChange(val,type) {
        if(type=='login'){
          this.loginData.page = val;
          this.getLogin();
        }else if(type=='send'){
          this.sendData.page = val;
          this.getSend();
        }else if(type=='mail'){
          this.mailData.page = val;
          this.getMail()
        }else if(type=='delete'){
          this.deleteData.page = val;
          this.getDelete()
        }
      },
      getLogin(){
        this.loginData.loading = true;
        let param ={
          page:this.loginData.page,
          page_size:this.loginData.page_size,
          filterdate:this.loginfilterdate,
        };
        getLoginList(param).then(res=>{
          this.loginData.total = res.data.count;
          this.loginData.tableData = res.data.results;
          this.loginData.loading = false;
        }).catch(err=>{
          console.log('获取登录日志错误！',err)
          this.loginData.loading = false;
        })
      },
      getSend(){
        this.sendData.loading = true;
        let param ={
          page:this.sendData.page,
          page_size:this.sendData.page_size,
          filterdate:this.sendfilterdate,
        };
        getSendlog(param).then(res=>{
          this.sendData.total = res.data.count;
          this.sendData.tableData = res.data.results;
          this.sendData.loading = false;
          this.$nextTick(()=>{
            this.resetWidth()
          })
        }).catch(err=>{
          console.log('获取发信日志错误！',err)
          this.sendData.loading = false;
        })
      },
      getMail(){
        this.mailData.loading = true;
        let param ={
          page:this.mailData.page,
          page_size:this.mailData.page_size,
          filterdate:this.receivefilterdate,
        };
        if(this.mailData.status){
          param.status = this.mailData.status;
        }
        getMaillog(param).then(res=>{
          this.mailData.total = res.data.count;
          this.mailData.tableData = res.data.results;
          this.mailData.loading = false;
        }).catch(err=>{
          console.log('获取收信日志错误！',err)
          this.mailData.loading = false;
        })
      },
      getDelete(){
        this.deleteData.loading = true;
        let param ={
          page:this.deleteData.page,
          page_size:this.deleteData.page_size,
          filterdate:this.deleletfilterdate,
        };
        if(this.deleteData.status){
          param.type = this.deleteData.status;
        }
        getDeletellog(param).then(res=>{
          this.deleteData.total = res.data.count;
          this.deleteData.tableData = res.data.results;
          this.deleteData.loading = false;
        }).catch(err=>{
          console.log('获取删信日志错误！',err)
          this.deleteData.loading = false;
        })
      }
    },
    created(){
      if(sessionStorage['searchIndex']){
        let index = sessionStorage['searchIndex'];
        if(index == 0){
          this.activeName = 'login';
          this.getLogin();
        }else if(index==1){
          this.activeName = 'send';
          this.getSend();
        }else if(index == 2){
          this.activeName = 'mail';
          if(sessionStorage['searchStatus']){
            this.mailData.status = sessionStorage['searchStatus'];
          }
          this.getMail();
        }else if(index == 3){
          this.activeName = 'delete';
          if(sessionStorage['searchType']){
            this.deleteData.status = sessionStorage['searchType']
          }
          this.getDelete();
        }
      }else{
        this.activeName = 'login';
        this.getLogin();
      }


    },
  };
</script>
<style>
  .is_red{
    color:red !important;
  }
  #search .el-tabs__nav-wrap::after{
    background-color: #555C64;
  }
  #search .el-tabs--top .el-tabs__item.is-top:nth-child(2) {
    padding-left: 20px;
  }
  #search .el-tabs--top .el-tabs__item.is-top:last-child {
    padding-right: 20px;
  }
  #search .el-tabs__item{
    height:100%;
    line-height: 59px;
  }
  #search .el-tabs__nav.is-top{
    height:59px;
  }
  #search .el-tabs__nav-scroll{
    height:60px;
    line-height:59px;
  }
  #search .el-tabs{
    height:100%;
  }
  #search .el-tabs__content{
    overflow: auto;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    padding-bottom: 10px;
    /* min-height: 600px; */
    position: absolute;
    top: 75px;
    bottom: 0;
    left: 10px;
    right: 0;
  }
  #search .el-tabs__header{
    margin: 0 0 5px;
    background:#555C64;
  }
  #search .el-tabs__nav.is-top{
    /*padding-left:12px;*/
    box-sizing: border-box;
  }
  #search .el-tabs__header .el-tabs__item{
    color:#fff;
    height:100%;
  }
  #search .el-tabs__header .el-tabs__item:hover{
    background:rgb(74,76,80);
  }
  #search .el-tabs__header .el-tabs__item.is-active{
    color:rgb(255, 208, 75);
  }
  #search .el-tabs__header .el-tabs__active-bar {
    bottom: -1px;
    background-color: rgb(255, 208, 75);
    /*margin-left:12px;*/
  }
  #search .el-table__body-wrapper .el-table__expand-column i{
    /*visibility:hidden;*/
    color:transparent;
  }
  #search .el-table__expanded-cell[class*=cell]{
    padding:4px 0;
  }
  #search .nowrap{
    overflow: hidden;
    word-wrap: normal;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  #search .status_btn.active{
    background:#409EFF;
    color:#fff;
  }

</style>
