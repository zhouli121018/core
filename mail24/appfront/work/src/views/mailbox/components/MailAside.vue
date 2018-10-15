<template>
  <aside class="mlsidebar">
                <div class="mlsidebar-bg"></div>
                <div class="u-btns">
                    <button class="u-btn u-btn-default u-btn-large btn-compose j-mlsb" type="button" @click="goToCompose"><i class="iconfont icon-iconcreate"></i> <span class="title">写 信</span></button>
                    <button class="u-btn u-btn-default u-btn-large btn-inbox j-mlsb" type="button" @click="reloadMails"><i class="iconfont icon-iconinbox"></i></button>
                </div>

                <div class="wrapper u-scroll">
                    <el-tree
                      :data="folderList"
                      node-key="id"
                      :default-checked-keys="checkNodes"
                      default-expand-all
                      @node-click="handleNodeClick">
                      <span class="custom-tree-node" slot-scope="{ node, data }" :title="node.label">


                        <span>{{ node.label }} <el-badge v-if="data.unseen" class="mark" :value="data.unseen" /></span>

                        <span class="" style="position:absolute;right:2px;" class="hide_btn">
                          <el-button
                            type="text"
                            size="mini"
                            @click.stop.prevent="() => showDialog(data)" title="新建文件夹">
                            <i class="el-icon-plus"></i>
                          </el-button>
                          <el-button
                            type="text"
                            size="mini"
                            v-if="!data.is_default"
                            @click.stop="() => remove(node, data)" title="删除">
                            <i class="el-icon-delete"></i>
                          </el-button>
                        </span>
                      </span>
                    </el-tree>
                </div>

                      <el-dialog title="新建文件夹" :visible.sync="dialogFormVisible" :append-to-body="true">
                    <el-form :model="form" :rules="rules" ref="ruleForm">
                      <el-form-item label="文件夹名称" :label-width="formLabelWidth" prop="name">
                        <el-input v-model="form.name" auto-complete="off"></el-input>
                      </el-form-item>

                    </el-form>
                    <div slot="footer" class="dialog-footer">
                      <el-button @click="dialogFormVisible = false">取 消</el-button>
                      <el-button type="primary" @click="append">确 定</el-button>
                    </div>
                  </el-dialog>

            </aside>
</template>
<script>
  import {getFloder,creatFolder,deleteFolder} from "@/api/api";

  export default {
    name:'MailAside',
    data(){
      return{
        floderResult:[],
        checkNodes:[],

          defaultProps: {
            children: 'children',
            label: 'label',
          },
        dialogFormVisible: false,
        form: {
          title:'',
          name: '',
          region: '',
        },
        rules:{
          name:[{required:true,message:'请填写文件夹名称！',trigger:'blur'}]
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
      },
      folderList(){
        let folder = this.$parent.floderResult;
        let arr = [];
        for(let i=0;i<folder.length;i++){
          let obj={};
          obj['label'] = folder[i]['name'];
          obj['id'] = folder[i]['raw_name'];
          obj['flags'] = folder[i]['flags'];
          obj['unseen'] = folder[i]['unseen_count'];
          obj['is_default'] = folder[i]['is_default'];
          arr.push(obj);
        }
        return arr;
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
        this.$refs['ruleForm'].validate((valid) => {
          if (valid) {
            let newName = this.form.name;
            if (!this.rootFloder.children) {
              this.$set(this.rootFloder, 'children', []);
            }
            creatFolder({"name":this.form.name}).then((suc)=>{
              let obj={ id: suc.data['raw_name'],label: newName, children: [] };
              this.folderList.push(obj);
              this.form.name='';
              this.$message({
                type: 'success',
                message: '添加成功!'
              });
            },(err)=>{
              this.$message({
                type: 'error',
                message: '添加失败！'
              });
              console.log(err);
            })

            this.dialogFormVisible = false;
          } else {
            console.log('error submit!!');
            return false;
          }
        });

      },

      remove(node, data) {
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === data.id);
        this.$confirm('删除 "'+data.label+'" 文件夹, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteFolder(data.id).then((suc)=>{
            children.splice(index, 1);
            this.$message({
              type: 'success',
              message: '删除成功!'
            });
          },(err)=>{
            console.log(err)
            this.$message({
              type: 'error',
              message: '删除失败!'
            });
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });

      },
      handleNodeClick(data) {
        this.$emit('getData', data);
        this.checkNodes=[data.id];
        // this.$router.push('/mailbox/innerbox')
      },
      goToCompose(){
        this.$emit('getCompose', {activeTab:3});
        this.$router.push('/mailbox/compose')
      },
      getFloderfn(){
        let folder = this.$parent.floderResult;
        let arr = [];
        for(let i=0;i<folder.length;i++){
          let obj={};
          obj['label'] = folder[i]['name'];
          obj['id'] = folder[i]['raw_name'];
          obj['flags'] = folder[i]['flags'];
          obj['unseen'] = folder[i]['unseen_count'];
          obj['is_default'] = folder[i]['is_default'];
          arr.push(obj);
        }
        this.folderList = arr
      },
      reloadMails(){
        this.$parent.$refs.innerbox.getMessageList()
      },

    },

    beforeMount(){
      // this.getFloderfn();
    },


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
