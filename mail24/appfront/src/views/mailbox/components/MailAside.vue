<template>
  <aside class="mlsidebar">
                <div class="mlsidebar-bg"></div>
                <div class="u-btns">
                    <button class="u-btn u-btn-default u-btn-large btn-compose j-mlsb" type="button" data-op="compose"><i class="iconfont icon-iconcreate"></i> <span class="title">写 信</span></button>
                    <button class="u-btn u-btn-default u-btn-large btn-inbox j-mlsb" type="button" data-op="inbox"><i class="iconfont icon-iconinbox"></i></button>
                </div>

                <div class="wrapper u-scroll">
                    <el-tree
                      :data="folderList"
                      node-key="id"
                      default-expand-all
                      :expand-on-click-node="false" @node-click="handleNodeClick">
                      <span class="custom-tree-node" slot-scope="{ node, data }" :title="node.label">


                        <span>{{ node.label }} <el-badge v-if="data.unseen" class="mark" :value="data.unseen" /></span>

                        <span class="" style="position:absolute;right:2px;" class="hide_btn">
                          <el-button
                            type="text"
                            size="mini"
                            @click.stop.prevent="() => showDialog(data)" title="添加">
                            <i class="el-icon-plus"></i>
                          </el-button>
                          <el-button
                            type="text"
                            size="mini"
                            @click.stop="() => remove(node, data)" title="删除">
                            <i class="el-icon-delete"></i>
                          </el-button>
                        </span>
                      </span>
                    </el-tree>
                </div>

                      <el-dialog :title="'在 '+form.title+' 文件夹下新建'" :visible.sync="dialogFormVisible" :append-to-body="true">
                    <el-form :model="form">
                      <el-form-item label="文件夹名称" :label-width="formLabelWidth">
                        <el-input v-model="form.name" auto-complete="off"></el-input>
                      </el-form-item>
                      <!--<el-form-item label="活动区域" :label-width="formLabelWidth">-->
                        <!--<el-select v-model="form.region" placeholder="请选择活动区域">-->
                          <!--<el-option v-for="(v,k) in optionList" :key="k" :label="v.label" :value="v.id"></el-option>-->
                        <!--</el-select>-->
                      <!--</el-form-item>-->
                    </el-form>
                    <div slot="footer" class="dialog-footer">
                      <el-button @click="dialogFormVisible = false">取 消</el-button>
                      <el-button type="primary" @click="append">确 定</el-button>
                    </div>
                  </el-dialog>

            </aside>
</template>
<script>
  import {getFloder} from "@/api/api";

  let id = 100;

  export default {
    name:'MailAside',
    data(){
      return{
        folderList: [
            {
              id: 1,
              url:'innerbox',
              label: '收件箱',

            }, {
              id: 2,
              url:'outbox',
              label: '代办邮件',

            }, {
              id: 3,
              url:'innerbox',
              label: '草稿箱',

            },{
              id:4,
              url:'outbox',
              label:'已发送',
            },{
              id:5,
              label:'其他文件夹',
              children:[
                {id:6,label:'病毒文件夹'},
              ]
            }],
          defaultProps: {
            children: 'children',
            label: 'label',
            unseen: 'unseen',
          },
        dialogFormVisible: false,
        form: {
          title:'',
          name: '',
          region: '',
        },
        formLabelWidth: '120px',
        rootFloder:''

      }
    },
    computed:{
      optionList(){
        var result=[];
        function digui(arr){
          for(var i=0;i<arr.length;i++){
            result.push(arr[i]);
            console.log(arr[i].children&&arr[i].children.length>0)
            if(arr[i].children&&arr[i].children.length>0){
              digui(arr[i].children);
            }
          }
        }
        digui(this.folderList);
        return result;
      }
    }
    ,
    methods:{
      showDialog(data) {
        this.dialogFormVisible = true;
        this.rootFloder = data;
        this.form.title = data.label;

      },
      append(){
        const newChild = { id: id++, label: this.form.name, children: [] };
        if (!this.rootFloder.children) {
          this.$set(this.rootFloder, 'children', []);
        }
        this.rootFloder.children.push(newChild);
        this.form.name='';
        this.dialogFormVisible = false;
      },

      remove(node, data) {
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === data.id);
        this.$confirm('删除该文件夹, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          children.splice(index, 1);
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });

      },
      handleNodeClick(data) {
        console.log(data);
        this.$emit('getData', {id:data.id,'curr_folder':data.label,activeTab:1});
        this.$router.push('/mailbox')
      }

    },

    beforeMount(){
      getFloder().then((res)=>{
        let folder = res.data
        let arr = [];
        for(let i=0;i<folder.length;i++){
          let obj={};
          obj['label'] = folder[i]['name'];
          obj['id'] = folder[i]['raw_name'];
          obj['flags'] = folder[i]['flags'];
          obj['unseen'] = folder[i]['unseen_count'];
          arr.push(obj);
        }
        this.folderList = arr
      },(err)=>{
        console.log(err)
      });




    }

  }
</script>
<style>
  .fr{
    float:right;
  }
  .hide_btn{
    display:none;
  }
  .el-tree-node:hover .hide_btn{
    display:inline-block;
  }

</style>
