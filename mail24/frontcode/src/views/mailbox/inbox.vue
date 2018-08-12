<template>
    <div class="m-mllist">
        <div class="list-bg"></div>
        <div class="m-mllist-row">
          <div class="toolbar">
            <span class="u-btn u-btn-default u-btn-round f-fr j-setting"><el-button type="primary" icon="el-icon-setting" circle></el-button></span>
            <div id="pagination" class="f-fr">
              <div class="u-page u-page-round">
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
                  <el-button  size="small" icon="el-icon-arrow-left" plain></el-button>
                  <el-button  size="small" plain><i class="el-icon-arrow-right el-icon--right"></i></el-button>
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
            <div v-if="showMoreMenu" class="inline_block">
              <el-button  size="small" plain>
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

          <div class="mail-totals j-mail-totals">
            <div class="totals-info">
              收件箱(
              <span class="all-mail">共<span class="number">3</span>封</span>
              <span class="unread-mail"><span class="number">1</span>封</span>
              <a href="#" >未读</a>
              ,<a href="#" >全部设为已读</a>
              )
            </div>
          </div>
        </div>
        <div class="m-mllist-row mllist-list-row">
              <el-collapse v-model="activeNames" @change="handleChange">
                <el-collapse-item title="一致性 Consistency" name="1">
                                    <ul class="list-wrap j-mail-list "><li class="list-item j-mail read                      display-summary active" mid="1:1tbiAQAJEFXEqdgAXgADsl" index="0" fid="1">
                        <div class="item-content mail-info">
                            <div class="info-desc">
                                <div class="info-desc-left">
                                    <div class="desc-flag">
                                            <span class="flag-flagged j-flag unflag">
                                                <i title="设为红旗" class="iconfont iconflat"></i>
                                            </span>
                                        <span class="flag-defer unflag">
                                                <i title="设置待办" class="j-undefer iconfont iconclock"></i>
                                        </span>
                                    </div>
                                    <div class="desc-text">
                                        <span class="icon"><i class="j-priorityIcon iconfont " title=""></i></span>
                                        <span class="subject" title="[召回邮件失败] MEMZ彩虹猫病毒/[Recall mail 失败] MEMZ彩虹猫病毒">[召回邮件失败] MEMZ彩虹猫病毒/[Recall mail 失败] MEMZ彩虹猫病毒</span>
                                    </div>
                                </div>
                                <div class="info-desc-right">
                                    <span class="desc-time">08-09</span>
                                </div>
                            </div>
                            <div class="info-summary">
                                <p class="summary-text">
                                    <span class="fromto from" data-email="postmaster@xt5-dm100.coremail.cn">
                                      postmaster
                                    </span>
                                    <span class="fromto">：</span>
                                    <span class="summary">
                发给751296883@qq.com的邮件召回失败,原因：不支持召回
                email sent to 751296883@qq.com has been recalled unsucce</span>
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
                            
                            <input type="checkbox" name="mid" data-draft="" data-fid="1" value="1:1tbiAQAJEFXEqdgAXgADsl" from="postmaster@xt5-dm100.coremail.cn" class="rc-hidden"><i class="checkbox"></i>
                        </div>
                        <div class="item-active-border"></div>
                        <div class="item-divider"></div>
                    </li></ul>


                </el-collapse-item>
                <el-collapse-item title="反馈 Feedback" name="2">
                  <div>控制反馈：通过界面样式和交互动效让用户可以清晰的感知自己的操作；</div>
                  <div>页面反馈：操作后，通过页面元素的变化清晰地展现当前状态。</div>
                </el-collapse-item>
                <el-collapse-item title="效率 Efficiency" name="3">
                  <div>简化流程：设计简洁直观的操作流程；</div>
                  <div>清晰明确：语言表达清晰且表意明确，让用户快速理解进而作出决策；</div>
                  <div>帮助用户识别：界面简单直白，让用户快速识别而非回忆，减少用户记忆负担。</div>
                </el-collapse-item>
                <el-collapse-item title="可控 Controllability" name="4">
                  <div>用户决策：根据场景可给予用户操作建议或安全提示，但不能代替用户进行决策；</div>
                  <div>结果可控：用户可以自由的进行操作，包括撤销、回退和终止当前操作等。</div>
                </el-collapse-item>
              </el-collapse>

        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
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
          showMoreMenu:false,
          activeNames: ['1']
        }
    },
    methods:{
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
        }else{
          this.checkIndex='';
        }
      },
      orderHandleCommand:function(index){
        this.orderCheckIndex = index;
      },
      viewHandleCommand:function(index){
        this.viewCheckIndex = index;
      },
      moveHandleCommand:function(index){
        this.moveCheckIndex = index;
      },
      moreHandleCommand:function(index){
        this.moreCheckIndex = index;
      },
      handleChange(value) {
        console.log(value);
      },

    },
    computed:{
      
    },
    watch:{
      
    }
}
</script>
<style>
.dropdown_item.active{
  color:#409EFF;
}
.inline_block{
  display:inline-block;
}
.width_100{
  width:100px;
}
.hide{
  display:none;
}
.f-fr{
  float:right;
}
#pagination{
  margin-right:10px;
}
.m-mllist .el-collapse-item__header{
  padding:0 14px;
  border-bottom: 1px solid #ebeef5;

}
.m-mllist .mllist-list-row .el-collapse-item>div:first-child>div{
  font-weight: bold;
  /* border-bottom: 1px solid #e3e4e5; */
}
.el-dropdown{
  outline:none;
}
.m-mllist .list-bg {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: #fff;
    opacity: .9;
    filter: alpha(opacity=90);
    z-index: -1;
}
  .m-mllist .m-mllist-row {
    display: block;
    width: 100%;
}
  .m-mllist .mllist-list-row {
    position: relative;
}

.m-mllist .m-mllist-row {
    display: block;
    width: 100%;
}
  .m-mllist .toolbar {
    margin: 0;
    padding: 6px;
    border-bottom: 1px solid #d4d7d9;
}

.toolbar {
    font-size: 13px;
    padding: 10px 0;
}
.m-mllist .mail-totals .all-mail, .m-mllist .mail-totals .unread-mail {
    color: #999;
}
  .m-mllist .mail-totals .number {
    color: #ee791a;
    padding: 0 2px;
}
  .m-mllist .mail-totals a {
    color: #0079bd;
    text-decoration: none;
    font-weight: normal;
}
.m-mllist .mail-totals {
    line-height: 32px;
    font-size: 12px;
    color: #333;
    font-weight: bold;
    padding: 0 14px;
    background-color: #fafafa;
    border-bottom: 1px solid #e3e4e5;
}
.m-mllist a {
    color: #333;
}
a {
    background-color: transparent;
}
  .u-btn{
    font-size:16px;
    color:#057ab8;
  }
  .el-button.is-circle {
    border-radius: 50%;
    padding: 6px;
    font-size:16px;
}
*::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
*::-webkit-scrollbar-thumb {
    background-color: #ccc;
    border-radius: 10px;
}
*::-webkit-scrollbar-track {
    border-radius: 10px;
    box-shadow: inset 0 0 6px rgba(0,0,0,0);
}



</style>
