<template>
  <div style="box-sizing: border-box" id="search">
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="登录查询" name="login">
        <el-pagination style="text-align: right;"
          @size-change="sizeChange($event,'login')"
          @current-change="currentChange($event,'login')"
          :current-page="loginData.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="loginData.page_size"
          layout="total, sizes, prev, pager, next "
          :total="loginData.total">
        </el-pagination>
        <el-table

          :data="loginData.tableData"
          stripe
          :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}"
          size="mini"
          style="width: 100%">
          <el-table-column
            prop="created"
            label="登录时间">
            <template slot-scope="scope">
              <div>
                {{scope.row.created.replace('T',' ')}}

              </div>
            </template>
          </el-table-column>

          <el-table-column
            prop="client_ip"
            label="IP地址"
            >
          </el-table-column>
          <el-table-column
            prop="type"
            label="登录方式">
          </el-table-column>

          <el-table-column
            prop="remark"
            label="登录结果">
            <template slot-scope="scope">
              <div>
                <span style="color:#45AB19;"> {{scope.row.remark }} </span>
              </div>

            </template>
          </el-table-column>
        </el-table>

      </el-tab-pane>
      <el-tab-pane label="发信查询" name="send">
        <el-pagination style="text-align: right;"
          @size-change="sizeChange($event,'send')"
          @current-change="currentChange($event,'send')"
          :current-page="sendData.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="sendData.page_size"
          layout="total, sizes, prev, pager, next "
          :total="sendData.total">
        </el-pagination>
        <el-table ref="sendTable" id="sendTable"

          :data="sendData.tableData"
          stripe
          :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}"
          size="mini"
          style="width: 100%">
          <el-table-column type="expand" class="expand">
            <template slot-scope="props">
              <el-row v-for="(r,k) in props.row.details" v-if="props.row.details.length>1" :key="k" style="padding:4px 0;">
                <el-col :style="{marginLeft:expand_table.marginLeft+'px',width:expand_table.col1+'px'}" :title="r.recipient" style="box-sizing:border-box;overflow: hidden;white-space: nowrap;text-overflow: ellipsis;padding-left:10px;">
                  <span v-if="r.name">{{r.name +' '}} &lt;</span> <span> {{r.recipient}}</span> <span v-if="r.name">&gt;</span>
                <!--<span style="color:#45AB19;margin-left:20px;"> {{r.status_show +','+ r.recall_status_show}}</span>-->
                </el-col>
                <el-col :style="{width:expand_table.col2+'px'}" style="overflow: hidden; white-space: nowrap;text-overflow: ellipsis;box-sizing:border-box;padding-left:10px;">
                  <span style="color:#45AB19;margin:20px;"> {{r.inform||''}}</span>
                </el-col>
                <el-col :style="{width:expand_table.col3+'px'}" style="overflow: hidden;white-space: nowrap;text-overflow: ellipsis;box-sizing:border-box;padding-left:10px;">
                  <el-button type="text" size="mini" v-if="r.recall_status == 'stay'" @click="recall(props.row,'single',r.recipient)">召回邮件</el-button>
                </el-col>
              </el-row>

            </template>
          </el-table-column>
          <el-table-column
            prop="send_time"
            label="时 间">
            <template slot-scope="scope">
              <div>
                {{scope.row.send_time.replace('T',' ')}}
              </div>
            </template>
          </el-table-column>

          <el-table-column
            prop="subject"
            label="主 题"
            >
            <template slot-scope="scope" >
              <div class="nowrap" :title="scope.row.subject">
                {{scope.row.subject}}
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop=""
            label="收件人">
            <template slot-scope="scope">
              <div v-if="scope.row.details.length>1">
                <el-button type="text" size="mini" icon="el-icon-arrow-up" @click="changeExpand(scope.row)"> 所有收件人{{'（'+scope.row.details.length+'）'}}</el-button>
                <!--<p v-for="(r,k) in scope.row.recipients" :key="k"> {{ r[0] +' <'+r[1]+'>'}}</p>-->
              </div>
              <div v-if="scope.row.details.length==1">
                <span v-if="scope.row.details[0].name">{{scope.row.details[0].name+' '}} &lt;</span>
                <span>{{scope.row.details[0].recipient}}</span>
                <span v-if="scope.row.details[0].name">&gt;</span>

              </div>
            </template>
          </el-table-column>

          <el-table-column
            prop="details"
            label="状 态">
            <template slot-scope="scope" >
              <div v-if="scope.row.details.length==1">
                <!--<span style="color:#45AB19;"> {{scope.row.details[0].status_show+','+scope.row.details[0].recall_status_show}} </span>-->
                <span style="color:#45AB19;"> {{scope.row.details[0].inform||''}} </span>
              </div>
            </template>
          </el-table-column>

          <el-table-column
            label="操 作">
            <template slot-scope="scope">
              <div>
                <el-button type="text" size="mini" v-if="scope.row.details.length == 1 && scope.row.details[0].recall_status == 'stay'" @click="recall(scope.row)">召回邮件</el-button>
                <el-button type="text" size="mini" v-if="show_recall_all(scope.row)" @click="recall(scope.row)">召回全部邮件</el-button>
              </div>

            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="收信查询" name="mail">
        <div>
          <span>信件来源： </span>
          <el-button-group>
            <el-button class="status_btn" size="mini" :class="{active:mailData.status == ''}" @click="changeStatus('')">全部来信</el-button>
            <el-button class="status_btn" size="mini" :class="{active:mailData.status == 'success'}" @click="changeStatus('success')">收件箱和个人文件夹</el-button>
            <el-button class="status_btn" size="mini" :class="{active:mailData.status == 'spam-flag'}" @click="changeStatus('spam-flag')">垃圾箱</el-button>
            <el-button class="status_btn" size="mini" :class="{active:mailData.status == 'virus'}" @click="changeStatus('virus')">病毒拦截</el-button>
            <el-button class="status_btn" size="mini" :class="{active:mailData.status == 'spam'}" @click="changeStatus('spam')">垃圾拦截</el-button>
          </el-button-group>
        </div>
        <el-pagination style="text-align: right;"
          @size-change="sizeChange($event,'mail')"
          @current-change="currentChange($event,'mail')"
          :current-page="mailData.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="mailData.page_size"
          layout="total, sizes, prev, pager, next "
          :total="mailData.total">
        </el-pagination>
        <el-table

          :data="mailData.tableData"
          stripe
          :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}"
          size="mini"
          style="width: 100%">
          <el-table-column
            prop="logtime"
            label="时 间">
            <template slot-scope="scope">
              <div>
                {{scope.row.logtime.replace('T',' ')}}
              </div>
            </template>
          </el-table-column>

          <el-table-column
            prop="subject"
            label="主题"
            >
            <template slot-scope="scope" >
              <div class="nowrap" :title="scope.row.subject">
                {{scope.row.subject}}
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="send_mail"
            label="发件人">
          </el-table-column>

          <el-table-column
            prop="folder"
            label="存储位置">
            <template slot-scope="scope">
              <div>
                <span> {{scope.row.folder }} </span>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="remark"
            label="备注">
            <template slot-scope="scope">
              <div>
                <span> {{scope.row.remark }} </span>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="删信查询" name="delete">
        <div>
          <span>信件来源： </span>
          <el-button-group>
            <el-button class="status_btn" size="mini" :class="{active:deleteData.status == ''}" @click="changeType('')">全部删信</el-button>
            <el-button class="status_btn" size="mini" :class="{active:deleteData.status == 'web'}" @click="changeType('web')">网页删信</el-button>
            <el-button class="status_btn" size="mini" :class="{active:deleteData.status == 'system'}" @click="changeType('system')">自动清理</el-button>
            <el-button class="status_btn" size="mini" :class="{active:deleteData.status == 'client'}" @click="changeType('client')">客户端删信</el-button>
          </el-button-group>
        </div>
        <el-pagination style="text-align: right;"
          @size-change="sizeChange($event,'delete')"
          @current-change="currentChange($event,'delete')"
          :current-page="deleteData.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="deleteData.page_size"
          layout="total, sizes, prev, pager, next "
          :total="deleteData.total">
        </el-pagination>
        <el-table

          :data="deleteData.tableData"
          stripe
          :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}"
          size="mini"
          style="width: 100%">
          <el-table-column
            prop="created"
            label="删除时间">
            <template slot-scope="scope">
              <div>
                {{scope.row.created.replace('T',' ')}}
              </div>
            </template>
          </el-table-column>

          <el-table-column
            prop="subject"
            label="主题"
            >
            <template slot-scope="scope" >
              <div class="nowrap" :title="scope.row.subject">
                {{scope.row.subject}}
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="send_mail"
            label="发件人">
          </el-table-column>

          <el-table-column
            prop="folder"
            label="删除信息">
            <template slot-scope="scope">
              <div>
                <span> {{scope.row.type_show }} </span>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
    <el-dialog title="邮件召回" :visible.sync="recallTableVisible" :append-to-body="true" size="mini">
      <el-table :data="recallData">
        <el-table-column property="email" label="收件人"></el-table-column>
        <el-table-column property="recall_status_info" label="召回状态" width="200"></el-table-column>
        <el-table-column property="inform" label="邮件详情"></el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>

import {getLoginList,getSendlog,getMaillog,getDeletellog,sendRecall} from '@/api/api'
export default {
  data() {
    return {
      expand_table:{
        marginLeft:0,
        col1:100,
        col2:100,
        col3:100,
      },
      recallTableVisible:false,
      recallData:[],
      activeName: 'login',
      loginData:{
        loading:false,
        page: 1,
        page_size:20,
        total:200,
        tableData: [
        // {
        //   "id": 499369,
        //   "created": "2018-11-01T14:27:30",
        //   "client_ip": "192.168.1.200",
        //   "area": "",
        //   "type": "web",
        //   "is_login": true,
        //   "remark": "登录成功"
        // },
        // {
        //   "id": 499364,
        //   "created": "2018-11-01T14:25:08",
        //   "client_ip": "192.168.1.24",
        //   "area": "",
        //   "type": "imap",
        //   "is_login": true,
        //   "remark": "登录成功"
        // },
        // {
        //   "id": 499343,
        //   "created": "2018-11-01T14:24:52",
        //   "client_ip": "192.168.1.200",
        //   "area": "",
        //   "type": "web",
        //   "is_login": true,
        //   "remark": "登录成功"
        // }
        ]
      },
      sendData:{
        loading:false,
        page: 1,
        page_size:20,
        total:200,
        tableData: [
        // {
        //   "id": 113,
        //   "mailbox": 7368,
        //   "message_id": "<2596ac02dd7d11e885b1005056a7d988@test.com>",
        //   "send_time": "2018-11-01T10:23:40",
        //   "subject": "lw@test.com",
        //   "recipients":[['李威','lw@test.com'],['李威','lw@test.com']],
        //   "details":{
        //     "status": "deliver",
        //     "status_show": "已投递",
        //     "inform": null,
        //     "recall_status": "stay",
        //     "recall_status_show": "未召回",
        //     "recipient": "lw@test.com"
        //   }
        // },
        // {
        //   "id": 114,
        //   "mailbox": 7368,
        //   "message_id": "<2596ac02dd7d11e885b1005056a7d988@test.com>",
        //   "send_time": "2018-11-01T10:23:40",
        //   "subject": "lw@test.com",
        //   "recipients":[['李威','lw@test.com']],
        //   "details":{
        //     "status": "deliver",
        //     "status_show": "已投递",
        //     "inform": null,
        //     "recall_status": "stay",
        //     "recall_status_show": "未召回",
        //     "recipient": "lw@test.com"
        //   }
        // }
        ]
      },
      mailData:{
        loading:false,
        page: 1,
        page_size:20,
        total:200,
        tableData: [
          // {
          //   "id": 275591,
          //   "logtime": "2018-11-01 10:21:44",
          //   "subject": "lw@test.com",
          //   "result": "1",
          //   "result_show": "成功",
          //   "send_mail": "lw@test.com",
          //   "folder": "收件箱",
          //   "remark": ""
          // },
          // {
          //   "id": 275589,
          //   "logtime": "2018-11-01 10:15:19",
          //   "subject": "测试",
          //   "result": "1",
          //   "result_show": "成功",
          //   "send_mail": "anna@test.com",
          //   "folder": "收件箱",
          //   "remark": ""
          // }
        ],
        status:''
      },
      deleteData:{
        loading:false,
        page: 1,
        page_size:20,
        total:200,
        tableData: [
          // {
          //   "id": 7,
          //   "created": "2018-10-29T17:29:06",
          //   "subject": "aaaaaaaaaaaaaaaaaaaaaa",
          //   "send_mail": "lw@test.com",
          //   "type": "web",
          //   "type_show": "网页删信",
          //   "message_id": "<f94dec6adb4611e885b1005056a7d988@test.com>",
          //   "folder": "Drafts"
          // },
          // {
          //   "id": 6,
          //   "created": "2018-10-29T17:29:06",
          //   "subject": "",
          //   "send_mail": "lw@test.com",
          //   "type": "web",
          //   "type_show": "网页删信",
          //   "message_id": "<355e0662db5211e885b1005056a7d988@test.com>",
          //   "folder": "Drafts"
          // }
        ],
        status:''
      }

    };
  },
  methods: {
    show_recall_all(row){
      let result =  row.details.length > 1;
      for(let i=0;i<row.details.length;i++){
        if(row.details[i].recall_status!='stay'){
          result = false;
          break;
        }
      }
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
            if(type && type =='single'){
              str = r;
            }else{
              row.details.forEach(val=>{
                str += val.recipient+','
              })
              str = str.slice(0,str.length-1)
            }
            let param = {
              message_id: message_id,
              recipient: str
            }
            sendRecall(param).then(res => {
              this.recallData = res.data.results;
              this.recallTableVisible = true;
              this.getSend();
            }).catch(err=>{
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
        page_size:this.loginData.page_size
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
        page_size:this.sendData.page_size
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
        page_size:this.mailData.page_size
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
        page_size:this.deleteData.page_size
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
      if(index==1){
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
