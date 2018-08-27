<template>
    <div class="mltabview-content">
      <div class="mltabview-panel">
        <section class="m-mlcompose">
          <div class="toolbar" style="background:#fff;">
            <div id="pagination" class="f-fr">
                <div class="">
                    <el-button size="small">通讯录</el-button>
                </div>
            </div>

            <el-button size="small" type="primary">发送</el-button>
            <el-button-group >
              <el-button size="small">预览</el-button>
              <el-button size="small">存草稿</el-button>
            </el-button-group>

             <el-button  size="small" plain>
                取消
            </el-button>
          </div>


          <div class="main" ref="iframe_height">
            <div class="mn-aside">
              <div class="u-tab">

              </div>
              <div class="content-wrapper">

              </div>
            </div>
            <form class="u-form mn-form">
              <div class="form-tt">
                测试
              </div>
              <div class="form-edr">

              </div>
              <div class="form-toolbar">

              </div>
            </form>
          </div>
        </section>
      </div>
    </div>

</template>

