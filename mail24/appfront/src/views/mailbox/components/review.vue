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
                    <el-button  v-if="status=='wait'" type="success" size="mini" @click="updateStatus('permit',sels)" :disabled="sels.length==0">{{lan.MAILBOX_COM_REVIEW_PASS}}</el-button>
                    <el-button style="margin-right:12px;" v-if="status=='wait'"  type="warning" size="mini" @click="show_reject_dialog(sels)" :disabled="sels.length==0">{{lan.MAILBOX_COM_REVIEW_REJECT}}</el-button>
                    <el-button-group>
                      <el-button class="status_btn" size="small" :class="{active:status=='wait'}"  @click="changeStatus('wait')">{{lan.MAILBOX_COM_REVIEW_WAIT_LIST}}</el-button>
                      <el-button class="status_btn" size="small" :class="{active:status=='permit'}" @click="changeStatus('permit')">{{lan.MAILBOX_COM_REVIEW_PASS_LIST}}</el-button>
                      <el-button class="status_btn" size="small" :class="{active:status=='reject'}" @click="changeStatus('reject')">{{lan.MAILBOX_COM_REVIEW_REJECT_LIST}}</el-button>
                    </el-button-group>

                  </el-col>
                  <el-col :span="12">
                    <el-pagination style="text-align: right;"
                      @size-change="sizeChange($event,'wait')"
                      @current-change="currentChange($event,'wait')"
                      :current-page="waitData.page"
                      :page-sizes="[10, 20, 50, 100]"
                      :page-size="waitData.page_size"
                      layout="total, sizes, prev, slot, next,jumper"
                                   v-if="waitData.total>0"
                      :total="waitData.total">
                      <span> {{waitData.page+' / '+Math.ceil(waitData.total/waitData.page_size)}}</span>
                    </el-pagination>
                  </el-col>
                </el-row>
                <!--@row-click="rowClick_wait"-->
                <!--:height="table_height"-->
                <el-table :data="waitData.tableData"
                          v-loading="reviewLoading"
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
                    :label="lan.COMMON_SUBJECT2"
                    >
                    <template slot-scope="scope">
                      <div v-if="status!='wait'" class="nowrap" :title="scope.row.subject">{{scope.row.subject}}</div>
                      <div v-if="status=='wait'" class="nowrap" @click.stop="readMailReview(scope.row)" :title="scope.row.subject" style="cursor:pointer;color:#409EFF;">{{scope.row.subject}}</div>
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="sender"
                    :label="lan.COMMON_SENDER" width="180">
                    <template slot-scope="scope">
                      <div class="nowrap" :title="scope.row.sender">
                        {{scope.row.sender}}
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="recipient"
                    :label="lan.COMMON_RECAIVER" width="180">
                    <template slot-scope="scope">
                      <div class="nowrap" :title="scope.row.recipient">
                        {{scope.row.recipient}}
                      </div>
                    </template>
                  </el-table-column>


                  <el-table-column
                    prop="datetime"
                    :label="lan.MAILBOX_COM_REVIEW_DATE" width="150">
                    <template slot-scope="scope">
                      <div class="nowrap" >
                        {{scope.row.datetime.replace('T',' ')}}
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="mailsize"
                    :label="lan.COMMON_SIZE" width="100">
                    <template slot-scope="scope">
                      <div>
                        {{scope.row.mailsize |mailsize}}
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="reason"
                    :label="lan.MAILBOX_COM_REVIEW_OTHER">
                    <template slot-scope="scope">
                      <div class="nowrap" :title="scope.row.reason">
                        {{scope.row.reason}}
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column
                    :label="lan.COMMON_OPRATE" width="180" v-if="status=='wait'">
                    <template slot-scope="scope">
                      <div>
                        <el-button type="text" size="small" @click.stop="updateStatus('permit',[scope.row])">{{lan.MAILBOX_COM_REVIEW_PASS_ACTION}}</el-button>
                        <el-button type="text" size="small" @click.stop="show_reject_dialog([scope.row])" style="color:#f56c6c;">{{lan.MAILBOX_COM_REVIEW_REJECT_ACTION}}</el-button>
                        <el-button type="text" size="small" @click.stop="readMailReview(scope.row)">{{lan.MAILBOX_COM_REVIEW_VIEW_MAIL}}</el-button>
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
          <el-dialog :title="lan.MAILBOX_COM_REVIEW_REJECT_MAIL"  :visible.sync="waitData.show_reason"  :append-to-body="true" width="520px">
            <el-form :model="waitData.rejectForm" label-width="100px" :rules="waitData.rejectRule" ref="dbForm" size="small">

              <el-form-item :label="lan.MAILBOX_COM_REVIEW_REJECT_REASON" prop="reason" >
                <el-input v-model="waitData.rejectForm.reason" :placeholder="lan.MAILBOX_COM_REVIEW_INPUT_REJECT_REASON" type="textarea" autosize></el-input>
              </el-form-item>

            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click.native="waitData.show_reason = false" size="small">{{lan.COMMON_BUTTON_CANCELL}}</el-button>
              <el-button type="primary" @click.native="updateStatus('reject',waitData.rejectForm.reject_id)" size="small">{{lan.COMMON_BUTTON_CONFIRM}}</el-button>
            </div>
          </el-dialog>
        </div>
      <!--</div>-->
    </div>

  <!--</article>-->
</template>

<script>
  import lan from '@/assets/js/lan';
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
        reviewLoading:false,
        hashTab:[],
        tableTabs: [{
          title: '',
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
              { required: true, message: '', trigger: 'blur' },
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
            title: subject|| this.lan.MAILBOX_NO_SUBJECT,
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
          this.$confirm('<p>'+this.lan.MAILBOX_COM_REVIEW_IS_PASS+'</p>', this.lan.MAILBOX_COM_READ_SYSTEM_NOTICE, {
            confirmButtonText: this.lan.COMMON_BUTTON_CONFIRM,
            cancelButtonText: this.lan.COMMON_BUTTON_CANCELL,
            dangerouslyUseHTMLString: true,
            type: 'warning'
          }).then(() => {
            param.reason = '';
            uploadReviews(param).then(res=>{
              this.$message({
                type:'success',
                message:this.lan.COMMON_OPRATE_SUCCESS
              })
              this.waitData.page = 1;
              this.getWait('wait');
              this.$parent.getReviewShow();
            }).catch(err=>{
              console.log(err)
              this.$message({
                type:'error',
                message:this.lan.COMMON_OPRATE_FAILED
              })
            })
          }).catch(() => {

          });
        }else{
          if(!this.waitData.rejectForm.reason){
            this.$message({
              type:'error',
              message:this.lan.MAILBOX_COM_REVIEW_INPUT_REJECT_REASON
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
              message:this.lan.COMMON_OPRATE_SUCCESS
            })
          }).catch(err=>{
            this.$message({
              type:'error',
              message:this.lan.COMMON_OPRATE_FAILED
            })
            console.log(err)
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
        this.reviewLoading = true;
        mailReview(param).then(res=>{
          this.reviewLoading = false;
          this.waitData.total = res.data.count;
          this.waitData.tableData = res.data.results;
        }).catch(err=>{
          this.reviewLoading = false;
          console.log(err)
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
    computed:{
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
        this.tableTabs[0] = {
          title: lang.MAILBOX_COM_REVIEW_TITLE_NAME,
          name: '1',
        }
        this.rejectRule = {
          reason:[
            { required: true, message: lang.MAILBOX_COM_REVIEW_INPUT_REJECT_REASON, trigger: 'blur' },
          ]
        }
        return lang
      },
    }
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

