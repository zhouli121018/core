<template>
  <div>
    <div class="ctmain-bg"></div>
    <div class="j-contact-content">
      <div data-panel="contact.oab:business1473/102" class="j-contact-panel" style="display: block;">
        <section class="m-ctoab" data-view-cid="view-20" data-view-name="contact.oab">

          <div class="main-wrapper switch-list">
            <div class="content-wrapper">

              <!-- 普通列表 -->
              <section class="content content-list">
                <header class="toolbar">
                  <button class="u-btn u-btn-primary u-btns-hide j-goPrevLevel" data-action="goPrev" style="display: inline-block;">
                    <i class="iconfont iconupperlayer"></i>返回上层2
                  </button>
                  <button class="u-btn u-btn-default" data-operation="showSearchList">
                    <i class="iconfont iconsreachm"></i>
                  </button>
                </header>
                <div class="deptInfo"><b>人力资源部</b><label class="totalcnt">共 0 个,</label><label class="deptcnt" style="display: none;">0 个子部门,</label><label>0 个地址</label></div>
                <div class="u-list u-scroll">
                  <table class="u-table u-table-assign u-table-row">
                    <thead>
                    <tr>
                      <th class="firstTH">
                      <span class="j-selectAll">
                        <input class="rc-hidden" type="checkbox"><i class="checkbox checkbox-checked"></i>
                      </span>
                      </th>
                      <th class="nth2TH">&nbsp;</th>
                      <th data-sort="true_name" class="" width=""><div class="f-ellipsis">姓名<i class="iconfont"></i></div></th>
                      <th data-sort="email" class="" width=""><div class="f-ellipsis">邮件地址<i class="iconfont"></i></div></th>
                      <th data-sort="mobile_number" class="hideForShrink" width=""><div class="f-ellipsis">手机号码<i class="iconfont"></i></div></th>
                      <th data-sort="security_level" class="hideForShrink" width=""><div class="f-ellipsis">收信密级<i class="iconfont"></i></div></th>
                      <th data-sort="sender_security_level" class="hideForShrink" width=""><div class="f-ellipsis">发信密级<i class="iconfont"></i></div></th>
                      <th data-sort="duty" class="hideForShrink" width=""><div class="f-ellipsis">职位<i class="iconfont"></i></div></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr><td colspan="8">{{msg}}</td></tr>
                    </tbody>
                  </table>
                </div>
              </section>

            </div>

          </div>

        </section>
      </div>
    </div>
  </div>
</template>
<script>
import router from '@/router'
  export default {
    data(){
      return{
        msg:''
      }
    },
    mounted:function(){
      this.msg = this.$route.params.id
    },
     watch: {
        $route: function (val) {
          this.msg = this.$route.params.id
          console.log(this.$route.params.id)
        },
      }

  }
</script>
