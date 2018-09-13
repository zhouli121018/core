<template>
  <div class="j-module-content j-maillist mllist-list height100 " >


    <section class="content content-list height100" style="background-color: #fff;">
      <el-row class="" style="border-bottom:1px solid #ddd;">
        <el-col :span="24" class="breadcrumb-container">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item><a href="#">文件中心</a></el-breadcrumb-item>
            <el-breadcrumb-item>个人网盘</el-breadcrumb-item>
          </el-breadcrumb>
        </el-col>
      </el-row>

      <div>
        <div style="padding:4px 0 4px 4px;">
          <el-upload
              action=""
              :http-request="uploadFile"
              :show-file-list="false"
              multiple  style="display:inline-block;">
              <el-button size="small" type="primary" plain icon="el-icon-upload"> 上传</el-button>
          </el-upload>
          <el-button plain size="small" type="primary" icon="el-icon-download">下载</el-button>
          <el-button plain size="small" type="danger" icon="el-icon-delete">删除</el-button>
          <el-dropdown  trigger="click" placement="bottom-start"  @command="handleCommand">
            <el-button type="primary" size="small" plain>
              更多<i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="新建文件夹">新建文件夹</el-dropdown-item>
              <el-dropdown-item command="下载个人网盘">下载个人网盘</el-dropdown-item>
              <el-dropdown-item command="修改个人网盘">修改个人网盘</el-dropdown-item>
              <el-dropdown-item command="查看站内用户共享">查看站内用户共享</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>

          <el-input
            placeholder="请输入内容"
            prefix-icon="el-icon-search" style="width:auto;" size="small"
            >
          </el-input>
        </div>
        <div style="padding:10px 0 10px 6px;">
            <b>个人网盘</b>
            <span style="font-size:12px;color:#bbb;margin:0 20px;">2 个文件夹，4 个文件 </span>
            <span style="font-size:12px;color:#bbb;"> 容量：</span>
            <el-progress :percentage="50" style="width:200px;display: inline-block;"></el-progress>
        </div>
        <el-row class="file-table">
          <el-col :span="8" style="padding-left:6px;">
            <span>路径：</span>
            <span>个人网盘</span>
          </el-col>
          <el-col :span="16" style="text-align:right">
            <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="1"
            :page-sizes="[100, 200, 300, 400]"
            :page-size="100"
            layout="total, sizes, prev, pager, next"
            :total="400">
          </el-pagination>
          </el-col>


          <el-table
            :data="fileData"
            tooltip-effect="dark"
            style="width: 100%"
            @selection-change="handleSelectionChange" :header-cell-style="{background:'#f0f1f3'}">
            <el-table-column
              type="selection"
              width="55">
            </el-table-column>
            <el-table-column
              label="名称">
              <template slot-scope="scope">
                <el-row >
                  <el-col :span="1" style="width:42px;padding-top:8px;">
                    <span class="bico" :class="scope.row.classObject"></span>
                  </el-col>
                  <el-col :span="20" style="font-size:12px;">
                    <div>{{scope.row.name}}</div>
                    <div class="actions_a">
                      <span>下载</span>
                      <span>发信</span>
                      <span>共享</span>
                      <span>重命名</span>
                      <span>删除</span>
                    </div>
                  </el-col>
                </el-row>


              </template>
            </el-table-column>

            <el-table-column
              label="大小"
              width="120">
              <template slot-scope="scope">
                <span style="margin-left: 10px">{{scope.row.size|mailsize}}</span>
              </template>
            </el-table-column>

            <el-table-column
              label="上传时间"
              width="180">
              <template slot-scope="scope">
                <i class="el-icon-time"></i>
                <span style="margin-left: 10px">{{scope.row.date}}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-row>
      </div>


    </section>

  </div>
</template>

<script>
  import { settingZhaohuiGet } from '@/api/api'

  export default {
    data() {
      return {
        total: 0,
        page: 1,
        page_size: 15,
        listLoading: false,
        listTables: [],
        fileData:[
          {
            date:'2018-09-09',
            name:'我的文档',
            classObject:{bfFOLDER:true}
          },
          {
            date: '2016-05-02',
            name: 'abc.png',
            size: 1234578,
            classObject:{bfPNG:true}
          },
          {
            date: '2016-05-02',
            name: 'aDSFASDF.jpg',
            size: 12345798,
            classObject:{bfJPG:true}
          },
          {
            date: '2016-05-02',
            name: 'abcseohdsc.doc',
            size: 51234578,
            classObject:{bfDOC:true}
          },
          {
            date: '2016-05-02',
            name: 'abc.xml',
            size: 123422578,
            classObject:{bfXML:true}
          }
        ],
      }
    },

    mounted: function () {
      this.getTables();
    },

    methods: {
      handleCommand(a){
        console.log(a)
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
      },
      uploadFile(param){
        var file = param.file;
        var formData=new FormData();
        formData.append('filepath', file)

        return true;
      },

      // 每页数目改变
      f_TableSizeChange(val) {
        this.page_size = val;
        this.getTables();
        // console.log(`当前页: ${val}`);
      },
      // 翻页改变
      f_TableCurrentChange(val) {
        this.page = val;
        this.getTables();
      },
      getTables: function(){
        this.listLoading = true;
        settingZhaohuiGet().then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        });
      },

    },

  }
</script>
<style>
  .bico{
    display:inline-block;
    width: 32px;
    height: 32px;
    background-image: url(../../assets/img/icons.png);
    background-position: -672px -352px;
  }
  .actions_a>span{
    color: #0479bc;
    margin-right:10px;
    cursor:pointer;
  }
</style>
