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
                  <el-button type="primary" size="small" icon="el-icon-arrow-left" plain></el-button>
                  <el-button type="primary" size="small" plain><i class="el-icon-arrow-right el-icon--right"></i></el-button>
                </el-button-group>
              </div>
            </div>

            <!--选择-->
            <el-dropdown>
              <el-button type="primary" size="small" plain>
                <span>全选</span>
                <i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>所有</el-dropdown-item>
                <el-dropdown-item divided><i class="el-icon-check vibility_hide"></i>当前页</el-dropdown-item>
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>未读</el-dropdown-item>
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>已读</el-dropdown-item>
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>反选</el-dropdown-item>
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>不选</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>

            <!--排序-->
            <el-dropdown>
              <el-button type="primary" size="small" plain>
                <span>排序</span>
                <i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>按时间从新到旧</el-dropdown-item>
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>按时间从旧到新</el-dropdown-item>
                <el-dropdown-item divided><i class="el-icon-check vibility_hide"></i>按发件人降序</el-dropdown-item>
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>按发件人升序</el-dropdown-item>
                <el-dropdown-item divided><i class="el-icon-check vibility_hide"></i>按主题降序</el-dropdown-item>
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>按主题升序</el-dropdown-item>
                <el-dropdown-item divided><i class="el-icon-check vibility_hide"></i>按附件降序</el-dropdown-item>
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>按附件升序</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>

            <!--查看-->
            <el-dropdown>
              <el-button type="primary" size="small" plain>
                <span>查看</span>
                <i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>所有</el-dropdown-item>
                <el-dropdown-item divided><i class="el-icon-check vibility_hide"></i>当前页</el-dropdown-item>
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>未读</el-dropdown-item>
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>已读</el-dropdown-item>
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>反选</el-dropdown-item>
                <el-dropdown-item><i class="el-icon-check vibility_hide"></i>不选</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>

            <!--刷新-->
            <el-button type="primary" size="small" plain>
                刷新
                <i class="el-icon-refresh el-icon--right"></i>
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

        </div>
    </div>
</template>
<script>
export default {
    
}
</script>
<style scoped>
.f-fr{
  float:right;
}
#pagination{
  margin-right:10px;
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
</style>
