<template>
  <!--<article class="mlmain mltabview">-->
    <div class="mltabview-content">
      <div class="mltabview-panel">
      <div class="m-mlwelcome">
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="待审核列表" name="wait">
            <el-row style="margin:12px 0">
              <el-col :span="12">
                <el-button type="primary" size="small" @click="updateStatus('permit')" :disabled="sels.length==0">审核通过</el-button>
                <el-button type="warning" size="small" @click="show_reject_dialog" :disabled="sels.length==0">拒绝通过</el-button>
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

            <el-table

              :data="waitData.tableData"
              stripe
              :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}"
              @selection-change="selsChange"
              @row-click="rowClick_wait"
              ref="waitTable"
              size="mini"
              style="width: 100%">
              <el-table-column
                type="selection"
                width="55">
              </el-table-column>
              <el-table-column
                prop="subject"
                label="主题"
                >
              </el-table-column>
              <el-table-column
                prop="sender"
                label="发件人">
                <template slot-scope="scope">
                  <div>
                    {{scope.row.sender}}
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                prop="recipient"
                label="收件人">
                <template slot-scope="scope">
                  <div>
                    {{scope.row.recipient}}
                  </div>
                </template>
              </el-table-column>


              <el-table-column
                prop="datetime"
                label="日期">
                <template slot-scope="scope">
                  <div>
                    {{scope.row.datetime.replace('T',' ')}}
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                prop="mailsize"
                label="大小">
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
                  <div>
                    {{scope.row.reason}}
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                label="操作">
                <template slot-scope="scope">
                  <div>
                    <el-button type="text" size="small" @click.stop="">查看邮件</el-button>
                  </div>
                </template>
              </el-table-column>

            </el-table>

          </el-tab-pane>
          <el-tab-pane label="审核通过列表" name="permit">
            <el-pagination style="text-align: right;"
              @size-change="sizeChange($event,'permit')"
              @current-change="currentChange($event,'permit')"
              :current-page="permitData.page"
              :page-sizes="[10, 20, 50, 100]"
              :page-size="permitData.page_size"
              layout="total, sizes, prev, pager, next "
              :total="permitData.total">
            </el-pagination>
            <el-table ref="sendTable" id="sendTable"

              :data="permitData.tableData"
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
          <el-tab-pane label="拒绝通过列表" name="reject">
            <div v-if="false">
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
              @size-change="sizeChange($event,'reject')"
              @current-change="currentChange($event,'reject')"
              :current-page="rejectData.page"
              :page-sizes="[10, 20, 50, 100]"
              :page-size="rejectData.page_size"
              layout="total, sizes, prev, pager, next "
              :total="rejectData.total">
            </el-pagination>
            <el-table

              :data="rejectData.tableData"
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
        </el-tabs>

        <el-dialog title="拒绝审核"  :visible.sync="waitData.show_reason"  :append-to-body="true" width="420px">
        <el-form :model="waitData.rejectForm" label-width="100px" :rules="waitData.rejectRule" ref="dbForm" size="small">

          <el-form-item label="拒绝原因：" prop="reason" >
            <el-input v-model="waitData.rejectForm.reason" placeholder="请输入拒绝原因" type="textarea" autosize></el-input>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="waitData.show_reason = false" size="small">取消</el-button>
          <el-button type="primary" @click.native="updateStatus('reject')" size="small">确定</el-button>
        </div>
      </el-dialog>

      </div>
    </div>
    </div>

  <!--</article>-->
</template>

<script>
  import cookie from '@/assets/js/cookie';
  import {mailReview,updateReview,uploadReviews} from '@/api/api'
  export default {
    name:'Review',
    data(){
      return {
        sels:[],
        activeName:'wait',
        waitData:{
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
          },
          rejectRule:{
            reason:[
              { required: true, message: '请输入拒绝原因！', trigger: 'blur' },
            ]
          },
          show_reason:false
        },
        permitData:{
          page:1,
          page_size:10,
          total:0,
          tableData:[]
        },
        rejectData:{
          page:1,
          page_size:10,
          total:0,
          tableData:[]
        }
      }
    },
    methods:{
      rowClick_wait(row){
        console.log(arguments)
        this.$refs.waitTable.toggleRowSelection(row)
      },
      updateStatus(status){
        let arr = [];
        this.sels.forEach(val=>{
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
              console.log(res)
            }).catch(err=>{
              console.log('更新审核状态出错！',err)
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
            this.waitData.rejectForm.reason = ''
          }).catch(err=>{
            console.log('更新审核状态出错2！',err)
          })
        }
      },
      show_reject_dialog(){
        this.waitData.show_reason = true;
      },
      selsChange(sels){
        console.log(sels)
        this.sels = sels
      },
      handleClick(tab, event) {
        console.log(tab)
        let index = tab.$data.index;
        sessionStorage['reviewIndex'] = index;
        this.getWait(tab.name);
      },
      sizeChange(val,type) {
        if(type=='wait'){
          this.waitData.page_size = val;
          this.getWait('wait');
        }else if(type=='permit'){
          this.permitData.page_size = val;
          this.getWait('permit');
        }else if(type=='reject'){
          this.rejectData.page_size = val;
          this.getWait('reject')
        }
      },
      currentChange(val,type) {
        if(type=='wait'){
          this.waitData.page = val;
          this.getWait('wait');
        }else if(type=='permit'){
          this.permitData.page = val;
          this.getWait('permit');
        }else if(type=='reject'){
          this.rejectData.page = val;
          this.getWait('reject')
        }
      },
      getWait(status){
        let param ={
          page:1,
          page_size:10,
          status:status
        };
        if(status == 'wait'){
          param.page = this.waitData.page
          param.page_size = this.waitData.page_size
        }else if(status == 'permit'){
          param.page = this.permitData.page
          param.page_size = this.permitData.page_size
        }else if(status == 'reject'){
          param.page = this.rejectData.page
          param.page_size = this.rejectData.page_size
        }
        mailReview(param).then(res=>{
          console.log(res)
          if(status == 'wait'){
            this.waitData.total = res.data.count;
            this.waitData.tableData = res.data.results;
          }else if(status == 'permit'){
            this.permitData.total = res.data.count;
            this.permitData.tableData = res.data.results;
          }else if(status == 'reject'){
            this.rejectData.total = res.data.count;
            this.rejectData.tableData = res.data.results;
          }

        }).catch(err=>{
          console.log('getWait错误',err)
        })
      },
    },
    mounted: function(){

    },
    created(){
      if(sessionStorage['reviewIndex']){
        let index = sessionStorage['reviewIndex'];
        if(index==1){
          this.activeName = 'permit';
          this.getWait('permit');
        }else if(index == 2){
          this.activeName = 'reject';
          this.getWait('reject');
        }
      }else{
        this.activeName = 'wait';
        this.getWait('wait');
      }
    },
    watch: {

    }
  }
</script>

<style>

</style>

