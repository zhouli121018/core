<template>
  <!--<article class="mlmain mltabview">-->
    <div class="mltabview-content" id="review"  ref="box_height" style="padding-bottom:10px;box-sizing:border-box">
      <!--<div class="mltabview-panel">-->
        <div class="tab_box" style="overflow:hidden">
          <el-tabs v-model="tabsValue"  type="border-card" closable @tab-remove="removeTab" class="tab_style_tt" @tab-click="tabClick"  style="height:100%;">
            <el-tab-pane
              v-for="(item, index) in tableTabs"
              :key="item.name"
              :label="item.title"
              :name="item.name"

            >
               <span slot="label" class="tab_title" :class="{no_close:item.name==1}" :title="item.title"> {{item.title | hide_subject}} </span>
              <div v-if="item.name == 1">

                <el-row style="margin:12px 0 0;" class="toolbar">
                  <el-col :span="12">
                    <el-button  v-if="status=='wait'" type="success" size="mini" @click="updateStatus('permit',sels)" :disabled="sels.length==0">审核通过</el-button>
                    <el-button style="margin-right:12px;" v-if="status=='wait'"  type="warning" size="mini" @click="show_reject_dialog(sels)" :disabled="sels.length==0">拒绝通过</el-button>
                    <el-button-group>
                      <el-button class="status_btn" size="small" :class="{active:status=='wait'}"  @click="changeStatus('wait')">待审核列表</el-button>
                      <el-button class="status_btn" size="small" :class="{active:status=='permit'}" @click="changeStatus('permit')">审核通过列表</el-button>
                      <el-button class="status_btn" size="small" :class="{active:status=='reject'}" @click="changeStatus('reject')">拒绝通过列表</el-button>
                    </el-button-group>

                  </el-col>
                  <el-col :span="12">
                    <el-pagination style="text-align: right;"
                      @size-change="sizeChange($event,'wait')"
                      @current-change="currentChange($event,'wait')"
                      :current-page="waitData.page"
                      :page-sizes="[10, 20, 50, 100]"
                      :page-size="waitData.page_size"
                      layout="total, sizes, prev, pager, next "
                      :total="waitData.total">
                    </el-pagination>
                  </el-col>
                </el-row>
                <!--@row-click="rowClick_wait"-->
                <!--:height="table_height"-->
                <el-table
                  :data="waitData.tableData"
                  border
                  stripe
                  :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}"
                  @selection-change="selsChange"
                  ref="waitTable"
                  :key="status"
                  size="mini"
                  style="width: 100%;background:rgba(255,255,255,0.4)">
                  <el-table-column v-if="status=='wait'"
                    type="selection"
                    width="55">
                  </el-table-column>
                  <el-table-column
                    prop="subject"
                    label="主题"
                    >
                    <template slot-scope="scope">
                      <div v-if="status!='wait'" class="nowrap" :title="scope.row.subject">{{scope.row.subject}}</div>
                      <div v-if="status=='wait'" class="nowrap" @click.stop="readMailReview(scope.row)" :title="scope.row.subject" style="cursor:pointer;color:#409EFF;">{{scope.row.subject}}</div>
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="sender"
                    label="发件人" width="180">
                    <template slot-scope="scope">
                      <div class="nowrap" :title="scope.row.sender">
                        {{scope.row.sender}}
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="recipient"
                    label="收件人" width="180">
                    <template slot-scope="scope">
                      <div class="nowrap" :title="scope.row.recipient">
                        {{scope.row.recipient}}
                      </div>
                    </template>
                  </el-table-column>


                  <el-table-column
                    prop="datetime"
                    label="日期" width="150">
                    <template slot-scope="scope">
                      <div class="nowrap" >
                        {{scope.row.datetime.replace('T',' ')}}
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="mailsize"
                    label="大小" width="100">
                    <template slot-scope="scope">
                      <div>
                        {{scope.row.mailsize |mailsize}}
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="reason"
                    label="其他">
                    <template slot-scope="scope">
                      <div class="nowrap" :title="scope.row.reason">
                        {{scope.row.reason}}
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="操作" width="180" v-if="status=='wait'">
                    <template slot-scope="scope">
                      <div>
                        <el-button type="text" size="small" @click.stop="updateStatus('permit',[scope.row])">通过</el-button>
                        <el-button type="text" size="small" @click.stop="show_reject_dialog([scope.row])" style="color:#f56c6c;">拒绝</el-button>
                        <el-button type="text" size="small" @click.stop="readMailReview(scope.row)">查看邮件</el-button>
                      </div>
                    </template>
                  </el-table-column>

                </el-table>
                <el-row class="toolbar"><el-col :span="24"></el-col></el-row>
              </div>
              <!--:style="{height:read_height}"-->
              <div v-if="item.name!='1'"  class="read_box">
                <Readreview v-if="item.name!='1'" :readId="item.id" readFolderId="review"></Readreview>
              </div>
            </el-tab-pane>
          </el-tabs>
          <el-dialog title="拒绝审核"  :visible.sync="waitData.show_reason"  :append-to-body="true" width="520px">
            <el-form :model="waitData.rejectForm" label-width="100px" :rules="waitData.rejectRule" ref="dbForm" size="small">

              <el-form-item label="拒绝原因：" prop="reason" >
                <el-input v-model="waitData.rejectForm.reason" placeholder="请输入拒绝原因" type="textarea" autosize></el-input>
              </el-form-item>

            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click.native="waitData.show_reason = false" size="small">取消</el-button>
              <el-button type="primary" @click.native="updateStatus('reject',waitData.rejectForm.reject_id)" size="small">确定</el-button>
            </div>
          </el-dialog>
        </div>
      <!--</div>-->
    </div>

  <!--</article>-->
</template>

<script>
  import Readreview from './readreview'
  import cookie from '@/assets/js/cookie';
  import {mailReview,updateReview,uploadReviews} from '@/api/api'
  export default {
    name:'Review',
    components:{
      Readreview
    },
    data(){
      return {
        hashTab:[],
        tableTabs: [{
          title: '邮件审核列表',
          name: '1',
        }],
        tabIndex: 1,
        tabsValue:'1',
        status:'wait',
        table_height:'300px',
        read_height:'300px',
        sels:[],
        activeName:'wait',
        waitData:{
          table_height:300,
          page:1,
          page_size:10,
          total:0,
          tableData:[
            // {
            //   id:0,
            //   sender:'123',
            //   recipient:'123@qq.com',
            //   subject:'主题',
            //   datetime:'2018-10-10 15:20:10',
            //   mailsize:123456,
            //   reason:'kdsokjdsf',
            // },
          ],
          rejectForm:{
            reason:'',
            reject_id:[]
          },
          rejectRule:{
            reason:[
              { required: true, message: '请输入拒绝原因！', trigger: 'blur' },
            ]
          },
          show_reason:false
        },
      }
    },
    methods:{
      tabClick(){},
      addTab(rid,subject) {

        if(rid && this.hashTab[rid]){
          this.tabsValue = this.hashTab[rid];
        }else{
          let newTabName = ++this.tabIndex + '';
          this.hashTab[rid] = newTabName;
          this.tableTabs.push({
            title: subject||'无主题',
            name: newTabName,
            id:rid,
          });
          this.tabsValue = newTabName;
        }

      },
      removeTab(targetName) {
        let tabs = this.tableTabs;
        let activeName = this.tabsValue;
        if (activeName === targetName) {
          tabs.forEach((tab, index) => {
            if (tab.name === targetName) {
              let nextTab = tabs[index + 1] || tabs[index - 1];
              if (nextTab) {
                activeName = nextTab.name;
              }
            }
          });
        }
        this.tabsValue = activeName;
        for(let i=0;i<tabs.length;i++){
          if(tabs[i].name == targetName){
            if(tabs[i].id){
              this.hashTab[tabs[i].id] = false;
            }
          }
        }
        this.tableTabs = tabs.filter(tab => tab.name !== targetName);

      },
      changeStatus(status){
        this.status = status;
        sessionStorage['reviewStatus'] = status;
        this.waitData.page = 1;
        this.getWait();
      },
      readMailReview(row){
        console.log(this)
        this.addTab(row.id,row.subject);
      },
      rowClick_wait(row){
        console.log(arguments)
        this.$refs.waitTable.toggleRowSelection(row)
      },
      updateStatus(status,sels){
        let arr = [];
        sels.forEach(val=>{
          arr.push(val.id);
        })
        let param = {
          status:status,
          review_ids:arr,
          reason:this.waitData.rejectForm.reason
        }
        if(status == 'permit'){
          this.$confirm('<p>审核通过选中邮件?</p>', '系统信息', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            dangerouslyUseHTMLString: true,
            type: 'warning'
          }).then(() => {
            param.reason = '';
            uploadReviews(param).then(res=>{
              this.$message({
                type:'success',
                message:'操作成功！'
              })
              this.waitData.page = 1;
              this.getWait('wait');
              this.$parent.getReviewShow();
            }).catch(err=>{
              console.log('更新审核状态出错！',err)
              this.$message({
                type:'error',
                message:'操作失败！'
              })
            })
          }).catch(() => {

          });
        }else{
          if(!this.waitData.rejectForm.reason){
            this.$message({
              type:'error',
              message:'请输入拒绝原因！'
            })
            return;
          }
          uploadReviews(param).then(res=>{
            console.log(res)
            this.waitData.show_reason = false;
            this.waitData.rejectForm.reason = '';
            this.waitData.page = 1;
            this.getWait('wait')
            this.$parent.getReviewShow();
            this.$message({
              type:'success',
              message:'操作成功！'
            })
          }).catch(err=>{
            this.$message({
              type:'error',
              message:'操作失败！'
            })
            console.log('更新审核状态出错2！',err)
          })
        }
      },
      show_reject_dialog(reject_id){
        this.waitData.show_reason = true;
        this.waitData.rejectForm.reject_id = reject_id;
      },
      selsChange(sels){
        console.log(sels)
        this.sels = sels
      },
      handleClick(tab, event) {
        console.log(tab)
        let index = tab.$data.index;
        sessionStorage['reviewIndex'] = index;
        // this.getWait(tab.name);
      },
      sizeChange(val,type) {
        this.waitData.page = 1;
        this.waitData.page_size = val;
        this.getWait();
      },
      currentChange(val,type) {
        this.waitData.page = val;
        this.getWait();
      },
      getWait(){
        let param ={
          page:this.waitData.page,
          page_size:this.waitData.page_size,
          status:this.status
        };
        mailReview(param).then(res=>{
          console.log(res)
          this.waitData.total = res.data.count;
          this.waitData.tableData = res.data.results;
        }).catch(err=>{
          console.log('getWait错误',err)
        })
      },
    },
    mounted: function(){
      this.$nextTick(()=>{
        this.table_height = (this.$refs.box_height.getBoundingClientRect().height-148 )+'px'
        this.read_height = (this.$refs.box_height.getBoundingClientRect().height-83 )+'px'
      })
    },
    created(){
      if(sessionStorage['reviewStatus']){
        this.status = sessionStorage['reviewStatus'];
        this.getWait();
      }else{
        this.getWait();
      }

    },
    watch: {

    },
    filters: {
      hide_subject: function (value) {
        if (!value) return ''
        value = value.toString()
        if(value.length>6){
          return value.slice(0,6)+'...'
        }else{
          return value
        }
      },
    },
  }
</script>

<style>
  #review .el-tabs--border-card>.el-tabs__content{
    /*padding-left:0;*/
    padding-top:0;
  }
  #review .el-tabs--border-card{
    border:none;
  }
  #review .action_btns{
    visibility: hidden;
  }
  #review .action_btns.show_btns{
    visibility: visible;
  }
#review .nowrap{
    overflow: hidden;
    word-wrap: normal;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  #review .status_btn.active{
    background:#409EFF;
    color:#fff;
  }
  #review div.el-tabs.hide_tab_top.tab_style_tt>.el-tabs__content{
    top:0 !important;
  }
  #review div.el-tabs.tab_style_tt>.el-tabs__content{
    overflow:auto;
    box-sizing: border-box;
    padding-bottom:10px;
    /*min-height:600px;*/
    position: absolute;
    top: 41px;
    bottom: 0;
    left: 0;
    right: 0;
  }
  #review .el-tabs.el-tabs--card.el-tabs--top{
    height:100%;
  }
</style>

