<template>
        <div class="mltabview-content">
            <div v-if="collapseItems[0].lists.length>0" class="mltabview-panel">
                <div class="m-mllist">
                    <div class="list-bg"></div>
                    <div class="m-mllist-row">
                        <div class="toolbar" style="background:#fff;">
                            <span class=" f-fr j-setting">
                                <el-button  icon="el-icon-setting" circle></el-button></span>
                            <div id="pagination" class="f-fr">
                            <div class="">
                                <el-dropdown trigger="click">
                                <span class="el-dropdown-link">
                                    1 / 1 <i class="el-icon-arrow-down el-icon--right"></i>
                                </span>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item>1</el-dropdown-item>
                                    <el-dropdown-item>2</el-dropdown-item>
                                </el-dropdown-menu>
                                </el-dropdown>
                                <el-button-group>
                                <el-button  size="small" icon="el-icon-arrow-left" plain round></el-button>
                                <el-button  size="small" plain round><i class="el-icon-arrow-right el-icon--right"></i></el-button>
                                </el-button-group>
                            </div>
                            </div>

                            <!--选择-->
                            <el-dropdown @command="handleCommand">
                                <el-button  size="small" plain>
                                    <span><el-checkbox v-model="checkAll" @change="tabCheckAll"></el-checkbox></span>
                                    <i class="el-icon-arrow-down el-icon--right"></i>
                                </el-button>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item v-for="item in checkItems" :key="item.id" class="dropdown_item" :class="{ active: checkIndex===item.id }"
                                    :divided="item.divided" :command="item.id">
                                    <b><i class="el-icon-check vibility_hide" :class="{ vibility_show: checkIndex===item.id }"></i>
                                    </b> {{item.text}}
                                    </el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>

                            <!--排序-->
                            <el-dropdown @command="orderHandleCommand">
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
                            <el-dropdown @command="viewHandleCommand">
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
                            <div v-if="selectCounts" class="inline_block">
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

                                <div class="inline_block">
                                    <el-button  size="small" plain >
                                        <span>标记为</span>
                                        <i class="el-icon-arrow-down el-icon--right"></i>
                                    </el-button>

                                </div>

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
                    </div>

                    <div class="mail-totals j-mail-totals" v-if="!selectCounts">
                        <div class="totals-info">
                        收件箱(
                        <span class="all-mail">共<span class="number">3</span>封</span>
                        <span class="unread-mail"><span class="number">1</span>封</span>
                        <a href="#" >未读</a>
                        ,<a href="#" >全部设为已读</a>
                        )

                        </div>
                    </div>
                    <div class="j-select-count select-count" v-if="selectCounts">
                        <span class="j-desc desc">已选择 {{selectCounts}} 封</span>
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
                        <el-collapse v-show="false" v-model="activeNames" @change="handleChange">
                            <el-collapse-item v-for="t in collapseItems" :key="t.id" :title="'更早（'+titleCount+'）'" :name="t.id">
                                <ul class="list-wrap j-mail-list ">
                                    <li class="list-item j-mail display-summary"  v-for="(l,k) in t.lists" :key="l.uid" :class="{flagged:l.flagged,'label0-0':l.flagged,selected:l.checked,read:l.isread,unread:!l.isread}" >
                                        <div @click="readmail(t.id,k,l.uid,l.subject)" class="item-content mail-info">
                                            <div class="info-desc">
                                                <div class="info-desc-left">
                                                    <div class="desc-flag">
                                                            <span class="flag-flagged j-flag" :class="{unflag:!l.flagged}" @click.stop="changeFlag(t.id,k)">
                                                                <i :title="l.flagged?'点击取消旗帜':'设为红旗'" class="iconfont" :class="l.flagged?'icon-iconflatcolor':'icon-iconflat'"></i>
                                                            </span>
                                                        <span class="flag-defer unflag">
                                                                <i title="设置待办" class="j-undefer iconfont icon-iconclock"></i>
                                                        </span>
                                                    </div>
                                                    <div class="desc-text">
                                                        <span class="icon"><i class="j-priorityIcon iconfont " title=""></i></span>
                                                        <span class="subject" title="l.text">{{l.subject||'无主题'}}</span>
                                                    </div>
                                                </div>

                                                <div class="info-desc-right">
                                                    <span class="desc-time">{{l.internaldate}}</span>
                                                </div>
                                            </div>
                                            <div class="info-summary">
                                                <p class="summary-text">
                                                    <span class="fromto from" v-if="l.mfrom"> {{(l.mfrom[1]==null?'':l.mfrom[1]) + " <"+l.mfrom[0]+">"}}</span>
                                                    <span class="fromto" v-if="l.plain">：</span>
                                                    <span class="summary"> {{l.plain}}</span>
                                                </p>
                                                <div class="summary-stat">
                                                    <div class="summary-stat-bg"></div>
                                                </div>
                                            </div>
                                            <div class="info-icon">
                                                <span><i class="j-normalIcon iconfont state-icon icon-SYSTEM" title="系统认证可信任来源"></i></span>
                                            </div>
                                        </div>
                                        <div class="item-chk check-col" title="系统认证可信任来源">

                                            <el-checkbox :v-model="l.checked" @change="changeSelect(t.id,k)"></el-checkbox>
                                        </div>
                                        <div class="item-active-border"></div>
                                        <div class="item-divider"></div>
                                    </li>
                                </ul>
                            </el-collapse-item>
                        </el-collapse>

                        <!--<div class="mllist-pagination">-->
                        <!--</div>-->
                        <div>
                          <el-table :data="collapseItems[0].lists" style="width: 100%;" class="vertical_align_top"
                              highlight-current-row
                            >
                            <el-table-column
                              type="selection"
                              width="36"
                              @selection-change="handleSelectionChange"
                            >
                            </el-table-column>

                            <el-table-column prop="subject"  label="" @click="">
                              <template slot-scope="scope">
                                <div class="clear" style="font-size:16px;" :class="{flagged:scope.row.flagged,unseen:!scope.row.isread}">
                                  <span class="fl_l" >{{scope.row.subject}}</span>
                                  <span class="fl_r">
                                    <i title="点击取消旗帜" class="iconfont" :class="{'icon-iconflatcolor':scope.row.flagged,'icon-iconflat':!scope.row.flagged}"></i>
                                  </span>
                                </div>
                                <div class="info-summary">
                                  <p class="summary-text">
                                    <span class="fromto from" v-if="scope.row.mfrom">{{scope.row.mfrom[1]}} <{{scope.row.mfrom[0]}}></span>
                                    <span class="fromto">:</span>
                                    <span class="summary">
                                      sdajpofjsdfhup测试
                                    </span>
                                  </p>
                                </div>
                              </template>
                            </el-table-column>



                            <el-table-column  prop="date" label=""  width="160" :formatter="formatter"></el-table-column>
                          </el-table>
                        </div>
                      </div>

                    </div>
                </div>
            </div>
            <div v-if="collapseItems[0].lists.length==0" class="mltabview-panel">
               <h3 style="margin:30px 0 0 20px;font-size:24px;font-weight:normal;"> "{{curr_folder}}" 没有邮件</h3>
            </div>
        </div>
</template>
<script>
  import {getMailMessage,moveMails,getFloder,getFloderMsg,deleteMail} from "@/api/api";

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
          multipleSelection:[],
          tableData: [{
          date: '2016-05-02',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
          tag: '家'
        }, {
          date: '2016-05-04',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1517 弄',
          tag: '公司'
        }, {
          date: '2016-05-01',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1519 弄',
          tag: '家'
        }, {
          date: '2016-05-03',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1516 弄',
          tag: '公司'
        }],
          totalCount:100,
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
            {id:0,text:'全部邮件',divided:false},
            {id:1,text:'未读邮件',divided:false},
            {id:2,text:'已读邮件',divided:false},
            {id:3,text:'已标记邮件',divided:true},
            {id:4,text:'未标记邮件',divided:false},
            {id:5,text:'紧急',divided:true},
            {id:6,text:'普通',divided:false},
            {id:7,text:'缓慢',divided:false},
            {id:8,text:'包含附件',divided:true},
            {id:9,text:'不包含附件',divided:false},
            {id:10,text:'已回复',divided:true},
            {id:11,text:'已转发',divided:false},
          ],
          moveCheckIndex:'',
          moveItems:[
            {id:0,text:'已发送',divided:false},
            {id:1,text:'已删除',divided:false},
            {id:2,text:'垃圾邮件',divided:false},
            {id:3,text:'病毒文件夹',divided:false}
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
       handleSelectionChange(val) {
        this.multipleSelection = val;
        console.log(this.multipleSelection)
      },
      formatter(row, column) {
        return row.date.replace('T','  ');
      },
      filterTag(value, row) {
        return row.tag === value;
      },
      filterHandler(value, row, column) {
        const property = column['property'];
        return row[property] === value;
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
      changeSelect(pid,cid){
          this.collapseItems[pid].lists[cid].checked = !this.collapseItems[pid].lists[cid].checked
          if(this.collapseItems[pid].lists[cid].checked){

          }else{

          }
      },
      changeFlag(pid,cid){
          this.collapseItems[pid].lists[cid].flagged = !this.collapseItems[pid].lists[cid].flagged;
      },
      readmail(pid,cid,mid,subject){
          this.collapseItems[pid].lists[cid].isread = true;
          console.log(mid,subject)
          this.$emit('getRead', {'id':mid,'subject':subject,'activeTab':2});
          // this.jumpTo('read',mid)

      },
      getMessageList(){
        let params = {
          folder:this.boxId,
          limit:this.pageSize,
          offset:(this.currentPage-1)*this.pageSize
        }
        getMailMessage(params).then((res)=>{
          var items = res.data
          for(var i=0;i<items.length;i++){
            items[i].flagged = (items[i].flags.join('').indexOf('Flagged')>=0);
            console.log(items[i].flags)
            items[i].isread = (items[i].flags.join(' ').indexOf('Seen')>=0);
            items[i].plain = '';
            items[i].checked = false;
          }
          this.collapseItems[0].lists = items;
        },(err)=>{
          console.log(err)
        })
      },
      getFloderMsgById(param){
        getFloderMsg(param).then((suc)=>{
          this.totalCount = suc.data.count;
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
      }
    },
    computed:{
        selectCounts:function(){
            for (var i=0,count=0;i<this.collapseItems.length;i++){
                for(var k=0;k<this.collapseItems[i].lists.length;k++){
                    if(this.collapseItems[i].lists[k].checked){
                        count++;
                    }
                }
            }

            return count;
        },
      checkedMails:function(){
          let list=[];
          for (var i=0,count=0;i<this.collapseItems.length;i++){
                for(var k=0;k<this.collapseItems[i].lists.length;k++){
                    if(this.collapseItems[i].lists[k].checked){
                        list.push(this.collapseItems[i].lists[k].uid)
                    }
                }
          }
          return list;
      },
      titleCount:function(){
          return this.collapseItems[0].lists.length;
      },


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

