<template>
  <!--<article class="mlmain mltabview">-->
    <div class="mltabview-content" id="review">
      <div class="mltabview-panel">
      <div class="m-mlwelcome" ref="box_height">
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="待审核列表" name="wait">
            <el-row style="margin:12px 0">
              <el-col :span="12">
                <el-button type="primary" size="small" @click="updateStatus('permit',sels)" :disabled="sels.length==0">审核通过</el-button>
                <el-button type="warning" size="small" @click="show_reject_dialog(sels)" :disabled="sels.length==0">拒绝通过</el-button>
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
            <el-table :height="table_height"
              :data="waitData.tableData"
              stripe
              :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}"
              @selection-change="selsChange"
              @row-click="rowClick_wait"
              ref="waitTable"
              size="mini"
              style="width: 100%;background:rgba(255,255,255,0.4)">
              <el-table-column
                type="selection"
                width="55">
              </el-table-column>
              <el-table-column
                prop="subject"
                label="主题"
                >
                <template slot-scope="scope">
                  <div class="nowrap" @click.stop="readMailReview(scope.row)" :title="scope.row.subject" style="cursor:pointer;color:#409EFF;">{{scope.row.subject}}</div>
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
                label="操作" width="180">
                <template slot-scope="scope">
                  <div>
                    <el-button type="text" size="small" @click.stop="updateStatus('permit',[scope.row])">通过</el-button>
                    <el-button type="text" size="small" @click.stop="show_reject_dialog([scope.row])" style="color:#f56c6c;">拒绝</el-button>
                    <el-button type="text" size="small" @click.stop="readMailReview(scope.row)">查看邮件</el-button>
                  </div>
                </template>
              </el-table-column>

            </el-table>


          </el-tab-pane>
          <el-tab-pane label="审核通过列表" name="permit">
            <el-row style="margin:12px 0">
              <el-col :span="12" :offset="12">
                <el-pagination style="text-align: right;"
                  @size-change="sizeChange($event,'permit')"
                  @current-change="currentChange($event,'permit')"
                  :current-page="permitData.page"
                  :page-sizes="[10, 20, 50, 100]"
                  :page-size="permitData.page_size"
                  layout="total, sizes, prev, pager, next "
                  :total="permitData.total">
                </el-pagination>
              </el-col>
            </el-row>

            <el-table ref="sendTable" id="sendTable"
              :height="table_height"
              :data="permitData.tableData"
              stripe
              :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}"
              size="mini"
              style="width: 100%;background:rgba(255,255,255,0.4)">

              <el-table-column
                prop="subject"
                label="主题"
                >
              </el-table-column>
              <el-table-column
                prop="sender"
                label="发件人" width="180">
                <template slot-scope="scope">
                  <div>
                    {{scope.row.sender}}
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                prop="recipient"
                label="收件人" width="180">
                <template slot-scope="scope">
                  <div>
                    {{scope.row.recipient}}
                  </div>
                </template>
              </el-table-column>


              <el-table-column
                prop="datetime"
                label="日期" width="150">
                <template slot-scope="scope">
                  <div>
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
                  <div>
                    {{scope.row.reason}}
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="拒绝通过列表" name="reject">
            <el-row style="margin:12px 0">
              <el-col :span="12" :offset="12">
                <el-pagination style="text-align: right;"
                  @size-change="sizeChange($event,'reject')"
                  @current-change="currentChange($event,'reject')"
                  :current-page="rejectData.page"
                  :page-sizes="[10, 20, 50, 100]"
                  :page-size="rejectData.page_size"
                  layout="total, sizes, prev, pager, next "
                  :total="rejectData.total">
                </el-pagination>
              </el-col>
            </el-row>

            <el-table
              :height="table_height"
              :data="rejectData.tableData"
              stripe
              :header-cell-style="{background:'#f0f1f3',fontSize:'14px'}"
              size="mini"
              style="width: 100%;background:rgba(255,255,255,0.4)">
              <el-table-column
                prop="subject"
                label="主题"
                >
              </el-table-column>
              <el-table-column
                prop="sender"
                label="发件人" width="180">
                <template slot-scope="scope">
                  <div>
                    {{scope.row.sender}}
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                prop="recipient"
                label="收件人" width="180">
                <template slot-scope="scope">
                  <div>
                    {{scope.row.recipient}}
                  </div>
                </template>
              </el-table-column>


              <el-table-column
                prop="datetime"
                label="日期" width="150">
                <template slot-scope="scope">
                  <div>
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
                  <div>
                    {{scope.row.reason}}
                  </div>
                </template>
              </el-table-column>
            </el-table>
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
        table_height:'300px',
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
      readMailReview(row){
        this.$parent.addTab('readreview',row.subject,row.id,'review')
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
      this.$nextTick(()=>{
        this.table_height = (this.$refs.box_height.getBoundingClientRect().height-101 )+'px'
      })
    },
    created(){
      if(sessionStorage['reviewIndex']){
        let index = sessionStorage['reviewIndex'];
        if(index==0){
          this.activeName = 'wait';
          this.getWait('wait');
        }else if(index==1){
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
#review .nowrap{
    overflow: hidden;
    word-wrap: normal;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
</style>

